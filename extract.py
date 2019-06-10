import os, pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
pol_db = myclient["policy_db"]
pol_data = pol_db["policy_data"]

def segments(company, classes):
    workpath = os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in

    df = pd.read_csv(os.path.join(workpath, 'classification.csv'))
    data = {}
    count=0
    for i in df.itertuples():
        url = i[9]
        url = url.replace('.','')
        if company in url:
            category = i[6]
            segement_id = i[5]
            data[count] = {segement_id: category}
            count+=1
    segment = []
    for key, value in data.items():
        for seg, cat in value.items():
            if str(classes) in cat:
                if seg not in segment:
                    segment.append(seg)
    return segment

obj = pol_data.find_one({"name" : str(company)})['data']
total_segments = segments(str(company), classes)
clauses = []
for k, v in obj.items():
    for i in total_segments:
        if k == str(i):
            clauses.append(v)
            # print(message)
