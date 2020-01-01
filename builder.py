import subprocess as sp
from languages import languages


def build(filename, filepath, lang):
    data = languages[lang]
    print(data['compilation'].replace('$file', filename).split())
    sp.call(data['compilation'].replace('$file', filename).split())
    return data['running'].replace('$file', filename)
