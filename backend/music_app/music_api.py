import requests

def get_music_url(song_id):
    url = f'https://api.imjad.cn/cloudmusic/?type=song&id={song_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200 and data.get('data'):
                return data['data'][0].get('url')
    except requests.RequestException:
        pass
    return None