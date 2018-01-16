import json
import requests
import wikipedia

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
    #7700 dagen gelden tot 7750 dagen geleden
	FILTER(7700 <= ?distance && ?distance < 7750).
    #FILTER(lang(?label) = 'nl').
}

LIMIT 10'''

wikidataSparqlUrl = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(wikidataSparqlUrl, params={'query': query, 'format': 'json'}).json()
wikiDataEntityUrl = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids='

for i in data["results"]["bindings"]:
    id = i["event"]["value"].rsplit('/', 1)[-1]
    title = requests.get(wikiDataEntityUrl+id, params={'format': 'json'}).json()["entities"][id]["sitelinks"]["enwiki"]["title"]
    page = wikipedia.page(title);
    print(page.summary)
