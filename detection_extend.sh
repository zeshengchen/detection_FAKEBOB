archi=gmm 
epsilon=002

for k in {1..20}
do
	date +"%T.%3N"

	python3 detection_extend.py $archi $epsilon $k > ./logs_${archi}_epsilon_${epsilon}/detection_${archi}_epsilon_${epsilon}_extend_min_${k}_results.txt 2> ./logs_${archi}_epsilon_${epsilon}/detection_${archi}_epsilon_${epsilon}_extend_min_${k}_err.txt
	
	date +"%T.%3N"
done

