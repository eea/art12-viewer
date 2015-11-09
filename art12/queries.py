SPECIESNAME_Q = """
SELECT DISTINCT A.speciesname
  FROM art12rp1_eu.data_birds_check_list A
 WHERE A.speciescode = '{code}';"""

SUBUNIT_Q = """
SELECT DISTINCT A.sub_unit
  FROM art12rp1_eu.data_birds_check_list A
 WHERE (A.speciescode = '{code}');"""

ANNEX_Q = """
SELECT DISTINCT REPLACE(REPLACE(A.annexI, 'N', 'No'), 'Y', 'Yes')
  FROM art12rp1_eu.data_birds_check_list A
 WHERE A.speciescode = '{code}';"""

PLAN_Q = """
SELECT DISTINCT REPLACE(A.plan, 'NA', 'No')
  FROM art12rp1_eu.data_birds A
 WHERE A.speciescode = '{code}';"""

MS_TABLE_Q = """
SELECT
  A.country,
  A.percentage_distribution_grid_area,
  IF(A.population_minimum_size_bs IS null
       AND A.population_maximum_size_bs IS null,
     null,
     CONCAT_WS(' ', A.population_minimum_size_bs,
               '-', A.population_maximum_size_bs,
               A.population_size_unit_bs))
    AS breeding_population_size,
  A.population_trend_bs,
  A.population_trend_long_bs,
  A.range_surface_area_bs,
  A.range_trend_bs,
  A.range_trend_long_bs,
  IF(A.population_minimum_size_ws IS null
       AND A.population_maximum_size_ws IS null,
     null,
     CONCAT_WS(' ', A.population_minimum_size_ws,
               '-', A.population_maximum_size_ws,
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
                                             t_lu_threats.name_corrected AS level2_name
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
       100 * SQRT(IF(t.spa_population_min = 0, 1,
                 IF(t.spa_population_min IS NULL,
       t.spa_population_max, t.spa_population_min)) *
       IF(t.spa_population_max = 0, 1, IF(t.spa_population_max IS NULL,
       t.spa_population_min, t.spa_population_max))) /
       SQRT(IF(t.population_minimum_size = 0, 1,
       IF(t.population_minimum_size IS NULL,
       t.population_maximum_size,
       t.population_minimum_size)) * IF(t.population_maximum_size = 0, 1,
       IF(t.population_maximum_size IS NULL, t.population_minimum_size,
       t.population_maximum_size))), 2))     AS pc
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

CONS_MEASURES_Q = """
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
                  FROM ((art12rp1_eu.data_bmeasures m
                         INNER JOIN art12rp1_eu.data_birds a
                                 ON ( a.specieshash = m.specieshash ))
                         INNER JOIN art12rp1_eu.data_birds_check_list b
                                 ON ( a.country = b.country
                                      AND a.speciescode = b.speciescode
                                      AND a.season = b.season ))
                         LEFT JOIN (SELECT DISTINCT q_lu_measures.*,
                                                    t_lu_measures.NAME AS level2_name
                                    FROM (SELECT t.code,
                                                 LEFT(t.code, 3) AS level2_code
                                          FROM art12rp1_eu.lu_measures t)
                                          q_lu_measures
                                          LEFT JOIN art12rp1_eu.lu_measures t_lu_measures
                                                 ON q_lu_measures.level2_code = t_lu_measures.code) c
                                ON ( c.code = m.measurecode )
                  WHERE  a.speciescode = '{subject}'
                         AND a.use_for_statistics = true
                         AND b.spa_trigger = true
                         AND Ucase(m.rankingcode) = 'H'
                         AND ( NOT m.measurecode LIKE '1*' )) AS e
            GROUP  BY e.level2_code,
                      e.level2_name) AS rs1
      INNER JOIN (SELECT Count(e.speciescode) AS pl2_tot,
                         1                    AS pl2_set
                  FROM (SELECT DISTINCT a.country,
                                          a.speciescode,
                                          a.season,
                                          LEFT(c.code, 3) AS level2_code
                        FROM ((art12rp1_eu.data_bmeasures m
                               INNER JOIN art12rp1_eu.data_birds a
                                       ON a.specieshash = m.specieshash)
                               INNER JOIN art12rp1_eu.data_birds_check_list b
                                       ON (a.country = b.country
                                           AND a.speciescode = b.speciescode
                                           AND a.season = b.season))
                               LEFT JOIN art12rp1_eu.lu_measures c
                                      ON ( c.code = m.measurecode )
                        WHERE  a.speciescode = '{subject}'
                               AND a.use_for_statistics = true
                               AND b.spa_trigger = true
                               AND Ucase(m.rankingcode) = 'H'
                               AND ( NOT m.measurecode LIKE '1*' )) AS e
                  ) AS rs2
              ON rs1.pl2_set = rs2.pl2_set
      ORDER  BY Round(100 * rs1.pl2_num / rs2.pl2_tot) DESC) AS rst
ORDER BY rst.pc DESC,
         rst.code ASC
LIMIT 10;"""
