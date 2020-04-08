import curses
from curses import COLOR_WHITE,COLOR_GREEN,COLOR_RED, COLOR_CYAN,COLOR_BLACK, COLOR_MAGENTA

from blobfish_terminal_ui_panes import Window, StringWindow, EditorWindow, MenuWindow, MenuTuple
from blobfish_wikipedia_wrapper import WikipediaWrapper
from blobfish_image_to_ascii import ImageToAscii
#from blobfish_gnuplot_wrapper import GnuPlotWrapper


from itertools import cycle

from random import randint

from time import time, sleep



# most of the curses bootstrapper jacked from https://github.com/Permafacture/terminal_windows
# Note -- only tested with python 2.7
# To Install:
#       NOTE: ONLY TESTED IN Powershell v5.1.18362.628 / Windows 10 / Python 2.7
#       <INSTALL PYTHON 2.7 or above>
#       <OPEN POWERSHELL>
#       Install Dependency
#           py -2 -m pip install windows_curses
#       Run that sh**
#           py -2 blobfish-terminal-ui.py



#can't rely on curses to find tab, enter, etc.
KEY_TAB = 9

#name some colors (foreground/background pairs)
#actually defined later through curses.init_pair
BASIC = 0  #not editable
TITLE_ACTIVE = 1
TITLE_INACTIVE = 2
MENU_MESSAGE = 3

class BlobfishTerminalUi(StringWindow):
    '''String Window that just spews out some words at random times'''

    def __init__(self,*args,**kwargs):

        super(BlobfishTerminalUi,self).__init__(*args,**kwargs)
        self.next_time = time() + randint(1,4)
        self.things_to_say = self.output_window_text_gen()
        
        self.currentWikipediaPage = self.wikipedia_text_gen()

    def wikipedia_text_gen(self):
    
        wikipedia_wrapper = WikipediaWrapper(500)     
        #intro = wikipedia_wrapper.getSearchResult() #works
        
        wikipediaPageAttributes = [""]

        #get images
        
        # get random wikipedia page
        pageTitle = wikipedia_wrapper.getRandomPageTitle()
        page = wikipedia_wrapper.getPage(pageTitle)
        pageSummary = page.summary
        
        
        # drop all unicode characters 
        # works around "UnicodeEncodeError" from python
        pageTitle = pageTitle.encode('ascii', 'ignore').decode('ascii')
        pageSummary = pageSummary.encode('ascii', 'ignore').decode('ascii')
        
        
        wikipediaPageAttributes.append("***pageTitle*** --> " + pageTitle)
        wikipediaPageAttributes.append("***pageUrl*** --> " + page.url)
        wikipediaPageAttributes.append("***pageSummary*** --> " + pageSummary)
        wikipediaPageAttributes.append("***firstPngImageUrl*** --> " + wikipedia_wrapper.getFirstPngImageUrl(page))
        
        #image to Ascii!!!
        imageToAscii = ImageToAscii("https://upload.wikimedia.org/wikipedia/commons/1/10/Python_3._The_standard_type_hierarchy.png")
        asciiImage = imageToAscii.getImage()
        wikipediaPageAttributes.append("***asciiImageRender*** -->")
        
        #need the actual image appended row by row to keep design
        asciiImageRows = asciiImage.split('\n')
        for imageRow in asciiImageRows:
            wikipediaPageAttributes.append(imageRow)
        
        for s in wikipediaPageAttributes:
            yield s

    def output_window_text_gen(self):
    
        intro = [
            "Press TAB to switch between windows", 
            "something else"
        ]

        annoying = cycle(["this is the song that never ends","It goes on and on my FRIEND!",
                            "Some people started singing it not knowing what it was.",
                            "and then they kept on singing it for-ever just because..."])

        for s in intro:
          yield s
          
        for s in annoying:
          yield s

    def update(self):
    
        now = time()
    
        if now > self.next_time:
          self.next_time = now+randint(1,2)
          #self.add_str(self.things_to_say.next(),palette=BASIC)
          
          #TRY STREAMING WIKIPEDIA DATA, None is default value if iterator !hasNext
          nextOutputLine = next(self.currentWikipediaPage, None)         
          
          #might be end of iterator
          if nextOutputLine is None:
            self.currentWikipediaPage = self.wikipedia_text_gen()
            nextOutputLine = next(self.currentWikipediaPage, None)
          
          #WIKIPEDIA
          self.add_str(nextOutputLine,palette=BASIC)
        
        super(BlobfishTerminalUi,self).update()
 
