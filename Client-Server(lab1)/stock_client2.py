import socket
import matplotlib.pyplot as plt

# Client configuration
host = "127.0.0.1"
port = 8888

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

# Initialize lists to store data for plotting
timestamps = []
stock_values = []

# Create initial empty plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot(timestamps, stock_values)
ax.set_xlabel('Time')
ax.set_ylabel('Stock Value')
ax.set_title('Stock Value Updates')

while True:
    # Receive and print the stock value from the server
    data = client_socket.recv(1024)
    stock_value = float(data.decode())
    print(f"Stock value received: {stock_value}")

    # Append received data to lists
    timestamps.append(len(timestamps) + 1)  # Just for the sake of demonstration, use incremental timestamps
    stock_values.append(stock_value)

    # Update plot
    line.set_xdata(timestamps)
    line.set_ydata(stock_values)
    ax.relim()
    ax.autoscale_view()

    # Pause to update plot
    plt.pause(0.01)  # Adjust the pause duration if needed
