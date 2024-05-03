import java.rmi.*;
import java.rmi.server.*;

public class RemoteObjectImpl extends UnicastRemoteObject implements RemoteObject {
    public RemoteObjectImpl() throws RemoteException {
        super();
    }

    @Override
    public String sayHello() throws RemoteException {
        return "Hello from the server!";
    }

    @Override
    public int add(int a, int b) throws RemoteException {
        return a + b;
    }
}