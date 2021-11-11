from requisicoes import RequisicoesFunc


def validate_email_basic(email):
    validator = 0
    if len(email) > 9:
        validator += 1
    if "." in email and "@" in email:
        validator += 1
    if validator == 2:
        return True
    else:
        return False


def validate_senha(senha):
    validator = 0
    especiais = "!@#$%¨&*()_+{`}^´[]~;><.,"
    for e in especiais:
        if e in senha:
            validator += 1
    if len(senha) > 3:
        validator += 1

    if validator == 2:
        return True
    else:
        return False


def validate_username(username):
    novarequisicao = RequisicoesFunc()
    resposta = novarequisicao.get_usernames()
    lista_users = resposta.json()
    if username in lista_users["logins"] or len(username) < 4:
        return False
    else:
        return True

