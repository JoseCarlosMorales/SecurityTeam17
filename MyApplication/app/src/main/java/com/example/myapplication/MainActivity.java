package com.example.myapplication;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;


public class MainActivity extends AppCompatActivity {

    // Setup Server information
    protected static String server = "192.168.1.133";
    protected static int port = 7070;
    int numSabanas;
    int numAlmohadas;
    int numSillas;
    int numMesas;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Capturamos el boton de Enviar
        View button = findViewById(R.id.button_send);

        // Llama al listener del boton Enviar
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDialog();
            }
        });


    }

    // Creación de un cuadro de dialogo para confirmar pedido
    private void showDialog() throws Resources.NotFoundException {
        CheckBox sabanas = (CheckBox) findViewById(R.id.checkBox_sabanas);
        CheckBox almohadas = (CheckBox) findViewById(R.id.checkBox_almohadas);
        CheckBox sillas = (CheckBox) findViewById(R.id.checkBox_sillas);
        CheckBox mesas = (CheckBox) findViewById(R.id.checkBox_mesas);

        if (!sabanas.isChecked()) {
            // Mostramos un mensaje emergente;
            Toast.makeText(getApplicationContext(), "Selecciona al menos un elemento", Toast.LENGTH_SHORT).show();
        } else {
            new AlertDialog.Builder(this)
                    .setTitle("Enviar")
                    .setMessage("Se va a proceder al envio")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                                // Catch ok button and send information
                                public void onClick(DialogInterface dialog, int whichButton) {

                                    // 1. Extraer los datos de la vista

                                    // 2. Firmar los datos
                                    try {
                                        KeyPairGenerator kgen = KeyPairGenerator.getInstance("RSA");
                                        kgen.initialize(2048);
                                        KeyPair keys = kgen.generateKeyPair();

                                        Signature sg = Signature.getInstance("SHA256withRSA");
                                        sg.initSign(keys.getPrivate());
                                        sg.update(data.getBytes());

                                        byte[] firma = sg.sign();

                                    // 3. Enviar los datos
                                        String[] protocols = new String[]{"TLSv1.3"};
                                        SSLSocketFactory socketFactory = (SSLSocketFactory) SSLSocketFactory.getDefault();
                                        SSLSocket socket = (SSLSocket) socketFactory.createSocket("localhost", 7070);
                                        socket.setEnabledProtocols(protocols);

                                        PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

                                        String sol = data + ";" + firma;

                                        output.println(sol);
                                        output.flush();

                                        BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                                        String response = input.readLine();
                                        output.close();
                                        input.close();
                                        socket.close();

                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }

                                    Toast.makeText(MainActivity.this, "Petición enviada correctamente", Toast.LENGTH_SHORT).show();
                                }
                            }

                    )
                    .

                            setNegativeButton(android.R.string.no, null)

                    .

                            show();
        }
    }


}
