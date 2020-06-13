from subprocess import Popen
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('input.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        print(type(message))
        Popen(["./flite/bin/flite", "-voice", "flite/voices/cmu_indic_kan_plv.flitevox", \
             message, "-w", "op.wav"])
    # 	vect = cv.transform(data).toarray()
    # 	my_prediction = classifier.predict(vect)
    return render_template('output.html')
    #os.system(f"./flite/bin/flite flite/doc/alice")
    #./flite/bin/flite   "-voice" flite/voices/cmu_indic_kan_plv.flitevox "അണ<0d4d>ണാൻ ക<0d41>ഞ<0d4d>ഞ<0d41>ം തന<0d4d>നാലായത<0d4d>."
    # ./flite/bin/flite --setf duration_stretch=1.5  "-voice" flite/voices/cmu_indic_kan_plv.flitevox "അണ<0d4d>ണാൻ ക<0d41>ഞ<0d4d>ഞ<0d41>ം തന<0d4d>നാലായത<0d4d>

if __name__ == "__main__":
    app.run(debug=True)