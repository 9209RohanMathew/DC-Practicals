import java.rmi.*;

public interface RemoteObject extends Remote {
    // Define remote methods to be invoked by the client
    String sayHello() throws RemoteException;
    int add(int a, int b) throws RemoteException;
}