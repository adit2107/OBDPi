import java.sql.*;
import com.microsoft.sqlserver.jdbc.*;
import java.io.*;

public class maxspeed
{
	public static void main(String[] args) 
	{
	String connectionUrl = "jdbc:sqlserver://boschsql.database.windows.net:1433;database=boschdb;user=bosch@boschsql;password=Asd12345****;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;";
      	Connection con = null;
      	Statement stmt = null;
	ResultSet rs = null;
	try
	{
        	Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
         	con = DriverManager.getConnection(connectionUrl);
	        String SQL = "SELECT thresh FROM dbo.thresh where id = 'speed';";
         	stmt = con.createStatement();
	        rs = stmt.executeQuery(SQL);
	        while (rs.next())
		{
			FileWriter fw = new FileWriter("speedthresh.txt");
			BufferedWriter out = new BufferedWriter(fw);
			out.write(rs.getString(1));
			out.close();
FileWriter fw1 = new FileWriter("startflag.txt", true);
			BufferedWriter out1 = new BufferedWriter(fw1);
			out1.write("\n");
			out1.write("1");
			out1.close();

         	}
      }

      catch (Exception e) 
      {
      		e.printStackTrace();
		System.out.println("Exception :" + e);
      }
      finally 
      {
         if (rs != null) try { rs.close(); } catch(Exception e) {}
         if (stmt != null) try { stmt.close(); } catch(Exception e) {}
         if (con != null) try { con.close(); } catch(Exception e) {}
      }

   }
}
