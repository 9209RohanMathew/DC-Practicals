import java.rmi.*;
import java.rmi.registry.*;

public class Client {
    public static void main(String[] args) {
        try {
            // Get reference to the remote object from the RMI registry
            Registry registry = LocateRegistry.getRegistry("localhost", 37083);
            RemoteObject remoteObject = (RemoteObject) registry.lookup("RemoteObject");
            
            // Invoke remote method
            String message = remoteObject.sayHello();
            System.out.println("Message from server: " + message);
            
            // Invoke remote method to add two numbers
            int result = remoteObject.add(5, 3);
            System.out.println("Result of addition: " + result);
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}