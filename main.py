import requests
import os
from dotenv import load_dotenv
import datetime
from atproto import Client
from collections import defaultdict

# Carrega as variáveis de ambiente, com o objetivo de esconder as credenciais
load_dotenv()

# Pega o código de API da .env
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
username = "amiseralk"
start_timestamp = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
end_timestamp =  int(datetime.datetime.now().timestamp())

# Retorna os scrobble dos últimos 7 dias
response = requests.get(
    f"http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user={username}&api_key={LASTFM_API_KEY}&format=json&from={start_timestamp}&to={end_timestamp}"
)
tracks = response.json()["recenttracks"]["track"]

# Conta a quantidade de artistas
artist_counts = defaultdict(int)
for track in tracks:
    artist = track["artist"]["#text"]
    artist_counts[artist] += 1

# Ordena e seleciona o top 10 artistas (o parâmetro reserve faz com que retorne a lista do mais ouvido para o menos ouvido)
top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:10]

client = Client()
client.login(os.getenv("BLUESKY_USERNAME"), os.getenv("BLUESKY_PASSWORD"))
text = "Meus top 10 artistas da semana: " + ", ".join([artist for artist, _ in top_artists])  + "\n- Provido por ScrobbleToSky"
client.send_post(text)