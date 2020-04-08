import wikipedia


class WikipediaWrapper(object):
    '''Basic Window object draw a border for itself and can write 
    colored strings into itself'''
    publicField = 0;

    def __init__(self, fieldVal):
        # constructor
        self.publicField = fieldVal;
        
    def getSearchResult(object):
        # TODO: Convert all unicode to ASCII strings? as in:
        #            [x.encode('UTF8') for x in searchResult]
        
        searchResult = wikipedia.search("Bill")
        
        return searchResult
        
    def getFirstImageUrl(object):
        
        pageResult = wikipedia.page("Python")
        
        for i in range(len(pageResult.images)):
        
            if ".png" in pageResult.images[i]:
                return pageResult.images[i]

        #return null
                
def main():
    some_value = WikipediaWrapper(500)
    some_value.getSearchResult()
    
    print(some_value.publicField)

# python2 support (not really tested in python2, so probably nothing works)
if __name__ == "__main__":
    main()
 