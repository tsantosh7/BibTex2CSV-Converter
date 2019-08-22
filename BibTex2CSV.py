from pybtex.database.input import bibtex
import pandas as pd


from dateutil import parser

colNames = ['Authors','Title','Abstract','Journal','Pub Year','Pub Month','Volume','Number','Starting Page','Last Page','DOI']

#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file('Tirunagari_Santosh.bib')

#loop through the individual references
for bib_id in bibdata.entries:
    b = bibdata.entries[bib_id].fields
    try:
        title = b['title'].replace('{','').replace('}','')
    except:
        title = ''

    try:
        doi = b['doi']
    except:
        doi = ''

    try:
        year = b['year']
    except:
        year = ''

    try:
        dt = parser.parse(b['timestamp'])
        month = dt.month
    except:
        month = ''


    try:
        journal = b['journal'].replace('{','').replace('}','')
    except:
        try:
            journal = b['booktitle'].replace('{','').replace('}','')
        except:
            journal = ''

    try:
        pages = b['pages'].split('--')
        start_page = pages[0]
        last_page = pages[1]
    except:
        start_page = ''
        last_page = ''

    try:
        volume = b['volume']
    except:
        volume = ''

    try:
        number = b['number']
    except:
        number = ''

    authors = ''
    #deal with multiple authors
    try:
        for person in bibdata.entries[bib_id].persons["author"]:
            authors = authors + person.first_names[0] + ' ' + person.last_names[0][0] + ', '
        authors = authors[:-2]
    except:
        continue

    abstract = ''

    colNames = ['Authors', 'Title', 'Abstract', 'Journal', 'Pub Year', 'Pub Month', 'Volume', 'Number', 'Starting Page',
                'Last Page', 'DOI']
    bib_info = [authors, title, abstract, journal, year, month, volume, number, start_page, last_page, doi]
    bib_data = pd.DataFrame(columns=colNames)

    bib_dict = dict(zip(colNames, bib_info))
    bib_CSV = bib_data.append(bib_dict, ignore_index=True)

    bib_CSV.to_csv('./' + 'bib2csv.csv', encoding='utf-8', index=False, mode='a', header=False)

    del bib_data  # Very important to delete or it will consume the memory

