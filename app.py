from flask import Flask, render_template, redirect
from flask import request
from db_connector import connect_to_database, execute_query

# Create app
app = Flask (__name__)

@app.route('/')
def welcome():
    print(request)
    return render_template('welcome.html')


@app.route('/placeBets', methods=["POST","GET"])
def placeBets():
    print("I am in the placeBets route")
    if request.method == "GET":
        print("request method was GET")
        return render_template('placeBets.html')

    # initalize all variables needed if it was a POST request
    email = False
    newEmail = False
    userID = False
    user_bDate = True
    user_bTime = True
    user_bWeight = True
    user_bLength = True
    user_bHair = True
    user_bFName = True
    user_bMName = True
    date = (None,)
    hour = (None,)
    minute = (None,)
    lb = (None,)
    oz = (None,)
    inches = (None,)
    hair = (None,)
    FNletter = (None,)
    MNletter = (None,)

    print("Content length: {0}".format(request.content_length))
    print("Data: {0}".format(request.data))
    print("Request.form contains the following: {0}".format(request.form))
    if 'newEmail' in request.form:
        dbConnection = connect_to_database()
        query = 'SELECT userID FROM users WHERE email=%s;'
        testEmail = (request.form['newEmail'],)
        user = execute_query(dbConnection, query, testEmail)
        # check if the email is already registered to a user, if not, prompt for user info along with
        # prompting for all bets
        if user.rowcount == 0:
            newEmail = testEmail
        # check if the user has any bets entered, if so do not prompt for a bet in that cateogry
        else:
            email = testEmail
            userID = user.fetchone()[0]

            query = 'SELECT * FROM user_bDate WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bDate = False

            query = 'SELECT * FROM user_bTime WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bTime = False

            query = 'SELECT * FROM user_bWeight WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bWeight = False

            query = 'SELECT * FROM user_bLength WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bLength = False

            query = 'SELECT * FROM user_bHair WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bHair = False

            query = 'SELECT * FROM user_bFName WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bFName = False

            query = 'SELECT * FROM user_bMName WHERE userID=%s;'
            if execute_query(dbConnection, query, (userID,)).rowcount > 0:
                user_bMName = False

        # get data to populate bet form with
        if user_bDate:
            query = 'SELECT bDateID, date FROM bDate;'
            date = execute_query(dbConnection, query).fetchall()
        if user_bTime:
            query = 'SELECT bHourID, hour FROM bHour;'
            hour = execute_query(dbConnection, query).fetchall()
            query = 'SELECT bMinuteID, minute FROM bMinute;'
            minute = execute_query(dbConnection, query).fetchall()
        if user_bWeight:
            query = 'SELECT bLbID, lb FROM bLb;'
            lb = execute_query(dbConnection, query).fetchall()
            query = 'SELECT bOzID, oz FROM bOz;'
            oz = execute_query(dbConnection, query).fetchall()
            print("oz request return: {0}".format(oz))
        if user_bLength:
            query = 'SELECT bLengthID, inches FROM bLength;'
            inches = execute_query(dbConnection, query).fetchall()
        if user_bHair:
            query = 'SELECT bHairID, hair FROM bHair;'
            hair = execute_query(dbConnection, query).fetchall()
        if user_bFName:
            query = 'SELECT bFNameID, letter FROM bFName;'
            FNletter = execute_query(dbConnection, query).fetchall()
        if user_bMName:
            query = 'SELECT bMNameID, letter FROM bMName;'
            MNletter = execute_query(dbConnection, query).fetchall()

        # return with the template and all information needed to populate the form
        # true/false values on whether or not the user has a bet yet and
        # option values for bets
        return render_template('placeBets.html', userID=userID, email=email, newEmail=newEmail, user_bDate=user_bDate, user_bTime=user_bTime, user_bWeight=user_bWeight, user_bLength=user_bLength, user_bHair=user_bHair, user_bFName=user_bFName, user_bMName=user_bMName, date=date, hour=hour, minute=minute, lb=lb, oz=oz, inches=inches, hair=hair, FNletter=FNletter, MNletter=MNletter)

    else:
        return render_template('placeBets.html')

@app.route('/betsPlaced', methods=["POST","GET"])
def betsPlaced():
    # if a form was not posted to get to this page, tell the user
    # where they can go to place bets
    if request.method == "GET":
        return render_template('betsPlaced.html', get=True)

    user = False
    bDate = False
    bTime = False
    bWeight = False
    bLength = False
    bHair = False
    bFName = False
    bMName = False
    dbConnection = connect_to_database()
    # get the information from the form used to place bets and
    # if there is a userID use it to submit the bets, otherwise create a user
    # then use that to submit the bets
    if 'userID' in request.form:
        userID = request.form['userID']
    elif 'submitEmail' in request.form:
        print("Request form in place bets: {0}".format(request.form))
        userData = (request.form['firstName'], request.form['lastName'], request.form['submitEmail'])
        query = "INSERT INTO users (firstName, lastName, email) VALUES (%s, %s, %s);"
        execute_query(dbConnection, query, userData)
        email = (request.form['submitEmail'],)
        query = "SELECT userID FROM users WHERE email=%s"
        userID = execute_query(dbConnection, query, email).fetchone()[0]
        user = True

    # for each type of bet, if it was submitted, enter it as a bet
    if 'birthDate' in request.form:
        bDateData = (userID, request.form['birthDate'])
        query = "INSERT INTO user_bDate (userID, bDateID, amountBet) VALUES (%s, %s, 0);"
        execute_query(dbConnection, query, bDateData)
        bDate = True
    if 'birthHour' in request.form and 'birthMinute' in request.form:
        bTimeData = (userID, request.form['birthHour'], request.form['birthMinute'])
        query = "INSERT INTO user_bTime (userID, bHourID, bMinuteID, amountBet) VALUES (%s,%s,%s,0);"
        execute_query(dbConnection, query, bTimeData)
        bTime = True
    if 'birthLb' in request.form and 'birthOz' in request.form:
        bWeightData = (userID, request.form['birthLb'], request.form['birthOz'])
        query = "INSERT INTO user_bWeight (userID, bLbID, bOzID, amountBet) VALUES (%s,%s,%s,0);"
        execute_query(dbConnection, query, bWeightData)
        bWeight = True
    if 'birthLength' in request.form:
        bLengthData = (userID, request.form['birthLength'])
        query = "INSERT INTO user_bLength (userID, bLengthID, amountBet) VALUES (%s,%s,0);"
        execute_query(dbConnection, query, bTimeData)
        bLength = True
    if 'birthHair' in request.form:
        bHairData = (userID, request.form['birthHair'])
        query = "INSERT INTO user_bHair (userID, bHairID, amountBet) VALUES (%s,%s,0);"
        execute_query(dbConnection, query, bHairData)
        bHair = True
    if 'birthFN' in request.form:
        bFNData = (userID, request.form['birthFN'])
        query = "INSERT INTO user_bFName (userID, bFNameID, amountBet) VALUES (%s,%s,0);"
        execute_query(dbConnection, query, bFNData)
        bFName = True
    if 'birthMN' in request.form:
        bMNData = (userID, request.form['birthMN'])
        query = "INSERT INTO user_bMName (userID, bMNameID, amountBet) VALUES (%s,%s,0);"
        execute_query(dbConnection, query, bMNData)
        bMName= True

    return render_template('betsPlaced.html', user=user, bDate=bDate, bTime=bTime, bWeight=bWeight, bLength=bLength, bHair=bHair, bFName=bFName, bMName=bMName)



if __name__ == '__main__': app.run(debug=True)