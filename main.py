from utils import init, cadastro, login, uploadVideo, clear, perfil
import os

if not os.path.exists('./data/users.txt'): open('./data/users.txt', 'a')
if not os.path.exists('./data/videos.txt'): open('./data/videos.txt', 'a')
if not os.path.exists('./data/playlists.txt'): open('./data/playlists.txt', 'a')
if not os.path.exists('./data/favs.txt'): open('./data/favs.txt', 'a')

auth_status = False
current_user = {}

while True:
    opt = init(auth_status)

    if auth_status == False:
        if opt == 'C': current_user, auth_status = cadastro()
        elif opt == 'L': current_user, auth_status = login()
        elif opt == 'S':
            clear()
            break
    else:
        if opt == 'E': uploadVideo(current_user['nome'])
        if opt == 'U': perfil(current_user['nome'])
        if opt == 'S': auth_status = False

