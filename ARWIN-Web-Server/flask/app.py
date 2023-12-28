from flask import Flask, render_template

# Set up Flask
app = Flask(__name__)

# Website Routes

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# API Routes

@app.route("/ping", methods = ["GET"])
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = False)

# tutorial: https://www.raspberrypi-spy.co.uk/2018/12/running-flask-under-nginx-raspberry-pi/≈