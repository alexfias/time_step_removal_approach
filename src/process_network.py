import pypsa

def mask_snapshots_without_week(network, week):
    """Return a network with masked snapshots, removing the given week."""
    mask = network.snapshots.isocalendar().week != week
    network.set_snapshots(network.snapshots[mask])
    return network

def process_network(network, week):
    """Apply processing steps and solve the network."""
    # Adjusting network settings
    network.generators_t.p_max_pu.where(lambda df: df > 0.01, other=0., inplace=True)
    network.loads_t.p_set[network.loads_t.p_set < 1e-03] = 0
    network.storage_units_t.inflow[network.storage_units_t.inflow < 1e-03] = 0
    network.generators.marginal_cost[network.generators.marginal_cost < 10.0] = 0
    
    # Mask the snapshots to remove the specified week
    network = mask_snapshots_without_week(network, week)
    
    # Solve the network
    network.lopf(
        solver_name='gurobi',
        solver_options={
            'Method': 2,
            'NumericFocus': 3,
            'Crossover': 0,
            'OutputFlag': 1,
            'BarConvTol': 1.e-5,
            'FeasibilityTol': 1.e-4,
            'OptimalityTol': 1.e-4,
            'ObjScale': -0.5
        }
    )

    # Export the network to a CSV folder
    network.export_to_csv_folder(f'./model_without_week_{week}/')

# Main execution
if __name__ == "__main__":
    # Load the network once outside the loop
    base_network = pypsa.Network()
    base_network.import_from_netcdf("myopic_0.nc")

    # Loop through weeks
    for i in range(52):
        # Clone the network for each iteration to avoid side effects
        network = base_network.copy()
        process_network(network, i)
