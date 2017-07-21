import pyexcel as pyxl 
from bs4 import BeautifulSoup
import httplib2
import Queue
from worker_api import Worker 

class ParseAPI: 
    def __init__(self, target, consumes=5):
    	self.URL = "https://www.ncbi.nlm.nih.gov/nucest/"
	self.target = target
	self.consumes = consumes
	self.queue = Queue.PriorityQueue(len(self.target))

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
    
    def wrapper(self, *args):

        @Worker(target=self.target, consumes=self.consumes)
	def work(*args):
            target = args[0]
            gene = parser.get_gene(target[1])
            self.queue.put((target[0], gene))
       
        work()

    def flatten(self):
        return [self.queue.get()[1] for x in xrange(self.queue.qsize())] 


if __name__ == "__main__": 
    sheet = pyxl.get_sheet(file_name="GPCR set with plate scores.xlsx")
    sheet.name_columns_by_row(0)
    parser = ParseAPI(target=sheet.column['GB ACCNUM'])
    parser.wrapper() 
    genes = parser.flatten() 
    sheet.column['Gene Name'] = [x for x in genes]
    sheet.save_as("GPCR set with plate scores - Updated.xlsx")

