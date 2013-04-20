package centaurexp;

import java.sql.*;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;


public class DataFetcher extends HttpServlet{

    private static final String FILENAME = "/scratch/centaur/log/centaur.log";
    private static final String DB_URL = "jdbc:mysql://tareka03.cs.uiuc.edu:3306/centaur";
    private static final String DB_USR = "centaur";
    private static final String DB_PWD = "centaur";

    private static final boolean DEBUG = false;
    private static long [] dbBound = {925000L, 3124997L, 7524999L, 13324998L, 20925000L, 26625000L, 33928886L};

    private static boolean initialized = false;
    private static MemConnPool memConnPool = null;
    private static DBConnPool dbConnPool = null;
    private static ConfKeeper confKeeper = null;   
    private static Logger logger = null;

    private static final String strGetTextStmt  = "select old_text from text where old_id =" +
        "(select rev_text_id from revision where rev_id =" +
        "(select page_latest from page where page_id = ? ))";

    private static final String strPutUserStatus = "insert into user_status values (?, ?, ?, ?, ?, ?)";

    private int memServerSize = 0;

    private Connection getDBConnection(String url, String usr, String pwd){
        Connection c = null;
        try{
            c = DriverManager.getConnection(url, usr, pwd);
        }
        catch(Exception ex){
            if(DEBUG){
                logger.write("Exception in DBConnFactory.makeObject : " + ex.getMessage() + ", " + ex.getStackTrace().toString());
            }
            c = null;
        }
        return c;
    }

    private void insertUserStatus(long time, String uid, String ip, String addr, double latitude, double longitude){
        Connection c = getDBConnection(this.DB_URL, this.DB_USR, this.DB_PWD);
        PreparedStatement pStmnt = c.prepareStatement(this.strPutUserStatus);
        pStmnt.setLong(1, time);
        pStmnt.setString(2, uid);
        pStmnt.setString(3, ip);
        pStmnt.setString(4, addr);
        pStmnt.setDouble(5, latitude);
        pStmnt.setDouble(6, longitude);


    }

    public void doGet(HttpServletRequest request, HttpServletResponse response){
        this.doPost(request, response);
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response){
        if(false == initialized){
            logger = Logger.getLogger(FILENAME);
            initialized = true;
        }

        this.memServerSize = confKeeper.getMemServerSize();

        String op = request.getParameter("op");
        String uid = request.getParameter("uid");
        long ts = System.currentTimeMillis();



    }
}
