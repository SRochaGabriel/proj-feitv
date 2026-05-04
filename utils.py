import ast
import datetime
import os
import textwrap
import getpass
import time

def clear(): os.system('clear' if os.name == 'posix' else 'clear')

def formataDuracao(horas, minutos, segundos):
    if horas == '': horas = '0'
    if minutos == '': minutos = '0'
    if segundos == '': segundos = '0'

    if horas != '0' and len(horas) == 1: horas = f'0{horas}'
    if len(minutos) == 1: minutos = f'0{minutos}'
    if len(segundos) == 1: segundos = f'0{segundos}'

    if horas == '0': return f'{minutos}:{segundos}'
    else: return f'{horas}:{minutos}:{segundos}'

def printOpts(opt_layout, videoIds = 0, user_func = 'usuario'):
    opcoes = []

    if opt_layout == 'gerais':
        if user_func == 'admin':
            print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Enviar vídeo    U - Meu perfil    T - Listagem de usuários    S - Sair da conta')
            opcoes = ['I', 'F', 'P', 'Q', 'E', 'U', 'T', 'S']
        else:
            print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Enviar vídeo    U - Meu perfil    S - Sair da conta')
            opcoes = ['I', 'F', 'P', 'Q', 'E', 'U', 'S']
    elif opt_layout == 'meu_perfil':
        print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Editar informações    D - Deletar conta    S - Sair da conta')
        opcoes = ['I', 'F', 'P', 'Q', 'E', 'D', 'S']
    elif opt_layout == 'perfil':
        print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    S - Sair da conta')
        opcoes = ['I', 'F', 'P', 'Q', 'S']
    elif opt_layout == 'playlists':
        print('\nI - Página inicial    F - Favoritos    Q - Buscar    C - Criar playlist    U - Meu perfil    S - Sair da conta')
        opcoes = ['I', 'F', 'Q', 'C', 'U', 'S']
    elif opt_layout == 'playlist_page':
        print('\nI - Página inicial    Q - Buscar    P - Minhas playlists    E - Editar playlist    D - Deletar playlist    X - Remover vídeo da playlist    S - Sair da conta')
        opcoes = ['I', 'Q', 'P', 'E', 'D', 'X', 'S']
    elif opt_layout == 'video_page':
        print('\nI - Página inicial    P - Minhas playlists    C - Curtir    D - Descurtir    A - Adicionar à playlist    V - Ver perfil de usuário    S - Sair da conta')
        opcoes = ['I', 'P', 'C', 'D', 'A', 'V', 'S']
    elif opt_layout == 'owner_video_options':
        print('\nI - Página inicial    C - Curtir    D - Descurtir    E - Editar informações    X - Excluir vídeo    A - Adicionar à playlist    V - Ver perfil de usuário    S - Sair da conta')
        opcoes = ['I', 'C', 'D', 'E', 'X', 'A', 'V', 'S']
    elif opt_layout == 'admin_video_options':
        print('\nI - Página inicial    C - Curtir    D - Descurtir    X - Excluir vídeo    A - Adicionar à playlist    V - Ver perfil de usuário    S - Sair da conta')
        opcoes = ['I', 'C', 'D', 'X', 'A', 'V', 'S']
    elif opt_layout == 'all_users' and user_func == 'admin':
        print('\nI - Página inicial    Q - Buscar    V - Ver perfil de usuário     X - Remover usuário    U - Meu perfil    S - Sair da conta')
        opcoes = ['I', 'Q', 'V', 'X', 'E', 'U', 'S']
    else:
        print('C - Cadastrar    L - Efetuar login    S - Sair do FeiTV')
        opcoes = ['C', 'L', 'S']

    if videoIds != 0:
            for id in videoIds:
                opcoes.append(id)

    return opcoes

