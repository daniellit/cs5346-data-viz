Starting page for gdelt:
https://bigquery.cloud.google.com/table/gdelt-bq:full.events

https://www.gdeltproject.org/data/
data dictionary:
https://www.gdeltproject.org/data/documentation/ - 

list of columns:
Data Dictionaries: https://www.gdeltproject.org/data/lookups/ 

CAMEO event codes found here: https://gdeltproject.org/data/lookups/CAMEO.eventcodes.txt
to find the EVENTROOTCODES

SAMPLE QUERY - supposedly MySQL
https://www.gdeltproject.org/data/lookups/SQL.samplequeryexport.txt
#This shows an example command for doing a large-scale search of events matching specific criteria
select * 
from GDELT_DAILYUPDATES 
where SQLDATE > 20110000 and SQLDATE < 20110399 
and (Actor1CountryCode='EGY' or Actor2CountryCode='EGY' or ActionGeo_CountryCode='EG');


Just be aware of a need to 'normalize' the event count https://www.gdeltproject.org/data.html#documentation
The comma-delimited (CSV) files below are updated daily and record the total number of events in the GDELT 1.0 Event Database across all event types broken down by time and country. This is important for normalization tasks, to compensate the exponential increase in the availability of global news material over time. Due to GDELT 2.0's live updating, we do not currently make normalization files available for GDELT 2.0, but you can easily construct your own normalization files by performing a basic summation over the 15 minute update files.
--normalize is like
--this compares the total events to the specified events
select MonthYear, count(*) c, count(IF(ActionGeo_CountryCode='UP',1,null)) c_up
from [full.events]
group by MonthYear order by MonthYear



testing queries:
the results could be leading, at the same time or lagging, still useful otherwise

-- overall tone of the news article whic may include different topics and events
SELECT DATE(PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(DATE AS STRING))) AS DateOnly, AVG(SAFE_CAST(SPLIT(V2Tone, ',')[OFFSET(0)] AS FLOAT64)) AS AvgTone
FROM `gdelt-bq.gdeltv2.gkg`
WHERE Themes LIKE '%ECON_%' OR Themes LIKE '%FINANCE%' or themes LIKE '%ECONOMY%' OR themes LIKE '%STOCKMARKET%'
GROUP BY DateOnly
ORDER BY DateOnly
LIMIT 100;

OUTPUT: tone is -100 to +100, rising tone +ve economic news
Row	
DateOnly
AvgTone
1	
2015-02-17
-1.1624059580532913
2	
2015-02-18
-1.003775088759409
3	
2015-02-19
-0.98245575470834667
4	
2015-02-20
-1.0496685920616557
5	
2015-02-21
-1.2642401598849791
6	
2015-02-22
-1.0496393182673383
7	
2015-02-23
-0.905048139171

--event related to financials/stock - volatility
SELECT SQLDATE,COUNT(*) AS EventCount
FROM `gdelt-bq.full.events`
WHERE EventCode LIKE '17%' OR EventCode LIKE '18%' OR EventCode LIKE '19%'
AND (Actor1Name LIKE '%market%' OR Actor2Name LIKE '%market%' OR Actor1Name LIKE '%financial%' OR Actor2Name LIKE '%financial%' OR Actor1Name LIKE '%stock%' OR Actor2Name LIKE '%stock%')
GROUP BY SQLDATE
ORDER BY SQLDATE
LIMIT 100;


--economic and geopolitical events in the USA, might need to normalize to know if significant or not (compared to total events that day)
--the can select economic OR geopolitical separately.

SELECT 
    SQLDATE, 
    COUNT(*) AS NumEvents, 
    AVG(GoldsteinScale) AS AvgGoldsteinScore, 
    SUM(NumMentions) AS TotalMentions
FROM `gdelt-bq.full.events`
WHERE 1=1
    and EventCode IN ('043', '044', '045', '061', '062', '063') -- Economic events
    --and EventCode IN ('020', '021', '022', '023', '024', '040', '041', '042') -- Geopolitical events
    AND (Actor1CountryCode = 'USA' OR Actor2CountryCode = 'USA') -- Filter for USA
    AND SQLDATE BETWEEN 20230101 AND 20231231 -- Specify your date range
