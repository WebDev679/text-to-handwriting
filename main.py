from PIL import Image
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-t",
                "--text",
                required=True,
                help="path to input text to be converted")
args = vars(ap.parse_args())



BG = Image.open("myfont/bg.png")
sizeOfSheet = BG.width
heightOfSheet = BG.height
print(sizeOfSheet)
print(heightOfSheet)
gap, _ = 100, 100
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890\n'

def writeFile(char):
    global gap, _
    if char != '\n':
        cases = Image.open("myfont/%s.png" % char.lower())        
        BG.paste(cases, (gap, _))
        size = cases.width
        gap += size
    else:
        _ += 200
        gap = 100

def writeLetter(word):
    global gap, _
    if gap > sizeOfSheet - 70 * len(word):
        gap = 100
        _ += 200
    special_char = {'.':'fullstop','!':'exclamation','?':'question',',':'comma','(':'braketop', ')':'braketcl','-':'hiphen'}
    for letter in word:
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter == '\n':
                pass
            elif letter.isdigit():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter += 'upper'
            elif special_char[letter] != None:
                letter = special_char[letter]
           
            writeFile(letter)


def worddd(Input):
    wordlist = Input.split(' ')
    for i in wordlist:
        writeLetter(i)
        writeFile('space')


if __name__ == '__main__':
    try:
        with open(args["text"], 'r') as file:
            data = file.read().replace('\n', ' \n ')

        with open('final_output.pdf', 'w') as file:
            pass

        l = len(data)
        nn = len(data) // 600
        chunks, chunk_size = len(data), len(data) // (nn + 1)
        p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        print(p)
        num = 0
        for i in range(0, len(data.split(' '))):
            listOfWords = data.split(' ')
            if _ > heightOfSheet - 400 and gap > sizeOfSheet - 95 * (len(listOfWords[i])):
                BG.save('%doutt.png' % num)
                num += 1
                BG1 = Image.open("myfont/bg.png")
                BG = BG1
                gap = 100
                _ = 100
                print(num)
            worddd(listOfWords[i])
        BG.save('%doutt.png' % num)
            
    except ValueError as E:
        print("{}\nTry again".format(E))

imagelist = []
for i in range(0, num+1):
    imagelist.append('%doutt.png' % i)

#Converting images to pdf
#Source:https://datatofish.com/images-to-pdf-python/


def pdf_creation(PNG_FILE, flag=False):
    rgba = Image.open(PNG_FILE)
    print(rgba.size)
    rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
    rgb.paste(rgba, mask=rgba.split()[3])  # paste using alpha channel as mask
    rgb.save('final_output.pdf',
             append=flag)  #Now save multiple images in same pdf file


#First create a pdf file if not created
pdf_creation(imagelist.pop(0))

#Now I am opening each images and converting them to pdf
#Appending them to pdfs
for PNG_FILE in imagelist:
    pdf_creation(PNG_FILE, flag=True)
