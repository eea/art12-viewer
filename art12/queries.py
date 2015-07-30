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

SPA_TRIGGER_Q = """
SELECT count(*) AS count
    FROM art12rp1_eu.data_birds_check_list
  WHERE speciescode = '{subject}' AND spa_trigger = True;"""


PRESS_THRE_Q = """
SELECT rst.*
FROM (SELECT rs1.level2_code                        AS code,
             rs1.level2_name                        AS name,
             Round(100 * rs1.pl2_num / rs2.pl2_tot) AS pc
      FROM (SELECT e.level2_code,
                   e.level2_name,
                   Count(e.speciescode) AS pl2_num,
                   1                    AS pl2_set
            FROM (SELECT DISTINCT a.country,
                                  a.speciescode,
                                  a.season,
                                  c.level2_code,
                                  c.level2_name
                  FROM ((art12rp1_eu.data_bpressures_threats t
                         INNER JOIN art12rp1_eu.data_birds a
                                 ON ( a.specieshash = t.specieshash ))
                        INNER JOIN art12rp1_eu.data_birds_check_list b
                                ON ( a.country = b.country
                                     AND a.speciescode = b.speciescode
                                     AND a.season = b.season ))
                  LEFT JOIN (SELECT DISTINCT q_lu_threats.*,
                                             t_lu_threats.name AS level2_name
                             FROM (SELECT t.code,
                                          Substring_index(t.code, '.', 1) AS level2_code
                                   FROM   art12rp1_eu.lu_threats t) q_lu_threats
                                   LEFT JOIN art12rp1_eu.lu_threats t_lu_threats
                                          ON q_lu_threats.level2_code = t_lu_threats.code) c
                               ON ( c.code = t.pressurecode )
                  WHERE  a.speciescode = '{subject}'
                         AND a.use_for_statistics = true
                         AND b.spa_trigger = true
                         AND NOT ( t.pressurecode ) IN ( 'U', 'X' )
                         AND Upper(t.rankingcode) = 'H') AS e
            GROUP BY e.level2_code,
                     e.level2_name) AS rs1
      INNER JOIN (SELECT Count(e.speciescode) AS pl2_tot,
                         1                    AS pl2_set
                  FROM (SELECT DISTINCT a.country,
                                        a.speciescode,
                                        a.season,
                                        Substring_index(c.code, '.', 1) AS level2_code
                        FROM ((art12rp1_eu.data_bpressures_threats t
                               INNER JOIN art12rp1_eu.data_birds a
                                       ON ( a.specieshash = t.specieshash ))
                              INNER JOIN art12rp1_eu.data_birds_check_list b
                                      ON (a.country = b.country
                                          AND a.speciescode = b.speciescode
                                          AND a.season = b.season))
                        LEFT JOIN art12rp1_eu.lu_threats c
                               ON ( c.code = t.pressurecode )
                        WHERE  a.speciescode = '{subject}'
                               AND a.use_for_statistics = true
                               AND b.spa_trigger = true
                               AND NOT ( t.pressurecode ) IN ( 'U', 'X' )
                               AND Upper(t.rankingcode) = 'H') AS e)
                  AS rs2
      ON rs1.pl2_set = rs2.pl2_set
      ORDER  BY Round(100 * rs1.pl2_num / rs2.pl2_tot) DESC)
AS rst
ORDER  BY rst.pc DESC,
          rst.code ASC
LIMIT 10;"""

N2K_Q = """
SELECT t.country                                AS reg,
       IF(t.season = 'W', 'winter', 'breeding') AS wb,
       'YES'                                    AS spa,
       IF(( ( t.spa_population_min IS NULL
              AND t.spa_population_max IS NULL )
             OR ( t.population_minimum_size IS NULL
                  AND t.population_maximum_size IS NULL )
             OR ( t.population_size_unit <> t.spa_population_unit ) )
          AND ( NOT t.population_size_unit IS NULL
                 OR NOT t.spa_population_unit IS NULL ), 'x', Round(
       100 * Pow(IF(t.spa_population_min = 0, 1,
                 IF(t.spa_population_min IS NULL,
       t.spa_population_max, t.spa_population_min)) *
       IF(t.spa_population_max = 0, 1, IF(t.spa_population_max IS NULL,
       t.spa_population_min, t.spa_population_max)), 2) /
       Pow(IF(t.population_minimum_size = 0, 1,
       IF(t.population_minimum_size IS NULL,
       t.population_maximum_size,
       t.population_minimum_size)) * IF(t.population_maximum_size = 0, 1,
       IF(t.population_maximum_size IS NULL, t.population_minimum_size,
       t.population_maximum_size)), 2), 2))     AS pc
FROM   art12rp1_eu.data_birds AS t
       INNER JOIN art12rp1_eu.data_birds_check_list AS b
               ON ( t.country = b.country )
                  AND ( t.speciescode = b.speciescode )
                  AND ( t.season = b.season )
WHERE  ( ( ( t.season ) IN ( 'W', 'B' ) )
         AND t.use_for_statistics = true
         AND ( ( b.spa_trigger ) = true )
         AND ( ( b.speciescode ) = '{subject}' ) )
UNION
SELECT t.country,
       IF(t.season = 'W', 'winter', 'breeding') AS wb,
       'NO'                                     AS spa,
       NULL                                     AS pc
FROM   art12rp1_eu.data_birds AS t
       INNER JOIN art12rp1_eu.data_birds_check_list AS b
               ON ( t.season = b.season )
                  AND ( t.speciescode = b.speciescode )
                  AND ( t.country = b.country )
WHERE  ( ( ( t.season ) IN ( 'W', 'B' ) )
         AND t.use_for_statistics = true
         AND ( ( b.spa_trigger ) = false )
         AND ( ( b.speciescode ) = '{subject}' ) )
ORDER  BY reg ASC,
          wb ASC;"""
