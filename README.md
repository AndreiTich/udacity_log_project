# Log Report Generator

Hello and welcome to the log report generator! This is a small project for the udacity fullstack nanodegree. I tried to make it as flexible for future modification as possible, which is my my python functions include arguments, and the SQL views contain more data than necessary.

## Setting up your views

Please create the following views in the news database to make sure your the log report generator works properly!

### Required views

Top Articles
```
CREATE VIEW top_articles AS SELECT articles.title, COUNT(*) as num FROM articles, log
WHERE log.path = (CONCAT('/article/',articles.slug)) 
GROUP BY articles.title
ORDER BY num DESC;
```
Article-Author relationship
```
CREATE VIEW article_authors AS SELECT articles.title, authors.name FROM authors, articles
WHERE articles.author = authors.id
GROUP BY authors.id, articles.title;
```
Log status percentages grouped by day
```
CREATE VIEW log_percentage_status_by_day AS SELECT date_trunc('day', time) AS day, status, 
COUNT(*) / CAST( SUM(COUNT(*)) OVER (PARTITION BY date_trunc('day', time)) AS float) AS percent
FROM log 
GROUP BY day, status;
```

### Optional views
You can also add this view which lets you see the sum of the request statuses grouped by day and status type. This is not required but may be usedful in future anaysis of this data.
```
CREATE VIEW log_status_sums_by_day AS SELECT date_trunc('day', time) AS day, status, COUNT(*) AS num 
FROM log 
GROUP BY day, status;
```

## Run the generator!

That should be it. The generator will create text files wherever it is run. The files are timestamped and so is the filename so they do not overwrite each other.