def printTables(table_type, table_data, table_order = 'none'):
    if len(table_data) == 0:
            print('Nada a ver aqui por enquanto...')
            return 0

    max_data_size = 0

    if table_type == 'videos':
        headers = ['ID', 'TÍTULO', 'DURACAO', 'ENVIADO POR', 'DATA DE ENVIO', 'LIKES', 'DISLIKES']
        campos = ['id', 'titulo', 'duracao', 'uploader', 'data_envio', 'likes', 'dislikes']
        max_data_size = 30

        if table_order == 'recentes' or table_order == 'recentes_10':
            table_data.reverse()
        elif table_order == 'likes' or table_order == 'top_likes':
            for i in range(len(table_data)):
                for j in range(i + 1, len(table_data)):
                    if table_data[i]['likes'] < table_data[j]['likes']:
                        substituto = table_data[i]
                        table_data[i] = table_data[j]
                        table_data[j] = substituto

        if table_order == 'top_likes': table_data = table_data[:5]
        elif table_order == 'recentes_10': table_data = table_data[:10]

        tamanhos_coluna = [5, 35, 10, 35, 15, 10, 10]
        length_table = 8
    elif table_type == 'playlists':
        headers = ['ID', 'NOME']
        campos = ['id', 'nome']
        tamanhos_coluna = [10, 110]
        length_table = 3
        max_data_size = 95
    elif table_type == 'users':
        headers = ['ID', 'NOME', 'EMAIL', 'NÍVEL', 'DATA DE CRIAÇÃO']
        campos = ['id', 'nome', 'email', 'funcao', 'criacao']
        tamanhos_coluna = [5, 35,  35, 15, 25]
        length_table = 5
        max_data_size = 30
        for i in range(len(table_data)):
            for j in range(i + 1, len(table_data)):
                if table_data[i]['nome'] > table_data[j]['nome']:
                    substituto = table_data[i]
                    table_data[i] = table_data[j]
                    table_data[j] = substituto

    for tamanho in tamanhos_coluna: length_table += tamanho

    for linha in range(len(table_data)):
        if linha == 0:
            print('\033[1;94m|\033[0m', end='')
            for i in range(len(tamanhos_coluna)):
                print(f'\033[0;33m{headers[i]:^{tamanhos_coluna[i]}}\033[0m', end='\033[1;94m|\033[0m')
            print()
            for i in range(length_table): print('\033[1;94m#\033[0m', end='')
            print()
        
        print('\033[1;94m|\033[0m', end='')
        for i in range(len(campos)):
            if len(str(table_data[linha][campos[i]])) > max_data_size: 
                table_data[linha][campos[i]] = table_data[linha][campos[i]][:(max_data_size - 3)] + '...'

            print(f'{table_data[linha][campos[i]]:^{tamanhos_coluna[i]}}', end='\033[1;94m|\033[0m')
        print()
    
    ids = []
    for item in table_data:
        if table_type == 'videos' or table_type == 'playlists': ids.append(item['id'])
        elif table_type == 'users': ids.append(item['nome'])

    return ids

