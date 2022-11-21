import json

from flask import Flask, request, render_template
import OCR


app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello_world():
    return render_template("index.html")

@app.route('/',methods=['POST'])
def predict():
    result = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            if len(url)==0:
                raise invalidUrl;
            result = OCR.ocr(url)
            #print(result)
        except ValueError:
            print("invalid url")

    return json.dumps(result, ensure_ascii=False)

class invalidUrl(Exception):
    pass
if __name__ == '__main__':
    app.run(debug=True)
