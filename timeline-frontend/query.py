import re

import requests
import wikipedia


# getting entities from wikidata should we use NER
# def get_entities(keyword):
#     query = '''SELECT DISTINCT ?s
#     WHERE {
#      ?s ?label "''' + keyword + '''"@nl . ?s ?p ?o
#      }
#         LIMIT 5'''
#
#     wikidataSparqlUrl = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
#     data = requests.get(wikidataSparqlUrl, params={'query': query, 'format': 'json'}).json()
#     wikiDataEntityUrl = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids='
#
#     result = []
#
#     print(data)
#
#     for i in data["results"]["bindings"]:
#         id = i["s"]["value"].rsplit('/', 1)[-1]
#
#         print(id)

def get_events(distancefrom, distanceto):
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
        FILTER(''' + str(distancefrom) + ''' <= ?distance && ?distance < ''' + str(distanceto) + '''.)
    
    }
    
    LIMIT 4'''

    wikidata_sparql_url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(wikidata_sparql_url, params={'query': query, 'format': 'json'}).json()
    wiki_data_entity_url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids='

    result = []

    for i in data["results"]["bindings"]:
        id = i["event"]["value"].rsplit('/', 1)[-1]
        title = \
            requests.get(wiki_data_entity_url + id, params={'format': 'json'}).json()["entities"][id]["sitelinks"][
                "enwiki"][
                "title"]
        wikipedia.set_lang("nl")
        try:
            page = wikipedia.page(title)
        except:
            break
        page = page.content.encode("utf-8")
        lines = page.splitlines()
        parsed_page = []
        for line in lines:
            if (len(line) > 0 and line[0] != "="):
                parsed_page.append(line.decode("utf-8"))

        result.append((title, "\n".join(x for x in parsed_page),
                       i["date"]["value"].split('T', 1)[0]))
    return result


def convert_to_mysql(content):
    insert_list = []
    for elem in content:
        ps = "insert into wiki(wikipagename, content, date) VALUES ( \""
        ps = ps + elem[0] + "\", \""
        for st in elem[1].split(" "):
            ps = ps + re.sub('[^A-Za-z0-9]+', '', st) + " "
        ps = ps.strip() + "\" , "
        ps = ps + "\"" + elem[2]
        ps = ps + "\");"
        print(ps)
        insert_list.append(ps)

    return insert_list


def main():
    events = get_events(7750, 10000)  # between days
    insert_list = convert_to_mysql(events) # get list of insert queries

    create_insert_into = open("insertwikidata.sql", "w")
    for wiki in insert_list:
        create_insert_into.write("%s" % wiki)
    create_insert_into.close()


if __name__ == "__main__":
    main()
