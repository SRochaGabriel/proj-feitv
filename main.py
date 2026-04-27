from utils import init, cadastro, login, uploadVideo, clear, perfil, deletarConta, editarConta, playlists, criarPlaylist, videoDetails, curtir_descurtir, buscar, favoritos, deletarVideo, editarVideo, addToPlaylist, playlistDetails, deletarPlaylist, editarPlaylist, removeVideo
import os

if not os.path.exists('./data/users.txt'): open('./data/users.txt', 'a')
if not os.path.exists('./data/videos.txt'): open('./data/videos.txt', 'a')
if not os.path.exists('./data/playlists.txt'): open('./data/playlists.txt', 'a')
if not os.path.exists('./data/favs.txt'): open('./data/favs.txt', 'a')
if not os.path.exists('./data/dislikes.txt'): open('./data/dislikes.txt', 'a')

auth_status = False
current_user = {}
pagina = 'inicial'
opt = 'I'

while True:
    if opt == 'I':
        pagina = 'inicial'
        opt = init(auth_status)
    
    if auth_status == False:
        if opt == 'C': 
            current_user, auth_status = cadastro()
            opt = 'I'
        elif opt == 'L': 
            current_user, auth_status = login()
            opt = 'I'
        elif opt == 'S':
            clear()
            break
    else:        
        if pagina == 'inicial':
            if opt == 'E': 
                uploadVideo(current_user['nome'])
                opt = 'I'
        if pagina == 'perfil':
            if opt == 'D': 
                operacao = deletarConta(current_user)
                if operacao == 1:
                    opt = 'I'
                    auth_status = False
                    current_user = {}
            if opt == 'E':
                opt = 'U'
                current_user = editarConta(current_user)
        if pagina == 'playlists':
            if opt == 'C':
                opt = 'P'
                criarPlaylist(current_user['nome'])
            if opt.isdigit():
                playlist_id = opt
                opt = playlistDetails(playlist_id)
                pagina = 'playlist_page'
        if pagina == 'playlist_page':
            if opt == 'D': 
                opt = deletarPlaylist(playlist_id)
            if opt == 'E':
                pagina = 'playlists'
                opt = editarPlaylist(playlist_id)
        if pagina == 'video_page':
            if opt == 'C': 
                curtir_descurtir(current_user['nome'], video_id, 'curtir')
                opt = video_id
            if opt == 'D':
                curtir_descurtir(current_user['nome'], video_id, 'descurtir')
                opt = video_id
            if opt == 'X':
                opt = deletarVideo(video_id, current_user['senha'])
            if opt == 'E':
                opt = editarVideo(video_id, current_user['senha'])
            if opt == 'A':
                opt = addToPlaylist(video_id, current_user['nome'])

        if pagina != 'playlists' and opt.isdigit():
            video_id = opt
            opt = videoDetails(video_id, current_user['nome'])
            pagina = 'video_page'
        if opt == 'Q': 
            opt = buscar()
        if opt == 'U': 
            pagina = 'perfil'
            opt = perfil(current_user)
        if opt == 'P': 
            pagina = 'playlists'
            opt = playlists(current_user['nome'])
        if opt == 'S': 
            opt = 'I'
            auth_status = False
        if opt == 'F':
            opt = favoritos(current_user['nome'])
