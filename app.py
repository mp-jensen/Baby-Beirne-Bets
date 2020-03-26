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
        print("userID in placeBets: {0}".format(userID))
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
        execute_query(dbConnection, query, bLengthData)
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


@app.route('/viewMyBets', methods=["POST","GET"])
def viewMyBets():
    if request.method == "GET":
        return render_template('viewMyBets.html')

    if 'myEmail' in request.form:
        dbConnection = connect_to_database()

        userID = False
        bDate = False
        bHour = False
        bMinute = False
        bLb = False
        bOz = False
        bLength = False
        bHair = False
        bFName = False
        bMName = False

        email = request.form['myEmail']

        # get userID, if the email is not associated with a user, return the template
        query = "SELECT userID FROM users WHERE email=%s"
        userID = execute_query(dbConnection, query, (email,))
        if userID.rowcount > 0:
            userID = userID.fetchone()[0]
        else:
            userID = False
            return render_template('viewMyBets.html', email=email,userID=userID)

        # get the user's birth date bet
        query = "SELECT bd.date FROM bDate bd INNER JOIN user_bDate ubd ON bd.bDateID=ubd.bDateID WHERE ubd.userID=%s;"
        bDate = execute_query(dbConnection, query, (userID,))
        if bDate.rowcount > 0:
            bDate = bDate.fetchone()[0]
        else:
            bDate = False

        # get the user's hour from the birth time bet
        query = "SELECT bh.hour FROM bHour bh INNER JOIN user_bTime ubt ON bh.bHourID=ubt.bHourID WHERE ubt.userID=%s;"
        bHour = execute_query(dbConnection, query, (userID,))
        if bHour.rowcount > 0:
            bHour = bHour.fetchone()[0]
        else:
            bHour = False

        # get the user's minute from the birth time bet
        query = "SELECT bm.minute FROM bMinute bm INNER JOIN user_bTime ubt ON bm.bMinuteID=ubt.bMinuteID WHERE ubt.userID=%s;"
        bMinute = execute_query(dbConnection, query, (userID,))
        if bMinute.rowcount > 0:
            bMinute = bMinute.fetchone()[0]
        else:
            bMinute = False

        # get the user's lbs from the birth weight bet
        query = "SELECT bl.lb FROM bLb bl INNER JOIN user_bWeight ubw ON bl.bLbID=ubw.bLbID WHERE ubw.userID=%s;"
        bLb = execute_query(dbConnection, query, (userID,))
        if bLb.rowcount > 0:
            bLb = bLb.fetchone()[0]
        else:
            bLb = False

        # get user's oz from the birth weight bet
        query = "SELECT bo.oz FROM bOz bo INNER JOIN user_bWeight ubw ON bo.bOzID=ubw.bOzID WHERE ubw.userID=%s;"
        bOz = execute_query(dbConnection, query, (userID,))
        if bOz.rowcount > 0:
            bOz = bOz.fetchone()[0]
        else:
            bOz = False

        # get user's inches from birth length bet
        query = "SELECT bl.inches FROM bLength bl INNER JOIN user_bLength ubl ON bl.bLengthID=ubl.bLengthID WHERE ubl.userID=%s;"
        bLength = execute_query(dbConnection, query, (userID,))
        if bLength.rowcount > 0:
            bLength = bLength.fetchone()[0]
        else:
            bLength = False

        # get user's hair from birth hair bet
        query = "SELECT bh.hair FROM bHair bh INNER JOIN user_bHair ubh ON bh.bHairID=ubh.bHairID WHERE ubh.userID=%s"
        bHair = execute_query(dbConnection, query, (userID,))
        if bHair.rowcount > 0:
            bHair = bHair.fetchone()[0]
        else:
            bHair = False

        # get user's letter from first initial bet
        query = "SELECT bf.letter FROM bFName bf INNER JOIN user_bFName ubf ON bf.bFNameID=ubf.bFNameID WHERE ubf.userID=%s"
        bFName = execute_query(dbConnection, query, (userID,))
        if bFName.rowcount > 0:
            bFName = bFName.fetchone()[0]
        else:
            bFName = False

        # get user's letter for middle initial bet
        query = "SELECT bm.letter FROM bMName bm INNER JOIN user_bMName ubm ON bm.bMNameID=ubm.bMNameID WHERE ubm.userID=%s"
        bMName = execute_query(dbConnection, query, (userID,))
        if bMName.rowcount > 0:
            bMName = bMName.fetchone()[0]
        else:
            bMName = False

        # render template with all information about user's bets
        return render_template("viewMyBets.html",email=email, userID=userID, bDate=bDate, bHour=bHour, bMinute=bMinute, bLb=bLb, bOz=bOz, bLength=bLength, bHair=bHair, bFName=bFName, bMName=bMName)

    else:
        return render_template('viewMyBets.html')