def getUsers():
    with open('./data/users.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

def getVideos():
    with open('./data/videos.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

def buscar():
    clear()
    printLogo()
    search = input('\033[1;94mBusca (para cancelar, envie 0):\033[0m ').lower()
    if search == '0': return 'I'
    print()

    search = search.split()
    videos = getVideos()
    search_results = []

    for search_item in search:
        for video in videos:
            if search_item.lower() in video['titulo'].lower() or search_item in video['uploader']:
                search_results.append(video)
    
    video_ids = printTables('videos', search_results, 'likes')

    opcoes = printOpts('gerais', video_ids)
    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
        
    return opt

def getAllFavoritesOrDislikes(file):
    with open(f'./data/{file}.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

def getUserFavoritesOrDisliked(username, file):
    with open(f'./data/{file}.txt', 'r') as f:
        try: 
            items = ast.literal_eval(f.read())
            for item in items:
                if item['user'] == username: 
                    return item
                    break
            else:
                raise Exception
        except:
            if file == 'favs':
                return {"user": username, "curtidos": []}
            else:
                return {"user": username, "descurtidos": []}

def getAllPlaylists():
    with open('./data/playlists.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

def getUserPlaylists(username):
    with open('./data/playlists.txt', 'r') as f:
        try: 
            playlists = ast.literal_eval(f.read())
            userPlaylists = []

            for playlist in playlists:
                if playlist['user'] == username: userPlaylists.append(playlist)
            
            return userPlaylists
        except: return []

def uploadVideo(user):
    print('\033[1;94mVamos pedir as informações dos vídeos que você quer registrar na plataforma. Para cancelar, envie "SAIR"\033[0m')
    titulo, horas, minutos, segundos = '', '', '', ''
    videos = getVideos()
    id = len(videos) + 1

    for vid in videos:
        if str(id) == vid['id']:
            id += 1
    
    while titulo == '':
        titulo = input('\033[1;94mInsira o título do vídeo (obrigatório):\033[0m ')
        if titulo == '0':
            print('\033[1;91mEsse título de vídeo não é válido. Tente novamente.\033[0m')
            titulo = ''
    if titulo == 'SAIR': return 

    descricao = input('\033[1;94mInsira a descrição do vídeo (opcional):\033[0m ')
    if descricao == 'SAIR': return 

    while horas == '':
        horas = input('\033[1;94mQuantas horas o vídeo possui?\033[0m ')
        if horas == 'SAIR': return
        elif not (horas.isdigit()):
            print('\033[1;91mPara campos de tempo do vídeo, envie valores numéricos válidos ou digite SAIR para cancelar o upload do vídeo.\033[0m')
            horas = ''

    while minutos == '':
        minutos = input('\033[1;94mQuantos minutos o vídeo possui?\033[0m ')
        if minutos == 'SAIR': return
        elif not (minutos.isdigit()) or int(minutos) >= 60:
            print('\033[1;91mPara campos de tempo do vídeo, envie valores numéricos válidos ou digite SAIR para cancelar o upload do vídeo.\033[0m')
            minutos = ''
    
    while segundos == '':
        segundos = input('\033[1;94mQuantos segundos o vídeo possui?\033[0m ')
        if segundos == 'SAIR': return
        elif not (segundos.isdigit()) or int(segundos) >= 60:
            print('\033[1;91mPara campos de tempo do vídeo, envie valores numéricos válidos ou digite SAIR para cancelar o upload do vídeo.\033[0m')
            segundos = ''

    duracao = formataDuracao(horas, minutos, segundos)

    video = {
        "id": str(id),
        "titulo": titulo,
        "descricao": descricao,
        "duracao": duracao,
        "data_envio": datetime.date.today().strftime('%d/%m/%Y'),
        "likes": 0,
        "dislikes": 0,
        "uploader": user
    }

    videos.append(video)

    with open('./data/videos.txt', 'w') as f:
        f.write(str(videos))

def usersPage():
    clear()
    printLogo()
    print()
    userIds = printTables('users', getUsers())
    opcoes = printOpts('all_users', userIds, 'admin')
    return inputOpts(opcoes)

def removeUser():
    user_id = ''
    users = getUsers()
    user_ids = []
    for user in users:
        user_ids.append(user['id'])

    while user_id == '':
        user_id = input('\033[1;94mInsira o ID do usuário a ser removido da plataforma (para cancelar, envie 0): \033[0m')
        if user_id == '0': return 'T'
        elif user_id not in user_ids:
            print('\033[1;91mSelecione um nome de usuário válido.\033[0m')
            user_id = ''

    opcao = ''
    while opcao == '':
        opcao = input('\033[1;94mTem certeza que deseja remover o usuário e todos os seus registros? (S/N): \033[0m').upper()
        if opcao not in ['S', 'N']:
            print('\033[1;91mSelecione uma opção válida.\033[0m')
            opcao = ''
    if opcao == 'N': return 'T'

    for i in range(len(users)):
        if users[i]['id'] == user_id:
            username = users[i]['nome']
            users.pop(i)
            break
    
    removeAllUserData(username)
    with open('./data/users.txt', 'w') as f: f.write(str(users))
    return 'T'

def verPerfil(curr_user, user = ''):
    if user == '':
        users = getUsers()
        user_ids = []
        for u in users:
            user_ids.append(u['id'])

        while user == '':
            user = input('\033[1;94mInsira o ID do usuário para ver o perfil (para cancelar, envie 0): \033[0m')
            if user == '0': return 'T'
            elif user not in user_ids:
                print('\033[1;91mSelecione um ID de usuário válido.\033[0m')
                user = ''
        
        for i in range(len(users)):
            if users[i]['id'] == user: username = users[i]['nome']
    
    return perfil(curr_user, username)

def init(auth_status, user_func = ''):
    clear()
    printLogo()

    opt = ''

    if auth_status == False:
        print('\nBem-vindo ao sistema da \033[1;94mFei\033[0mTV! Por favor, selecione uma das opções abaixo')
        opcoes = printOpts('opcoes_sem_login')
    else:
        if user_func == 'usuario':
            print('\n\033[1;97m##################################################### VÍDEOS MAIS RECENTES #####################################################\033[0m')
            print()
            videoIds = printTables('videos', getVideos(), 'recentes_10')
            opcoes = printOpts('gerais', videoIds)
        else:
            print('\n\033[1;97m##################################################### ESTATÍSTICAS DO SISTEMA #####################################################\033[0m')
            print('\n\033[1;94m##################################################### VÍDEOS MAIS CURTIDOS #####################################################\033[0m')
            videoIds = printTables('videos', getVideos(), 'top_likes')
            print(f'\033[1;94mTotal de usuários:\033[0m {len(getUsers())}\n\033[1;94mTotal de vídeos:\033[0m {len(getVideos())}')
            opcoes = printOpts('gerais', videoIds, 'admin')

    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
        
    return opt

def videoDetails(video_id, user):
    clear()
    printLogo()
    videos = getVideos()
    for i in range(len(videos)):
        if videos[i]['id'] == video_id: video = videos[i]

    print('\n\033[1;97m########################################################## INFORMAÇÕES DO VÍDEO #########################################################\033[0m')

    print(f'\033[1;94mTítulo:\033[0m {video['titulo']}')
    print(f'\033[1;94mDescrição:\033[0m {textwrap.fill(video['descricao'], width=80)}')
    print(f'\033[1;94mUploader:\033[0m {video['uploader']}')
    print(f'\033[1;94mDuração:\033[0m {video['duracao']}    \033[1;94mData de envio:\033[0m {video['data_envio']}')
    print(f'\033[1;94mLikes:\033[0m {video['likes']}    \033[1;94mDislikes:\033[0m {video['dislikes']}')

    if video['uploader'] == user['nome']:
        opcoes = printOpts('owner_video_options')
    elif user['funcao'] == 'admin':
        opcoes = printOpts('admin_video_options')
    else:
        opcoes = printOpts('video_page')
    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()

    if opt == 'V': return opt, video['uploader']
    else: return opt, None

def deletarVideo(video_id, user):
    senha = ''
    while senha == '':
        senha = getpass.getpass('\033[1;94mInsira sua senha para confirmar ou envie 0 para cancelar a exclusão:\033[0m ')
        if senha == '0': return video_id
        elif senha != user['senha']:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar.')
            senha = ''

    videos = getVideos()
    for i in range(len(videos)):
        if videos[i]['id'] == video_id: 
            videos.pop(i)
            break

    with open('./data/videos.txt', 'w') as f: f.write(str(videos))
    if user['funcao'] == 'usuario': return 'U'
    else: return 'I'

def editarVideo(video_id, user_senha):
    print('\n\033[1;94mVamos pedir que insira as informações do vídeo a serem alteradas. Para manter uma informação como está, pressione Enter sem digitar nada. Para cancelar, envie \'SAIR\' em qualquer campo.\033[0m')
    
    videos = getVideos()
    video = {}
    for vid in videos:
        if vid['id'] == video_id: video = vid

    og_duracao = video['duracao'].split(':')
    try: og_horas, og_minutos, og_segundos = og_duracao[0], og_duracao[1], og_duracao[2]
    except: og_horas, og_minutos, og_segundos = '00', og_duracao[1], og_duracao[2] 
    horas, minutos, segundos = 'a', 'a', 'a'

    titulo = input('\033[1;94mTítulo:\033[0m ')
    if titulo == 'SAIR': return video_id
    desc = input('\033[1;94mDescrição:\033[0m ')
    if desc == 'SAIR': return video_id
    
    while horas == 'a':
        horas = input('\033[1;94mHoras:\033[0m ')
        if horas == 'SAIR': return video_id
        elif not horas.isdigit() and horas != '':
            print('\033[1;91mEnvie um valor numérico válido ou deixe o campo vazio para manter o valor anterior.\033[0m')
            horas = 'a'

    while minutos == 'a':
        minutos = input('\033[1;94mMinutos:\033[0m ')
        if minutos == 'SAIR': return video_id
        elif (not minutos.isdigit() and minutos != '') or (minutos.isdigit() and int(minutos) >= 60):
            print('\033[1;91mEnvie um valor numérico válido ou deixe o campo vazio para manter o valor anterior.\033[0m')
            minutos = 'a'

    while segundos == 'a':
        segundos = input('\033[1;94mSegundos:\033[0m ')
        if segundos == 'SAIR': return video_id
        elif (not segundos.isdigit() and segundos != '') or (segundos.isdigit() and int(segundos) >= 60):
            print('\033[1;91mEnvie um valor numérico válido ou deixe o campo vazio para manter o valor anterior.\033[0m')
            segundos = 'a'

    if horas == '': horas = og_horas
    if minutos == '': minutos = og_minutos
    if segundos == '': segundos = og_segundos
    duracao = formataDuracao(horas, minutos, segundos)

    senha = ''
    while senha == '':
        senha = getpass.getpass('\n\033[1;94mInsira sua senha para confirmar ou envie 0 para cancelar:\033[0m ')
        if senha == '0': return video_id
        elif senha != user_senha:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar.\033[0m')
            senha = ''
    
    videos = getVideos()
    for i in range(len(videos)):
        if videos[i]['id'] == video_id:
            if titulo != '': videos[i]['titulo'] = titulo
            if desc != '': videos[i]['descricao'] = desc
            if duracao != '00:00': videos[i]['duracao'] = duracao
    
    with open('./data/videos.txt', 'w') as f: f.write(str(videos))
    
    return video_id

def addToPlaylist(video_id, username):
    clear()
    playlists = getUserPlaylists(username)
    if len(playlists) == 0:
        print('\033[1;91mVocê não tem nenhuma playlist criada ainda. Crie uma playlist para poder adicionar vídeos.\033[0m')
        opcao = ''
        while opcao == '':
            opcao = input('\033[1;94mVocê deseja ir para a área de playlists para criar uma nova? (S/N)\033[0m ').upper()
            if opcao == 'S': return 'P'
            elif opcao == 'N': return video_id
            else:
                print('\033[1;91mOpção inválida.\033[0m')
                opcao = ''

    print('\033[1;97m################################################### PLAYLISTS ###################################################\033[0m')
    print()
    playlist_ids = printTables('playlists', playlists)
    print()

    selected_playlist = ''
    while selected_playlist == '':
        selected_playlist = input('\033[1;94mInforme o ID da playlist a qual você quer adicionar o vídeo ou envie 0 para cancelar:\033[0m ')
        if selected_playlist == '0': return video_id
        elif selected_playlist not in playlist_ids:
            print('\033[1;91mA opção informada não é válida. Digite o ID de uma das playlists ou 0 para cancelar.\033[0m')
            print()
            selected_playlist = ''

        for playlist in playlists:
            if playlist['id'] == selected_playlist and video_id in playlist['videos']:
                print('\033[1;91mEsse vídeo já está incluído nessa playlist.\033[0m')
                selected_playlist = ''

    for i in range(len(playlists)):
        if playlists[i]['id'] == selected_playlist: playlists[i]['videos'].append(video_id)

    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))
    
    return video_id

def curtir_descurtir(username, video_id, funcao):
    videos = getVideos()
    fav = getUserFavoritesOrDisliked(username, 'favs')
    disliked = getUserFavoritesOrDisliked(username, 'dislikes')
    init_fav = fav['curtidos'][:]
    init_disliked = disliked['descurtidos'][:]

    if funcao == 'curtir':
        operacao = 'add_like'

        if video_id in fav['curtidos']:
            operacao = 'remove_like'
            fav['curtidos'].remove(video_id)
        else:
            fav['curtidos'].append(video_id)
    else:
        operacao = 'add_dislike'

        if video_id in disliked['descurtidos']:
            operacao = 'remove_dislike'
            disliked['descurtidos'].remove(video_id)
        else:
            disliked['descurtidos'].append(video_id)
        
    for video in videos:
        if video['id'] == video_id:
            if operacao == 'add_like' and video_id in disliked['descurtidos']: 
                video['likes'] += 1
                video['dislikes'] -= 1
                disliked['descurtidos'].remove(video_id)
            elif operacao == 'add_dislike' and video_id in fav['curtidos']: 
                video['likes'] -= 1
                video['dislikes'] += 1
                fav['curtidos'].remove(video_id)
            elif operacao == 'add_like' and video_id not in disliked['descurtidos']: video['likes'] += 1
            elif operacao == 'add_dislike' and video_id not in fav['curtidos']: video['dislikes'] += 1
            elif operacao == 'remove_like': video['likes'] -= 1
            elif operacao == 'remove_dislike': video['dislikes'] -= 1 

    if init_fav != fav['curtidos']:
        favs = getAllFavoritesOrDislikes('favs')
        for i in range(len(favs)):
            if favs[i]['user'] == fav['user'] and favs[i] != fav: 
                favs[i] = fav
                with open('./data/favs.txt', 'w') as f: f.write(str(favs))
                break
        else:
            favs.append(fav)
            with open('./data/favs.txt', 'w') as f: f.write(str(favs))

    if init_disliked != disliked['descurtidos']:
        dislikes = getAllFavoritesOrDislikes('dislikes')
        for i in range(len(dislikes)):
            if dislikes[i]['user'] == disliked['user'] and dislikes[i] != disliked:
                dislikes[i] = disliked
                with open('./data/dislikes.txt', 'w') as f: f.write(str(dislikes))
                break
        else:
            dislikes.append(disliked)    
            with open('./data/dislikes.txt', 'w') as f: f.write(str(dislikes))

    with open('./data/videos.txt', 'w') as f: f.write(str(videos))

def criarPlaylist(username):
    print('\033[1;94mPara cancelar o processo de criar uma nova playlist, digite e envie 0.\033[0m')
    n_playlist = ''
    userPlaylists = getUserPlaylists(username)
    playlists = getAllPlaylists()
    id = len(playlists) + 1

    while n_playlist == '':
        n_playlist = input('\033[1;94mInforme o nome da playlist a ser criada: \033[0m')
        for playlist in userPlaylists:
            if playlist['nome'] == n_playlist:
                print('\033[1;91mVocê já possui uma playlist com esse nome.\033[0m')
                n_playlist = ''
    if n_playlist == '0': return

    for playlist in playlists:
        if str(id) == playlist['id']: id += 1

    playlist = {"id": str(id), "user": username, "nome": n_playlist, "videos": []}

    playlists.append(playlist)
    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))

def playlists(username):
    clear()
    printLogo()
    print('\n\033[1;97m################################################ MINHAS PLAYLISTS ###############################################\033[0m')
    print()
    playlists = getUserPlaylists(username)
    playlist_ids = printTables('playlists', playlists)
        
    if len(playlists) != 0: print('\nPara selecionar uma playlist, envie o número de ID dela')
    
    opcoes = printOpts('playlists', playlist_ids)
    return inputOpts(opcoes)

def playlistDetails(playlist_id):
    clear()
    playlists = getAllPlaylists()
    for pl in playlists:
        if pl['id'] == playlist_id: playlist = pl
    
    videos = getVideos()
    pl_videos = []
    for video in videos:
        if video['id'] in playlist['videos']: pl_videos.insert(0, video)
    
    print(f'\n\033[1;97m##################################################### {playlist['nome'].upper()} #####################################################\033[0m')
    print()
    video_ids = printTables('videos', pl_videos)
    
    opcoes = printOpts('playlist_page', video_ids)
    return inputOpts(opcoes)

def deletarPlaylist(playlist_id):
    opcao = ''
    while opcao == '':
        opcao = input('\033[1;94mTem certeza que deseja deletar essa playlist? (S/N)\033[0m ').upper()
        if opcao not in ['S', 'N']:
                print('\033[1;91mOpção inválida.\033[0m')
                opcao = ''
    if opcao == 'N':
        return playlist_id

    playlists = getAllPlaylists()
    for i in range(len(playlists)):
        if playlists[i]['id'] == playlist_id:
            playlists.pop(i)
            break

    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))
    return 'P'

