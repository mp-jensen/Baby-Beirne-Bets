-- Count how many bets are in each category
SELECT count(*) FROM user_bDate;
SELECT count(*) FROM user_bTime;
SELECT count(*) FROM user_bWeight;
SELECT count(*) FROM user_bLength;
SELECT count(*) FROM user_bHair;
SELECT count(*) FROM user_bFName;
SELECT count(*) FROM user_bMName;

-- Count how many paid bets there are in each category
SELECT count(*) FROM user_bDate WHERE paidStatus > 0;
SELECT count(*) FROM user_bTime WHERE paidStatus > 0;
SELECT count(*) FROM user_bWeight WHERE paidStatus > 0;
SELECT count(*) FROM user_bLength WHERE paidStatus > 0;
SELECT count(*) FROM user_bHair WHERE paidStatus > 0;
SELECT count(*) FROM user_bFName WHERE paidStatus > 0;
SELECT count(*) FROM user_bMName WHERE paidStatus > 0;

-- Sum how much money is on the line for each bet
SELECT sum(amountPaid) FROM user_bDate WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bTime WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bWeight WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bLength WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bHair WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bFName WHERE paidStatus > 0;
SELECT sum(amountPaid) FROM user_bMName WHERE paidStatus > 0;

-- get count and value of bets of each type for all bets
SELECT count(*),bd.date FROM user_bDate ubd INNER JOIN bDate bd ON ubd.bDateID=bd.bDateID GROUP BY bd.bDateID;
SELECT count(*),bh.hour,bm.minute FROM user_bTime ubt INNER JOIN bHour bh ON ubt.bHourID=bh.bHourID INNER JOIN bMinute bm ON ubt.bMinuteID=bm.bMinuteID GROUP BY ubt.bHourID, ubt.bMinuteID;
SELECT count(*),bl.lb,bo.oz FROM user_bWeight ubw INNER JOIN bLb bl ON ubw.bLbID=bl.bLbID INNER JOIN bOz bo ON ubw.bOzID=bo.bOzID GROUP BY ubw.bLbID, ubw.bOzID;
SELECT count(*),bl.inches FROM user_bLength ubl INNER JOIN bLength bl ON ubl.bLengthID=bl.bLengthID GROUP BY ubl.bLengthID;
SELECT count(*),bh.hair FROM user_bHair ubh INNER JOIN bHair bh ON ubh.bHairID=bh.bHairID GROUP BY ubh.bHairID;
SELECT count(*),bf.letter FROM user_bFName ubf INNER JOIN bFName bf ON ubf.bFNameID=bf.bFNameID GROUP BY ubf.bFNameID;
SELECT count(*),bm.letter FROM user_bMName ubm INNER JOIN bMName bm ON ubm.bMNameID=bm.bMNameID GROUP BY ubm.bMNameID;

-- get count and value of bets of each type for all paid bets
SELECT count(*),bd.date FROM user_bDate ubd INNER JOIN bDate bd ON ubd.bDateID=bd.bDateID WHERE ubd.paidStatus>0 GROUP BY ubd.bDateID;
SELECT count(*),bh.hour,bm.minute FROM user_bTime ubt INNER JOIN bHour bh ON ubt.bHourID=bh.bHourID INNER JOIN bMinute bm ON ubt.bMinuteID=bm.bMinuteID WHERE ubt.paidStatus>0 GROUP BY ubt.bHourID, ubt.bMinuteID;
SELECT count(*),bl.lb,bo.oz FROM user_bWeight ubw INNER JOIN bLb bl ON ubw.bLbID=bl.bLbID INNER JOIN bOz bo ON ubw.bOzID=bo.bOzID WHERE ubw.paidStatus>0 GROUP BY ubw.bLbID, ubw.bOzID;
SELECT count(*),bl.inches FROM user_bLength ubl INNER JOIN bLength bl ON ubl.bLengthID=bl.bLengthID WHERE ubl.paidStatus>0 GROUP BY ubl.bLengthID;
SELECT count(*),bh.hair FROM user_bHair ubh INNER JOIN bHair bh ON ubh.bHairID=bh.bHairID WHERE ubh.paidStatus>0 GROUP BY ubh.bHairID;
SELECT count(*),bf.letter FROM user_bFName ubf INNER JOIN bFName bf ON ubf.bFNameID=bf.bFNameID WHERE ubf.paidStatus>0 GROUP BY ubf.bFNameID;
SELECT count(*),bm.letter FROM user_bMName ubm INNER JOIN bMName bm ON ubm.bMNameID=bm.bMNameID WHERE ubm.paidStatus>0 GROUP BY ubm.bMNameID;
