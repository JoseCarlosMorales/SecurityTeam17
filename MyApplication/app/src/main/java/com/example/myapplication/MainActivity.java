package com.example.myapplication;

import static android.util.Base64.NO_WRAP;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.os.Bundle;
import android.os.StrictMode;
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
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.Socket;
import java.net.SocketException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.util.Base64;
import java.util.Enumeration;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;


public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    // Setup Server information
    String numSabanas,numAlmohadas,numSillas,numMesas;
    KeyPair clave1,clave2,clave3,claveAdmin,keys;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                .permitAll().build();
        StrictMode.setThreadPolicy(policy);

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

    @Override
    public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
        String user = adapterView.getItemAtPosition(i).toString();
    }

    @Override
    public void onNothingSelected(AdapterView<?> adapterView) {

    }

    // Creación de un cuadro de dialogo para confirmar pedido
    private void showDialog() throws Resources.NotFoundException {

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

        final CheckBox sabanas = (CheckBox) findViewById(R.id.checkBox_sabanas);
        final CheckBox almohadas = (CheckBox) findViewById(R.id.checkBox_almohadas);
        final CheckBox sillas = (CheckBox) findViewById(R.id.checkBox_sillas);
        final CheckBox mesas = (CheckBox) findViewById(R.id.checkBox_mesas);
        final EditText inSabanas = (EditText) findViewById(R.id.input_sabanas);
        final EditText inAlmohadas = (EditText) findViewById(R.id.input_almohadas);
        final EditText inSillas = (EditText) findViewById(R.id.input_sillas);
        final EditText inMesas = (EditText) findViewById(R.id.input_mesas);
        final Spinner spinner = (Spinner) findViewById(R.id.spinner);
        spinner.setOnItemSelectedListener(this);

        String user = spinner.getSelectedItem().toString();
        if(user.equals("Usuario 1")){
            keys = clave1;
        }else if (user.equals("Usuario 2")){
            keys = clave2;
        }else if (user.equals("Usuario 3")){
            keys = clave3;
        }else{
            keys = claveAdmin;
        }

        if (!sabanas.isChecked() && !almohadas.isChecked() && !sillas.isChecked() && !mesas.isChecked()) {
            // Mostramos un mensaje emergente;
            Toast.makeText(getApplicationContext(), "Selecciona al menos un elemento", Toast.LENGTH_SHORT).show();
        }if(sabanas.isChecked() && (inSabanas == null || Integer.valueOf(inSabanas.getText().toString()) < 0 || Integer.valueOf(inSabanas.getText().toString()) > 300)
                ||almohadas.isChecked() && (inAlmohadas == null || Integer.valueOf(inAlmohadas.getText().toString()) < 0|| Integer.valueOf(inAlmohadas.getText().toString()) > 300)
                ||sillas.isChecked() && (inSillas == null || Integer.valueOf(inSillas.getText().toString()) < 0|| Integer.valueOf(inSillas.getText().toString()) > 300)
                ||mesas.isChecked() && (inMesas == null|| Integer.valueOf(inMesas.getText().toString()) < 0 || Integer.valueOf(inMesas.getText().toString()) > 300)){
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
                                        numSabanas = inSabanas.getText().toString();
                                    }
                                    if (!almohadas.isChecked()){
                                        numAlmohadas = "0";
                                    }else{
                                        numAlmohadas = inAlmohadas.getText().toString();
                                    }
                                    if (!sillas.isChecked()){
                                        numSillas = "0";
                                    }else{
                                        numSillas = inSillas.getText().toString();
                                    }
                                    if (!mesas.isChecked()){
                                        numMesas = "0";
                                    }else{
                                        numMesas = inMesas.getText().toString();
                                    }

                                    final String data = "Sabanas:" + numSabanas + " Almohadas:" + numAlmohadas +
                                            " Sillas:" + numSillas + " Mesas:" + numMesas;

                                    // 2. Firmar los datos
                                    try {
                                        Signature sg = Signature.getInstance("SHA256withRSA");
                                        sg.initSign(keys.getPrivate());
                                        sg.update(data.getBytes());
                                        byte[] firma = sg.sign();

                                        // ========== Traspaso de firma ========== //
                                        System.out.println("TAMAñO FIRMA::" + firma.length);
                                        System.out.println("FIRMA::" + firma);
                                        //converting byte to String
                                        String str_sg = Base64.getEncoder().encodeToString(firma);
                                        System.out.println("\nSTRING FIRMA::" + str_sg.length());
                                        //=================================================//

                                        // ========== Traspaso de clave publica ========== //
                                        System.out.println("PUBLIC KEY::" + keys.getPublic());
                                        //converting public key to byte
                                        byte[] byte_pubkey = keys.getPublic().getEncoded();
                                        System.out.println("\nBYTE KEY::: " + byte_pubkey);
                                        //converting byte to String
                                        String str_key = Base64.getEncoder().encodeToString(byte_pubkey);
                                        System.out.println("\nSTRING KEY::" + str_key);
                                        //=================================================//


                                    // 3. Enviar los datos

                                        Socket socket = new Socket("192.168.56.1", 3343);

                                        PrintWriter output = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

                                        String sol = data + ";" + str_sg + ";" + str_key;

                                        output.println(sol);
                                        output.flush();

                                        BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                                        String response = input.readLine();
                                        System.out.println(response);
                                        Toast.makeText(MainActivity.this, response, Toast.LENGTH_SHORT).show();
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
