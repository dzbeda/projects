# This task create AWS RDS using TF
## The TF run will create the below aws objects
1. Create VPN
2. Create 2 private subntes
3. Create 2 public subntes
4. Subnet group for private subnet
5. Create Internet Gateway
6. Create route table
7. Create ec2 instance on public subnet
8. Create Security Group for Ec2 instance
9. Create Security Group for RDS
10. Create RDS based on postgres 

  i. The RDS is based on postgres version 12 ; this can be changed by modify the  "engine_version" parameter 
  
  ii. Defualt password is "thispassword" ; this can be changed by modify the  "password" parameter

  iii. The RDS is public and accessable from the outside


## EC2 instance
1. From this instance you can connect the RDS
2. In order to download the psql client run the follwoing command 
    i. sudo apt-get update
    ii. sudo apt-get install postgresql-client
    
3. In orrder to connect to the postgres db run the following :     "psql -h <hostname or ip address> -p <port number of remote machine> -d <database name which you want to connect> -U <username of the database server>"
