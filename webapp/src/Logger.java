package centaurexp;

import java.io.*;
import java.util.*;
import java.text.*;


public class Logger{

    private String fileName = null;
    private File file = null;
    private Calendar cal = null;
    private DateFormat dateFormat = null;

    private static Logger logger = null;

    private Logger(String filename){
        this.fileName = filename;
        try{
            this.dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
            this.cal = Calendar.getInstance();
            this.file = new File(this.fileName);
        }
        catch(Exception ex){
            System.out.println("In Logger-Constructor Exception : " + ex.getMessage());
            ex.printStackTrace();
        }

    }


    public static synchronized Logger getLogger(String filename){
        if(null == logger){
            logger = new Logger(filename);
        }
        return logger;
    }

    public synchronized void write(String msg){
        try{
            FileWriter fileWriter = new FileWriter(this.file, true);
            fileWriter.write(dateFormat.format(cal.getTime()) + " --- " + msg + "\n");
            fileWriter.close();

        }
        catch(Exception ex){
            System.out.println("Exception in Logger-write : " + ex.getMessage());
            ex.printStackTrace();
        }
    }

}
