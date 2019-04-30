#!/bin/bash
#
runTestCase() {
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++ case$num +++++++++++++++++++++++++++++++++++++++++++++++++++++" >> test.log
	echo "expectOutput:" >> test.log
	echo $output|jq . >> test.log
	echo "response:" >> test.log
	case $url in
	/login |/register)
		{
			res=`curl -H "Content-Type: application/json" "http://192.168.137.2:81$url" -X$method -d@test.json`
			token=`echo $res|jq .token`
			token=${token//\"/}
			Auth="Authorization: $token"
		}
		;;
	*)
		{
			if [ $input = 'null' ];then
                		res=`curl -H "Authorization: $token" "http://192.168.137.2:81$url" -X$method`
        		else
				echo $Auth
                		res=`curl -H "Content-Type: application/json" -H "Authorization: $token" "http://192.168.137.2:8103$url" -X$method -d@test.json`
        		fi

		}
		;;
	esac

	echo "response:"
	#tee追加到文件
	echo $res|jq . |tee -a test.log
	echo "testResult:" >> test.log
	comResult $output $res
	echo >> test.log
	let num++
}

comResult() {
	echo 11
	if [ $1 = $2 ];then
		echo "pass" >> test.log
	else
		echo "fail" >> test.log
	fi
}

readCase() {
	num=1
	cat $1 |while read content;do
		method=`echo $content|jq '.method'`
		method=${method//\"/}
		#echo “这是method: $method”
		echo "+++++++++"
		url=`echo $content|jq '.url'`
		url=${url//\"/}
		#echo "这是url: $url"
		echo "+++++++++"
		input=`echo $content|jq '.input' -c|tee test.json`
		#echo $input
		echo '++++++'
		output=`echo $content|jq '.output' -c`
		#echo $output
		echo '++++++'
		#contentArr=("${method}" "${url}" "${input}" "${output}")
		#for i in ${contentArr[@]};do
		#	echo $i
		#done
		runTestCase
		sleep 1
	done
}

if [ $# -gt 0 ];then
	echo "Running all case..., pls wait!"
	readCase $1
	echo $1
	echo $url
	echo $method
	#curl -H "Content-Type: application/json" $url -d@test.json -v >> test.log
fi

#nic=(`cat /proc/net/dev|grep :|awk '{print $1}'`)
#for i in ${nic[@]};do
#	echo $i
#done

#while true;do
#	sleep 1
#	arr=()
#	cat /proc/net/dev|grep :|while read line;do
#		arr+=(`echo $line|awk '{print $2" "$10}'`)
#	done
#	echo ${arr[@]}
#	for nic in ${nic[@]};do
#		
#		echo "$nic\tarr[1]"
#	done
#done
