import json
import requests
import wikipedia

query = '''SELECT ?event ?eventLabel ?date
WHERE
{
	# find events
	?event wdt:P31/wdt:P279* wd:Q1190554.
    ?languagelink schema:about ?event.
    ?languagelink schema:inLanguage "nl".
	# with a point in time or start date
	OPTIONAL { ?event wdt:P585 ?date. }
	OPTIONAL { ?event wdt:P580 ?date. }
	# not in the future, and not more than 31 days ago
	BIND(NOW() - ?date AS ?distance).
    #7700 dagen gelden tot 7750 dagen geleden
	FILTER(7700 <= ?distance && ?distance < 10000.)

}

LIMIT 100'''

wikidataSparqlUrl = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(wikidataSparqlUrl, params={'query': query, 'format': 'json'}).json()
wikiDataEntityUrl = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids='

result = [];

for i in data["results"]["bindings"]:
    id = i["event"]["value"].rsplit('/', 1)[-1]
    title = requests.get(wikiDataEntityUrl+id, params={'format': 'json'}).json()["entities"][id]["sitelinks"]["enwiki"]["title"]
    wikipedia.set_lang("nl")
    try:
        page = wikipedia.page(title)
    except:
        break
    page = page.content.encode("utf-8")
    lines = page.splitlines()
    parsedPage = []
    for line in lines:
        if(len(line) > 0 and line[0] != "="):
            parsedPage.append(line)
    result.append("\n".join(x for x in parsedPage))
print(result)
