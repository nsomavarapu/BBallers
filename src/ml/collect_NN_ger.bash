#!/bin/bash
# file_list[0]="twenty_five.arff"
# file_list[1]="fifty.arff"
# file_list[2]="seventy_five.arff"
# file_list[3]="train.arff"

vals[0]="10"
vals[1]="25"
vals[2]="50"
vals[3]="75"
vals[4]="100"
vals[5]="200"
vals[6]="300"
vals[7]="400"
vals[8]="500"
vals[9]="1000"
vals[10]="1500"
vals[11]="2000"
vals[12]="2500"
vals[13]="3000"
vals[14]="3500"
vals[15]="4000"
vals[16]="4500"
vals[17]="5000"


L[0]="0.5"
M[0]="0.6"


for i in "${vals[@]}";
do
  java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -L 0.5 -M 0.6 -N $i -t /Users/nathan/Dropbox/Spring_2016/CS_4641/sup_learning/data_sets/germancredit/train.arff -x 10 > "$i.txt"
done
