import requests
import yaml
import json
import logging
from string import Template

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


DB_HOSTNAME = 'es1'
DB_PORT = '9200'
BASE_URL = '_opendistro/_ism/policies'
URL_HEADERS = {'content-type': 'application/json'}
SITE_INFO_FILE_PATH = './ism-input.yml'


def check_input_file(list_of_ism_retention_policies_to_upload):
    for policy_name in list_of_ism_retention_policies_to_upload:
        if policy_name['status'] != 'enable' and policy_name['status'] != 'disable':
            print('status value is not configured correctly for '+ policy_name['index_name'] + ' index.  status should be set to enable or disable , currently it is set to ' + policy_name['status'] )
            return False
def get_policies():
    active_ism_policies = []
    active_ism_policies_names = []
    try:
        get_response = requests.get(url=f'http://{DB_HOSTNAME}:{DB_PORT}/{BASE_URL}', headers=URL_HEADERS, verify=False)
    except:
        print(f'Please check the connection to Elastic server. Elastic Hostname {DB_HOSTNAME} and port {DB_PORT}')
    get_policies_response = json.loads(get_response.content)
    for policy in get_policies_response["policies"]:
        policy_details = {'policy_name': policy['_id'],
                          'policy_sequential_number': policy['_seq_no'],
                          'policy_primary_term': policy['_primary_term']}
        active_ism_policies.append(policy_details)
    for policy_name_id in active_ism_policies:
        active_ism_policies_names.append(policy_name_id['policy_name'])
    return (active_ism_policies,active_ism_policies_names)

def delete_policy(policy_name):
    delete_response = requests.delete(url=f'http://{DB_HOSTNAME}:{DB_PORT}/{BASE_URL}/{policy_name}', headers=URL_HEADERS,
                                      verify=False)
    if delete_response.status_code == 200:
        logging.info(f'policy {policy_name} was delete successfully')
        return True
    else:
        print('policy {policy_name} was not created - please check connectivity to the server ,check if index prefix'
              ' already exsists or other policy parameters')
        print(f'status code is : {delete_response.status_code} and status content is {delete_response.content}')
        return False

def update_policy_template(policy_name,min_index_age_in_days):
    policy_template = '''{
        "policy": {
            "description": "$policy_name index retention flow",
            "default_state": "hot",
            "schema_version": 1,
            "states": [
                {
                    "name": "hot",
                    "actions": [
                        {
                            "open": {}
                        }
                    ],
                    "transitions": [
                        {
                            "state_name": "delete",
                            "conditions": {
                                "min_index_age": "${min_index_age_in_days}d"
                            }
                        }
                    ]
                },
                {
                    "name": "delete",
                    "actions": [
                        {
                            "delete": {}
                        }
                    ]
                }
            ],
            "ism_template": [
                {
                    "index_patterns": [
                        "$policy_name-*"
                    ],
                    "priority": 100
                }
            ]
        }
    }'''
    policy_template_obj = Template(policy_template)
    updated_policy = policy_template_obj.substitute(policy_name=policy_name, min_index_age_in_days=min_index_age_in_days)
    return updated_policy

def create_policy(policy_name,min_index_age_in_days):
    policy_json_format = update_policy_template(policy_name, min_index_age_in_days)
    create_response = requests.put(url=f'http://{DB_HOSTNAME}:{DB_PORT}/{BASE_URL}/{policy_name}', data=policy_json_format,
                                   headers=URL_HEADERS, verify=False)
    if create_response.status_code == 201:
        logging.info(f'policy {policy_name} was created successfully')
        return True
    elif create_response.status_code == 409:
        logging.error(f'Policy {policy_name} was not created - Please check if policy name already exsists')
        logging.error(f'status code is : {create_response.status_code} and status content is {create_response.content}')
        return False
    else:
        logging.error(f'policy {policy_name}  was not created - please check connectivity to the server ,check if index'
                      f' prefix already exsists or other policy parameters')
        logging.error(f'status code is : {create_response.status_code} and status content is {create_response.content}')
        return False

def update_policy(policy_name,min_index_age_in_days,policy_sequential_number,policy_primary_term):
    policy_json_format = update_policy_template(policy_name, min_index_age_in_days)
    update_response = requests.put(url=f'http://{DB_HOSTNAME}:{DB_PORT}/{BASE_URL}/{policy_name}?if_seq_no={policy_sequential_number}&if_primary_term={policy_primary_term}',
                                   data=policy_json_format, headers=URL_HEADERS, verify=False)
    if update_response.status_code == 200:
        logging.info(f'policy {policy_name} was update successfully')
        return True
    elif update_response.status_code == 400:
        logging.error(f'Policy {policy_name} was not updated - Please check if index prefix is defined in other ism policy')
        logging.error(f'status code is : {update_response.status_code} and status content is {update_response.content}')
        return False
    elif update_response.status_code == 409:
        logging.error(f'Policy {policy_name} was not updated - Please check if opensearch_main_ism_retention_policy'
                      f'section under site-info file includes multiple index name ')
        logging.error(f'status code is : {update_response.status_code} and status content is {update_response.content}')
        return False
    else:
        logging.error(f'policy {policy_name} was not updated - please check connectivity to the server or policy parameters')
        logging.error(f'status code is : {update_response.status_code} and status content is {update_response.content}')
        return False

def main():
    with open(rf'{SITE_INFO_FILE_PATH}') as file:
        opensearch_main_ism_retention_policy = yaml.load(file)
        list_of_ism_retention_policies_to_upload = (opensearch_main_ism_retention_policy['opensearch_main_ism_retention_policy'])
        check_input_file_status = check_input_file(list_of_ism_retention_policies_to_upload)
        if check_input_file_status == 'false':
            exit()
    active_ism_policies, active_ism_policies_names = get_policies()
    for policy in list_of_ism_retention_policies_to_upload:
        if (policy['status']) == 'disable':
            if (policy['index_name']) in active_ism_policies_names:
                logging.info('policy ' + policy['index_name'] + ' will be delete..Verify delete policy message confirmation was received')
                delete_policy_status = delete_policy(policy['index_name'])
                if delete_policy_status == False:
                    logging.error(f'check what went wrong and re-run the playbook')
                    exit(1)
            else:
                logging.info(('policy ' + policy['index_name'] + ' is not active policy in opensearch therefore it was not delete'))
        elif (policy['status']) == 'enable':
            if (policy['index_name']) in active_ism_policies_names:
                for policy_details in active_ism_policies:
                    if policy['index_name'] == policy_details['policy_name']:
                        policy_sequential_number = policy_details['policy_sequential_number']
                        policy_primary_term = policy_details['policy_primary_term']
                        update_policy_status = update_policy(policy['index_name'], policy['min_index_age_in_days'],  policy_sequential_number, policy_primary_term)
                        if update_policy_status == False:
                            logging.error(f'check what went wrong and re-run the playbook')
                            exit(1)
            else:
                create_policy_status = create_policy(policy['index_name'],policy['min_index_age_in_days'])
                if create_policy_status == False:
                    logging.error(f'check what went wrong and re-run the playbook')
                    exit(1)
        else:
            logging.error('something is wrong - Please check the "opensearch_main_ism_retention_policy" section under '
                          'site-info.yml file')
if __name__ == '__main__':
    main()
