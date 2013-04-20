package centaurexp;

import java.sql.*;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;


public class UserStatus extends HttpServlet{
    private static Logger logger = null;

    private static final String strInsertUserStatus = "insert into user_status values (?, ?, ?, ?, ?, ?)";
    private static final String strInsertOnlineUser = "insert into online_user values (?, ?)  ON DUPLICATE KEY UPDATE ip = values(ip)";
    private static final String strDeleteOnlineUser = "delete from online_user where user_id = ?";

    private static boolean initialized = false; 

    private Connection getDBConnection(String url, String usr, String pwd){
        Connection c = null;
        try{
            c = DriverManager.getConnection(url, usr, pwd);
        }
        catch(Exception ex){
            if(ConfKeeper.DEBUG){
                logger.write("Exception in UserStatus.getDBConnection : " + ex.getMessage() + ", " + ex.getStackTrace().toString());
            }
            c = null;
        }
        return c;
    }

    private boolean insertUserStatus(long time, String uid, String ip, String addr, double latitude, double longitude){
        try{
            Connection c = getDBConnection(ConfKeeper.DB_URL, ConfKeeper.DB_USR, ConfKeeper.DB_PWD);
            PreparedStatement pStmnt = c.prepareStatement(this.strInsertUserStatus);
            pStmnt.setLong(1, time);
            pStmnt.setString(2, uid);
            pStmnt.setString(3, ip);
            pStmnt.setString(4, addr);
            pStmnt.setDouble(5, latitude);
            pStmnt.setDouble(6, longitude);

            pStmnt.executeUpdate();
            c.close();
            return true;
        }
        catch(Exception ex){
            if(ConfKeeper.DEBUG){
                logger.write("Exception in UserStatus.insertUserStatus: " + time + ", " + uid + ", " + ip + ", " + addr + ", " + latitude + ", " + longitude);
            }
        }
        return false;
    }

    private boolean insertOnlineUser(String uid, String ip){
        try{
            Connection c = getDBConnection(ConfKeeper.DB_URL, ConfKeeper.DB_USR, ConfKeeper.DB_PWD);
            PreparedStatement pStmnt = c.prepareStatement(this.strInsertOnlineUser);
            pStmnt.setString(1, uid);
            pStmnt.setString(2, ip);

            pStmnt.executeUpdate();
            c.close();
            return true;
        }
        catch(Exception ex){
            if(ConfKeeper.DEBUG){
                logger.write("Exception in UserStatus.insertOnlineUser: " + uid + ", " + ip);
            }
        }
        return false;
    }

    private boolean deleteOnlineUser(String uid){
        try{
            Connection c = getDBConnection(ConfKeeper.DB_URL, ConfKeeper.DB_USR, ConfKeeper.DB_PWD);
            PreparedStatement pStmnt = c.prepareStatement(this.strDeleteOnlineUser);
            pStmnt.setString(1, uid);

            pStmnt.executeUpdate();
            c.close();
            return true;
        }
        catch(Exception ex){
            if(ConfKeeper.DEBUG){
                logger.write("Exception in UserSttaus.deleteOnlineUser: " + uid);
            }
        }
        return false;
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response){
        this.doPost(request, response);
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response){
        if(false == initialized){
            logger = Logger.getLogger(ConfKeeper.FILENAME);
            try{
                Class.forName(ConfKeeper.DB_DRIVER_NAME);
                logger.write("Driver loaded : " + ConfKeeper.DB_DRIVER_NAME);
            }
            catch(Exception ex){
                System.out.println("In UserStatus.doPost, initilization: " + ex.getMessage());
                ex.printStackTrace();
            } 
            initialized = true;
        }

        String op = request.getParameter("op");

        String res = null;
        if("login".equals(op) || "heartbeat".equals(op)){
            long ts = System.currentTimeMillis();
            String uid = request.getParameter("uid");
            String ip = request.getParameter("ip");
            String addr = request.getParameter("addr");
            double latitude = Double.parseDouble(request.getParameter("lat"));
            double longitude = Double.parseDouble(request.getParameter("lon"));

            if(insertUserStatus(ts, uid, ip, addr, latitude, longitude)  && insertOnlineUser(uid, ip)){
                res = "Entry (" + ts + ", " + uid + ", " + ip + ", " + addr + ", " + latitude + ", " + longitude +  ") Inserted";
            } 
        }
        else if("logout".equals(op)){
            long ts = System.currentTimeMillis();
            String uid = request.getParameter("uid");

            if(deleteOnlineUser(uid)){
                res = "user " + uid + "logout at time " + ts;
            }
        }
        else{
            res = "unrecognized operation";
        }
        

        if(null == res){
            res = "Error"; 
        }

        try{
            response.setContentType("text/html");
            PrintWriter toClient = response.getWriter();
            toClient.println(res);
        }
        catch(Exception ex){
            System.out.println("EXCEPTION in UserStatus.doPost: " + ex.getMessage());
            ex.printStackTrace();
        }

    }
}
