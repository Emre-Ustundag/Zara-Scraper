from flask import Flask,request,jsonify
from flask_cors import CORS
import sys
sys.path.append('.')
from DB_Connect import connectdb, add_Product, close_Connection,pull_LicenceKey,keyCounter
from ServerSide.licence import generate_license_key
from waitress import serve
import logging


print(__name__)
app = Flask(__name__)

CORS(app, resources={
    r"/check": {
        "origins": "*", 
        "methods": ["POST","OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization","key"]
    },
    r"/gl-key": {
        "origins": "*", 
        "methods": ["POST","OPTIONS"],  
        "allow_headers": ["Content-Type", "Authorization","key","L_key"] 
    }
})


@app.route('/', methods=['GET'])
def index():
    return "I guess you are lost."


@app.route('/check', methods=['POST','OPTIONS'])
def admin():
    if request.method == 'POST':
        connectdb()
        print(request.headers)
        jsoned = request.get_json()
        key = request.headers.get('key')
        if key != "":
            returnValue = pull_LicenceKey(request.headers.get('key'))
            print("returnValue: ",returnValue)
            if returnValue != None:
                add_Product(jsoned['product_link'],jsoned['size'],jsoned['mail'])
                keyCounter(key)
                close_Connection()
                return jsonify({"message": "Hoşgeldiniz. İşleminiz gerçekleştirilmiştir."})
            else:
                close_Connection()
                return jsonify({"message": "Kullanılan anahtar geçerli değil. Lütfen yeni bir tane alınız."}), 401
        else:
            close_Connection()
            return jsonify({"message": "Kullanılan anahtar geçerli değil. Lütfen yeni bir tane alınız."}), 401
    elif request.method == 'OPTIONS':
        return jsonify({"message": "Options method is allowed."}),200



@app.route('/gl-key', methods=['POST','OPTIONS'])
def generate_license():
    if request.method == 'POST':
        connectdb()
        jsoned = request.get_json()
        if jsoned['key'] == "":
            print(jsoned['L_key'])
            print(request.headers)
            licenceKey= generate_license_key(jsoned['L_key'])
            close_Connection()
            return jsonify({"message": f"{licenceKey}"})
        else:
            close_Connection()
            return jsonify({"message": "Kullanılan anahtar geçerli değil. Lütfen yeni bir tane alınız."}), 401
    elif request.method == 'OPTIONS':
        return jsonify({"message": "Options method is allowed."}),200



if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=5000,debug=True)
    logging.basicConfig(level=logging.DEBUG)
    serve(app, host='0.0.0.0', port=5000)
