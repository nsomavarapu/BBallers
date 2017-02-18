vals[0]="500"
vals[1]="1000"
vals[2]="1500"
vals[3]="2000"
vals[4]="2500"
vals[5]="3000"
vals[6]="3500"
vals[7]="4000"
vals[8]="4500"
vals[9]="5000"
vals[10]="6000"
vals[11]="7000"

echo "">/Users/nathan/Dropbox/Spring_2016/ECE_4813/BBallers/out/mlp_training_data.txt

for i in "${vals[@]}";
do
  java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -N $i -t /Users/nathan/Dropbox/Spring_2016/ECE_4813/BBallers/data/player_diff.arff -x 10 | grep "Incorrectly" >> /Users/nathan/Dropbox/Spring_2016/ECE_4813/BBallers/out/mlp_training_data.txt
done
