# script to automatically generate html from bibtex entries, will remove old html
# requires pybtex, pybtex-apa-style

import pybtex.database.input.bibtex
import pybtex.plugin
import codecs
import latexcodec
import fileinput
import re
import time
from pybtex.plugin import find_plugin
from pybtex.database import parse_string

selected_publications = ['bond2020gradient', 'ramaswamy2019learning', 'nguyen2020unsupervised', 'bondtaylor2021deep']

APA = find_plugin('pybtex.style.formatting', 'apa')()
HTML = find_plugin('pybtex.backends', 'html')()

def filter_by(bibliography, words):
    out = []
    bibliography = parse_string(bibliography.to_string('bibtex'), 'bibtex')
    for entry,key in zip(bibliography.entries.values(), bibliography.entries.keys()):
        if entry.fields.__dict__['_dict']['keywords'] in words:
            out.append(key)
    return out

def bib2html(bibliography, keys=None, spacing=True):
    formattedBib = APA.format_bibliography(bibliography)
    if keys is not None:
        formattedBib.entries = [item for item in formattedBib.entries if item.key in keys]
        # ensure order is same
        tmp = []
        for item in keys:
            for entry in formattedBib.entries:
                if item == entry.key:
                    tmp.append(entry)
        formattedBib.entries = tmp
    output = '<ul>'
    for entry in formattedBib:
        if spacing:
            output += '<li class="x">'+entry.text.render(HTML)+'</li>'
        else:
            output += '<li>'+entry.text.render(HTML)+'</li>'
            
    return output+'</ul>'

parser = pybtex.database.input.bibtex.Parser()
with codecs.open("cgw.bib", encoding="latex") as stream:
    data = parser.parse_stream(stream)
html = bib2html(data, selected_publications, spacing=False)

# 1) add selected publications to index.html
loc = '<!--GENERATED-PUBLICATIONS-->'
end = '<!--END-GENERATED-->'
with open('../index.html') as f:
    text=f.read()
    p1=text.find(loc)
    p2=text.find(end)
# toggle this line to clear
# newText = text.replace(text[p1:p2], loc+'\n') 
newText = text.replace(text[p1:p2], loc+'\n'+html+'\n') 
with open('../index.html', "w") as f:
    f.write(newText)

# 2) 
html = bib2html(data, keys=filter_by(data, words=['Journal']))
loc = '<!--GENERATED-JOURNALS-->'
end = '<!--END-JOURNALS-->'
with open('../publications.html') as f:
    text=f.read()
    p1=text.find(loc)
    p2=text.find(end)
# toggle this line to clear
# newText = text.replace(text[p1:p2], loc+'\n') 
newText = text.replace(text[p1:p2], loc+'\n'+html+'\n') 
with open('../publications.html', "w") as f:
    f.write(newText)

time.sleep(0.5)

html = bib2html(data, keys=filter_by(data, words=['Conference']))
loc = '<!--GENERATED-CONFERENCE-->'
end = '<!--END-CONFERENCE-->'
with open('../publications.html') as f:
    text=f.read()
    p1=text.find(loc)
    p2=text.find(end)
# toggle this line to clear
# newText = text.replace(text[p1:p2], loc+'\n') 
newText = text.replace(text[p1:p2], loc+'\n'+html+'\n') 
with open('../publications.html', "w") as f:
    f.write(newText)

time.sleep(0.5)

html = bib2html(data, keys=filter_by(data, words=['Preprint']))
loc = '<!--GENERATED-REVIEW-->'
end = '<!--END-REVIEW-->'
with open('../publications.html') as f:
    text=f.read()
    p1=text.find(loc)
    p2=text.find(end)
# toggle this line to clear
# newText = text.replace(text[p1:p2], loc+'\n') 
newText = text.replace(text[p1:p2], loc+'\n'+html+'\n') 
with open('../publications.html', "w") as f:
    f.write(newText)
