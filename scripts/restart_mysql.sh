cd /scratch/shenli3/software/mysql-5.5.19-linux2.6-x86_64
bin/mysqladmin -u root shutdown &> /scratch/shenli3/log/greencache/mysql_down.log
bin/mysqld_safe --user=shenli3 &> /scratch/shenli3/log/greencache/mysql_up.log &
