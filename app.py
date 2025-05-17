from flask import Flask, render_template, request
from TRM import trm_prediction

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
  table = None
  error = None
  if request.method == 'POST':
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    usd_cost = request.form['usd_cost']

    try:
      table, error = trm_prediction(start_date, end_date, float(usd_cost))
    except Exception as e:
      error = str(e)
      table = None

  return render_template('index.html', table=table, error=error)

@app.route("/fase1")
def PhaseOne():
  return render_template("PhaseOne.html")

@app.route("/fase2")
def PhaseTwo():
  return render_template("PhaseTwo.html")

@app.route("/fase3")
def PhaseThree():
  return render_template("PhaseThree.html")

@app.route("/fase4")
def PhaseFourth():
  return render_template("PhaseFourth.html")

@app.route("/fase5")
def PhaseFive():
  return render_template("PhaseFive.html")

@app.route("/fase6")
def PhaseSix():
  return render_template("PhaseSix.html")

if __name__ == '__main__':
  app.run(debug=True)