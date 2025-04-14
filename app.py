from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route to serve the home page
@app.route('/')
def home():
    return render_template('Home.html')

# About page
@app.route('/about')
def aboutus():
    return render_template('aboutus.html')

# Giving page
@app.route('/give')
def giving():
    return render_template('giving.html')

# Contact page (GET)
@app.route('/contact', methods=['GET'])
def contactus_page():
    return render_template('contactus.html')

# Contact form submission (POST)
@app.route('/contact', methods=['POST'])
def contactus_submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # You can log it or print it to your console
    print(f"New contact message:\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")

    # Later, plug in your SMS or email sender here
    return jsonify({'status': 'success', 'message': 'Message received! We will reach out to you soon.'})

if __name__ == '__main__':
    app.run(debug=True)
