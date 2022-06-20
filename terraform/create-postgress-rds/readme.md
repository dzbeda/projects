# This task create AWS RDS using TF
## The TF run will create the below aws objects
1. Create VPN
2. Create 2 public subntes
3. Subnet group
4. Create 2 Internet Gateway
5. Create route table
6. Create Security Group
7. Create RDS based on postgres 

  A. The RDS is based on postgres version 12 ; this can be changed by modify the  "engine_version" parameter 
  B. Defualt password is "thispassword" ; this can be changed by modify the  "password" parameter
  C. The RDS is public and accessable from the outside
