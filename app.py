from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('Home.html')  # Make sure home.html is in the 'templates' folder

@app.route('/about')
def aboutus():
    return render_template('aboutus.html')  # You can add more routes to serve other pages
@app.route('/give')
def giving():
    return render_template('giving.html')  # You can add more routes to serve other pages
@app.route('/contact')
def contactus():
    return render_template('contactus.html')  # You can add more routes to serve other pages


if __name__ == '__main__':
    app.run(debug=True)