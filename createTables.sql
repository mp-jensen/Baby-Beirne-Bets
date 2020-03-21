-- Drop Tables if they exist
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `bDate`;
DROP TABLE IF EXISTS `bHour`;
DROP TABLE IF EXISTS `bMinute`;
DROP TABLE IF EXISTS `bLb`;
DROP TABLE IF EXISTS `bOz`;
DROP TABLE IF EXISTS `bLength`;
DROP TABLE IF EXISTS `bHair`;
DROP TABLE IF EXISTS `bFName`;
DROP TABLE IF EXISTS `bMName`;
DROP TABLE IF EXISTS `winners`;
DROP TABLE IF EXISTS `user_bDate`;
DROP TABLE IF EXISTS `user_bTime`;
DROP TABLE IF EXISTS `user_bWeight`;
DROP TABLE IF EXISTS `user_bLength`;
DROP TABLE IF EXISTS `user_bHair`;
DROP TABLE IF EXISTS `user_bFName`;
DROP TABLE IF EXISTS `user_bMName`;

-- Create Tables for DB
CREATE TABLE `users` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255),
  `lastName` varchar(255),
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT UNIQUE(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bDate` (
  `bDateID` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  PRIMARY KEY (`bDateID`),
  CONSTRAINT UNIQUE(`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bHour` (
  `bHourID` INT NOT NULL AUTO_INCREMENT,
  `hour` INT(2) NOT NULL,
  PRIMARY KEY (`bHourID`),
  CONSTRAINT UNIQUE(`hour`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bMinute` (
  `bMinuteID` INT NOT NULL AUTO_INCREMENT,
  `minute` INT(2) NOT NULL,
  PRIMARY KEY (`bMinuteID`),
  CONSTRAINT UNIQUE(`minute`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bLb` (
  `bLbID` INT NOT NULL AUTO_INCREMENT,
  `lb` INT(2) NOT NULL,
  PRIMARY KEY (`bLbID`),
  CONSTRAINT UNIQUE(`lb`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bOz` (
  `bOzID` INT NOT NULL AUTO_INCREMENT,
  `oz` INT(2) NOT NULL,
  PRIMARY KEY (`bOzID`),
  CONSTRAINT UNIQUE(`oz`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bLength` (
  `bLengthID` INT NOT NULL AUTO_INCREMENT,
  `inches` DECIMAL(4,2) NOT NULL,
  PRIMARY KEY (`bLengthID`),
  CONSTRAINT UNIQUE(`inches`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bHair` (
  `bHairID` INT NOT NULL AUTO_INCREMENT,
  `hair` CHAR(15) NOT NULL,
  PRIMARY KEY (`bHairID`),
  CONSTRAINT UNIQUE(`hair`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bFName` (
  `bFNameID` INT NOT NULL AUTO_INCREMENT,
  `letter` CHAR(1) NOT NULL,
  PRIMARY KEY (`bFNameID`),
  CONSTRAINT UNIQUE(`letter`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `bMName` (
  `bMNameID` INT NOT NULL AUTO_INCREMENT,
  `letter` CHAR(1) NOT NULL,
  PRIMARY KEY (`bMNameID`),
  CONSTRAINT UNIQUE(`letter`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `winners` (
  `bDateID` INT,
  `bHourID` INT,
  `bMinuteID` INT,
  `bLbID` INT,
  `bOzID` INT,
  `bLengthID` INT,
  `bHairID` INT,
  `bFNameID` INT,
  `bMNameID` INT,
  FOREIGN KEY (`bDateID`) REFERENCES bDate(`bDateID`),
  FOREIGN KEY (`bHourID`) REFERENCES bHour(`bHourID`),
  FOREIGN KEY (`bMinuteID`) REFERENCES bMinute(`bMinuteID`),
  FOREIGN KEY (`bLbID`) REFERENCES bLb(`bLbID`),
  FOREIGN KEY (`bOzID`) REFERENCES bOz(`bOzID`),
  FOREIGN KEY (`bLengthID`) REFERENCES bLength(`bLengthID`),
  FOREIGN KEY (`bHairID`) REFERENCES bHair(`bHairID`),
  FOREIGN KEY (`bFNameID`) REFERENCES bFName(`bFNameID`),
  FOREIGN KEY (`bMNameID`) REFERENCES bMName(`bMNameID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bDate` (
  `userID` INT NOT NULL,
  `bDateID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bDateID`) REFERENCES bDate(`bDateID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `user_bTime` (
  `userID` INT NOT NULL,
  `bHourID` INT NOT NULL,
  `bMinuteID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bHourID`) REFERENCES bHour(`bHourID`),
  FOREIGN KEY (`bMinuteID`) REFERENCES bMinute(`bMinuteID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bWeight` (
  `userID` INT NOT NULL,
  `bLbID` INT NOT NULL,
  `bOzID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bLbID`) REFERENCES bLb(`bLbID`),
  FOREIGN KEY (`bOzID`) REFERENCES bOz(`bOzID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bLength` (
  `userID` INT NOT NULL,
  `bLengthID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bLengthID`) REFERENCES bLength(`bLengthID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bHair` (
  `userID` INT NOT NULL,
  `bHairID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bHairID`) REFERENCES bHair(`bHairID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bFName` (
  `userID` INT NOT NULL,
  `bFNameID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bFNameID`) REFERENCES bFName(`bFNameID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_bMName` (
  `userID` INT NOT NULL,
  `bMNameID` INT NOT NULL,
  `amountBet` INT NOT NULL,
  `amountPaid` INT NOT NULL DEFAULT 0,
  `paidStatus` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`userID`),
  FOREIGN KEY (`userID`) REFERENCES users(`userID`),
  FOREIGN KEY (`bMNameID`) REFERENCES bMName(`bMNameID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert queries into DB
INSERT INTO users
  (firstName, lastName, email)
VALUES
  ('Manda', 'Jensen', 'mandaphad@gmail.com');


