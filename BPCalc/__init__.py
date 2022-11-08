from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bp(systolic, diastolic):
    pass

@app.route("/", methods = ['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        systolic = request.form.get('bpsystolic')
        diastolic = request.form.get('diastolic')
        response = calculate_bp(systolic, diastolic)
    return render_template('index.html.j2', response=response)
    