def run():

    #Manual tiling
    maxy,maxx = stdscr.getmaxyx()
    splity = int(maxy*.8)
    splitx = int(maxx*.8)

    #initialize windows
    #specify Upper left corner, size, title, color scheme and border/no-border
    main_border = Window((0,0),(maxx, maxy),"Main Window",TITLE_INACTIVE)
    display_output = BlobfishTerminalUi((1,1),(splitx-1,splity-1),"Main Output Pane",TITLE_INACTIVE)
    menu_window = MenuWindow((splitx,1),((maxx-splitx-1),maxy-2),"Menu Pane",TITLE_INACTIVE)
    editor_window = EditorWindow((1,splity),(splitx-1,maxy-splity-1), "Command Pane", palette=TITLE_INACTIVE,
                             callback=display_output.add_str)

    #Set menu options with corrisponding callbacks
    menu_actions = [MenuTuple("Dummy text add",(display_output.add_str,"-------THIS TEXT CAME FROM THE MENU------", MENU_MESSAGE)),
                    MenuTuple("SKIN - Cyan",(curses.init_pair,TITLE_INACTIVE,COLOR_CYAN,COLOR_BLACK)),
                    MenuTuple("SKIN - Green",(curses.init_pair,TITLE_INACTIVE,COLOR_GREEN,COLOR_BLACK)),
                    MenuTuple("SKIN - Default",(curses.init_pair,TITLE_INACTIVE,COLOR_WHITE,COLOR_BLACK)),
                    MenuTuple("QUIT",(display_output.quit,TITLE_INACTIVE,COLOR_WHITE,COLOR_BLACK)),
                    ]
    menu_window.set_menu(menu_actions)

    #Put all the windows in a list so they can be updated together
    windows = [main_border, display_output, menu_window, editor_window]

    #create input window cycling
    # an input window must have a process_key(key) method
    input_windows = cycle([menu_window,editor_window])
    active_window = input_windows.next()
    active_window.draw_border(TITLE_ACTIVE)

    #Main Program loop.
    while True:
      
      #asynchronously try to get the key the user pressed
      key = stdscr.getch()
      
      if key == curses.ERR:
          #no key was pressed.  Do house-keeping
          dirtied = 0
          for win in windows:
            dirtied += win.dirty
            win.update()
          #if dirtied:
          stdscr.refresh()
          sleep(.1) #don't be burnin up the CPU, yo.
      elif key == KEY_TAB:
          #cycle input window
          active_window.draw_border() #uses window default
          active_window = input_windows.next()
          active_window.draw_border(TITLE_ACTIVE)
      else:
        #every other key gets processed by the active input window
        active_window.process_key(key)

#Set up screen.  Try/except to make sure the terminal gets put back
#  together no matter what happens
try:
  
  #https://docs.python.org/2/howto/curses.html
  stdscr = curses.initscr()
  curses.start_color()
  curses.noecho()  #let input windows handle drawing characters to the screen
  curses.cbreak()  #enable key press asynch
  stdscr.nodelay(1)  #enable immediate time out (don't wait for keys at all)
  stdscr.keypad(1)  #enable enter, tab, and other keys

  #Set initial palette
  curses.init_pair(TITLE_ACTIVE, COLOR_RED, COLOR_BLACK)
  curses.init_pair(TITLE_INACTIVE, COLOR_WHITE, COLOR_BLACK)
  curses.init_pair(MENU_MESSAGE, COLOR_MAGENTA, COLOR_BLACK)

  #run while wrapped in this try/except
  run()

except Exception:
  
  #put the terminal back in it's normal mode before raising the error
  curses.nocbreak(); stdscr.keypad(0); curses.echo();curses.endwin()
  
  raise

finally:
  
  curses.nocbreak(); stdscr.keypad(0); curses.echo();curses.endwin()
  
  #exit message
  print("")
  print(" ---------------------------")
  print("|                           |")
  print("|    Just Blob with it.     |")
  print("|                           |")
  print("|  #TeamBlobfish #RetroPI   |")
  print("|                           |")
  print(" ---------------------------")
  print("")
  
  #DEBUG
  #print "\nThis terminal can%s display color\n" % ["'t",""][curses.has_colors()]
