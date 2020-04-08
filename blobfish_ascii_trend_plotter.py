import aplotter
import math

class AsciiTrendPlotter(object):

    def __init__(self):     
        print ("entered ctor")
    
    def plot(self):
         
        print("entered plot()")
        
        print('****** Sin([0,2pi]) ******')
        scale=0.1
        n=int(2*math.pi/scale)
        plotx=[scale*i for i in xrange(n)]
        ploty=[math.sin(scale*i) for i in xrange(n)]
        aplotter.plot(plotx,ploty)

        print('****** Some discrete data sequence ******')
        data=[ord(c) for c in 'ASCII Plotter example']
        aplotter.plot(data)

        #return asciiPlot

#DEBUG         
def main():
    print("entered main()")

    something = AsciiTrendPlotter()
    
    something.plot()
    
    
if __name__ == "__main__":
    main()
