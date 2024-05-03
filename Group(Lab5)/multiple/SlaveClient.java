import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class SlaveClient {
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        try (Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
             BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            while (true) {
                String message = reader.readLine();
                if (message == null) {
                    break;
                }
                System.out.println("Received message from server: " + message);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
} 
    

