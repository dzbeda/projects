# This task creates AWS RDS using TF. The RDS will be created on the public subnet and is accessible from external network 

Values can be updated under **terraform.tfvars file

## The TF run will create the below aws objects
1. Create VPN
2. Create 2 public subntes
3. Subnet group
4. Create 2 Internet Gateway
5. Create a route table
6. Create a decurity Group
7. Create RDS based on postgres 
    1. The RDS is based on postgres version 12 ; this can be changed by modifying the "engine_version" parameter 
    2. Default password is "thispassword" ; this can be changed by modifying the "password" parameter
    3. The RDS is public and accessible from the outside
