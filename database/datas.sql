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
-- Dumping data for table `ActionTypes`
--

LOCK TABLES `ActionTypes` WRITE;
/*!40000 ALTER TABLE `ActionTypes` DISABLE KEYS */;
INSERT INTO `ActionTypes` VALUES (1,'Arduino','Command','Argument','','','',''),(2,'PushOver','Title','Message','Priority','','',''),(3,'Freebox','','','','','',''),(4,'SamsungTv','','','','','','');
/*!40000 ALTER TABLE `ActionTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Actions`
--

LOCK TABLES `Actions` WRITE;
/*!40000 ALTER TABLE `Actions` DISABLE KEYS */;
INSERT INTO `Actions` VALUES (1,'Notification1','Arduino',0,'notification','1','','','0'),(2,'Notification2','Arduino',0,'notification','2','','','0'),(3,'Notification3','Arduino',0,'notification','3','','','0'),(4,'Alarm','Arduino',0,'alarm','','','','0'),(5,'Sleep','Arduino',0,'sleep','','','','0'),(6,'Wake up','Arduino',0,'wakeup','','','','0'),(7,'Debout','PushOver',0,'C\'est l\'heure de se lever','Hello','1','','');
/*!40000 ALTER TABLE `Actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Alarms`
--

LOCK TABLES `Alarms` WRITE;
/*!40000 ALTER TABLE `Alarms` DISABLE KEYS */;
INSERT INTO `Alarms` VALUES (1,'*','*','*','*','*',0,0,0,0,0,0,0,1);
/*!40000 ALTER TABLE `Alarms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Config`
--

LOCK TABLES `Config` WRITE;
/*!40000 ALTER TABLE `Config` DISABLE KEYS */;
/*!40000 ALTER TABLE `Config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Emails`
--

LOCK TABLES `Emails` WRITE;
/*!40000 ALTER TABLE `Emails` DISABLE KEYS */;
/*!40000 ALTER TABLE `Emails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `EventActions`
--

LOCK TABLES `EventActions` WRITE;
/*!40000 ALTER TABLE `EventActions` DISABLE KEYS */;
INSERT INTO `EventActions` VALUES (1,1,1,0,0,0),(2,1,0,1,0,0),(3,1,0,2,0,0),(4,2,0,0,1,0),(5,2,0,0,2,0),(6,7,1,0,0,0);
/*!40000 ALTER TABLE `EventActions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `SensorTypes`
--

LOCK TABLES `SensorTypes` WRITE;
/*!40000 ALTER TABLE `SensorTypes` DISABLE KEYS */;
INSERT INTO `SensorTypes` VALUES (1,'Temperature',1,'',''),(2,'Light',1,'',''),(3,'Sound',1,'',''),(4,'LongButton',0,'',''),(5,'ShortButton',0,'',''),(6,'Rain',0,'',''),(7,'Fog',0,'',''),(8,'Snow',0,'',''),(9,'Clouds',0,'','');
/*!40000 ALTER TABLE `SensorTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Sensors`
--

LOCK TABLES `Sensors` WRITE;
/*!40000 ALTER TABLE `Sensors` DISABLE KEYS */;
INSERT INTO `Sensors` VALUES (1,'Temperature',20,1,'',''),(2,'Light',400,0,'','');
/*!40000 ALTER TABLE `Sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Switches`
--

LOCK TABLES `Switches` WRITE;
/*!40000 ALTER TABLE `Switches` DISABLE KEYS */;
/*!40000 ALTER TABLE `Switches` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-22 11:13:08
