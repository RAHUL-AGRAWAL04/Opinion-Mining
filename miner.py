#using stemmer to get root word of the perticular words
#so that multiple similar words isn't repeated
#for example:- camera and cameras refer to same context camera
from nltk.stem import PorterStemmer
ps = PorterStemmer()

import os
path = "/home/kali/PROJECTS/ONGOING/Opinion_mining/Data/" #path where data is stored
dirs = os.scandir(path) #Scanning data directory

product_reviews = {} #{name:{feature:{P:n,N:n}}} ## format to store data

#for each directory in data directory
for d in dirs: 
    if d.name[0] != '.': #Condition to skip hidden files
        files = os.scandir(str(path)+str(d.name)+'/') #scanning directory within data directory to get list files
    else:continue
    
    #for each files in directory d
    for file1 in files:
        _file = file1.name #getting file/product name
        
        if _file.lower() != 'readme.txt' and _file[0]!='.': #condition to skip readme and hidden files
           
            #opening files
            with open(str(path)+str(d.name)+'/'+_file, errors='ignore') as f: 
                feature = {}            #Dictionary to store feature names and its positive and negative reviews.
                lines = f.read()        #reading file content
                lines=lines.split('\n') #Creating list of lines available in file
                
                #parsing each line in a file
                for line in lines: 
                    if line[0:2] !='##' and ('##' in line): #Skiping lines which doesn't have product review value
                        
                        #splitting line wrt '##' to get feature and its review value
                        sl = line.split('##') 
                        sl = sl[0].split(',') #splitting by ',' to get list of each feature with its value
                        
                        #for each feature in feature list named 'sl'
                        for fe in sl:
                            #Splitting feature by '[' to get feature name and feature value
                            #attr contains feature_name at position 0 and its value at position 1 with garbage character ']' at end
                            attr = fe.split('[') 
                            
                            #1. Stemming each feature name using stemmer in order to ensure no repetation
                            #2. checking if feature name exists in features dictionry or not. If not adding it to the dict
                            if ps.stem(attr[0].strip()) not in feature: 
                                feature[ps.stem(attr[0].strip())] = {'positive':0,'negative':0}
                            
                            #clearing garbage character form freature value and adding feature value to the appropriate feature
                            try:
                                rate = (attr[1].split(']'))[0].strip()
                                if rate[0] == '+':
                                    feature[ps.stem(attr[0].strip())]['positive'] += int(rate[1:])
                                elif rate[0] == '-':
                                    feature[ps.stem(attr[0].strip())]['negative'] += int(rate[1:])
                            except:pass
                #Here opinion mining of one product is completed and stored in dictionary names features
                #adding features of product to product_reviews dictionary
                #we need to remove extintion of file to get product name
                product_reviews[(_file.split('.'))[0]] = feature

import json
with open("result.json", "w") as outfile: 
    json.dump(product_reviews, outfile)

#Printing mined opinions
for k1,v1 in product_reviews.items():
    print(f'\n\n\nProdut : {k1}')
    i=0
    for k2,v2 in v1.items():
        i+=1
        print(f'\tFeature{i} : {k2}')
        print(f'\t\tPositive : {v2["positive"]}')
        print(f'\t\tNegative : {v2["negative"]}')
        
