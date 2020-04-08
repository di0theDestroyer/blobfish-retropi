import sys
import warnings
import requests
from io import BytesIO


from PIL import Image



# jacked from https://dev.to/anuragrana/generating-ascii-art-from-colored-image-using-python-4ace
# and from https://github.com/anuragrana/Python-Scripts/blob/master/image_to_ascii.py
# full PIL (pillow) documentation: https://pillow.readthedocs.io/en/stable/



class ImageToAscii(object):
    '''Basic Window object draw a border for itself and can write 
    colored strings into itself'''
    imageUrl = "";

    def __init__(self, imageUrl):
        # constructor
        self.imageUrl = imageUrl;
    
    def getImage(self):
    
        # pass the image as command line argument
        #image_path = sys.argv[1]
        #img = Image.open(image_path)
        
        response = requests.get(self.imageUrl)
        img = Image.open(BytesIO(response.content))

        # get rid of PIL warning -- 
        #   UserWarning: Palette images with Transparency expressed in 
        #                bytes should be converted to RGBA images
        #background = Image.new("RGB", img.size, (255, 255, 255))
        #background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        warnings.filterwarnings("ignore")

        # resize the image
        width, height = img.size
        aspect_ratio = height/width
        new_width = 30
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))
        # new size of image
        # print(img.size)

        # convert image to greyscale format
        # https://stackoverflow.com/questions/52307290/what-is-the-difference-between-images-in-p-and-l-mode-in-pil
        img = img.convert('L')

        pixels = img.getdata()

        # replace each pixel with a character from array
        chars = ["B","S","#","&","@","$","%","*","!",":","."]
        new_pixels = [chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)

        # split string of chars into multiple strings of length equal to new width and create a list
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        
        #DEBUG
        #print(ascii_image)
        
        return ascii_image

#DEBUG         
def main():
    some_value = ImageToAscii("https://upload.wikimedia.org/wikipedia/commons/1/10/Python_3._The_standard_type_hierarchy.png")

    print(some_value.imageUrl)

    asciiImage = some_value.getImage()
    
    print(asciiImage)
    
# python2 support (not really tested in python2, so probably nothing works)
if __name__ == "__main__":
    main()




# write to a text file.
#with open("ascii_image.txt", "w") as f:
#    f.write(ascii_image)