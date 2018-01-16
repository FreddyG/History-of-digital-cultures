import requests

query = '''SELECT ?event ?eventLabel ?date
WHERE
{
	# find events
	?event wdt:P31/wdt:P279* wd:Q1190554.
	# with a point in time or start date
	OPTIONAL { ?event wdt:P585 ?date. }
	OPTIONAL { ?event wdt:P580 ?date. }
	# not in the future, and not more than 31 days ago
	BIND(NOW() - ?date AS ?distance).
	FILTER(7700 <= ?distance && ?distance < 7750).
    #FILTER(lang(?label) = 'nl').
}

LIMIT 10'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()
print(data);
