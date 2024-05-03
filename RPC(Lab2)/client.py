import xmlrpc.client

client = xmlrpc.client.ServerProxy("http://localhost:8000/")

def perform_addition(x, y):
    result = client.add(x, y)
    return result

# Example usage:
number1 = 5
number2 = 10
result = perform_addition(number1, number2)
print(f"Result of adding {number1} and {number2} is: {result}")
