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
