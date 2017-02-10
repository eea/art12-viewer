-- MySQL dump 10.13  Distrib 5.6.17, for Win64 (x86_64)
--
-- Host: localhost    Database: art12rp1_temp_dump
-- ------------------------------------------------------
-- Server version	5.6.17

--
-- Table structure for table `lu_birds_name`
--

CREATE TABLE `lu_birds_name` (
  `speciescode` varchar(10) DEFAULT NULL,
  `speciesname` varchar(128) DEFAULT NULL,
  `ext_dataset_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
