import pandas as pd
import pypsa

def compute_cost_differences(n_full, n_full_total_capital_cost):
    cost_difference = pd.DataFrame(columns=['Cost Difference'])
    cost_difference.loc[0] = 0.0
    
    for i in range(52):
        d_n = pypsa.Network()
        pypsa.Network.import_from_csv_folder(d_n, f"./model_without_week_{i+1}/")
        
        # Calculate and print cost differences
        obj_difference = (d_n.objective - n_full.objective) / n_full.objective
        cost_difference.loc[i+1] = obj_difference

        # Compute capital costs
        total_capital_cost_generators = (d_n.generators.p_nom_opt * d_n.generators.capital_cost).sum()
        total_capital_cost_links = (d_n.links.p_nom_opt * d_n.links.capital_cost).sum()
        total_capital_cost_storage_units = (d_n.storage_units.p_nom_opt * d_n.storage_units.capital_cost).sum()

        # Sum and print capital costs
        total_capital_cost = total_capital_cost_generators + total_capital_cost_links + total_capital_cost_storage_units

    return cost_difference