def editarPlaylist(playlist_id):
    playlist_name = input('\033[1;94mInsira o novo nome da playlist:\033[0m ')
    opcao = ''
    while opcao == '':
        opcao = input('\033[1;94mTem certeza que deseja alterar o nome da playlist? (S/N)\033[0m ').upper()
        if opcao not in ['S', 'N']:
                print('\033[1;91mOpção inválida.\033[0m')
                opcao = ''
    if opcao == 'N':
        return playlist_id

    playlists = getAllPlaylists()
    for i in range(len(playlists)):
        if playlists[i]['id'] == playlist_id: playlists[i]['nome'] = playlist_name
    
    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))
    return playlist_id

def removeVideo(playlist_id):
    playlist = {}
    playlists = getAllPlaylists()
    for pl in playlists:
        if pl['id'] == playlist_id: playlist = pl

    video_id = ''
    while video_id == '':
        video_id = input('\033[1;94mDigite o ID do vídeo que deseja remover da playlist\033[0m ')
        if video_id not in playlist['videos']:
            print('\033[1;91mInsira um ID válido entre os vídeos da playlist.\033[0m')
            video_id = ''
    playlist['videos'].remove(video_id)
    for i in range(len(playlists)):
        if playlists[i]['id'] == playlist_id: playlists[i] = playlist

    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))
    return playlist_id

