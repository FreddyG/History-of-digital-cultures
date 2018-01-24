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

def get_events(events, distancefrom, distanceto):
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
    LIMIT 10 '''

    wikidata_sparql_url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    try:
        data = requests.get(wikidata_sparql_url, params={'query': query, 'format': 'json'}).json()
    except:
        data = ""
        pass

    wiki_data_entity_url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids='


    if data != "":
        for i in data["results"]["bindings"]:
            print("Doing result: " + str(i["event"]["value"]))
            id = i["event"]["value"].rsplit('/', 1)[-1]
            try:
                title = \
                    requests.get(wiki_data_entity_url + id, params={'format': 'json'}).json()["entities"][id]["sitelinks"][
                        "nlwiki"][
                        "title"]
                wikipedia.set_lang("nl")
            except:
                print("Could not find Dutch wiki")
                continue
            try:
                page = wikipedia.page(title)
            except:
                print("Cannot find wiki page")
                continue

            try:
                page = page.content.encode("utf-8")
            except:
                print("Page: " + wikipedia.page(title) + " has no content, continue")
                continue

            lines = page.splitlines()
            parsed_page = []
            for line in lines:
                if (len(line) > 0 and line[0] != "="):
                    parsed_page.append(line.decode("utf-8"))

            events.append((title, "\n".join(x for x in parsed_page),
                       i["date"]["value"].split('T', 1)[0]))
    return events


def convert_to_mysql(content):
    insert_list = []
    for elem in content:
        ps = "insert into wiki(wikipagename, content, date) VALUES ( \""
        ps = ps + elem[0] + "\", \""
        for st in elem[1].split(" "):
            ps = ps + re.sub('\"', '', st) + " "
        ps = ps.strip() + "\" , "
        ps = ps + "\"" + elem[2]
        ps = ps + "\");"
        insert_list.append(ps)

    return insert_list


def main():
    events = []

    get_events(events, 7700, 7800)  # between days
    get_events(events, 7800, 7900)  # between days
    get_events(events, 7900, 8000)  # between days
    get_events(events, 8000, 8100)  # between days
    get_events(events, 8100, 8200)  # between days
    get_events(events, 8200, 8300)  # between days
    get_events(events, 8300, 8400)  # between days
    get_events(events, 8400, 8500)  # between days
    get_events(events, 8500, 8600)  # between days
    get_events(events, 8600, 8700)  # between days
    get_events(events, 8700, 8800)  # between days
    get_events(events, 8800, 8900)  # between days
    get_events(events, 8900, 9000)  # between days
    get_events(events, 9000, 9100)  # between days
    get_events(events, 9100, 9200)  # between days


    print("Processed: " + str(len(events)) + " events")

    insert_list = convert_to_mysql(events) # get list of insert queries
    create_insert_into = open("insertwikidata.sql", "w")

    i = 1
    for wiki in insert_list:
        message = "Inserted wiki " + str(i)
        try:
            create_insert_into.write("%s" % wiki)
        except:
            toUTF = wiki.encode("utf-8")
            create_insert_into.write("%s" % toUTF)
        finally:
            i += 1
            print(message)
    create_insert_into.close()


if __name__ == "__main__":
    main()
