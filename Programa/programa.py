from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import spotipy

# Conexion con la API
sp = spotipy.Spotify()
cid = "******"
secret = "****"
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

# Usuario 50 cent
# https://open.spotify.com/user/1217753577

# Playlists de 50 cent
# The Singles Collection: https://open.spotify.com/playlist/1hBQZ8nCtIHrEByxICx8tU
# Featuring 50cent: https://open.spotify.com/playlist/3pDliBuh3MwiSfjOKo5mKl
# 50 cent best of: https://open.spotify.com/playlist/49RoQF55lyRSgSZwRAHh5K
# 50 my playlist: https://open.spotify.com/playlist/1s7ipxTB42mCucqQUWVMP4


#lista donde tenemos todas las playlists anteriores
pp = ["3pDliBuh3MwiSfjOKo5mKl", "1hBQZ8nCtIHrEByxICx8tU",
      "49RoQF55lyRSgSZwRAHh5K", "1s7ipxTB42mCucqQUWVMP4"]

for i in pp:
    # obtenemos una playlist
    playlist = sp.user_playlist("1217753577", i, fields="tracks,next")
    tracks = playlist["tracks"]
    songs = tracks["items"]

    ids = []
    song = []
    artist = []

    # obtenemos las canciones
    for k in range(len(songs)):
        s = songs[k]["track"]
        ids.append(s["id"])
        artists = []

        for j in range(len(s["artists"])):
            # dataset de playlists
            artists.append(s["artists"][j]["name"])
            song.append([s["name"], s["popularity"], artists])

            # dataset de artistas
            a = sp.artist(s["artists"][j]["id"])
            artist.append(
                [a["name"], a["genres"], a["popularity"], a["followers"]["total"]])

    # Exportamos a Json los datos recabados
    dataArtists = pd.DataFrame(artist)
    dataSongs = pd.DataFrame(song)
    outputArtists = "api/50cent-dataArtists"+str(pp.index(i)+1)+".json"
    output = "api/50cent-dataPlaylist"+str(pp.index(i)+1)+".json"
    dataSongs.to_json(output, orient='records')
    dataArtists.to_json(outputArtists, orient='records')
