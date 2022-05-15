package server.main.db;

import java.sql.*;

public class SQLiteJDBC {

                    public static void main( String args[] ) {
                    Connection c = null;
                    Statement stmt = null;
                    
                    try {
                        Class.forName("org.sqlite.JDBC");
                        c = DriverManager.getConnection("jdbc:sqlite:SQLiteDatabase.db");
                        System.out.println("Opened database successfully");

                        stmt = c.createStatement();
                        String sql = "CREATE TABLE REQUESTS " +
                                        "(ID INTEGER PRIMARY KEY    AUTOINCREMENT   NOT NULL, " +
                                        " TIMESTAMP      datetime2       NOT NULL, " + 
                                        " DATA           TEXT           NOT NULL, " + 
                                        " VERIFICATION   BIT                     )"
                                        ; 
                        stmt.executeUpdate(sql);
                        stmt.close();
                        c.close();
                    } catch ( Exception e ) {
                        System.err.println( e.getClass().getName() + ": " + e.getMessage() );
                        System.exit(0);
                    }
                    System.out.println("Table created successfully");
                }
                }