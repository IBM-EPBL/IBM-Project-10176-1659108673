from flask import Flask,render_template,request,jsonify
from DB2 import connection
import numpy as np
import pickle
#importing the inputScript file used to analyze the URL
import inputScript
import requests

# NOTE: Manually set API_KEY below using information retrieved from IBM Cloud account.
API_KEY = "KGdexk84M3lJ5NjGjTHB7Djxli0JxuQPQed0dUdNoMZa"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#load model
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl', 'rb'))

@app.route('/')
def Home():
    return render_template('index.html')

#Redirects to the page to give the user input URL.
@app.route('/Final')
def Final():
    return render_template('Final.html')

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    print(checkprediction)
    payload_scoring = {"input_data": [{"field": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20","f21","f22","f23","f24","f25","f26","f27","f28","f29"]], "values": checkprediction}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f414192c-67ae-40dd-a0cf-bf6b8af3cbb5/predictions?version=2022-10-31', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
   
    print("Scoring response")
    print(response_scoring.json())

    pred= response_scoring.json()
    print(pred)
    
    output = pred['predictions'][0]['values'][0][0]
    print(output)

    checkprediction = model.predict(checkprediction)
    print(checkprediction)
    output=checkprediction
    if(output==-1):

        pred="Your are safe!!  This is a Legitimate Website."
        
    else:
        pred="You are on the wrong site. Be cautious!"

    return render_template('Final.html', prediction_text='{}'.format(pred),url=url)

#Takes the input parameters fetched from the URL by inputScript and returns the predictions

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

@app.route("/RecievedData", methods=['POST'])
def result():
    USERNAME= request.form['USERNAME']
    EMAIL= request.form['EMAIL']
    MOBILE= request.form['MOBILE']
    MESSAGE= request.form['MESSAGE']
    connection.insertvalues(USERNAME,EMAIL,MOBILE,MESSAGE)
    return render_template('Thankyou.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

