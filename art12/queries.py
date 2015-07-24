SPECIESNAME_Q = """
SELECT DISTINCT A.speciesname
  FROM art12rp1_eu.data_birds_check_list A
 WHERE A.speciescode = '{code}';"""

SUBUNIT_Q = """
SELECT DISTINCT A.sub_unit
  FROM art12rp1_eu.data_birds_check_list A
 WHERE (A.speciescode = '{code}');"""

ANNEX_Q = """
SELECT DISTINCT A.annexI
  FROM art12rp1_eu.data_birds_check_list A
 WHERE A.speciescode = '{code}';"""

PLAN_Q = """
SELECT DISTINCT REPLACE(A.plan, 'NA', 'No')
  FROM art12rp1_eu.data_birds A
 WHERE A.speciescode = '{code}';"""

LISTS_Q = """
SELECT
  COALESCE(A.conclusion_status_level1_record,
           If(A.speciesname_subpopulation IS NULL,
              A.speciesname,
              CONCAT(A.speciesname,' [',A.speciesname_subpopulation,']')
             )
          ) AS first_list,
  COALESCE(A.conclusion_status_level2_record,
           If(A.speciesname_subpopulation IS NULL,
              A.speciesname,
              CONCAT(A.speciesname,' [',A.speciesname_subpopulation,']')
             )
           ) AS second_list
    FROM art12.etc_birds_eu_view A
  WHERE A.speciescode = '{subject}' AND (A.ext_dataset_id = {period});"""

MS_TABLE_Q = """
SELECT
  A.country,
  A.percentage_distribution_grid_area,
  CONCAT_WS(' ', A.population_minimum_size_bs,
            '-', A.population_maximum_size_bs,
            If(A.population_size_unit_bs = 'p',
               null,
               A.population_size_unit_bs))
    AS breeding_population_size,
  A.population_trend_bs,
  A.population_trend_long_bs,
  A.range_surface_area_bs,
  A.range_trend_bs,
  A.range_trend_long_bs,
  CONCAT_WS(' ', A.population_minimum_size_ws,
            '-', A.population_maximum_size_ws,
            If(A.population_size_unit_ws = 'i',
               null,
               A.population_size_unit_ws))
    AS winter_population_size,
  A.population_trend_ws,
  A.population_trend_long_ws
    FROM art12.etc_data_birds A
  WHERE (A.speciescode = '{subject}') AND (A.ext_dataset_id = {period});"""
