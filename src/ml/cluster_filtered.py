import csv, subprocess, re
file_list = ["/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/shuttle/", "/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/winequality/"]

def collect_clustering():
	cluster_list = [x for x in range(1,11)]
	data = {}
	data[file_list[0]] = [[],[]]
	data[file_list[1]] = [[],[]]

	for f in file_list:
		m = re.search('data_sets/[a-z]*', f)
		dSet_name = m.group(0).replace('data_sets/', '')
		f_open = open(dSet_name + '_clustering_all.csv', 'wb')
		csv_f = csv.writer(f_open)
		csv_f.writerow(["num_clusters", "KMeans_unfiltered", "KMeans_ICA", "KMeans_PCA", "KMeans_RCA", "KMeans_RU", "EM_unfiltered", "EM_ICA", "EM_PCA", "EM_RCA", "EM_RU" ])
		for n in cluster_list:
			val_arr = []
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_ICA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_PCA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_PCA5.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_PCA8.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_RCA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + 'train_RU.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))

			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_ICA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_PCA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_PCA5.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_PCA8.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_RCA.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + 'train_RU.arff -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, ))

			num_arr = []
			for val in val_arr:
				num_arr.append(100 - float(val.communicate()[0].split()[5]))
			print num_arr
			write_arr = [n] + num_arr
			csv_f.writerow(write_arr)
		f_open.close()

def collect_NN_filt():
	iters = [x for x in range(500,2500,500)]
	# iters = [100]
	f_open = open('NN_with_filts.csv', 'wb')
	csv_f = csv.writer(f_open)
	csv_f.writerow(["num_iter", "NN_ICA", "NN_PCA", "NN_RCA", "NN_RU"])
	f = file_list[1]
	print "Starting NN trining with iterations " + str(iters)

	for n in iters:
		print "Collecting iteration number " + str(n)
		val_arr = []
		val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_ICA.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))
		val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_PCA.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))
		val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_RCA.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))
		val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_RU.arff  -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))


		num_arr = []
		for val in val_arr:
			num_arr.append(val.communicate()[0].split()[10])
		print num_arr
		write_arr = [n] + num_arr
		csv_f.writerow(write_arr)
	f_open.close()

def collect_original_NN():
	iters = [x for x in range(500,2500,500)]
	f_open = open('NN_orig.csv', 'wb')
	csv_f = csv.writer(f_open)
	csv_f.writerow(["num_iter", "NN_correct"])
	f = file_list[1]

	print "Starting NN trining with iterations " + str(iters)

	for n in iters:
		print "Collecting iteration number " + str(n)
		value = subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, )

		csv_f.writerow([n, value.communicate()[0].split()[10]])
	f_open.close()

def collect_NN_clustering():
	iters = [x for x in range(500,2500,500)]
	clust_num = [2, 3, 4]
	f_open = open('NN_clust.csv', 'wb')
	csv_f = csv.writer(f_open)
	csv_f.writerow(["num_clust", "num_iter", "NN_KMeans", "NN_EM"])
	f = file_list[1]

	print "Starting NN trining with iterations " + str(iters)

	for j in clust_num:
		for n in iters:
			print "Collecting iteration number " + str(n)
			val_arr = []
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_KM' + str(j) + '.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))
			val_arr.append(subprocess.Popen('java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -t ' + f + 'train_EM' + str(j) + '.arff -N ' + str(n)  + ' | grep Correctly', shell=True, stdout=subprocess.PIPE, ))

			num_arr = []
			for val in val_arr:
				num_arr.append(val.communicate()[0].split()[10])
			print num_arr
			csv_f.writerow([j, n] + num_arr)
	f_open.close()


if __name__ == '__main__':
	collect_clustering()
	# collect_NN_filt()
	# collect_original_NN()
	# collect_NN_clustering()
	