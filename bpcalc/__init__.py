import os
from flask import Flask, render_template, request, Response
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from opentelemetry import trace
from opentelemetry import metrics
from bpcalc.bpenums import BPCategory, BPLimits
from bpcalc.bpplot import make_plot


# Get telemtry meter/tracer and flask app
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

csp = {
    'default-src': '\'self\' cdn.jsdelivr.net'
}
CSRFProtect(app)
Talisman(app, force_https=False, content_security_policy=csp)

form_reponse_counter = meter.create_counter(
    "form_reponse_counter",
    description="The number of form reponses by success/error",
)

# Preload empty graph plot
EMPTY_PLOT = make_plot()


def validate_values(systolic, diastolic):
    """Ensure systolic and diastolic input values make sense."""
    errors = []
    if systolic < diastolic:
        errors += ["Systolic preasure must be higher than diastolic preasure"]
    if not BPLimits.YMIN <= systolic <= BPLimits.YMAX:
        errors += ["Systolic value must be between {min} and {max}"
                   .format(min=BPLimits.YMIN, max=BPLimits.YMAX)]
    if not BPLimits.XMIN <= diastolic <= BPLimits.XMAX:
        errors += ["Diastolic value must be between {min} and {max}"
                   .format(min=BPLimits.XMIN, max=BPLimits.XMAX)]
    return errors if len(errors) > 0 else None


def get_bp_category(systolic, diastolic):
    """
    Return a blood preasure category determed by
    systolic and diastolic values.
    """
    if systolic < BPLimits.IDEAL_YSTART and diastolic < BPLimits.IDEAL_XSTART:
        return BPCategory.LOW
    if systolic < BPLimits.PRE_HIGH_YSTART and diastolic < BPLimits.PRE_HIGH_XSTART:
        return BPCategory.IDEAL
    if systolic < BPLimits.HIGH_YSTART and diastolic < BPLimits.HIGH_XSTART:
        return BPCategory.PRE_HIGH
    return BPCategory.HIGH


@app.route("/", methods=['GET', 'POST'])
def index():
    """Index route containing BPCalculator."""
    response = None
    error = None
    sd_values = None
    if request.method == 'POST':
        try:
            systolic = float(request.form.get('bpsystolic'))
            diastolic = float(request.form.get('bpdiastolic'))
            error = validate_values(systolic, diastolic)
        except (ValueError, TypeError):
            error = ["Valid values must be entered"]
        with tracer.start_as_current_span("do_form") as formspan:
            success = error is None
            formspan.set_attribute("form.success", success)
            form_reponse_counter.add(1, {"form.success": success})
            if success:
                response = get_bp_category(systolic, diastolic)
                sd_values = (diastolic, systolic)
    return render_template('index.html.j2',
                           response=response,
                           error=error,
                           sd_values=sd_values)


@app.route("/plot")
@app.route("/plot/<systolic>/<diastolic>")
def plot_serve(systolic=None, diastolic=None):
    """Serve blood preasure plot."""
    response = EMPTY_PLOT
    if systolic is not None and diastolic is not None:
        response = make_plot((float(systolic), float(diastolic)))
    return Response(response, mimetype='image/png')


@app.context_processor
def utility_processor():
    """Add context processors used by jinja templates."""
    def env(var):
        """Get environment variable."""
        return os.environ.get(var, None)
    return dict(
        env=env
    )


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response
