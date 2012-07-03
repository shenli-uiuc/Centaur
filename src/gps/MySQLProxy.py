import MySQLdb
import db_conf

class MySQLProxy:
    
    #dump address from users table to address table
    def dump_location(self):
