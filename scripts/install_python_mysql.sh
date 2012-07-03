echo 76warty$ | sudo -S yum -y install python-setuptools.noarch
cd /home/tarek/shenli3/lib/MySQL-python-1.2.3/
python setup.py build
echo 76warty$ | sudo -S python setup.py install
echo 76warty$ | sudo -S ln -s /scratch/shenli3/software/mysql-5.5.19-linux2.6-x86_64/lib/libmysqlclient.so.18 /usr/lib/libmysqlclient.so.18
