import random

def shuffle(playlist):

    playlist_temp = playlist[:]

    len_playlist_temp = len(playlist_temp)
    for i in range(len_playlist_temp):
        # https://parzibyte.me/blog/2019/04/04/generar-numero-aleatorio-rango-python/
        random_index = random.randint(0, len_playlist_temp - 1)
        temporal = playlist_temp[i]
        playlist_temp[i] = playlist_temp[random_index]
        playlist_temp[random_index] = temporal

    return playlist_temp