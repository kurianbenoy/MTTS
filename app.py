from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
    	message = request.form['message']
    	data = [message]
    	vect = cv.transform(data).toarray()
    	my_prediction = classifier.predict(vect)
    	return render_template('result.html', prediction=my_prediction)
        os.system(f"./flite/bin/flite flite/doc/alice")

if __name__ == "__main__":
    app.run(debug=True)