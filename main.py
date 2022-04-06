import pickle

import flask
import numpy as np
from flask_mysqldb import MySQL
from sklearn.preprocessing import StandardScaler

app = flask.Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'csppa'

mysql = MySQL(app)
# Creating a connection cursor
cursor = mysql.connection.cursor()

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return flask.render_temolate('register.html')


@app.route('/login', methods=['GET'])
def login():
    return flask.render_template('login.html')


@app.route('/About', methods=['GET'])
def about():
    return flask.render_template('about-us.html')


@app.route('/Contact', methods=['GET'])
def contact():
    return flask.render_template('contact.html')


@app.route('/home', methods=['GET'])
def home():
    return flask.render_template('home.html')


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if flask.request.method == 'POST':
        Year = int(flask.request.form['Year'])
        Present_Price = float(flask.request.form['Present_Price'])
        Kms_Driven = int(flask.request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(flask.request.form['Owner'])
        Fuel_Type_Petrol = flask.request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        Year = 2020 - Year
        Seller_Type_Individual = flask.request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = flask.request.form['Transmission_Mannual']
        if Transmission_Mannual == 'Mannual':
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                     Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)
        if output < 0:
            return flask.render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return flask.render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return flask.render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
