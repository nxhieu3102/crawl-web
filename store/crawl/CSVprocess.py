import csv

def addLinkToCSV(fileLink, productLink):
    with open(fileLink,'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(productLink)
        
def csvToList(fileLink):
    file = open(fileLink)
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    return rows

def rewriteCSV(fileLink, productLink):
    with open(fileLink,'w',newline = '') as fd:
        writer = csv.writer(fd)
        for item in productLink:
            writer.writerow(item)

