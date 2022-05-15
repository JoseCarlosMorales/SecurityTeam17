package com.example.myapplication;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;


public class MainActivity extends AppCompatActivity {

    // Setup Server information
    protected static String server = "192.168.1.133";
    protected static int port = 7070;
    String numSabanas,numAlmohadas,numSillas,numMesas;

    KeyPair clave1,clave2,clave3,claveAdmin,keys;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        try{
            KeyPairGenerator kgen = KeyPairGenerator.getInstance("RSA");
            kgen.initialize(2048);
            clave1 = kgen.generateKeyPair();

            clave2 = kgen.generateKeyPair();

            clave3 = kgen.generateKeyPair();

            claveAdmin = kgen.generateKeyPair();

        }catch (Exception e) {
            e.printStackTrace();
        }
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
        final CheckBox sabanas = (CheckBox) findViewById(R.id.checkBox_sabanas);
        final CheckBox almohadas = (CheckBox) findViewById(R.id.checkBox_almohadas);
        final CheckBox sillas = (CheckBox) findViewById(R.id.checkBox_sillas);
        final CheckBox mesas = (CheckBox) findViewById(R.id.checkBox_mesas);
        final EditText inSabanas = (EditText) findViewById(R.id.input_sabanas);
        final EditText inAlmohadas = (EditText) findViewById(R.id.input_almohadas);
        final EditText inSillas = (EditText) findViewById(R.id.input_sillas);
        final EditText inMesas = (EditText) findViewById(R.id.input_mesas);
        final Spinner spinner = (Spinner) findViewById(R.id.spinner);

        if (!sabanas.isChecked() && !almohadas.isChecked() && !sillas.isChecked() && !mesas.isChecked()) {
            // Mostramos un mensaje emergente;
            Toast.makeText(getApplicationContext(), "Selecciona al menos un elemento", Toast.LENGTH_SHORT).show();
        }if(sabanas.isChecked() && (inSabanas == null || Integer.parseInt(inSabanas.toString()) < 0)
                ||almohadas.isChecked() && (inAlmohadas == null || Integer.parseInt(inAlmohadas.toString()) < 0)
                ||sillas.isChecked() && (inSillas == null || Integer.parseInt(inSillas.toString()) < 0)
                ||mesas.isChecked() && (inMesas == null|| Integer.parseInt(inMesas.toString()) < 0)){
            Toast.makeText(getApplicationContext(), "Debe introducir un valor adecuado", Toast.LENGTH_SHORT).show();
        }
        else {
            new AlertDialog.Builder(this)
                    .setTitle("Enviar")
                    .setMessage("Se va a proceder al envio")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {

                                // Catch ok button and send information
                                public void onClick(DialogInterface dialog, int whichButton) {

                                    // 1. Extraer los datos de la vista
                                    if (!sabanas.isChecked()){
                                        numSabanas = "0";
                                    }else{
                                        numSabanas = inSabanas.toString();
                                    }
                                    if (!almohadas.isChecked()){
                                        numAlmohadas = "0";
                                    }else{
                                        numAlmohadas = inAlmohadas.toString();
                                    }
                                    if (!sillas.isChecked()){
                                        numSillas = "0";
                                    }else{
                                        numSillas = inSillas.toString();
                                    }
                                    if (!mesas.isChecked()){
                                        numMesas = "0";
                                    }else{
                                        numMesas = inMesas.toString();
                                    }

                                    final String data = "Sabanas:" + numSabanas + " Almohadas:" + numAlmohadas +
                                            " Sillas:" + numSillas + " Mesas:" + numMesas;

                                    spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                                        @Override
                                        public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                                            String user = adapterView.getItemAtPosition(i).toString();
                                            if(user.equals("Usuario 1")){
                                                keys = clave1;
                                            }else if (user.equals("Usuario 2")){
                                                keys = clave2;
                                            }else if (user.equals("Usuario 3")){
                                                keys = clave3;
                                            }else if (user.equals("Admin")){
                                                keys = claveAdmin;
                                            }
                                        }

                                        @Override
                                        public void onNothingSelected(AdapterView<?> adapterView) {

                                        }
                                    });

                                    // 2. Firmar los datos
                                    try {
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
