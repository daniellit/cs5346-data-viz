Starting page for gdelt:
https://bigquery.cloud.google.com/table/gdelt-bq:full.events

https://www.gdeltproject.org/data/
data dictionary:
https://www.gdeltproject.org/data/documentation/ - 

list of columns:
Data Dictionaries: https://www.gdeltproject.org/data/lookups/ 

CAMEO event codes found here: https://gdeltproject.org/data/lookups/CAMEO.eventcodes.txt

SAMPLE QUERY - supposedly MySQL
https://www.gdeltproject.org/data/lookups/SQL.samplequeryexport.txt
#This shows an example command for doing a large-scale search of events matching specific criteria
select * 
from GDELT_DAILYUPDATES 
where SQLDATE > 20110000 and SQLDATE < 20110399 
and (Actor1CountryCode='EGY' or Actor2CountryCode='EGY' or ActionGeo_CountryCode='EG');
