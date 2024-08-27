import sys
sys.path.append('./packages')

from opcua import Client, ua

# Define the OPC UA server endpoint URL
url = "opc.tcp://192.168.1.1:4840/"

# Create a client object
client = Client(url)

# Set the username and password for authentication
username = "pass"
password = "pass"
client.set_user(username)
client.set_password(password)

# Track whether the connection was successful
connected = False

try:
    # Connect to the OPC UA server
    client.connect()
    print("Connected to OPC UA server.")
    connected = True  # Mark as connected

    # Get the root node
    root_node = client.get_root_node()

    # Get the objects node
    objects_node = root_node.get_child(["0:Objects"])

    # Define the namespace index and node path
    namespace_index = 2
    node_path = "plc/app/Application/sym/PLC_PRG/iCounter"

    # Create a node ID for the variable
    node_id = ua.NodeId(node_path, namespace_index)

    # Read the value of the node
    try:
        variable_node = client.get_node(node_id)
        value = variable_node.get_value()
        print(f"Value of node '{node_path}': {value}")
    except ua.UaStatusCodeError as e:
        print(f"Error accessing node '{node_path}': {e}")

    # Example: Write a new value to the node
    new_value = 100  # Example value to write
    try:
        variable_node.set_value(ua.Variant(new_value, ua.VariantType.Int32))
        print(f"Successfully wrote {new_value} to node '{node_path}'.")
    except ua.UaStatusCodeError as e:
        print(f"Error writing to node '{node_path}': {e}")

finally:
    # Disconnect from the OPC UA server if connected
    if connected:
        client.disconnect()
        print("Disconnected from OPC UA server.")
