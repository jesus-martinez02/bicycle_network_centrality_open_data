DROP TABLE greater_graz_results;

CREATE TABLE greater_graz_results AS
(
    SELECT f.id as id, f.geom as geom, f.category as category, f.count_occ as count_full, f.percentile as percentile_full,
c.count_occ as count_closure, c.percentile as percentile_closure, c.count_occ - f.count_occ as count_diff,
c.percentile - f.percentile as perc_diff, 
(CASE WHEN f.count_occ > 0 THEN CAST(c.count_occ - f.count_occ AS DECIMAL)/f.count_occ ELSE NULL END) as count_perc_diff 
FROM greater_graz_lambda_7 f
INNER JOIN greater_graz_lambda_9 c
ON f.id = c.id
ORDER BY (CASE WHEN f.count_occ > 0 THEN (c.count_occ - f.count_occ)/f.count_occ ELSE NULL END) 
)


