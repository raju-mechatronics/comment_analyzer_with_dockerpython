from googletrans import Translator

translator = Translator()

def translate(text):
    trans = translator.translate(text, dest='en')
    if type(text) is list:
        return [t.text for t in trans]
    elif type(text) is str:
        return trans.text
    raise Exception("text must be list or str")

