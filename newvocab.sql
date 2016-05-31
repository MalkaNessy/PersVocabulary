-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 31, 2016 at 05:11 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `slovar`
--

-- --------------------------------------------------------

--
-- Table structure for table `means`
--

CREATE TABLE IF NOT EXISTS `means` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `mean` text NOT NULL,
  `word_id` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `word_id` (`word_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `means`
--

INSERT INTO `means` (`ID`, `mean`, `word_id`) VALUES
(1, 'yabloko', 1),
(2, 'stol', 7),
(3, 'радуга', 8),
(4, 'стол', 9),
(5, 'derevo', 10),
(6, 'дерево', 10);

-- --------------------------------------------------------

--
-- Table structure for table `words`
--

CREATE TABLE IF NOT EXISTS `words` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(256) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `word` (`word`(255))
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `words`
--

INSERT INTO `words` (`ID`, `word`) VALUES
(1, 'apple'),
(2, '%s'),
(3, '%s'),
(4, '%s'),
(5, '%s'),
(6, '%s'),
(7, 'table'),
(8, 'rainbow'),
(9, 'table'),
(10, 'tree');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
