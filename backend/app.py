import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression

from flask import Flask, request
from flask_cors import CORS
import json

# Dataset handling
df = pd.read_csv('500_Cities_CDC.csv')
c = df.columns.values.tolist()
for i in c:
    if '95CI' in i:
        c.remove(i)
for i in c:
    if 'Crude' in i:
        c.remove(i)
df = df[c]
df.columns = ['StateAbbr', 'PlaceName', 'PlaceFIPS', 'Population2010', 'Lack of Health Insurance', 'Arthritis',
              'Binge Drinking', 'High Blood Pressure', 'Blood Pressure Medication', 'Cancer', 'Asthma',
              'Coronary Heart Disease', 'Annual Checkup', 'Cholesterol Screening', 'Colonoscopy',
              'Chronic obstructive pulmonary disease', 'Preventive Services (Older Men)',
              'Preventive Services (Older Women)', 'Smoking', 'Dental Visit', 'Diabetes', 'High Cholesterol',
              'Kidney Disease', 'Physical Inactivity', 'Mammography', 'Poor Mental Health', 'Obesity',
              'Cervical Cancer Screening', 'Poor Physical Health', 'Sleep < 7 hrs', 'Stroke', 'Teethlost',
             'Geolocation']

head = list(df.columns[3:-1])

def feature_select(col):
    X_train = df[df.columns[4:-1]].drop(col, axis=1)
    y_train = df[col]
    selected_feature = []

    # select feature by person coefficient
    skb = SelectKBest(score_func=f_regression, k=4)
    skb.fit(X_train, y_train)
    for i in skb.get_support(indices=True):
        selected_feature += [X_train.columns[i]]
    print('Selected Feature:', selected_feature)
    X_selected = pd.DataFrame(skb.transform(X_train))
    X_selected.columns = selected_feature
    # print('X_selected.shape:', [X_selected.shape])
    # print(type(X_selected))
    # print(skb.get_params)
    # print(skb.scores_)
    return selected_feature, X_selected, skb.scores_

def scatter(sharch):
    features = feature_select(sharch)[0]
    arr = []
    for i in range(len(features)):
        obj = {}
        obj['address'] = features[i]
        obj['key'] = []
        for j in range(len(df)):
            coor = [df[sharch][j], df[features[i]][j]]
            obj['key'].append(coor)
        arr.append(obj)
    return arr

def wordcloud(sharch):
    X_train = df[df.columns[4:-1]].drop(sharch, axis=1)
    y_train = df[sharch]
    selected_feature = []
    scores = []

    # select feature by person coefficient
    skb = SelectKBest(score_func=f_regression, k=27)
    skb.fit(X_train, y_train)
    for i in skb.get_support(indices=True):
        selected_feature += [X_train.columns[i]]
    scores = skb.scores_

    arr = []
    for i in range(len(selected_feature)):
        obj = {}
        obj['name'] = selected_feature[i]
        obj['value'] = scores[i]
        arr.append(obj)
    return arr

maphead = ['StateAbbr','Lack of Health Insurance','Arthritis','Binge Drinking','High Blood Pressure','Blood Pressure Medication','Cancer','Asthma','Coronary Heart Disease','Annual Checkup','Cholesterol Screening','Colonoscopy','Chronic obstructive pulmonary disease','Preventive Services (Older Men)','Preventive Services (Older Women)','Smoking','Dental Visit','Diabetes','High Cholesterol','Kidney Disease','Physical Inactivity','Mammography','Poor Mental Health','Obesity','Cervical Cancer Screening','Poor Physical Health','Sleep < 7 hrs','Stroke','Teethlost']

def dataFormat():
    global maphead
    df = pd.read_csv('CDC_for_map.csv')
    df_state = df[maphead]
    return df_state


def formatData(sharch):
    global maphead
    data = dataFormat()

    arr = []

    for index in range(len(data)):
        obj = {}
        obj['address'] = data['StateAbbr'][index]

        obj['key'] = data[sharch][index]
        arr.append(obj)

    return arr

app = Flask(__name__)

# 127.0.0.1:5000
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    sharch = request.json.get("sharch")
    #return scatter(sharch)
    return json.dumps(scatter(sharch))

@app.route('/word', methods=['GET', 'POST'])
def word():
    sharch = request.json.get("sharch")
    #return scatter(sharch)
    return json.dumps(wordcloud(sharch))

# 127.0.0.1:5000/list
@app.route('/list')
def list():
    #return head
    return json.dumps(head)

# 127.0.0.1:5000
@app.route('/map/', methods=['GET', 'POST'])
def map():
    sharch = request.json.get("sharch")
    return json.dumps(formatData(sharch))


# 127.0.0.1:5000/list
@app.route('/maplist')
def maplist():
    return json.dumps(maphead)

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(debug=True, port=5000)