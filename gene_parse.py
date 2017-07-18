import pyexcel as pyxl 
from bs4 import BeautifulSoup
import httplib2
import threading

class ParseAPI: 
    def __init__(self):
    	self.URL = "https://www.ncbi.nlm.nih.gov/nucest/"

    @staticmethod
    def _retrieve_from_url(url):
        print "Getting url: " + url 
        http = httplib2.Http()
	status, response = http.request(url)
	soup = BeautifulSoup(response, 'html.parser')
        gene_layer = soup.findAll("div", {"class": "portlet_title"})
	return gene_layer 
   
    def get_gene(self, gb_accnum):
        layer = self._retrieve_from_url(self.URL + gb_accnum)
        gene_code = "" 
	layer = [row.text.replace('\n','') for row in layer]
	for context in layer:
	    if 'ESTs' in context:
	        gene_code = context.replace("ESTs for the", '').replace(' gene', '') 	
                return gene_code
        return ""

def wrapper(start, end, sheet, meta):
    genes = [parser.get_gene(gb_accnum) for gb_accnum in sheet.column['GB ACCNUM'][start:end]]
    nval.append((meta, genes))

if __name__ == "__main__": 
    parser = ParseAPI()
    sheet = pyxl.get_sheet(file_name="GPCR set with plate scores.xlsx")
    sheet.name_columns_by_row(0)
    nval = []
    nval.append((0, sheet.column['Gene Name'][0:170]))
    threads = []
    threads.append(threading.Thread(target=wrapper, args=(171, 350, sheet, 1)))
    threads.append(threading.Thread(target=wrapper, args=(351, 500, sheet, 2)))
    threads.append(threading.Thread(target=wrapper, args=(501, 650, sheet, 3)))
    threads.append(threading.Thread(target=wrapper, args=(651, 949, sheet, 4)))
    
    for thread in threads: 
        thread.start()
    
    for thread in threads: 
        thread.join()
    
    nval.append((5, sheet.column['Gene Name'][950:-1]))
    q = [] 
    sorted(nval, key=lambda x: x[0])
    
    for i in nval:
        q += i[1]
      
    sheet.column['Gene Name'] = [x for x in q]
    sheet.save_as("GPCR set with plate scores - Updated.xlsx")

