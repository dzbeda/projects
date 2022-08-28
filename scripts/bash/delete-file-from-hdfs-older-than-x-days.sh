 #!/usr/bin/bash 
#Define the folder from which you wish to delete the files
folder_path="/sensor/_delta_log"
#Define the age of the files (in days) you wish to delte. for eaxmple 30 , means to delete files that are than 30 days 
delete_files_older_then=132
today=$(date +%F)  # Get current date 
#echo $today
today_time_converted=$(date -d ${today} '+%s')  #Convert date to epoch time
#echo $today_time_converted
hdfs dfs -ls -R ${folder_path} |  grep "^-" | while read line ; do  # Get list of files from folder 
filePath=$(echo ${line} | awk '{print $8}') #Extract file path 
#echo $filePath
file_date=$(echo ${line} | awk '{print $6}')  #get file date
#echo $file_date
file_time_converted=$(date -d ${file_date} '+%s')  #Convert date to epoch time 
#echo $file_time_converted
diffrencet=$(( ( today_time_converted - file_time_converted )/(60*60*24) )) #Verify the time diffrence from current date
#echo $diffrencet
if [ ${diffrencet} -gt ${delete_files_older_then} ]; then	
	echo "delete file" ${filePath}
	hdfs dfs -rm -r -skipTrash $filePath
fi
done
