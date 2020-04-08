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
    
    def getRandomPageTitle(object):
        
        #pageResult = wikipedia.page("Python")
        
        wikipediaPageTitle = wikipedia.random(1)
        
        return wikipediaPageTitle
    
    def getPage(object, pageTitle):
        
        #pageResult = wikipedia.page("Python")
        
        #wikipediaPageTitle = wikipedia.random(1)
        
        wikipediaPage = wikipedia.page(
                title = pageTitle, 
                pageid = None, 
                auto_suggest = True, 
                redirect = True, 
                preload = False
            )
        
        return wikipediaPage
        
    def getFirstPngImageUrl(object, wikipediaPage):
        
        #Debug
        #wikipediaPage = wikipedia.page("Python")
        
        for i in range(len(wikipediaPage.images)):
        
            if ".png" in wikipediaPage.images[i]:
                return wikipediaPage.images[i]

        #return null
                
def main():
    some_value = WikipediaWrapper(500)
    some_value.getSearchResult()
    
    print(some_value.publicField)

# python2 support (not really tested in python2, so probably nothing works)
if __name__ == "__main__":
    main()
 