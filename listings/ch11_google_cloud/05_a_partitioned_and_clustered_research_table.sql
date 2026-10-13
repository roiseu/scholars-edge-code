CREATE TABLE `your-project-id.research_data.flows`
PARTITION BY DATE(event_time)
CLUSTER BY label, protocol AS
SELECT *
FROM `your-project-id.research_data.flows_raw`;

-- Queries that filter on the partition column scan only the relevant days
SELECT label, COUNT(*) AS n
FROM `your-project-id.research_data.flows`
WHERE DATE(event_time) BETWEEN '2026-01-01' AND '2026-01-07'
GROUP BY label;
