package lab3;

import java.io.IOException;
import java.net.ServerSocket;

public class FreePortFinder {
    public static void main(String[] args) {
        findFreePort();
    }

    public static void findFreePort() {
        try {
            ServerSocket serverSocket = new ServerSocket(0);
            int port = serverSocket.getLocalPort();
            serverSocket.close();
            System.out.println("Free port found: " + port);
        } catch (IOException e) {
            System.err.println("Error finding free port: " + e.getMessage());
        }
    }
}