@app.route('/viewAllBets')
def viewAllBets():
    dbConnection = connect_to_database()

    bDateCount = execute_query(dbConnection, "SELECT count(*) FROM user_bDate;")
    bDateCount = False if bDateCount.rowcount < 1 else bDateCount.fetchall()
    bDatePaidCount = execute_query(dbConnection, "SELECT count(*) FROM user_bDate WHERE paidStatus > 0;")
    bDatePaidCount = False if bDatePaidCount.rowcount < 1 else bDatePaidCount.fetchall()
    bDateValue = execute_query(dbConnection, "SELECT sum(amountPaid) FROM user_bDate WHERE paidStatus > 0;")
    bDateValue = False if bDateValue.rowcount < 1 else bDateValue.fetchall()
    allBDateBets = execute_query(dbConnection, "SELECT count(*),bd.date FROM user_bDate ubd INNER JOIN bDate bd ON ubd.bDateID=bd.bDateID GROUP BY bd.bDateID;")
    allBDateBets = False if allBDateBets.rowcount < 1 else allBDateBets.fetchall()
    paidBDateBets = execute_query(dbConnection, "SELECT count(*),bd.date FROM user_bDate ubd INNER JOIN bDate bd ON ubd.bDateID=bd.bDateID WHERE ubd.paidStatus>0 GROUP BY bd.bDateID;")
    paidBDateBets = False if paidBDateBets.rowcount < 1 else paidBDateBets.fetchall()
    bDateData = (bDateCount, bDatePaidCount, bDateValue, allBDateBets, paidBDateBets)

    bTimeCount = execute_query(dbConnection, "SELECT count(*) FROM user_bTime;")
    bTimeCount = False if bTimeCount.rowcount < 1 else bTimeCount.fetchall()
    bTimePaidCount = execute_query(dbConnection, "SELECT count(*) FROM user_bWeight WHERE paidStatus > 0;")
    bTimePaidCount = False if bTimePaidCount.rowcount < 1 else bTimePaidCount.fetchall()
    bTimeValue = execute_query(dbConnection, "SELECT sum(amountPaid) FROM user_bTime WHERE paidStatus > 0;")
    bTimeValue = False if bTimeValue.rowcount < 1 else bTimeValue.fetchall()
    allBTimeBets = execute_query(dbConnection, "SELECT count(*),bh.hour,bm.minute FROM user_bTime ubt INNER JOIN bHour bh ON ubt.bHourID=bh.bHourID INNER JOIN bMinute bm ON ubt.bMinuteID=bm.bMinuteID GROUP BY ubt.bHourID, ubt.bMinuteID;")
    allBTimeBets = False if allBTimeBets.rowcount < 1 else allBTimeBets.fetchall()
    paidBTimeBets = execute_query(dbConnection, "SELECT count(*),bh.hour,bm.minute FROM user_bTime ubt INNER JOIN bHour bh ON ubt.bHourID=bh.bHourID INNER JOIN bMinute bm ON ubt.bMinuteID=bm.bMinuteID WHERE ubt.paidStatus>0 GROUP BY ubt.bHourID, ubt.bMinuteID;")
    paidBTimeBets = False if paidBTimeBets.rowcount < 1 else paidBTimeBets.fetchall()
    bTimeData = (bTimeCount, bTimePaidCount, bTimeValue, allBTimeBets, paidBTimeBets)

    return render_template('viewAllBets.html', bDateData=bDateData,bTimeData=bTimeData)


@app.route('/winners')
def winners():
    return render_template('winners.html')


if __name__ == '__main__': app.run(debug=True)