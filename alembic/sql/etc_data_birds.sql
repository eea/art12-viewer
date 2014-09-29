-- MySQL dump 10.13  Distrib 5.6.17, for Win64 (x86_64)
--
-- Host: localhost    Database: art12rp1_temp_dump
-- ------------------------------------------------------
-- Server version	5.6.17

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
-- Table structure for table `etc_data_birds`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `etc_data_birds` (
  `country` varchar(8) NOT NULL,
  `country_isocode` varchar(4) DEFAULT NULL,
  `delivery` tinyint(1) DEFAULT NULL,
  `envelope` varchar(60) NOT NULL,
  `filename` varchar(60) NOT NULL,
  `group` varchar(30) DEFAULT NULL,
  `family` varchar(30) DEFAULT NULL,
  `annex` varchar(11) DEFAULT NULL,
  `priority` varchar(1) DEFAULT NULL,
  `redlist` tinyint(4) DEFAULT NULL,
  `euringcode` varchar(30) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `speciescode` varchar(10) NOT NULL DEFAULT '',
  `speciesname` varchar(128) DEFAULT NULL,
  `species_name_different` tinyint(1) DEFAULT NULL,
  `subspecies_name` varchar(128) DEFAULT NULL,
  `eunis_species_code` int(20) DEFAULT NULL,
  `alternative_speciesname` varchar(128) DEFAULT NULL,
  `common_speciesname` varchar(128) DEFAULT NULL,
  `valid_speciesname` varchar(128) DEFAULT NULL,
  `n2000_species_code` int(11) DEFAULT NULL,
  `assesment_speciesname` varchar(128) DEFAULT NULL,
  `assesment_speciesname_changed` tinyint(1) DEFAULT NULL,
  `grouped_assesment` tinyint(1) DEFAULT NULL,
  `species_type` varchar(10) DEFAULT NULL,
  `species_type_asses` tinyint(1) DEFAULT NULL,
  `range_surface_area_bs` double DEFAULT NULL,
  `range_change_reason_bs` varchar(150) DEFAULT NULL,
  `percentage_range_surface_area_bs` double DEFAULT NULL,
  `range_additional_info_record_bs` varchar(1) DEFAULT NULL,
  `range_additional_info_bs` text,
  `range_trend_period_bs` varchar(30) DEFAULT NULL,
  `range_trend_bs` varchar(2) DEFAULT NULL,
  `range_trend_magnitude_min_bs` decimal(18,5) DEFAULT NULL,
  `range_trend_magnitude_max_bs` decimal(18,5) DEFAULT NULL,
  `range_trend_long_period_bs` varchar(30) DEFAULT NULL,
  `range_trend_long_bs` varchar(2) DEFAULT NULL,
  `range_trend_long_magnitude_min_bs` decimal(18,5) DEFAULT NULL,
  `range_trend_long_magnitude_max_bs` decimal(18,5) DEFAULT NULL,
  `range_trend_additional_info_record_bs` varchar(1) DEFAULT NULL,
  `range_trend_additional_info_bs` text,
  `range_yearly_magnitude_bs` double DEFAULT NULL,
  `complementary_favourable_range_op_bs` varchar(2) DEFAULT NULL,
  `complementary_favourable_range_bs` double DEFAULT NULL,
  `population_minimum_size_bs` double DEFAULT NULL,
  `percentage_population_minimum_size_bs` double DEFAULT NULL,
  `population_maximum_size_bs` double DEFAULT NULL,
  `percentage_population_maximum_size_bs` double DEFAULT NULL,
  `filled_population_bs` varchar(3) DEFAULT NULL,
  `population_size_unit_bs` varchar(10) DEFAULT NULL,
  `population_units_agreed_bs` varchar(50) DEFAULT NULL,
  `population_units_other_bs` varchar(50) DEFAULT NULL,
  `population_change_reason_bs` varchar(150) DEFAULT NULL,
  `number_of_different_population_units_bs` int(2) DEFAULT NULL,
  `different_population_percentage_bs` tinyint(1) DEFAULT NULL,
  `percentage_population_mean_size_bs` double DEFAULT NULL,
  `population_additional_info_record_bs` varchar(1) DEFAULT NULL,
  `population_additional_info_bs` text,
  `population_trend_period_bs` varchar(30) DEFAULT NULL,
  `population_trend_bs` varchar(2) DEFAULT NULL,
  `population_trend_magnitude_min_bs` decimal(18,5) DEFAULT NULL,
  `population_trend_magnitude_max_bs` decimal(18,5) DEFAULT NULL,
  `population_trend_long_period_bs` varchar(30) DEFAULT NULL,
  `population_trend_long_bs` varchar(2) DEFAULT NULL,
  `population_trend_long_magnitude_min_bs` decimal(18,5) DEFAULT NULL,
  `population_trend_long_magnitude_max_bs` decimal(18,5) DEFAULT NULL,
  `population_trend_additional_info_record_bs` varchar(1) DEFAULT NULL,
  `population_trend_additional_info_bs` text,
  `population_yearly_magnitude_bs` double DEFAULT NULL,
  `complementary_favourable_population_op_bs` varchar(2) DEFAULT NULL,
  `complementary_favourable_population_bs` double DEFAULT NULL,
  `filled_complementary_favourable_population_bs` varchar(3) DEFAULT NULL,
  `population_minimum_size_ws` double DEFAULT NULL,
  `percentage_population_minimum_size_ws` double DEFAULT NULL,
  `population_maximum_size_ws` double DEFAULT NULL,
  `percentage_population_maximum_size_ws` double DEFAULT NULL,
  `filled_population_ws` varchar(3) DEFAULT NULL,
  `population_size_unit_ws` varchar(10) DEFAULT NULL,
  `percentage_population_mean_size_ws` double DEFAULT NULL,
  `population_trend_period_ws` varchar(30) DEFAULT NULL,
  `population_trend_ws` varchar(2) DEFAULT NULL,
  `population_trend_magnitude_min_ws` decimal(18,5) DEFAULT NULL,
  `population_trend_magnitude_max_ws` decimal(18,5) DEFAULT NULL,
  `population_trend_long_period_ws` varchar(30) DEFAULT NULL,
  `population_trend_long_ws` varchar(2) DEFAULT NULL,
  `population_trend_long_magnitude_min_ws` decimal(18,5) DEFAULT NULL,
  `population_trend_long_magnitude_max_ws` decimal(18,5) DEFAULT NULL,
  `population_trend_additional_info_ws` text,
  `future_prospects` varchar(4) DEFAULT NULL,
  `conclusion_range_bs` varchar(4) DEFAULT NULL,
  `conclusion_population_bs` varchar(4) DEFAULT NULL,
  `conclusion_population_ws` varchar(4) DEFAULT NULL,
  `conclusion_future` varchar(4) DEFAULT NULL,
  `conclusion_assessment` varchar(4) DEFAULT NULL,
  `conclusion_assessment_trend` varchar(2) DEFAULT NULL,
  `conclusion_assessment_prev` varchar(4) DEFAULT NULL,
  `conclusion_assessment_change` varchar(2) DEFAULT NULL,
  `range_quality_bs` varchar(13) DEFAULT NULL,
  `range_trend_quality_bs` varchar(13) DEFAULT NULL,
  `range_trend_long_quality_bs` varchar(13) DEFAULT NULL,
  `population_quality_bs` varchar(13) DEFAULT NULL,
  `population_trend_quality_bs` varchar(13) DEFAULT NULL,
  `population_trend_long_quality_bs` varchar(13) DEFAULT NULL,
  `population_quality_ws` varchar(13) DEFAULT NULL,
  `population_trend_quality_ws` varchar(13) DEFAULT NULL,
  `population_trend_long_quality_ws` varchar(13) DEFAULT NULL,
  `further_information` text,
  `further_information_english` text,
  `range_grid_area` double DEFAULT NULL,
  `percentage_range_grid_area` double DEFAULT NULL,
  `distribution_grid_area` double DEFAULT NULL,
  `percentage_distribution_grid_area` double DEFAULT NULL,
  `ext_dataset_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`country`,`speciescode`,`ext_dataset_id`),
  KEY `group` (`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-09-26 13:37:51
