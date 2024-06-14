from flask import Flask, render_template, request
import pandas as pd
# from sklearn.externals import joblib
import joblib
import numpy as np
import urllib.request
import urllib.parse

app = Flask(_name_)
model = joblib.load('litemodel.sav')

from twilio.rest import Client

def sendSMS(account_sid, auth_token, to_number, from_number, message):
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Send the message
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )

        print(f"Message sent successfully! SID: {message.sid}")
        return "Message sent successfully!"
    except Exception as e:
        print(f"Error sending message: {e}")
        return f"Error sending message: {e}"


def cal(ip):
    input = dict(ip)
    Did_Police_Officer_Attend = input['Did_Police_Officer_Attend'][0]
    age_of_driver = input['age_of_driver'][0]
    vehicle_type = input['vehicle_type'][0]
    age_of_vehicle = input['age_of_vehicle'][0]
    engine_cc = input['engine_cc'][0]
    day = input['day'][0]
    weather = input['weather'][0]
    light = input['light'][0]
    roadsc = input['roadsc'][0]
    gender = input['gender'][0]
    speedl = input['speedl'][0]

    data = np.array([Did_Police_Officer_Attend, age_of_driver, vehicle_type, age_of_vehicle, engine_cc, day, weather, roadsc, light, gender, speedl])

    print("logging",data)
    data = data.astype(float)
    data = data.reshape(1, -1)

    x = np.array([1, 3.73, 3, 0.69, 125, 4, 1, 1, 1, 1, 30]).reshape(1, -1)

    try: result = model.predict(data)
    except Exception as e: result = str(e)

    return str(result[0])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/visual/', methods=['GET'])
def visual():
    return render_template('visual.html')


@app.route('/sms/', methods=['POST'])
def sms():
    form_data = request.form
    res = cal(form_data)    # here the resu are in 1,2,3
    accident_type = []
    if res==1:
        accident_type.append('Fatal')
    elif res==1:
        accident_type.append('Serious')
    else:
        accident_type.append('Slight')

        
    

    # Extract latitude, longitude, weather, light, and road surface conditions from the form
    latitude = form_data.get('latitude', 'Unknown Latitude')
    longitude = form_data.get('longitude', 'Unknown Longitude')
    weather = form_data.get('weather', 'Unknown Weather Condition')
    light = form_data.get('light', 'Unknown Light Condition')
    roadsc = form_data.get('roadsc', 'Unknown Road Surface Condition')

    # Twilio credentials
   
    account_sid = 'AC3df56437d1f3997b09c1df37'

    auth_token = '439183246f8469827fd609f00'

    from_number = '+12519091189'
    to_number = '+916386586735'  # Replace with the recipient's phone number

    # Construct message with latitude, longitude, weather, light, and road surface conditions
    if accident_type:
        message = f'Alert! {accident_type[0]} accident expected in region Latitude: {latitude}, Longitude: {longitude}.\n'
    message += f'Weather: {weather}\n'
    message += f'Light: {light}\n'
    message += f'Road Surface Condition: {roadsc}\n'
    message += 'Please take preventive measures.\nFrom AI TEAM.'

    # you can modify the mesage accrding to your need here 

    # Call the sendSMS function
    result = sendSMS(account_sid, auth_token, to_number, from_number, message)
    print(result)


@app.route('/', methods=['POST'])
def get():
    return cal(request.form)

if _name_ == '_main_':
    app.run(host='0.0.0.0', debug=True, port=4000)
