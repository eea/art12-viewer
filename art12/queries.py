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
