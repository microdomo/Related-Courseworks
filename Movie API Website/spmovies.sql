-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: sp_movies
-- ------------------------------------------------------
-- Server version	8.0.25

CREATE DATABASE  IF NOT EXISTS `sp_movies`;
USE `sp_movies`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `genretable`
--

DROP TABLE IF EXISTS `genretable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genretable` (
  `genreid` int NOT NULL AUTO_INCREMENT,
  `genre` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`genreid`),
  UNIQUE KEY `genre` (`genre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genretable`
--

LOCK TABLES `genretable` WRITE;
/*!40000 ALTER TABLE `genretable` DISABLE KEYS */;
INSERT INTO `genretable` VALUES (1,'Action','The action genre has close ties to classic strife and struggle narratives that you find across all manner of art and literature','2021-06-26 05:43:55'),(2,'Sci-Fi','One of the most experimental and thought-provoking of the classic genres, the science-fiction (popularized as “sci-fi”) film genre goes all the way back to the silent film era. ','2021-06-26 05:44:11'),(3,'Thriller','The thriller genre encapsulates the audience’s curiosity and reservations dealing with governmental conspiracy theory.','2021-06-27 11:10:40'),(4,'Horror','The horror genre dates back to the early days of cinema, and continues to be a treasured pastime. Elements of horror have long been a bedrock of classic cinema.','2021-06-27 11:13:57'),(5,'Adventure','The adventure genre consists of books where the protagonist goes on an epic journey, either personally or geographically. Often the protagonist has a mission and faces many obstacles in his way','2021-08-02 06:41:19'),(6,'Romance','Two basic elements comprise every romance novel: a central love story and an emotionally satisfying and optimistic ending.','2021-08-02 06:43:09'),(7,'Comedy','A genre of fiction comprised of discourses or works intended to be humorous or amusing by inducing laughter, especially in theatre, film, stand-up comedy, television, radio, books, or any other entertainment medium.','2021-08-02 06:43:09');
/*!40000 ALTER TABLE `genretable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moviegenre`
--

DROP TABLE IF EXISTS `moviegenre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moviegenre` (
  `moviegenreid` int NOT NULL AUTO_INCREMENT,
  `moviewithgenreid` int NOT NULL,
  `genreid` int NOT NULL,
  `genre` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`moviegenreid`),
  KEY `movieid_idx` (`moviewithgenreid`) /*!80000 INVISIBLE */,
  KEY `genreid_idx` (`genreid`),
  KEY `genre_idx` (`genre`) /*!80000 INVISIBLE */,
  CONSTRAINT `mg_genre` FOREIGN KEY (`genre`) REFERENCES `genretable` (`genre`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mg_genreid` FOREIGN KEY (`genreid`) REFERENCES `genretable` (`genreid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `moviewithgenreid` FOREIGN KEY (`moviewithgenreid`) REFERENCES `movietable` (`movieid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moviegenre`
--

LOCK TABLES `moviegenre` WRITE;
/*!40000 ALTER TABLE `moviegenre` DISABLE KEYS */;
INSERT INTO `moviegenre` VALUES (1,1,1,'Action','2021-08-08 07:32:54'),(2,1,2,'Sci-Fi','2021-08-08 07:32:54'),(3,1,3,'Thriller','2021-08-08 07:32:54'),(4,2,3,'Thriller','2021-08-08 07:35:01'),(5,2,4,'Horror','2021-08-08 07:35:01'),(6,3,1,'Action','2021-08-08 07:36:20'),(7,3,5,'Adventure','2021-08-08 07:36:20'),(8,4,1,'Action','2021-08-08 07:37:36'),(9,4,5,'Adventure','2021-08-08 07:37:36'),(10,4,7,'Comedy','2021-08-08 07:37:36'),(11,5,6,'Romance','2021-08-08 07:38:37'),(12,6,1,'Action','2021-08-08 07:39:57'),(13,6,2,'Sci-Fi','2021-08-08 07:39:57'),(23,7,1,'Action','2021-11-02 08:21:43'),(24,7,2,'Sci-Fi','2021-11-02 08:21:43'),(25,7,3,'Thriller','2021-11-02 08:21:43');
/*!40000 ALTER TABLE `moviegenre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movietable`
--

DROP TABLE IF EXISTS `movietable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movietable` (
  `movieid` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` mediumtext NOT NULL,
  `cast` varchar(255) NOT NULL,
  `time` varchar(255) NOT NULL,
  `opening date` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(255) DEFAULT 'default.jpg',
  `image2` varchar(255) DEFAULT 'default.jpg',
  PRIMARY KEY (`movieid`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movietable`
--

LOCK TABLES `movietable` WRITE;
/*!40000 ALTER TABLE `movietable` DISABLE KEYS */;
INSERT INTO `movietable` VALUES (1,'Godzilla vs. Kong','Legends collide as Godzilla and Kong, the two most powerful forces of nature, clash on the big screen in a spectacular battle for the ages. As a squadron embarks on a perilous mission into fantastic uncharted terrain, unearthing clues to the Titans\' very origins and mankind\'s survival, a conspiracy threatens to wipe the creatures, both good and bad, from the face of the earth forever.','Shun Oguri, Rebecca Hall, Kyle Chandler, Millie Bobby Brown, Brian Tyree Henry, Alexander Skarsgard , Eiza González, Julian Dennison, Demián Bichir','113 mins','24 Mar 2021','2021-08-08 07:32:54','godzilla.jpg','godzilla2.jpg'),(2,'A Quiet Place Part II','Following the events at home, the Abbott family now face the terrors of the outside world. Forced to venture into the unknown, they realize that the creatures that hunt by sound are not the only threats that lurk beyond the sand path.','Emily Blunt, Cillian Murphy, Millicent Simmonds, Noah Jupe','97 mins','17 Jun 2021','2021-08-08 07:35:01','quietplace.jpg','quietplace2.jpg'),(3,'Marvel Studios\' Black Widow','Scarlett Johansson reprises her role as Natasha/Black Widow in Marvel Studios\' action-packed spy thriller Black Widow- the first film in Phase Four of the Marvel Cinematic Universe. Florence Pugh stars as Yelena, David Harbour as Alexei aka The Red Guard...','Scarlett Johansson, Florence Pugh, David Harbour, Rachel Weisz','134 mins','08 Jul 2021','2021-08-08 07:36:20','blackwidow.jpg','blackwidow2.jpg'),(4,'Jungle Cruise','Based on Disneyland\'s theme park ride where a small riverboat takes a group of travelers through a jungle filled with dangerous animals and reptiles but with a supernatural element.','Dwayne Johnson, Emily Blunt, Edgar Ramírez, Jack Whitehall','127 mins','29 Jul 2021','2021-08-08 07:37:36','junglecruise.jpg','junglecruise2.jpg'),(5,'In The Heights','Lights up on Washington Heights...The scent of a cafecito caliente hangs in the air just outside of the 181st Street subway stop, where a kaleidoscope of dreams rallies this vibrant and tight-knit community. At the intersection of it all is the likeable,...','Anthony Ramos, Corey Hawkins, Leslie Grace, Olga Merediz','143 mins','08 Jul 2021','2021-08-08 07:38:37','intheheight.jpg','intheheight2.jpg'),(6,'Snake Eyes: G.I. Joe Origins','Snake Eyes: G.I. Joe Origins stars Henry Golding as Snake Eyes, a tenacious loner who is welcomed into an ancient Japanese clan called the Arashikage after saving the life of their heir apparent. Upon arrival in Japan, the Arashikage teach Snake Eyes the...','Henry Golding, Andrew Koji, Samara Weaving','121 mins','22 Jul 2021','2021-08-08 07:39:57','snakeeyes.jpg','snakeeyes2.jpg'),(7,'a','a','a','a','a','2021-11-02 08:21:43','default.jpg','default.jpg');
/*!40000 ALTER TABLE `movietable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviewtable`
--

DROP TABLE IF EXISTS `reviewtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviewtable` (
  `reviewid` int NOT NULL AUTO_INCREMENT,
  `movieid` int NOT NULL,
  `userid` int NOT NULL,
  `rating` int NOT NULL,
  `review` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reviewid`),
  KEY `reviewmovieid_idx` (`movieid`) /*!80000 INVISIBLE */,
  KEY ` reviewuserid_idx` (`userid`),
  CONSTRAINT ` reviewuserid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reviewmovieid` FOREIGN KEY (`movieid`) REFERENCES `movietable` (`movieid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviewtable`
--

LOCK TABLES `reviewtable` WRITE;
/*!40000 ALTER TABLE `reviewtable` DISABLE KEYS */;
INSERT INTO `reviewtable` VALUES (1,1,1,4,'Pretty Good','2021-08-08 07:45:37'),(2,2,1,4,'Pretty Good','2021-08-08 07:46:34'),(3,3,1,4,'Pretty Good','2021-08-08 07:46:40'),(4,2,2,3,'Average','2021-08-08 07:47:09'),(5,4,2,3,'Average','2021-08-08 07:49:57'),(6,5,2,3,'Average','2021-08-08 07:50:00'),(7,6,2,3,'Average','2021-08-08 07:50:03'),(8,5,1,2,'Meh','2021-08-08 07:52:26');
/*!40000 ALTER TABLE `reviewtable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `profile_pic_url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Terry','terry@gmail.com','91234567','123','Customer','https://www.abc.com/terry.jpg','2021-06-22 07:01:28'),(2,'Mary','mary@gmail.com','81234567','123','Customer','https://www.zxc.com/mary.jpg','2021-06-22 07:02:21'),(3,'Tom','tom@gmail.com','98765432','123','Admin','https://www.admin.com/tom.jpg','2021-06-22 07:20:18'),(4,'Ben','ben@gmail.com','88765432','123','Admin','https://www.admin.com/ben.jpg','2021-06-27 11:17:24'),(5,'John Tan','john@gmail.com','12345678','123','Customer','https://www.123.com/john.jpg','2021-07-04 07:10:38'),(6,'Timmy','timmy@gmail.com','01234567','123','Customer','https://www.abc.com/timmy.jpg','2021-07-09 06:40:27'),(7,'test','test@gmail.com','test','123','Customer','https://www.abc.com/test.jpg','2021-07-09 06:41:01');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-02 16:26:44
