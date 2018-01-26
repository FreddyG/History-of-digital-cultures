import re

import requests
import wikipedia


#########################################################
#                                                       #
# The Wikidata parser will extract data between a       #
# specified time. It will then convert the data for     #
# inserting in a SQL file for importing in Mysql.       #
# Please note that (if entities should be extracted     #
# also, a placeholder of this code has been placed in   #
# the beginning.                                        #
# Authors: Freddy de Greef & Kjell Zijlemaker           #
#                                                       #
#########################################################

# getting entities from wikidata should we use NER
#
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

# get the events from a specific time range
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
        
        #... days ago till ... days ago
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
                    requests.get(wiki_data_entity_url + id, params={'format': 'json'}).json()["entities"][id][
                        "sitelinks"][
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


# convert all content to insert in table
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

    # past events range from 8600 days ago (juli 1994)
    get_events(events, 7650, 7750)
    get_events(events, 7750, 7850)
    get_events(events, 7850, 7950)
    get_events(events, 7950, 8050)
    get_events(events, 8050, 8150)
    get_events(events, 8150, 8250)
    get_events(events, 8250, 8350)
    get_events(events, 8350, 8450)
    get_events(events, 8450, 8550)
    get_events(events, 8560, 8650)

    # recent events range from 0 - ... days ago
    get_events(events, 0, 100)  # between days
    get_events(events, 100, 200)  # between days
    get_events(events, 200, 300)  # between days
    get_events(events, 300, 400)  # between days
    get_events(events, 400, 500)  # between days
    get_events(events, 500, 600)  # between days
    get_events(events, 600, 700)  # between days
    get_events(events, 700, 800)  # between days
    get_events(events, 800, 900)  # between days
    get_events(events, 900, 1000)  # between days

    print("Processed: " + str(len(events)) + " events")

    insert_list = convert_to_mysql(events)  # get list of insert queries

    # write data to sql file
    create_insert_into = open("insertwikidata.sql", "w")
    write_to_file(create_insert_into, insert_list)
    create_insert_into.close()

# write the results to file
def write_to_file(create_insert_into, insert_list):
    i = 1
    for wiki in insert_list:
        message = "Inserted wiki " + str(i)
        try:
            create_insert_into.write("%s" % wiki)
        except:
            to_u_t_f = wiki.encode("utf-8")  # if str char does not have proper encoding, encode to utf,
            #  check insert statements before inserting
        finally:
            create_insert_into.write("%s" % to_u_t_f)
            i += 1
            print(message)


if __name__ == "__main__":
    main()
