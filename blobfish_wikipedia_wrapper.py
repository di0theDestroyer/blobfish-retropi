import wikipedia


class WikipediaWrapper(object):
    '''Basic Window object draw a border for itself and can write 
    colored strings into itself'''
    publicField = 0;

    def __init__(self, fieldVal):
        # constructor
        self.publicField = fieldVal;
        
    def getSearchResult(object):
        print(wikipedia.search("Bill"))
                
def main():
    some_value = WikipediaWrapper(500)
    some_value.getSearchResult()
    
    print(some_value.publicField)

# python2 support (not really tested in python2, so probably nothing works)
if __name__ == "__main__":
    main()
 