GROUP BY SQLDATE -- Group by date and event type
ORDER BY SQLDATE DESC
limit 100;


--can be improved here
--probably can be improved to use eventrootcodes economic and geopolitical
--    "Economic": [
        "02",  # APPEAL (for economic cooperation, aid, or sanctions relief)
        "03",  # EXPRESS INTENT TO COOPERATE (economic agreements, investment)
        "05",  # ENGAGE IN DIPLOMATIC COOPERATION (includes economic agreements)
        "07",  # PROVIDE AID (economic, humanitarian, and military aid)
        "08"   # YIELD (easing sanctions, debt forgiveness, policy changes)
    ],

--    "Geopolitical": [
        "04",  # CONSULT (high-level diplomatic talks, negotiations)
        "05",  # ENGAGE IN DIPLOMATIC COOPERATION (bilateral/multilateral agreements, alliances)
        "06",  # ENGAGE IN MATERIAL COOPERATION (joint military/economic cooperation)
        "08",  # YIELD (concessions in political or territorial disputes)
        "09",  # INVESTIGATE (spying, political inquiries)
        "10",  # DEMAND (economic or geopolitical pressures)
        "11",  # DISAPPROVE (diplomatic warnings, sanction threats)
        "12",  # REJECT (refusal to cooperate, exit agreements)
        "13",  # THREATEN (geopolitical coercion, war threats)
        "14",  # PROTEST (economic or political protests)
        "15",  # EXHIBIT FORCE POSTURE (military positioning)
        "16",  # REDUCE RELATIONS (diplomatic breakdowns)
        "17",  # COERCE (economic or military coercion)
        "18",  # ASSAULT (conflicts, military strikes)
        "19",  # FIGHT (wars, territorial disputes)
        "20"   # USE UNCONVENTIONAL MASS VIOLENCE (terrorism, coups)
    ]

Quadclass + ActionGeo_type (country level) + country = USA, eventrootcode. note: i tried without the US country filter and actiongeo_type and had 20mio rows...
--to improve, can consider giving up daily data and move to weekly or monthly even if we want more granular fields like eventcode, or just to filter only for some event codes...
SELECT 
    PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)) AS event_date,
    quadclass,  -- QuadClass: 1=Verbal Cooperation, 2=Material Cooperation, 3=Verbal Conflict, 4=Material Conflict
    actiongeo_countrycode,
    Eventrootcode,
    COUNT(*) AS event_count,
    SUM(NumMentions) AS TotalMentions,
    sum(numsources) as Sources,
    AVG(AvgTone) as AVGTONE,
    sum(AvgTone*NumSources) as sum_tone_source,
    sum(AvgTone*NumMentions) as sum_tone_mentions,
    AVG(goldsteinscale) AS avg_goldstein,  -- Average event impact for the group
    SUM(AvgTone * NumMentions) / SUM(NumMentions) AS MentionsWeightedAvgTone,
    SUM(AvgTone * NumSources) / SUM(NumSources) as SourcesWeightedAvgTone,
    SUM(AvgTone * NumMentions * NumSources) / SUM(NumMentions * NumSources) as MenSouWeightedAvgTone,
    SUM(GoldsteinScale * NumMentions) / SUM(NumMentions) AS MentionsWeightedAvgGoldsteinScore
    SUM(GoldsteinScale * NumSources) / SUM(NumSources) AS SourcesWeightedAvgGoldsteinScore
    SUM(GoldsteinScale * NumSources) AS sum_GoldsteinScore_Sources
    
FROM gdelt-bq.gdeltv2.events
WHERE 1=1
and actiongeo_countrycode = 'US'  -- Filter for USA events
and isrootevent = 1
and actiongeo_type = 1 --1 country, 2 state, 3 city, 4 neighborhood (rare)
  AND PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING))
      BETWEEN DATE('2013-01-01') AND DATE('2024-12-31')
GROUP BY event_date, quadclass, eventrootcode, actiongeo_countrycode
ORDER BY event_date DESC, quadclass, eventrootcode, actiongeo_countrycode
--LIMIT 100


other things i want to add
more correlations - vs avg, vs weight by src, weight by mentions, weight by src*mentions?
heatmap of correlations above across different windows 30,60,90
check correlation of lead/lag also across wnidows










