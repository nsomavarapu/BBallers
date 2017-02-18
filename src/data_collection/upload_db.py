from awscredentials import ACCESS_KEY,SECRET_KEY
import boto3, csv

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
# table = dynamodb.create_table(TableName='seasonstats',)

f_r = open('AllGames.csv', 'rb')
csv_r = csv.reader(f_r)
header = csv_r.next()

for line in csv_r:
	print line

f_r.close()