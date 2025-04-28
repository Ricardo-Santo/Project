SELECT DM.trimestre, SUM(FC.preco_maximo)
FROM fact_cotacoes AS FC
INNER JOIN dim_tempo AS DM
ON FC.tempo_id = DM.tempo_id
GROUP BY DM.trimestre ORDER BY DM.trimestre ASC