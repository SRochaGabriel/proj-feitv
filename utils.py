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

def printOpts(opt_layout):
    if opt_layout == 'gerais':
        print('\nI - Página inicial    F - Favoritos    P - Minhas playlists    Q - Buscar    E - Enviar vídeo    U - Meu perfil    S - Sair da conta')
        return ['I', 'F', 'P', 'Q', 'E', 'U', 'S']
    else:
        print('C - Cadastrar    L - Efetuar login    S - Sair do FeiTV')
        return ['C', 'L', 'S']

def printVideosTable(table_type, table_data):
    headers = ['TÍTULO', 'DURACAO', 'ENVIADO POR', 'DATA DE ENVIO', 'LIKES', 'DISLIKES']
    campos = ['titulo', 'duracao', 'uploader', 'data_envio', 'likes', 'dislikes']

    if len(table_data) == 0: return print('Nada a ver aqui por enquanto...')

    if table_type == 'recentes':
        table_data.reverse()
        table_data = table_data[:10]
    
    tamanhos_coluna = [35, 10, 35, 15, 10, 10]

    for linha in range(len(table_data)):
        if linha == 0:
            print('\033[1;94m|\033[0m', end='')
            for i in range(len(tamanhos_coluna)):
                print(f'\033[0;33m{headers[i]:^{tamanhos_coluna[i]}}\033[0m', end='\033[1;94m|\033[0m')
            print()
            for i in range(122): print('\033[1;94m#\033[0m', end='')
            print()
        
        print('\033[1;94m|\033[0m', end='')
        for i in range(len(tamanhos_coluna)):
            if len(str(table_data[linha][campos[i]])) > 14: 
                table_data[linha][campos[i]] = table_data[linha][campos[i]][:27] + '...'

            print(f'{table_data[linha][campos[i]]:^{tamanhos_coluna[i]}}', end='\033[1;94m|\033[0m')
        print()

def getUsers():
    with open('./data/users.txt', 'r') as f:
        try:
            return ast.literal_eval(f.read())
        except: return []

def getVideos():
    with open('./data/videos.txt', 'r') as f:
        try:
            return ast.literal_eval(f.read())
        except: return []

def uploadVideo(user):
    print('Vamos pedir as informações dos vídeos que você quer registrar na plataforma. Para cancelar, envie "SAIR"')
    titulo, descricao, horas, minutos, segundos = '', '', 0, 0, 0
    
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
        "titulo": titulo,
        "descricao": descricao,
        "duracao": duracao,
        "data_envio": datetime.date.today().strftime('%d/%m/%Y'),
        "likes": 0,
        "dislikes": 0,
        "uploader": user
    }

    videos = getVideos()
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
        print('\n\033[1;97m################################################## VÍDEOS MAIS RECENTES ##################################################\033[0m')
        print()
        printVideosTable('recentes', getVideos())
        opcoes = printOpts('gerais')

    opt = input().upper()
    while opt not in opcoes:
        print('\033[1;91mOpção inválida, escolha entre as opções disponíveis de acordo com a ação desejada\033[0m')
        opt = input().upper()
        
    return opt

def perfil(username):
    clear()
    printLogo()
    videos = getVideos()
    user_videos = list(filter(lambda video: video['uploader'] == username, videos))

    print('\n\033[1;97m####################################################### MEUS ENVIOS ######################################################\033[0m')
    print()
    printVideosTable('recentes', user_videos)



    opt = input()

def cadastro():
    clear()
    printLogo()

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

    new_user = {"nome": username, "email": email, "senha":senha, "criacao":datetime.date.today.strftime('%d/%m/Y')}
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