from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from random import randint
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "it's a secret"

toolbar = DebugToolbarExtension(app)


#==========================================
# functions to get error message for each filed

def get_name_err(name):
    """ get the name error message """

    return "This field is required." if not name else None


def get_year_err(year):
    """ get the birth year error message """

    if not year:
        return "This field is required."

    try:
        year = int(year)
    except:
        return "Birth year must be a number"
   
    if year < 1900 or year > 2000:
        year_err = "Birth year must be between 1900 and 2000, inclusive."
    else:
        year_err = None

    return year_err


def get_email_err(email):
    """ get the email error message """

    return "This field is required." if not email else None


def get_color_err(color):
    """ get the color error message """

    if not color:
        color_err = "This field is required."
    elif color not in ["red", "green", "orange", "blue"]:
        color_err = "Invalid value, must be one of: red, green, orange, blue."
    else:
        color_err = None

    return color_err


# ================================================
# function to collect all the error messages

def get_errors(name, year, email, color):
    """ collect all the valid error messages and put them in dict """

    errors = {
        "name": get_name_err(name),
        "year": get_year_err(year),
        "email": get_email_err(email),
        "color": get_color_err(color)
        }

    filtered_errors = {key:value for (key, value) in errors.items() if value}

    return filtered_errors


# ===================================================
# request facts from lucky-num API

def request_num_fact(num):
    response = requests.get(f'http://numbersapi.com/{num}')
    return {"num":num, "fact":response.text}


def request_year_fact(year):
    response = requests.get(f'http://numbersapi.com/{year}/year')
    return {"year":year, "fact":response.text}


# ===================================================
# Backend API routes

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")


@app.route("/api/get-lucky-num", methods=['POST'])
def get_lucky_num():
    """ get the lucky number facts from API """
    
    name = request.json.get("name")
    year = request.json.get("year")
    email = request.json.get("email")
    color = request.json.get("color")

    errs = get_errors(name, year, email, color)

    if errs:
        return jsonify(errors=errs)

    # If the user failed to provide valid data for all fields, return error response like this:
    # {
    #     "errors": {
    #         "color": 
    #             "Invalid value, must be one of: red, green, orange, blue."
    #         ,
    #         "name": 
    #             "This field is required."           
    #     }
    # }

    num = randint(1, 100)
    
    return jsonify(
        num=request_num_fact(num), 
        year=request_year_fact(year)
        )

    # If the user provided valid data, return the lucky number response response like this:
    # {
    #     "num": {
    #         "fact": "67 is the number of throws in Judo.",
    #         "num": 67
    #     },
    #     "year": {
    #         "fact": "1950 is the year that nothing remarkable happened.",
    #         "year": "1950"
    #     }
    # }

   


