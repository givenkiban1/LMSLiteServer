

from deep_translator import GoogleTranslator

def translate(to, from_="auto", text="hello guys"):
    translated = GoogleTranslator(source=from_, target=to).translate(text)

    return translated
