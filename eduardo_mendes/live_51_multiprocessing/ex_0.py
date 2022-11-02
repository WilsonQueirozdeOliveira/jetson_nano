from datetime import datetime
from os import makedirs
from os.path import exists
from pprint import pprint
from shutil import rmtree, copyfileobj
from urllib.parse import urljoin
from requests import get

start_time = datetime.now()

path = 'download'
base_url = 'https://pokeapi.co/api/v2/'

if exists(path):
    rmtree(path)
makedirs(path)

def download_file(name, url, *, path=path, type_='png'):
    response = get(url, stream=True)
    fname = f'{path}/{name}.{type_}'
    with open(fname, 'wb') as f:
        copyfileobj(response.raw, f)
    return fname

def get_sprite_url(url, sprite='front_default'):
    return get(url).json()['sprites'][sprite]

start_time = datetime.now()

pokemons = get(urljoin(base_url,'pokemon/?limit=100')).json()['results']

images_url = {j['name']: get_sprite_url(j['url']) for j in pokemons}

files = [download_file(name, url) for name, url in images_url.items()]

time_elapsed = datetime.now() - start_time

print( f'Total time (hh:mm:ss.ms) {time_elapsed}')


pprint(files)
