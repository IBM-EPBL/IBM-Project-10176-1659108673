from flask import Flask,render_template,request,jsonify
from DB2 import connection
import numpy as np
import pickle
#importing the inputScript file used to analyze the URL
import inputScript

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
    prediction = model.predict(checkprediction)
    print(prediction)
    output=prediction[0]
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
    app.run(host='0.0.0.0',debug=True)