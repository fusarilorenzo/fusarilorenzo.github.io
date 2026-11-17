import os
import shutil
from flask_frozen import Freezer
from app import app, LANGS, PROJECTS

if os.path.exists('build'):
    shutil.rmtree('build')

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*']
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

freezer = Freezer(app)

@freezer.register_generator
def home():
    for lang in LANGS:
        yield 'home', {'lang': lang}

@freezer.register_generator
def dettaglio_progetto():
    for lang in LANGS:
        for id_progetto in PROJECTS.keys():
            yield 'dettaglio_progetto', {'lang': lang, 'id_progetto': id_progetto}

@freezer.register_generator
def achievements():
    for lang in LANGS:
        yield 'achievements', {'lang': lang}

@freezer.register_generator
def publications():
    # Generata sempre, anche se la lista PUBLICATIONS e' vuota
    for lang in LANGS:
        yield 'publications', {'lang': lang}

def genera_404_statica():
    with app.test_client() as client:
        response = client.get('/en/non-esiste')
        build_dir = app.config.get('FREEZER_DESTINATION', 'build')
        os.makedirs(build_dir, exist_ok=True)
        with open(os.path.join(build_dir, '404.html'), 'wb') as f:
            f.write(response.data)

if __name__ == '__main__':
    freezer.freeze()
    genera_404_statica()
    print("Build completata con successo nella cartella 'build/'!")
