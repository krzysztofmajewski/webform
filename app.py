import secrets

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


target_name = "Krzysztof"

app = Flask(__name__)

foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    name = StringField(f"Please submit your feedback for {target_name}", validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    if form.validate_on_submit():
        feedback: str = form.name.data
        # TODO: Encrypt the feedback with a key that is not accessible to hosting admins
        # TODO: Push feedback to db table or flat file or blob storage
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
