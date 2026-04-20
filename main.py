from utils import init, cadastro, login, uploadVideo, clear, perfil, deletarConta, editarConta, playlists, criarPlaylist
import os

if not os.path.exists('./data/users.txt'): open('./data/users.txt', 'a')
if not os.path.exists('./data/videos.txt'): open('./data/videos.txt', 'a')
if not os.path.exists('./data/playlists.txt'): open('./data/playlists.txt', 'a')
if not os.path.exists('./data/favs.txt'): open('./data/favs.txt', 'a')

auth_status = False
current_user = {}
pagina = 'inicial'

while True:
    if pagina == 'inicial': opt = init(auth_status)

    if auth_status == False:
        if opt == 'C': current_user, auth_status = cadastro()
        elif opt == 'L': current_user, auth_status = login()
        elif opt == 'S':
            clear()
            break
    else:
        if pagina == 'inicial':
            if opt == 'E': uploadVideo(current_user['nome'])
        if pagina == 'perfil':
            if opt == 'D': 
                operacao = deletarConta(current_user)
                if operacao == 1:
                    pagina = 'inicial'
                    auth_status = False
                    current_user = {}
            if opt == 'E':
                opt = 'U'
                current_user = editarConta(current_user)
        if pagina == 'playlists':
            if opt == 'C':
                opt = 'P'
                criarPlaylist(current_user['nome'])
            
        if opt == 'U': 
            pagina = 'perfil'
            opt = perfil(current_user)
        if opt == 'P': 
            pagina = 'playlists'
            opt = playlists(current_user['nome'])
        if opt == 'I': pagina = 'inicial'
        if opt == 'S': 
            pagina = 'inicial'
            auth_status = False

