# Check if folder exists on HDFS 
hdfs dfs -test -d /new_folder
#echo $? ; If=0 folder exists , if=1 folder doesn't exists
if [ $? -eq 0 ]
then
	echo "new_folder exists in the hdfs file system"
else
	echo "new_folder doesn't exist in the hdfs file system"
fi



# Check if file exists on HDFS  
hdfs dfs -test -e /new_folder/new_file.xml
#echo $? ; If=0 file exists , if=1 file doesn't exists
if [ $? -eq 0 ]
then
	echo "new_file.xml exists in the hdfs file system"
else
	echo "new_file.xml doesn't exist in the hdfs file system"
fi
