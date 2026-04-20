import ast
import datetime
import os

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

def printOpts(opt_layout, videoIds = 0):
    opcoes = []

    if opt_layout == 'gerais':
        print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Enviar vídeo    U - Meu perfil    S - Sair da conta')
        opcoes = ['I', 'F', 'P', 'Q', 'E', 'U', 'S']
    elif opt_layout == 'perfil':
        print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Editar informações    D - Deletar conta    S - Sair da conta')
        opcoes = ['I', 'F', 'P', 'Q', 'E', 'D', 'S']
    elif opt_layout == 'playlists':
        print('\nI - Página inicial    F - Favoritos    Q - Buscar    C - Criar playlist    U - Meu perfil    S - Sair da conta')
        opcoes = ['I', 'F', 'Q', 'C', 'U', 'S']
    else:
        print('C - Cadastrar    L - Efetuar login    S - Sair do FeiTV')
        opcoes = ['C', 'L', 'S']

    if videoIds != 0:
            for id in videoIds:
                opcoes.append(id)

    return opcoes

def printVideosTable(table_type, table_data):
    headers = ['ID', 'TÍTULO', 'DURACAO', 'ENVIADO POR', 'DATA DE ENVIO', 'LIKES', 'DISLIKES']
    campos = ['id', 'titulo', 'duracao', 'uploader', 'data_envio', 'likes', 'dislikes']

    if len(table_data) == 0:
        print('Nada a ver aqui por enquanto...')
        return 0

    if table_type == 'recentes':
        table_data.reverse()
        table_data = table_data[:10]
    
    tamanhos_coluna = [5, 35, 10, 35, 15, 10, 10]

    for linha in range(len(table_data)):
        if linha == 0:
            print('\033[1;94m|\033[0m', end='')
            for i in range(len(tamanhos_coluna)):
                print(f'\033[0;33m{headers[i]:^{tamanhos_coluna[i]}}\033[0m', end='\033[1;94m|\033[0m')
            print()
            for i in range(128): print('\033[1;94m#\033[0m', end='')
            print()
        
        print('\033[1;94m|\033[0m', end='')
        for i in range(len(campos)):
            if len(str(table_data[linha][campos[i]])) > 30: 
                table_data[linha][campos[i]] = table_data[linha][campos[i]][:27] + '...'

            print(f'{table_data[linha][campos[i]]:^{tamanhos_coluna[i]}}', end='\033[1;94m|\033[0m')
        print()
    
    ids = []
    for video in table_data:
        ids.append(video['id'])

    return ids

