SELECT
  EXTRACT(YEAR FROM creation_date) AS year,
  COUNT(*) AS all_questions,
  COUNTIF(REGEXP_CONTAINS(tags, r'(^|\|)tensorflow(\||$)')) AS tensorflow,
  COUNTIF(REGEXP_CONTAINS(tags, r'(^|\|)pytorch(\||$)'))    AS pytorch,
  COUNTIF(REGEXP_CONTAINS(tags, r'(^|\|)scikit-learn(\||$)')) AS scikit_learn
FROM `bigquery-public-data.stackoverflow.posts_questions`
WHERE creation_date >= TIMESTAMP('2015-01-01')
GROUP BY year
ORDER BY year;
