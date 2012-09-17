#! /bin/sh
# just make sure there is no load on the server during packaging (main reason,
# because harvesting loads single CPU fully and causes even severe swapping
# in 512 MB VMs)
# don't package any open file (not sure, there shouldn't be any...) 
sudo service supervisord stop
sudo service tomcat6 stop
sudo service httpd stop
sudo service postgresql stop

