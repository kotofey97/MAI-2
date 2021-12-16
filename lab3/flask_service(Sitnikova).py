from flask import request, abort, make_response
from flask import Flask
from flask import jsonify
import math
#from sklearn.externals import joblib
from json import dumps
from joblib import load
app = Flask(__name__)

@app.before_first_request
def load_global_data():
    global model
    model = load('olya_model.mdl')

@app.route('/')
def hello_world():
    return 'Дз-4 модель и веб сервис (Ситникова)'
 

def get_prediction(r, g, b):
    
    y_pred = model.predict([[r,g,b]])
    if y_pred ==-1:
        s='Кислая среда'
    elif y_pred ==0: 
        s='Нейтральная среда'
    elif y_pred ==1: 
        s='Щелочная среда'    
   
    return f'pH = {y_pred[0]} следовательно {s} '


   
@app.route('/api/predict', methods=['GET'])
def predict():
    r = request.args.get('r', type=int)
    g = request.args.get('g', type=int)
    b = request.args.get('b', type=int)
    if r is None or g is None or b is None:
        bad_request('r, g, b  not specified')
    if (r < 0 or r > 255) or (g < 0 or g > 255) or (b < 0 or b > 255):
        bad_request('r, g, b should be greater then 0 and less then 255')
    
    return str(get_prediction(r, g, b));

def bad_request(message, code=400):
    abort(make_response(jsonify(message=message), code))
    
if __name__ == '__main__':
    app.run()