def favoritos(username):
    clear()
    printLogo()
    print('\n\033[1;97m########################################################## VÍDEOS CURTIDOS #####################################################\033[0m')
    print()

    fav = getUserFavoritesOrDisliked(username, 'favs')
    videos = getVideos()
    videos_curtidos = []

    for video in videos:
        if video['id'] in fav['curtidos']: videos_curtidos.insert(0, video)

    ids = printTables('videos', videos_curtidos)

    opcoes = printOpts('gerais', ids)
    return inputOpts(opcoes)

def perfil(user, selected_username):
    clear()
    printLogo()
    videos = getVideos()
    user_videos = []

    if user['nome'] == selected_username:
        titulo_pag = 'MEUS ENVIOS'
        opt_layout = 'meu_perfil'
    else:
        titulo_pag = 'ENVIADOS'
        opt_layout = 'perfil'
        users = getUsers()
        for u in users:
            if selected_username == u['nome']:
                user = u
                break
    
    for video in videos:
        if video['uploader'] == user['nome']: user_videos.append(video)
    
    print(f'\n\033[1;97m########################################################## {titulo_pag} #########################################################\033[0m')
    print()
    videoIds = printTables('videos', user_videos, 'recentes')
    if videoIds != 0: print('\nPara selecionar um vídeo, digite e envie o número de ID do vídeo desejado')

    if opt_layout == 'meu_perfil': print(f'\n\033[1;94mNome de usuário:\033[0m {user['nome']}    \033[1;94mE-mail:\033[0m {user['email']}    \033[1;94mPerfil criado em:\033[0m {user['criacao']}')
    else: print(f'\n\033[1;94mNome de usuário:\033[0m {user['nome']}    \033[1;94mPerfil criado em:\033[0m {user['criacao']}')

    opcoes = printOpts(opt_layout, videoIds)
    return inputOpts(opcoes)

