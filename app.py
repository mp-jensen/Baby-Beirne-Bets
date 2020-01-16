from flask import Flask, render_template, redirect
from flask import request

# Create app
app = Flask (__name__)

@app.route('/')
def homepage():
    #temporary page to test herokuapp connection
    return 'Hello Baby Beirne Bets!'

if __name__ == '__main__': app.run(debug=True)