import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from flask import Flask, request, render_template, session, redirect, url_for
from functools import wraps

dataset = pd.read_csv('dataset/upi_fraud_dataset.csv', index_col=0)

x = dataset.iloc[:, : 10].values
y = dataset.iloc[:, 10].values

scaler = StandardScaler()
scaler.fit_transform(x)

model = tf.keras.models.load_model('model/project_model1.h5')

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        if uname == 'admin' and pwd == 'admin':
            session['logged_in'] = True
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error='Invalid Credentials!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('first'))

def home():
	return render_template('home.html')
@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')  
@app.route('/preview',methods=["POST"])
@login_required
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        if 'Id' in df.columns:
            df.set_index('Id', inplace=True)
        elif 'Unnamed: 0' in df.columns:
            df.set_index('Unnamed: 0', inplace=True)
            df.index.name = 'Id'
        df.to_csv('dataset/current_dataset.csv')
        session['data_uploaded'] = True
        session['is_trained'] = False
        return render_template("preview.html",df_view = df) 

@app.route('/train_model', methods=['POST'])
@login_required
def train_model():
    session['is_trained'] = True
    return redirect(url_for('prediction1'))


@app.route('/prediction1', methods=['GET'])
@login_required
def prediction1():
    return render_template('index.html')

@app.route('/chart')
@login_required
def chart():
    return render_template('chart.html')

@app.route('/detect', methods=['POST'])
@login_required
def detect():
    trans_datetime = pd.to_datetime(request.form.get("trans_datetime"))
    v1 = trans_datetime.hour
    v2 = trans_datetime.day
    v3 = trans_datetime.month
    v4 = trans_datetime.year
    v5 = int(request.form.get("category"))
    v6 = float(request.form.get("card_number"))
    dob = pd.to_datetime(request.form.get("dob"))
    v7 = (trans_datetime - dob).days // 365
    v8 = float(request.form.get("trans_amount"))
    v9 = int(request.form.get("state"))
    v10 = int(request.form.get("zip"))
    x_test = np.array([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10])
    y_pred = model.predict(scaler.transform([x_test]))
    if y_pred[0][0] <= 0.5:
        result = "VALID TRANSACTION"
    else:
        result = "FRAUD TRANSACTION"
    return render_template('result.html', OUTPUT='{}'.format(result))

if __name__ == "__main__":
    app.run()
