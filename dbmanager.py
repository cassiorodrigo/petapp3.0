# from mysql.connector import connect
import os
import MySQLdb
import sshtunnel

sshtunnel.TUNNEL_TIMEOUT = 5.0
sshtunnel.SSH_TIMEOUT = 5.0

class Conexao:
    database = os.getenv('tabelahorasdb')
    senha_db = os.getenv('senhadb')
    route_db = os.getenv('routedb')
    user_name = 'PetPark'
    def conectar(self, query=None):
        with sshtunnel.SSHTunnelForwarder(
            'ssh.pythonanywhere.com',
            ssh_username=self.user_name,
            ssh_password=self.senha_db,
            remote_bind_address=(self.route_db, 3306)
        ) as tunnel:
            connection = MySQLdb.connect(
                user=self.user_name,
                passwd=self.senha_db,
                host="127.0.0.1",
                port=tunnel.local_bind_port,
                db="PetPark$horas_trabalhadas"
            )
            cursor = connection.cursor()
            criacao_tabela_usuarios = """
            CREATE FUNCIONARIOS IF NOT EXISTS(
            _ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME VARCHAR(100),
            SOBRENOME VARCHAR(255),
            EMAIL VARCHAR(255)
            )
            """
            criacao_tabela_senhas="""
            CREATE SENHAS IF NOT EXISTS(
            _ID INTEGER PRIMARY KEY AUTOINICREMENT,
            SENHA VARCHAR(255)
            )
            """
            resposta = cursor.execute(query)
            print(resposta)
            connection.close()


class Usuario:

    def regitrar_usuario(self, nome, email, usuario, senha):
        pass


class Caes:

    def registrar_presenca(self, cao, dono):
        pass

if __name__ == '__main__':
    conn = Conexao()
    conn.conectar()
