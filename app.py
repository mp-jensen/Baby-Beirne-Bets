from flask import Flask, render_template, redirect
from flask import request

# Create app
app = Flask (__name__)

@app.route('/')
def welcome():
    #temporary page to test herokuapp connection
    return render_template('welcome.html')

if __name__ == '__main__': app.run(debug=True)