import csv

def addLinkToCSV(fileLink, productLink):
    with open(fileLink,'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(productLink)
        
def csvToList(fileLink):
    file = open(fileLink)
    csvreader = csv.reader(file)
    header = next(csvreader)  
    rows = []
    for row in csvreader:
        rows.append(row)
    return rows