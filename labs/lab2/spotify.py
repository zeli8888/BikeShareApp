import requests
from json import loads
from pprint import pprint

headers = {
    "Authorization" : "Bearer BQCX0Ouo4m-_Aq2oZirHiEQLF4sO4D1ds-eSleH1P8yLy7_MNpjD0Om__X_zeTMDBfNiajmT4kv0OUrmi-LCrtLVtCVWk3M_0lWgrs31c75yCX725ZZd0SMvSLhRqH3bjsCVl-Bn1uc"
}

URI = "https://api.spotify.com/v1/search"
r = requests.get(URI, params={'q':'bob','type':'artist','limit':2},headers=headers)
pprint(loads(r.text))

# {'artists': {'href': 'https://api.spotify.com/v1/search?offset=0&limit=2&query=bob&type=artist',
#              'items': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/74ASZWbe4lXaubB36ztrGX'},
#                         'followers': {'href': None, 'total': 6886911},       
#                         'genres': ['folk rock',
#                                    'folk',
#                                    'singer-songwriter',
#                                    'roots rock',
#                                    'country rock'],
#                         'href': 'https://api.spotify.com/v1/artists/74ASZWbe4lXaubB36ztrGX',
#                         'id': '74ASZWbe4lXaubB36ztrGX',
#                         'images': [{'height': 640,
#                                     'url': 'https://i.scdn.co/image/ab6761610000e5eb791742524609864273747ef5',
#                                     'width': 640},
#                                    {'height': 320,
#                                     'url': 'https://i.scdn.co/image/ab67616100005174791742524609864273747ef5',
#                                     'width': 320},
#                                    {'height': 160,
#                                     'url': 'https://i.scdn.co/image/ab6761610000f178791742524609864273747ef5',
#                                     'width': 160}],
#                         'name': 'Bob Dylan',
#                         'popularity': 76,
#                         'type': 'artist',
#                         'uri': 'spotify:artist:74ASZWbe4lXaubB36ztrGX'},     
#                        {'external_urls': {'spotify': 'https://open.spotify.com/artist/2QsynagSdAqZj3U9HgDzjD'},
#                         'followers': {'href': None, 'total': 12984044},      
#                         'genres': ['reggae', 'roots reggae'],
#                         'href': 'https://api.spotify.com/v1/artists/2QsynagSdAqZj3U9HgDzjD',
#                         'id': '2QsynagSdAqZj3U9HgDzjD',
#                         'images': [{'height': 858,
#                                     'url': 'https://i.scdn.co/image/b5aae2067db80f694a980e596e7f49618c1206c9',
#                                     'width': 1000},
#                                    {'height': 549,
#                                     'url': 'https://i.scdn.co/image/4cd57e5e12ea2c24644c40886d65a9b22eca9802',
#                                     'width': 640},
#                                    {'height': 172,
#                                     'url': 'https://i.scdn.co/image/02fd758d9805ef44d1caafc35ff17a47f9dff098',
#                                     'width': 200},
#                                    {'height': 55,
#                                     'url': 'https://i.scdn.co/image/357fe6ef3655b1b33855e33546e3c174a38a1a36',
#                                     'width': 64}],
#                         'name': 'Bob Marley & The Wailers',
#                         'popularity': 79,
#                         'type': 'artist',
#                         'uri': 'spotify:artist:2QsynagSdAqZj3U9HgDzjD'}],    
#              'limit': 2,
#              'next': 'https://api.spotify.com/v1/search?offset=2&limit=2&query=bob&type=artist',
#              'offset': 0,
#              'previous': None,
#              'total': 100
# }}