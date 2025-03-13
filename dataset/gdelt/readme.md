# GDELT

Google BigQuery 
- Select all events where the USA is involved in the event, and the event date is between 2013 and 2024. The query returns the following columns: GLOBALEVENTID, event_date, EventRootCode, EventBaseCode, EventCode, QuadClass, Actor1Name, Actor1CountryCode, Actor1Type1Code, Actor2Name, Actor2CountryCode, Actor2Type1Code, ActionGeo_CountryCode, ActionGeo_Lat, ActionGeo_Long, GoldsteinScale, NumMentions, NumSources, NumArticles, AvgTone, IsRootEvent. The results are ordered by event_date in descending order.

```
SELECT
    GLOBALEVENTID,
    PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)) AS event_date,  -- Fixed date conversion
    EventRootCode,
    EventBaseCode,
    EventCode,
    QuadClass,
    Actor1Name,
    Actor1CountryCode,
    Actor1Type1Code,
    Actor2Name,
    Actor2CountryCode,
    Actor2Type1Code,
    ActionGeo_CountryCode,
    ActionGeo_Lat,
    ActionGeo_Long,
    GoldsteinScale,
    NumMentions,
    NumSources,
    NumArticles,
    AvgTone,
    IsRootEvent
FROM 
    `gdelt-bq.gdeltv2.events`
WHERE 
    (Actor1CountryCode = 'USA' OR Actor2CountryCode = 'USA' OR ActionGeo_CountryCode = 'USA')
    AND SQLDATE BETWEEN 20130101 AND 20241231  -- Filter for relevant time period
ORDER BY 
    event_date DESC;

```

Tableau Prep
Flow Steps
1. Replace type of event code, base event code and root event code to Number (Whole)
2. Left Join GDELT Events table and CAMEO_country
3. Left Join GDELT Events table and CAMEO_eventcodes 
4. Assigned geographic role to Actor 1 Country and Actor 2 Country 