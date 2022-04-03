import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import javax.net.ssl.*;

import javax.swing.JOptionPane;

public class LoginClientSocket {

	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
	try {

		// create SSLSocket from factory
		SSLSocketFactory socketFactory = (SSLSocketFactory) SSLSocketFactory.getDefault();
		SSLSocket socket = (SSLSocket) socketFactory.createSocket("localhost", 7070);

		// create PrintWriter for sending login to server
		PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

		
		String userName = JOptionPane.showInputDialog(null, "Enter User Name:"); 	// prompt user for user name
		output.println(userName); 													// send user name to server
		String password = JOptionPane.showInputDialog(null, "Enter Password:");		// prompt user for password
		output.println(password);
		String message  = JOptionPane.showInputDialog(null, "Enter the message:");	// prompt user for password
		output.println(message); 

		output.flush(); 															// send password to server


		BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream())); // create BufferedReader for reading server response

		String response = input.readLine(); // read response from server

		if (response.equals(message)){

			System.out.println(response);
			/*
			String message = JOptionPane.showInputDialog(null, "Enter a message:");
			output.println(message);
			output.flush();

			String messageConfirmation = input.readLine();
			JOptionPane.showMessageDialog(null, messageConfirmation);
			*/

			output.close();
			input.close();
		} else {
			JOptionPane.showMessageDialog(null, response);
			output.close();
			input.close();
		}
		
		socket.close(); // clean up streams and Socket

	} // end try

	// handle exception communicating with server
	catch (IOException ioException) {
		ioException.printStackTrace();
	}

	// exit application
	finally {
		System.exit(0);
	}
    }
}
