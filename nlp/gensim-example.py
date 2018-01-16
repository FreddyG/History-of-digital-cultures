import numpy as np
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from gensim import corpora, models, similarities


NLTK_DATA_PATH = '../venv/nltk_data'
RESOURCES = ['corpora/stopwords',
             'tokenizers/punkt']

documents = ["Het Openbaar Ministerie onderzoekt mogelijke fraude door de ex-directeur van vermogensbeheerder Box Consultants. Dat bevestigen het OM en het bedrijf zelf na berichtgeving van het Financieele Dagblad. Onder de klanten van Box zitten volgens het FD ook leden van het Koninklijk Huis. Het OM verdenkt de ex-directeur ervan dat hij jarenlang provisies, die hij ontving van beleggingsfondsen, niet aan klanten doorbetaalde. Hij wordt ook verdacht van valsheid in geschrifte om dit te verhullen. Volgens het FD gaat het om 8 miljoen euro, die Box en de ex-directeur in eigen zak hebben gestoken.",
			 "Sociaal was hij misschien niet de meest handige voorzitter van de Eurogroep. Soms bot, het hart vaak op de tong met stoere opmerkingen over vrouwen, drank en roken als een schoorsteen. Opmerkingen die niet altijd goed begrepen werden. Hij werd gehaat in Zuid-Europa, maar was de held van de Duitsers. De ultieme bewaker van de euro. Vandaag komt dan toch echt een einde aan Jeroen Dijsselbloem als aanvoerder van de Eurogroep. Een kleine bloemlezing van kwesties die hem (en Europa) vijf jaar lang bezighielden.",
			 "Huiseigenaren die na 14 juli 2016 te veel boeterente betaalden bij hun hypotheek, hebben een financiële meevaller. Ze hebben bij het oversluiten of vervroegd aflossen van de hypotheek te veel boeterente betaald en krijgen geld terug van de banken. Het gaat om circa 35.000 klanten en om gemiddeld 800 euro per hypotheek. Hypotheekmarktleider Rabobank heeft op last van de Autoriteit Financiële Markten (AFM) 52.000 hypotheekleningen opnieuw bekeken en 20.000 klanten blijken te veel betaald te hebben. ABN Amro compenseert 9000 klanten en bij ING gaat het om een paar duizend klanten. De tik op de vingers van de AFM kost de banken naar schatting tussen de 25 en 30 miljoen euro.",
			 "Het pensioenfonds van de ambtenaren, ABP, wil binnen een jaar alle belangen in tabak en kernwapens verkopen. Het fonds heeft voor 3,3 miljard euro aan belangen in bedrijven die zich daarmee bezighouden. Al jaren wordt er druk uitgeoefend op het pensioenfonds om de investeringen in tabak en kernwapens af te stoten. Het fonds zegt tot het inzicht te zijn gekomen dat er een duurzamer beleggingsbeleid moet worden gevoerd, na gesprekken met deelnemers, werkgevers en belangenorganisaties.",
			 "Maria Sjarapova is terug op de Australian Open. Twee jaar geleden leverde ze daar een positieve dopingtest af. Het kwam haar op een schorsing van vijftien maanden te staan, waardoor ze de editie van vorig jaar moest missen. Al die tijd bleef de Nederlandse coach Sven Groeneveld haar trouw. Groeneveld praat in de media nooit over de Russin. Dat is de afspraak die hij met haar maakte toen ze in 2013 met elkaar in zee gingen. Maar omdat het in Melbourne om een beladen toernooi gaat, sturen we hem toch maar weer een berichtje. Zijn pupil werd verguisd. Hoe heeft hij alle commotie rond haar schorsing beleefd?",
			 "Voetbalster Vanity Lewerissa heeft een punt gezet achter haar interlandcarrière. De 26-jarige aanvalster van PSV maakte afgelopen zomer deel uit van de Nederlandse selectie die de Europese titel won, maar kwam weinig aan spelen toe. De kans op een vaste basisplaats of meer speelminuten was voor mij onvoldoende om nog langer zo veel op te offeren, om alles te kunnen geven voor Oranje, aldus Lewerissa. Ze kwam elf keer uit voor Oranje en zat ook bij de selectie van het WK in 2015 in Canada.",
			 "Nederland is de regerend wereldkampioen zaalhockey maar degradeerde bij het vorige EK, in 2016, naar de Europese B-poule. Door die degradatie kan Nederland de wereldtitel op de volgende WK, volgende maand in Berlijn, niet verdedigen. Om weer te promoveren naar de hoogste Europese divisie moet Nederland in Alanya de finale in de B-poule halen.",
			 "Het kabinet moet onderzoeken of onveilige internet of things-apparaten geweerd kunnen worden van de markt. Daarvoor pleit de Cyber Security Raad, een adviesorgaan van het kabinet. In die raad zitten mensen uit het bedrijfsleven, de wetenschap en de overheid.",
			 "Doordat de lekken in de hardware van de computer zitten - en dus niet in de software, zoals vaker gebeurt - is het lastig oplossen. De enige échte oplossing is het maken en inbouwen van nieuwe chips. Op een gegeven moment zullen nieuwe apparaten dus veilig zijn voor dit probleem, maar dat duurt nog wel even. Vrijwel alle apparaten die nu nog in de winkel liggen zijn kwetsbaar voor een of beide lekken."]


             
def check_nltk_resources(path):
    for res in RESOURCES:
        try:
            nltk.data.find(res)
        except LookupError:
            nltk.download(res.split('/')[1], path)

check_nltk_resources(NLTK_DATA_PATH)
stopwords = nltk.corpus.stopwords.words('dutch')

def tokenize(text):
	# first tokenize by sentence, then by word to ensure that punctuation
        # is caught as it's own token
	tokens = [word.lower() for sent in nltk.sent_tokenize(text)
                               for word in nltk.word_tokenize(sent)]
	filtered_tokens = []
	# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	for token in tokens:
		if token in stopwords:
			continue
		if re.search('[a-zA-Z]', token):
			filtered_tokens.append(token)
	return filtered_tokens


def dump_keywords(topics):
    topic_keywords = []
    for topic in topics:
        topic_keywords1 = []
        for keyword in topic[1]:
            d={"keyword":keyword[0], "weight":keyword[1]}
            topic_keywords1.append(d)
        topic_keywords.append(topic_keywords1)

    import json
    with open('keywords.json', 'w') as f:
        json.dump(topic_keywords, f, ensure_ascii=False)


def dump_documents(corpus_lsi):
    documents = []
    for document in corpus_lsi:
        confidence = [score[1] for score in document]
        d={"name":"economy/10-12-1994", "confidence":confidence}
        documents.append(d)

    import json
    with open('clusters.json', 'w') as f:
        json.dump(documents, f, ensure_ascii=False)


if __name__ == "__main__":
    texts = [tokenize(document) for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)	# train model
    corpus_tfidf = tfidf[corpus]        # transform documents

    # initialize an LSI transformation
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
    # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    corpus_lsi = lsi[corpus_tfidf] 
    topics = lsi.show_topics(formatted=False)
    print(topics)

    # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
    for doc in corpus_lsi: 
        print(doc)

    dump_keywords(topics)
    dump_documents(corpus_lsi)
