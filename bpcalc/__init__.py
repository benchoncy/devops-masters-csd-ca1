from flask import Flask, render_template, request
from enum import Enum


class BPCategory(Enum):
    LOW = "low"
    IDEAL = "ideal"
    PRE_HIGH = "pre-high"
    HIGH = "high"


app = Flask(__name__)


def validate_values(systolic, diastolic):
    errors = []
    if systolic < diastolic:
        errors += ["Systolic preasure must be higher than diastolic preasure"]
    if not 70 <= systolic <= 190:
        errors += ["Systolic value must be between 70 and 190"]
    if not 40 <= diastolic <= 100:
        errors += ["Diastolic value must be between 40 and 100"]
    return errors if len(errors) > 0 else None


def get_bp_category(systolic, diastolic):
    if systolic < 90 and diastolic < 60:
        return BPCategory.LOW
    if systolic < 120 and diastolic < 80:
        return BPCategory.IDEAL
    if systolic < 140 and diastolic < 90:
        return BPCategory.PRE_HIGH
    return BPCategory.HIGH


@app.route("/", methods=['GET', 'POST'])
def index():
    response = None
    error = None
    if request.method == 'POST':
        try:
            systolic = float(request.form.get('bpsystolic'))
            diastolic = float(request.form.get('bpdiastolic'))
            error = validate_values(systolic, diastolic)
        except (ValueError, TypeError):
            error = ["Valid values must be entered"]
        if not error:
            response = get_bp_category(systolic, diastolic)
    return render_template('index.html.j2', response=response, error=error)
