from flask import Flask, request, jsonify
import pickle
model = pickle.load(open('model.pkl', 'rb'))

COLUMNS_ORDER = ['No_Transactions', 'No_Orders', 'No_Payments',
       'paymentMethodRegistrationFailure', 'transactionAmount',
       'transactionFailed', 'paymentMethodType_bitcoin',
       'paymentMethodType_card', 'paymentMethodType_paypal',
       'paymentMethodProvider_Diners Club / Carte Blanche',
       'paymentMethodProvider_Discover', 'paymentMethodProvider_JCB 15 digit',
       'paymentMethodProvider_JCB 16 digit', 'paymentMethodProvider_Maestro',
       'paymentMethodProvider_Mastercard',
       'paymentMethodProvider_VISA 13 digit',
       'paymentMethodProvider_VISA 16 digit', 'paymentMethodProvider_Voyager']

app = Flask(__name__)


@app.route('/get-prediction', methods=['GET', 'POST'])
def predict():
    # Getting the data sent to the API
    data = request.json
    # Setting the the categorical values and their possible values
    categorical_values = {'paymentMethodType' : ['bitcoin', 'card', 'paypal'],
                          'paymentMethodProvider' : ['Diners Club / Carte Blanche', 'Discover', 'JCB 15 digit',
                                                   'JCB 16 digit', 'Maestro', 'Mastercard', 'VISA 13 digit',
                                                   'VISA 16 digit', 'Voyager']}

    print(data)
    # Adding the dummy variables
    for value in categorical_values:
        for val in categorical_values[value]:
            if val == data[value]:
                data[value + '_' + str(val)] = 1
            else:
                data[value + '_' + str(val)] = 0
        del data[value]
    # Preparing the data for the model
    print(data)
    to_model = [data[col] for col in COLUMNS_ORDER]
    # Making the prediction76t
    pred = model.predict([to_model])
    # Preparing the response
    response = {"pred" : int(pred[0])}
    return jsonify(response)