def deletarConta(curr_user):
    senha = ''
    while senha == '':
        senha = getpass.getpass('\033[1;94mInforme a senha para confirmar (ou envie 0 para cancelar): \033[0m')
    
        if senha == '0': return 'U'
        elif senha != curr_user['senha']:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar o processo\033[0m')
            senha = ''
    
    users = getUsers()
    removeAllUserData(curr_user['nome'])
    users.remove(curr_user)
    with open('./data/users.txt', 'w') as f: f.write(str(users))

    return 1

def removeAllUserData(username):
    videos = getVideos()
    videos_to_del = []
    favs = getAllFavoritesOrDislikes('favs')
    fav = getUserFavoritesOrDisliked(username, 'favs')
    dislikes = getAllFavoritesOrDislikes('dislikes')
    disliked = getUserFavoritesOrDisliked(username, 'dislikes')
    playlists = getAllPlaylists()
    playlists_to_del = []

    for video in videos:
        if video['id'] in fav['curtidos']: video['likes'] -= 1
        if video['id'] in disliked['descurtidos']: video['dislikes'] -= 1
        if video['uploader'] == username: videos_to_del.append(video)
    for video in videos_to_del: videos.remove(video)

    for fav in favs:
        if fav['user'] == username: favs.remove(fav)

    for disliked in dislikes:
        if disliked['user'] == username: dislikes.remove(disliked)

    for playlist in playlists:
        if playlist['user'] == username: playlists_to_del.append(playlist)
    for playlist in playlists_to_del: playlists.remove(playlist)
    with open('./data/videos.txt', 'w') as f: f.write(str(videos))
    with open('./data/favs.txt', 'w') as f: f.write(str(favs))
    with open('./data/dislikes.txt', 'w') as f: f.write(str(dislikes))
    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))

