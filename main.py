from flask import Flask, request, jsonify
import pickle

# ML model
model = pickle.load(open('model.pkl', 'rb'))

COLUMNS_ORDER = ['No_Transactions', 'No_Orders', 'No_Payments',
       'paymentMethodRegistrationFailure', 'transactionAmount',
       'transactionFailed', "native_ip","native_device","last_time_purchase","black_list"]

app = Flask(__name__)

@app.route('/get-prediction', methods=['GET', 'POST'])
def predict():
    # Getting the data
    data = request.json
    to_model = [data[col] for col in COLUMNS_ORDER]

    # Making the prediction
    pred = model.predict([to_model])
    if pred[0] == 1:
        return "FRAUD"
    else:
        return "NOT FRAUD"       
           
             



