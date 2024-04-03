from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from datetime import date

from forms import ContactForm
from notification_manager import NotificationManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap5(app)

share_data = {'year': date.today().year}


@app.context_processor
def inject_data():
    """Injects the share_data dictionary into the context of all templates.

    Returns:
        dict: The share_data dictionary.
    """
    return {'share_data': share_data}


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Renders the contact page with a contact form.

    GET: Displays the contact form.
    POST: Processes the submitted form. Sends an email if validation succeeds.
    Redirects to the contact page upon successful submission or back to the contact form with validation errors.

    Returns:
        Response: The contact template on GET or redirect on successful POST.
    """
    form = ContactForm()
    if form.validate_on_submit():
        try:
            notification_manager = NotificationManager()
            notification_manager.send_email(form.data, app.config['MY_EMAIL'])
            flash('Thank you, your message has been sent.', 'success')
        except Exception as e:
            flash('Your message could not be sent. Please try again.', 'danger')
            app.logger.error(f"Failed to send email: {e}")
        return redirect(url_for('contact'))
    return render_template(
        'contact.html',
        form=form,  # Pass the form to the template
    )


if __name__ == "__main__":
    app.run(debug=True)