def editarConta(curr_user):
    print('\033[1;94mVamos pedir as informações que você deseja alterar.\nPara cancelar, digite e envie 0. Para manter uma informação, não envie nada.\033[0m')
    username, email, senha = '', '', ''

    users = getUsers()
    videos = getVideos()

    while True:
        username = input('\033[1;94mNovo nome de usuário: \033[0m')
        for user in users:
            if username != curr_user['nome'] and user['nome'] == username:
                print('\033[1;91mNome de usuário já está em uso. Escolha um nome diferente.\033[0m')
        else: break
    if username == '0': return curr_user

    while True:
        email = input('\033[1;94mNovo e-mail: \033[0m')
        for user in users:
            if email != curr_user['email'] and user['email'] == email:
                print('\033[1;91mE-mail já cadastrado! Use outro e-mail ou digite 0 para sair do cadastramento.\033[0m')
        else: break
    if email == '0': return curr_user

    while senha == '':
        senha = getpass.getpass('\033[1;94mInforme a senha para confirmar: \033[0m')
    
        if senha == '0': return curr_user
        elif senha != curr_user['senha']:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar o processo\033[0m')
            senha = ''

    for i in range(len(users)):
        if curr_user['nome'] == users[i]['nome']:
            if username != '': users[i]['nome'] = username
            if email != '': users[i]['email'] = email
            break
        
    if username != '': 
        for i in range(len(videos)):
            if curr_user['nome'] == videos[i]['uploader']: videos[i]['uploader'] = username
        curr_user['nome'] = username
    if email != '': curr_user['email'] = email
    
    with open('./data/users.txt', 'w') as f: f.write(str(users))
    with open("./data/videos.txt", 'w') as f: f.write(str(videos))

    return curr_user

def cadastro():
    clear()
    printLogo()
    print('\nPara voltar para a tela inicial, digite e envie 0.')
    username, email, senha = '', '', ''
    users = getUsers()
    id = len(users) + 1

    for user in users:
        if str(id) == user['id']:
            id += 1

    while username == '':
        username = input('\033[1;94mCrie seu nome de usuário:\033[0m ')

        for user in users:
            if user['nome'] == username:
                print('\033[1;91mNome de usuário já está em uso. Escolha um nome diferente.\033[0m')
                username = ''
    if username == '0': return {}, False 

    while email == '':
        email = input('\033[1;94mInsira seu E-mail:\033[0m ')

        for user in users:
            if user['email'] == email:
                print('\033[1;91mE-mail já cadastrado! Use outro e-mail ou digite 0 para sair do cadastramento.\033[0m')
                email = ''
    if email == '0': return {}, False

    while senha == '':
        senha = getpass.getpass('\033[1;94mCrie uma senha:\033[0m ')
        if senha == '0': return {}, False
        elif len(senha) < 6:
            print('\033[1;91mSua senha deve ter no mínimo 6 caracteres.\033[0m')
            senha = ''

    new_user = {"id": str(id), "nome": username, "email": email, "senha":senha, "funcao": "usuario", "criacao":datetime.date.today().strftime('%d/%m/%Y')}
    users.append(new_user)
    
    with open('./data/users.txt', 'w') as f:
        f.write(str(users))
    
    return new_user, True

def login(msg = 'Para voltar para a tela inicial, digite e envie 0.'):
    clear()
    printLogo()
    print('\n'+msg)
    email, senha = '', ''

    while email == '':
        email = input('\033[1;94mDigite seu e-mail:\033[0m ')
    if email == '0': return {}, False

    while senha == '':
        senha = getpass.getpass('\033[1;94mDigite sua senha:\033[0m ')
    if senha == '0': return {}, False

    users = getUsers()
    for user in users:
        if user['email'] == email and user['senha'] == senha:
            return user, True
    else:
        return login('\033[1;91mE-mail ou senha incorretos, tente novamente ou digite e envie 0 para retornar à tela inicial.\033[0m')

def inputOpts(opcoes):
    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
    return opt

def printLogo():
    print("\033[1;94m               __.....__     .--.\033[0m       .----.     .----.")
    print("\033[1;94m     _.._  .-''         '.   |__|\033[0m        \\    \\   /    /  ")
    print("\033[1;94m   .' .._|/     .-''\"'-.  `. .--.\033[0m     .|  '   '. /'   /   ")
    print("\033[1;94m   | '   /     /________\\   \\|  |\033[0m   .' |_ |    |'    /    ")
    print("\033[1;94m __| |__ |                  ||  |\033[0m .'     ||    ||    |    ")
    print("\033[1;94m|__   __|\\    .-------------'|  |\033[0m'--.  .-''.   `'   .'    ")
    print("\033[1;94m   | |    \\    '-.____...---.|  |\033[0m   |  |   \\        /     ")
    print("\033[1;94m   | |     `.             .' |__|\033[0m   |  |    \\      /      ")
    print("\033[1;94m   | |       `''-...... -'\033[0m          |  '.'   '----'       ")
    print("\033[1;94m   | |\033[0m                              |   /                 ")
    print("\033[1;94m   |_|\033[0m                              `'-'                  ")