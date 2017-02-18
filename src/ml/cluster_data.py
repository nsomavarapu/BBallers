import csv, subprocess, re
file_list = ["/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/shuttle/train.arff", "/Users/nathan/Dropbox/Spring_2016/CS_4641/usup_learning/data_sets/winequality/train.arff"]
cluster_list = [x for x in range(1,11)]
data = {}
data[file_list[0]] = [[],[]]
data[file_list[1]] = [[],[]]

for f in file_list:
	m = re.search('[a-z]*/[a-z]*.arff', f)
	# print m.group(0)
	n = re.search('[a-z]*.arff', f)
	n = n.group(0)
	# print n
	dSet_name = m.group(0)
	dSet_name = dSet_name.replace('/' + n, '')
	f_open = open(dSet_name + '_clustering.csv', 'wb')
	csv_f = csv.writer(f_open)
	for n in cluster_list:
		val_kmean = subprocess.Popen('java -cp weka.jar weka.clusterers.SimpleKMeans -t ' + f + ' -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, )
		val_em = subprocess.Popen('java -cp weka.jar weka.clusterers.EM -t ' + f + ' -c last -N ' + str(n)  + ' | grep Incorrectly', shell=True, stdout=subprocess.PIPE, )
		write_arr = [n, (100 - float(val_kmean.communicate()[0].split()[5])), (100 - float(val_em.communicate()[0].split()[5]))]
		csv_f.writerow(write_arr)
	f_open.close()