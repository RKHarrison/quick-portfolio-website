import os, secrets
from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# Secret key needed for flashing messages
app.secret_key = secrets.token_hex(16)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def landing():
    return redirect("/index.html", code=302)

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

# Route to handle the contact form submission
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        if not email or not subject or not message:
            flash('All fields are required!', 'error')
            return redirect("/contact.html")

        # Send email using Flask-Mail
        msg = Message(subject=subject,
                      sender=os.getenv('MAIL_USERNAME'),
                      recipients=['r.harr.k@gmail.com'],
                      body=f"Message from {email}:\n\n{message}")

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message: {str(e)}', 'error')

        return redirect("/contact.html")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)