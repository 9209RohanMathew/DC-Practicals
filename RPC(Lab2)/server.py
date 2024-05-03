import xmlrpc.server

class MathFunctions:
    def add(self, x, y):
        return x + y

server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(MathFunctions())
print("RPC Server is listening on port 8000...")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server terminated.")
    server.shutdown()
