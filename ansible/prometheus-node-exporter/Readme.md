# Node-exporter version

  1. The node-exporter supports linux OS
  2. The node-exporter is based on version 1.3.1

# Node-exporter upgrade
In case node-exporter upgrade is required , Please folow the below steps 

  1. Down load the node-exporter file from the follwoing website - https://prometheus.io/download/#node_exporter
   ** Make sure to downlaod the folowing file "node_exporter-<version>.linux-amd64.tar.gz"
  
  2. Extract the file
  3. Copy the node-exporter binary file under "roles\node-exporter\files\node-exporter"

  # How to use it 
  
  In your main playbook add the follwoing tasks 
  
  - hosts: all
  become: true
  any_errors_fatal: true
  gather_facts: False
  roles:
    - node-exporter
