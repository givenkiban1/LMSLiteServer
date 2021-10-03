import wikipedia

def search(query):
    img = image(query)
    print(img)
    return img, wikipedia.summary("Newton's first law")

def image(query):
    wikipage = wikipedia.page(query)
    return wikipage.images[0]


