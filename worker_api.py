import proconex

class Producer(proconex.Producer): 
    def __init__(self, target=None):
        super(Producer, self).__init__()
	self.target = target
    
    def produce_from_excel(self, target): 
        self.target = target
    
    def items(self):
        print "Yielding Items"
        for lineNumber, line in enumerate(self.target, 1):
	    yield (lineNumber, line)


class Consumer(proconex.Consumer):
    def __init__(self, func):
        super(Consumer, self).__init__()
	self.func = func
        print "Initializing Consumer with Function {}".format(self.func)
    
    def consume(self, item):
        print "Consuming Items" 
        self.func(item)

class Worker: 
    def __init__(self, target, consumes): 
        self.target = target 
	self.consumes = consumes
    
    def __call__(self, fn, *args, **kwargs): 
        
	def produce_and_consume():
	    producer = Producer(self.target) 
	    consumers = [Consumer(fn) for consumerId in xrange(self.consumes)]
	    
	    with proconex.Worker(producer, consumers) as worker: 
	        worker.work()
            
	return produce_and_consume 

