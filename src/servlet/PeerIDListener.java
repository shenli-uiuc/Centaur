package centaur;

import java.sql.*;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class PeerIDListener extends HttpServlet{

    private Logger logger = null;

    public void doGet(HttpServletRequest request, HttpServletResponse response){
        this.doPost(request, response);
    }


    public void doPost(HttpServletRequest request, HttpServletResponse response){
        
        logger = Logger.getLogger("peerIDLog");
        String peerID = request.getParameter("peer_id");
        logger.write("Got peer id: " + peerID);
        
        

        try{
            response.setContentType("text/html");
            PrintWriter toClient = response.getWriter();
            toClient.println(peerID);

            //construct tree structure 
            //StringBuffer sb = new StringBuffer();
            //sb.append("(");
            String tree = String.format("(%s(%s(%s)(%s))(%s(%s)(%s)))", peerID, peerID, peerID, peerID, peerID, peerID, peerID);
            //call p2p executable
            
            ProcessBuilder pb = new ProcessBuilder("path....", tree, "hello hello");
        }
        catch(Exception ex){
            System.out.println("EXCEPTION in experiments: " + ex.getMessage());
            ex.printStackTrace();
        }
    }
}

