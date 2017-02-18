# file_list[0]="/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/shuttle/train.arff"
# file_list[1]="/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/winequality/train.arff"

# cluster_list[0]="1"
# cluster_list[1]="2"
# cluster_list[2]="3"
# cluster_list[3]="4"
# cluster_list[4]="5"
# cluster_list[5]="6"
# cluster_list[6]="7"
# cluster_list[7]="8"
# cluster_list[8]="9"
# cluster_list[9]="10"

# for $f in "${file_list[@]}"
# do
# 	for $n in "${cluster_list[@]}"
# 	do
# 		per_i$(java -cp weka.jar weka.clusterers.SimpleKMeans -t $f -c last -N $n | grep "Incorrectly")
# 	done
# done

# pwd_var=$(pwd)
# echo $pwd_var

var1=100
var2=17
result=$((var1-var2))
echo $result