def getUsers():
    with open('./data/users.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

def getVideos():
    with open('./data/videos.txt', 'r') as f:
        try: return ast.literal_eval(f.read())
        except: return []

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
    print('Vamos pedir as informações dos vídeos que você quer registrar na plataforma. Para cancelar, envie "SAIR"')
    titulo, descricao, horas, minutos, segundos = '', '', 0, 0, 0
    videos = getVideos()
    
    while titulo == '':
        titulo = input('Insira o título do vídeo (obrigatório): ')
    if titulo.upper() == 'SAIR': return 

    descricao = input('Insira a descrição do vídeo (opcional): ')
    if descricao.upper() == 'SAIR': return 

    horas = input('Quantas horas o vídeo possui? ')
    if horas.upper() == 'SAIR': return 

    minutos = input('Quantos minutos o vídeo possui? ')
    if minutos.upper() == 'SAIR': return 

    segundos = input('Quantos segundos o vídeo possui? ')
    if segundos.upper() == 'SAIR': return 

    duracao = formataDuracao(horas, minutos, segundos)

    video = {
        "id": str(len(videos) + 1),
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

def init(auth_status):
    clear()
    printLogo()

    opt = ''

    if auth_status == False:
        print('\nBem-vindo ao sistema da \033[1;94mFei\033[0mTV! Por favor, selecione uma das opções abaixo')
        opcoes = printOpts('opcoes_sem_login')
    else:
        print('\n\033[1;97m##################################################### VÍDEOS MAIS RECENTES #####################################################\033[0m')
        print()
        videoIds = printVideosTable('recentes', getVideos())
        opcoes = printOpts('gerais', videoIds)

    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
        
    return opt

def criarPlaylist(username):
    print('\033[1;94mPara cancelar o processo de criar uma nova playlist, digite e envie 0.\033[0m')
    n_playlist = ''
    userPlaylists = getUserPlaylists(username)
    playlists = getAllPlaylists()

    while n_playlist == '':
        n_playlist = input('\033[1;94mInforme o nome da playlist a ser criada: \033[0m')
        for playlist in userPlaylists:
            if playlist['nome'] == n_playlist:
                print('\033[1;91mVocê já possui uma playlist com esse nome.\033[0m')
                n_playlist = ''
    if n_playlist == '0': return

    playlist = {"id": len(playlists) + 1, "user": username, "nome": n_playlist, "videos": []}

    playlists.append(playlist)
    with open('./data/playlists.txt', 'w') as f: f.write(str(playlists))

def playlists(username):
    clear()
    printLogo()
    print('\n\033[1;97m####################################################### MINHAS PLAYLISTS ######################################################\033[0m')
    print()
    playlists = getUserPlaylists(username)

    if len(playlists) == 0: print('Nada a ver aqui por enquanto...')
    else:
        print(f'\033[1;94m| {'ID':^10} | {'NOME':^100} |\033[0m')
        for i in range(117): print('\033[1;94m+\033[0m', end='')
        print()
        for i in range(len(playlists)):
            print(f'\033[1;94m|\033[0m {i + 1:^10} \033[1;94m|\033[0m {playlists[i]['nome']:^100} \033[1;94m|\033[0m')
        
        print('\nPara selecionar uma playlist, envie o número de ID dela')
    
    opcoes = printOpts('playlists', len(playlists))

    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
    return opt

def perfil(user):
    clear()
    printLogo()
    videos = getVideos()
    user_videos = list(filter(lambda video: video['uploader'] == user['nome'], videos))

    print('\n\033[1;97m########################################################## MEUS ENVIOS #########################################################\033[0m')
    print()
    videoIds = printVideosTable('recentes', user_videos)
    if videoIds != 0: print('\nPara selecionar um vídeo, digite e envie o número de ID do vídeo desejado')

    print(f'\n\033[1;94mNome de usuário:\033[0m {user['nome']}    \033[1;94mE-mail:\033[0m {user['email']}    \033[1;94mPerfil criado em:\033[0m {user['criacao']}')

    opcoes = printOpts('perfil', videoIds)
    
    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
        
    return opt

def deletarConta(user):
    users = getUsers()
    videos = getVideos()
    index = 0
    senha = ''

    while senha == '':
        senha = input('\033[1;94mInforme a senha para confirmar: \033[0m')
    
        if senha != user['senha']:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar o processo\033[0m')
            senha = ''
    if senha == '0': return 0

    for i in range(len(users)):
        if user['nome'] == users[i]['nome']: index = i
    users.pop(index)

    for i in range(len(videos)):
        if user['nome'] == videos[i]['uploader']: index = i
    videos.pop(index)

    with open('./data/users.txt', 'w') as f:
        f.write(str(users))

    with open('./data/videos.txt', 'w') as f:
        f.write(str(videos))

    return 1

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
        senha = input('\033[1;94mInforme a senha para confirmar: \033[0m')
    
        if senha != curr_user['senha']:
            print('\033[1;91mSenha incorreta. Tente novamente ou envie 0 para cancelar o processo\033[0m')
            senha = ''
    if senha == '0': return curr_user

    for i in range(len(users)):
        if curr_user['nome'] == users[i]['nome']:
            if username != '': users[i]['nome'] = username
            if email != '': users[i]['email'] = email
        
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
    print('\n''Para voltar para a tela inicial, digite e envie 0.')
    username, email, senha = '', '', ''
    users = getUsers()

    while username == '':
        username = input('Crie seu nome de usuário: ')

        for user in users:
            if user['nome'] == username:
                print('\033[1;91mNome de usuário já está em uso. Escolha um nome diferente.\033[0m')
                username = ''
    if username == '0': return {}, False 

    while email == '':
        email = input('Insira seu E-mail: ')

        for user in users:
            if user['email'] == email:
                print('\033[1;91mE-mail já cadastrado! Use outro e-mail ou digite 0 para sair do cadastramento.\033[0m')
                email = ''
    if email == '0': return {}, False

    while senha == '':
        senha = input('Crie uma senha: ')
    if senha == '0': return {}, False

    new_user = {"nome": username, "email": email, "senha":senha, "criacao":datetime.date.today().strftime('%d/%m/%Y')}
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
        email = input('Digite seu e-mail: ')
    if email == '0': return {}, False

    while senha == '':
        senha = input('Digite sua senha: ')
    if senha == '0': return {}, False

    users = getUsers()
    for user in users:
        if user['email'] == email and user['senha'] == senha:
            return user, True
    else:
        return login('\033[1;91mE-mail ou senha incorretos, tente novamente ou digite e envie 0 para retornar à tela inicial.\033[0m')

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