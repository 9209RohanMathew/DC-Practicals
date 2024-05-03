import java.rmi.*;
import java.rmi.registry.*;

public class Server {
    public static void main(String[] args) {
        try {
            // Create a remote object
            RemoteObject remoteObject = new RemoteObjectImpl();
            
            // Bind the remote object to the RMI registry
            Registry registry = LocateRegistry.createRegistry(37083);
            registry.rebind("RemoteObject", remoteObject);
            
            System.out.println("Server is ready...");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}