package server.main.db;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.Signature;
import java.security.spec.X509EncodedKeySpec;
import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Base64;
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
		ServerSocket serverSocket = new ServerSocket(3343);
		
		while (true) {

		// wait for client connection and check login information
		try {
			System.err.println("Waiting for connection...");
			Socket socket = serverSocket.accept();
			System.err.println("Someone has connected.");
			// open BufferedReader for reading data from client
			BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			// open PrintWriter for writing data to client
			PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

			//Mensaje y firma
			String message = input.readLine();

			String[] mensajeFirma = message.split(";");
			String mensaje = mensajeFirma[0];

			String firmaString = mensajeFirma[1];
			byte[] encodedFirma = Base64.getDecoder().decode(firmaString);
			
			String publicKeyString = mensajeFirma[2];
			byte[] encodedPublicKey = Base64.getDecoder().decode(publicKeyString);
			//====================================//

			try {
    			KeyFactory kf = KeyFactory.getInstance("RSA");
				PublicKey publicKey = kf.generatePublic(new X509EncodedKeySpec(encodedPublicKey));

				Signature sg = Signature.getInstance("SHA256withRSA");
				sg.initVerify(publicKey);
				sg.update(mensaje.getBytes());
				
				//=====Conexion a la base de datos=====//
				Connection c = null;
    			Statement stmt = null;
				Class.forName("org.sqlite.JDBC");
        		c = DriverManager.getConnection("jdbc:sqlite:SQLiteDatabase.db");
        		c.setAutoCommit(false);
        		System.out.println("Opened database successfully");
				//====================================//
				
				//Fecha actual
				DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS", Locale.ENGLISH);
				String fecha = LocalDateTime.now().format(formatter);
				//====================================//
				//Coger el mensage y sacarle los datos
				String datos = mensaje.replace(" ", ";");
				//====================================//


				//Coger el mensage y sacarle la verificacion

				Boolean verif_firm = sg.verify(encodedFirma);
				Byte verificacion = null;
				if(verif_firm == true) {
					verificacion = 1;
				} else {
					verificacion = 0;
				}
				//---------------------------------//

				stmt = c.createStatement();
				System.out.println("Inserting in the database.");
        		String sql = "INSERT INTO REQUESTS (TIMESTAMP,DATA,VERIFICATION) VALUES (\'"+fecha+"\',\'"+datos+"\', \'"+verificacion+"\');"; 
        		stmt.executeUpdate(sql);
				stmt.close();
				c.commit();
				c.close();
				output.println("El servidor ha recibido y guardado su petición correctamente.");
				output.close();
				input.close();
				System.out.println("Connection close.");
			} catch (Exception e) {e.printStackTrace();}
			
		socket.close();
		} catch (IOException ioException) {
			ioException.printStackTrace();
		}
	}
}

}