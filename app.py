from subprocess import Popen
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('input.html')

@app.route('/',methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        print(type(message))
        Popen(["./flite/bin/flite", "-voice", "flite/voices/cmu_indic_tam_sdr.flitevox", \
             message,])
    # 	vect = cv.transform(data).toarray()
    # 	my_prediction = classifier.predict(vect)
    return render_template('output.html', message=message)


if __name__ == "__main__":
    app.run(debug=True)