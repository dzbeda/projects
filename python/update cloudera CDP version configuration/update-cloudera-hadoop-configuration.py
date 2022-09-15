import requests
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Enviroment configuration
cm_username = 'admin'
cm_password = 'Enter_cloudera_admin_ui_password'
api_version = '/api/v31'
headers = {'content-type': 'application/json'}
cm_port_tls = '7183'
cm_port_none_tls = '7180'

# Hadoop configuration
enable_acl = 'true'
yarn_acl_users = ''
yarn_http_kerberos = 'true'
resourcemanager_java_heapsize = 2
jobhistory_java_heapsize = 2
hdfs_http_kerberos = 'true'
spark2_dynamic_allocation = 'false'
spark3_dynamic_allocation = 'false'
hue_timezone = 'UTC'
nodemanager_java_heapsize = 2
datanode_java_heapsize = 6 # Memory GB. The data-node requires 1GB of memory + additional 1G for each 1M block - 6G for 5M blocks
namenode_java_heapsize = 16 # Memory GB. The name-node requires 1GB of memory + additional 1G for each 1M block in the cluster - 16G for 15M blocks in the cluster


def run_api (parameter_name,parameter_value,api_path):
    #print(base_url + api_path)
    response = requests.put(url=base_url + api_path,
                            data=f'{{"items":[{{ "name": "{parameter_name}","value": "{parameter_value}"}}]}}',
                            headers=headers, auth=(cm_username, cm_password), verify=False)
    if response.status_code == 200:
        print(f'{parameter_name} Configuration was updated to {parameter_value} \n')
    elif response.status_code == 400:
        print(f'{parameter_name} can not be updated due to bad parameters \n')
        exit()
    else:
        print(f'Problem connecting to cloudera admin, {parameter_name} could not be configured \n')
        exit()


###  Update configuration taken from cloudera_enviroment file ###
with open(r'./cloudera_environment.yml') as file:
    cloudera_environment = yaml.load(file)

cm_ip = (cloudera_environment['cloudera_managment_server']['ip'])
hdfs_system_user = (cloudera_environment['hadoop_system_user']['username'])
ingestion_cluster_name = (cloudera_environment['cloudera_ingestion_cluster_name'])
tls_support =(cloudera_environment['tls_support'])
print(f'cloudera management server IP: {cm_ip} \n')
print(f'Cloudera ingestion cluster name:  {ingestion_cluster_name} \n')
print(f'tls support: {tls_support} \n')

if tls_support == True:
    cm_port = cm_port_tls
    protocol = 'https://'
else:
    cm_port = cm_port_none_tls
    protocol = 'http://'

api_calls = []
base_url = f'{protocol}{cm_ip}:{cm_port}{api_version}/clusters/{ingestion_cluster_name}'
if __name__ == '__main__':

    api_calls.append({"parameter_name": "node_manager_java_heapsize",
                      "parameter_value": nodemanager_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/yarn/roleConfigGroups/yarn-NODEMANAGER-BASE/config'})
    api_calls.append({"parameter_name": "time_zone",
                      "parameter_value": hue_timezone,
                      "api_path": '/services/hue/config'})
    api_calls.append({"parameter_name": "spark_dynamic_allocation_enabled",
                      "parameter_value": spark3_dynamic_allocation,
                      "api_path": '/services/spark3_on_yarn/roleConfigGroups/spark3_on_yarn-GATEWAY-BASE/config'})
    api_calls.append({"parameter_name": "spark_dynamic_allocation_enabled",
                      "parameter_value": spark2_dynamic_allocation,
                      "api_path": '/services/spark_on_yarn/roleConfigGroups/spark_on_yarn-GATEWAY-BASE/config'})
    api_calls.append({"parameter_name": "hadoop_secure_web_ui",
                      "parameter_value": hdfs_http_kerberos,
                      "api_path": '/services/hdfs/config'})
    api_calls.append({"parameter_name": "mr2_jobhistory_java_heapsize",
                      "parameter_value": jobhistory_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/yarn/roleConfigGroups/yarn-JOBHISTORY-BASE/config'})
    api_calls.append({"parameter_name": "hadoop_secure_web_ui",
                      "parameter_value": yarn_http_kerberos,
                      "api_path": '/services/yarn/config'})
    api_calls.append({"parameter_name": "yarn_admin_acl",
                      "parameter_value": yarn_acl_users,
                      "api_path": '/services/yarn/config'})
    api_calls.append({"parameter_name": "yarn_acl_enable",
                      "parameter_value": enable_acl,
                      "api_path": '/services/yarn/config'})
    api_calls.append({"parameter_name": "resource_manager_java_heapsize",
                      "parameter_value": resourcemanager_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/yarn/roleConfigGroups/yarn-RESOURCEMANAGER-BASE/config'})
    api_calls.append({"parameter_name": "datanode_java_heapsize",
                      "parameter_value": datanode_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/hdfs/roleConfigGroups/hdfs-DATANODE-BASE/config'})
    api_calls.append({"parameter_name": "namenode_java_heapsize",
                      "parameter_value": namenode_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/hdfs/roleConfigGroups/hdfs-NAMENODE-BASE/config'})
    api_calls.append({"parameter_name": "secondary_namenode_java_heapsize",
                      "parameter_value": namenode_java_heapsize * 1024 * 1024 * 1024,
                      "api_path": '/services/hdfs/roleConfigGroups/hdfs-SECONDARYNAMENODE-BASE/config'})
    ## The following  parameters are required in order to support presto
    api_calls.append({"parameter_name": "core_site_safety_valve",
                      "parameter_value": f'<property><name>hadoop.proxyuser.{hdfs_system_user}.hosts</name><value>*</value><description>impersonate presto</description></property><property><name>hadoop.proxyuser.{hdfs_system_user}.groups</name><value>*</value><description>impersonate presto</description></property>',
                      "api_path": '/services/hdfs/config'})
    api_calls.append({"parameter_name": "hive_service_config_safety_valve",
                      "parameter_value": f'<property><name>hive.server2.tez.initialize.default.sessions</name><value>false</value></property>',
                      "api_path": '/services/hive_on_tez/config'})
    api_calls.append({"parameter_name": "hiveserver2_enable_impersonation",
                      "parameter_value": "true",
                      "api_path": '/services/hive/roleConfigGroups/hive-HIVESERVER2-BASE/config'})
    for api_call in api_calls:
        run_api(api_call["parameter_name"], api_call["parameter_value"], api_call["api_path"])
