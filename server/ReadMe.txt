Para crear la base de datos (si no está creada) ejecutar los siguientes comandos:
$ cd .\server\main\db\
$ java -classpath "sqlite-jdbc-3.34.0.jar" .\SQLiteJDBC.java

En caso de querer crearla de nuevo y ya existir una base de datos, solo hay que borrar el archivo .db y ejecutar los comandos citados anteriormente.

Para ejecutar el servidor introducir los siguientes comandos:
$ cd .\server\main\db\
$ java -classpath "sqlite-jdbc-3.34.0.jar" .\LoginServerSocket.java

Cuando ejecute la aplicación de android, es importante cambiar la ip en la lina 188
del codigo de MainActivity.java por su ip obtenida con el comando ipconfig