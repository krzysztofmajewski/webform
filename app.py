import secrets
import logging
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from from_root import from_root

target_name = "Krzysztof"

logger = logging.getLogger(__name__)
app = Flask(__name__)

foo = secrets.token_urlsafe(16)
app.secret_key = foo

bootstrap = Bootstrap5(app)

class NameForm(FlaskForm):
    class Meta:
        # This overrides the value from the base form.
        csrf = False
    label = f"The text you submit via this form will be visible only to {target_name}"
    name = TextAreaField(label, validators=[DataRequired(), Length(10, 200)])

    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    if form.validate_on_submit():
        feedback: str = form.name.data
        # TODO: Encrypt the feedback with a key that is not accessible to hosting admins
        uuid: str = secrets.token_urlsafe(16)
        filename: Path = from_root(f"./{uuid}.txt")
        logger.info(f"Wrote feedback of length {len(feedback)} to filename: {filename}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(feedback)
        return redirect(url_for('merci', id=id))

    return render_template('index.html', form=form, target=target_name)

@app.route('/merci')
def merci():
    return render_template('merci.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
