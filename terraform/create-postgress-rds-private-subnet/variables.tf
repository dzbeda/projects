variable "aws_region" {
  type = string
  description = "Describe the AWS working region"
}
variable "vpc_cidr" {
  type = string
  default = "10.0.0.0/16"
}
variable "tag_enviroment" {
  description = "Describe the enviroment"
}
variable "project_name" {
  type = string
  default = "main"
}
variable "ansible_server_instance-type" {
  type = string
  default = "t2.micro"
}
variable "private-subnet-block" {
  type = list(string)
}
variable "public-subnet-block" {
  type = list(string)
}
variable "availability_zone" {}
variable "key_name" {}
variable "ami_id" {}
variable "instance_type" {}


