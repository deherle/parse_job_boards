from googlesearch import search
import csv
import pandas as pd
import re
from datetime import datetime
print('================================================')
print('GOOGLE SEARCH')
print('================================================')
# Get user search keyword.
searchKeyWord = input('Enter your search keyword: ')
# Get Total number of records.
totalNoOfRecords = input('How many records you need to save in CSV? ')
print('Please wait. Your request is being processed. \n')
resultLinks = []
# Search the keyword in google.
results = search(searchKeyWord, num_results=int(totalNoOfRecords))
#results = '\n'.join([str(elem) for elem in results])
# Convert result into data frame.
df = pd.DataFrame(results)
now = datetime.now()
outputFileName = 'input_urls.csv'
# Write output in CSV format.
df.to_csv(outputFileName,mode='a', encoding='utf-8', index=False , header=False)
print('================================================\n')
print('Your data has been processed successfully!!. Please check the output in the below file!!\n')
print(outputFileName + '\n')
print('================================================\n')