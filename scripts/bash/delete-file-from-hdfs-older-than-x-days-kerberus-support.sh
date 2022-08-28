 #!/usr/bin/bash 
folder_path="/data/_delta_log"
delete_files_older_then=60  # In days
keytab_refresh_counter=3600 #set keytab referes token = default should be 3600
generate_keytab() {
  kinit $user@$domain -kt $keytab_path$keytab_file_name
	klist -s
	if [ $? -eq 0 ];
	then
	  echo "Keytab was generated"
	else
	  echo "Keytab can not be generated"
	  exit 1
	fi
}
verify_folder_path() {
  hdfs dfs -test -d $1
  if [ $? -eq 0 ]
  then
    echo $1 " exists in the hdfs file system"
  else
    echo $1 " doesn't exist in the hdfs file system -- exiting !!!"
    exit 1
  fi
}
get_current_date() {
  today=$(date +%F)  # Get current date
  #echo $today
  today_time_converted=$(date -d ${today} '+%s')  #Convert time to epoch
  #echo $today_time_converted
}

delete_files() {
  set_keytab_refresh_counter=$keytab_refresh_counter
  hdfs dfs -ls -R ${folder_path} |  grep "^-" | while read line ; do  #get file list
  set_keytab_refresh_counter=$(( set_keytab_refresh_counter - 1))
  echo $set_keytab_refresh_counter
  if [ $set_keytab_refresh_counter -eq "0" ];
  then
    generate_keytab
    set_keytab_refresh_counter=$keytab_refresh_counter
  else

    file_date=$(echo ${line} | awk '{print $6}')  #get file date
    #echo $file_date
    file_time_converted=$(date -d ${file_date} '+%s')  #Convert time to epoch
    #echo $file_time_converted
    diffrencet=$(( ( today_time_converted - file_time_converted )/(60*60*24) ))
    #echo $diffrencet

    if [ ${diffrencet} -gt ${delete_files_older_then} ]; then
        filePath=$(echo ${line} | awk '{print $8}')
        hdfs dfs -rm -skipTrash $filePath
    fi
  fi
  done
}
## Keytab parameters
if [ -z "$1" ];
then
	echo "Please note that since username was not entered to generate a keytab - zbeda user is the default"
	user=zbeda
else
	user=$1
fi

if [ -z "$2" ];
then
	echo "Please enter domain name were the keytab was generated  - Example : ZBEDA.LOCAL"
	domain=ZBEDA.LOCAL
	#exit 1
else
	domain=${2^^}
fi

if [ -z "$3" ];
then
	echo "Since no keytab path was defined - default value is /opt/"
	keytab_path=/opt/
else
  keytab_path=$3
fi

if [ -z "$4" ];
then
	echo "Since no keytab file name was define - default value is" $user".keyab"
	keytab_file_name=$user.keytab
else
  keytab_file_name=$4
fi

## Run
generate_keytab
verify_folder_path $folder_path
get_current_date
echo "files older then " $delete_files_older_then " days will be deleted"
delete_files
