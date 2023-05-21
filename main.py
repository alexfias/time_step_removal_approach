import pypsa
from my_code import pre_process_data, post_process_data, modify_network

def main():
    # Specify the path to the model
    model_path = './data/model_folder/'

    # Load the model
    n = pypsa.Network()
    pypsa.Network.import_from_netcdf(n,model_path)

    # Pre-process the data if necessary
    pre_process_data(n)

    # Make modifications to the network
    modify_network(n)

    # Run the model
    n.lopf()

    # Post-process the data, analyze results
    post_process_data(n)

    print("Analysis complete")

if __name__ == "__main__":
    main()
