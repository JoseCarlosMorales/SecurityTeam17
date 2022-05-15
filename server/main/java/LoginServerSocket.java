package server.main.java;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.security.PublicKey;
import java.security.Signature;
import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

import javax.net.ssl.*;


public class LoginServerSocket {

	private static final String[] protocols = new String[]{"TLSv1.3"};
	private static final String[] cipherSuites = new String[]{"TLS_AES_128_GCM_SHA256","TLS_AES_256_GCM_SHA384"};

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

			String message = input.readLine();
			String firma = input.readLine();
			PublicKey publicKey = null;

			try {

				Signature sg = Signature.getInstance("SHA256withRSA");
				sg.initVerify(publicKey);
				sg.update(message.getBytes());
				
				//=====Conexion a la base de datos=====//
				Connection c = null;
    			Statement stmt = null;
				Class.forName("org.sqlite.JDBC");
        		c = DriverManager.getConnection("jdbc:sqlite:test.db");
        		c.setAutoCommit(false);
        		System.out.println("Opened database successfully");
				//====================================//

				//Coger el mensage y sacarle la fecha
				DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS", Locale.ENGLISH);
				String fecha = LocalDateTime.now().format(formatter);
				//---------------------------------//
				//Coger el mensage y sacarle los datos
				String datos = message;
				//---------------------------------//
				//Coger el mensage y sacarle la verificacion
				Boolean verif_firm = sg.verify(firma.getBytes());
				Byte verificacion = null;
				if(verif_firm == true) {
					verificacion = 1;
				} else {
					verificacion = 0;
				}
				//---------------------------------//

				stmt = c.createStatement();
        		String sql = "INSERT INTO REQUESTS (TIMESTAMP,DATETIME,DATA,VERIFICATION) VALUES ('"+fecha+"','"+datos+"', '"+verificacion+"');"; 
        		stmt.executeUpdate(sql);

				output.println(message);
				output.close();
				input.close();

			} catch (Exception e) {e.printStackTrace();}
			
		socket.close();
		} catch (IOException ioException) {
			ioException.printStackTrace();
		}
	}
}

}
