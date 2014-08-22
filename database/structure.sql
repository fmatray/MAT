-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: arduino
-- ------------------------------------------------------
-- Server version	5.5.38-0+wheezy1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ActionTypes`
--

DROP TABLE IF EXISTS `ActionTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ActionTypes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` varchar(32) NOT NULL,
  `Argument1` tinytext NOT NULL,
  `Argument2` tinytext NOT NULL,
  `Argument3` tinytext NOT NULL,
  `Argument4` tinytext NOT NULL,
  `Argument5` tinytext NOT NULL,
  `Help` tinytext NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Type` (`Type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Actions`
--

DROP TABLE IF EXISTS `Actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Action` text NOT NULL,
  `Type` varchar(32) NOT NULL,
  `Rank` int(11) NOT NULL,
  `Argument1` text NOT NULL,
  `Argument2` text NOT NULL,
  `Argument3` text NOT NULL,
  `Argument4` text NOT NULL,
  `Argument5` text NOT NULL,
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Alarms`
--

DROP TABLE IF EXISTS `Alarms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Alarms` (
  `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `year` char(4) DEFAULT NULL,
  `month` char(2) NOT NULL,
  `day` char(2) NOT NULL,
  `hour` char(2) NOT NULL,
  `minute` char(2) NOT NULL,
  `monday` tinyint(1) NOT NULL DEFAULT '0',
  `thuesday` tinyint(1) NOT NULL DEFAULT '0',
  `wednesday` tinyint(1) NOT NULL DEFAULT '0',
  `thursday` tinyint(1) NOT NULL DEFAULT '0',
  `friday` tinyint(1) NOT NULL DEFAULT '0',
  `saturday` tinyint(1) NOT NULL DEFAULT '0',
  `sunday` tinyint(1) NOT NULL DEFAULT '0',
  `isactive` tinyint(1) NOT NULL DEFAULT '0',
  UNIQUE KEY `ID_2` (`ID`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Config`
--

DROP TABLE IF EXISTS `Config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Config` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Category` tinytext NOT NULL,
  `Key` tinytext NOT NULL,
  `Value` tinytext NOT NULL,
  `Help` tinytext NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Emails`
--

DROP TABLE IF EXISTS `Emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Emails` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `server` text NOT NULL,
  `port` tinyint(4) NOT NULL,
  `login` tinytext NOT NULL,
  `password` tinytext NOT NULL,
  `imap` tinyint(1) NOT NULL,
  `ssl` tinyint(1) NOT NULL DEFAULT '1',
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EventActions`
--

DROP TABLE IF EXISTS `EventActions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EventActions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IDAction` int(11) NOT NULL DEFAULT '0',
  `IDAlarm` int(11) NOT NULL DEFAULT '0',
  `IDEmail` int(11) NOT NULL DEFAULT '0',
  `IDSensor` int(11) NOT NULL DEFAULT '0',
  `IDSwitch` int(11) NOT NULL DEFAULT '0',
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SensorTypes`
--

DROP TABLE IF EXISTS `SensorTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SensorTypes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` varchar(32) NOT NULL,
  `Analogic` tinyint(1) NOT NULL DEFAULT '1',
  `Argument1` tinytext NOT NULL,
  `Argument2` tinytext NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Type` (`Type`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Sensors`
--

DROP TABLE IF EXISTS `Sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sensors` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` varchar(32) NOT NULL,
  `Threshold` float NOT NULL,
  `MinMax` tinyint(1) NOT NULL DEFAULT '0',
  `Argument1` tinytext NOT NULL,
  `Argument2` tinytext NOT NULL,
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Switches`
--

DROP TABLE IF EXISTS `Switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Switches` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  `Number` int(11) NOT NULL,
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-22 11:05:24
