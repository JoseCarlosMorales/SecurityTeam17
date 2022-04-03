import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import javax.net.ServerSocketFactory;
import javax.net.ssl.*;


public class LoginServerSocket {
	
	private static final String CORRECT_USER_NAME = "user";
	private static final String CORRECT_PASSWORD = "user";
	private static final String[] protocols = new String[]{"TLSv1.3"};
	private static final String[] cipherSuites = new String[]{"TLS_AES_128_GCM_SHA256"};

	/**
	 * @param args
	 * @throws IOException 
	 * @throws InterruptedException 
	 */
	public static void main(String[] args) throws IOException, InterruptedException {

		
		// perpetually listen for clients
		
		SSLServerSocketFactory socketFactory = (SSLServerSocketFactory) SSLServerSocketFactory.getDefault();
		SSLServerSocket serverSocket = (SSLServerSocket) socketFactory.createServerSocket(7070);
		
		while (true) {

		// wait for client connection and check login information
		try {
			System.err.println("Waiting for connection...");
			SSLSocket socket = (SSLSocket) serverSocket.accept();
			socket.setEnabledProtocols(protocols);
			socket.setEnabledCipherSuites(cipherSuites);
			socket.startHandshake();

			// open BufferedReader for reading data from client
			BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

			// open PrintWriter for writing data to client
			PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

			String userName = input.readLine();
			String password = input.readLine();
			String message = input.readLine();

			if (userName.equals(CORRECT_USER_NAME) && password.equals(CORRECT_PASSWORD) && (!message.equals("") || message != null)) {
				output.println(message);
				/*
				String message = input.readLine();

				if(message == null || message.equals("")){
					output.println("Invalid Message");
				}else{
					output.println("Message Received: " + message);
				}
				*/
				output.close();
				input.close();

			} else {
				output.println("Login Failed.");
				output.close();
				input.close();
			}
		socket.close();
		}

		// handle exception communicating with client
		catch (IOException ioException) {
			ioException.printStackTrace();
		}

	} // end while

}

}
