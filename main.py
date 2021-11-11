from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.button import Button
from kivymd.uix.list import IRightBodyTouch, TwoLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from requisicoes import Requisicoes, RequisicoesFunc
from datavalidators import validate_senha, validate_username, validate_email_basic
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.toast import toast


if platform == "android":
    from android.permissions import request_permissions, Permission
    from android import loadingscreen
    loadingscreen.hide_loading_screen()
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,
                         Permission.INTERNET])

Window.soft_inputmode = 'below_target'
meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
         'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


class Gerenciador(ScreenManager):
    pass


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class TwoItemWithCheck(TwoLineRightIconListItem):
    pass


class Login(Screen):
    def logar_usuario(self, usuario, senha):
        credentials = {"usuario": usuario,
                       "senha": senha}
        try:
            newreq = RequisicoesFunc()
            resultado = newreq.logar(credentials)
            # resultado = resultado.decode('UTF-8')
            if resultado == 'Credenciais Incorretas':
                toast("Usuario ou senha incorretos")
            else:
                toast(f'Bem vindo(a) {resultado["nome"][0]}')
                DogsApp.logged = resultado
                self.manager.current = 'menu'

        except Exception as err:
            print(err)
            toast(f"O Erro {err}\n\n ocorreu. Comunique imediatamente.")


class NewUser(Screen):

    def verificar_senhas_coincidem(self, senha, confirmacao):
        if senha != confirmacao:
            return False
        elif senha == confirmacao:
            return True

    def popular(self):
        self.ids.nome.text = "Cassio"
        self.ids.username_cadastro.text = "digo"
        self.ids.email.text = "cassiorodrigo@gmail.com"
        self.ids.senha_cadastro.text = "Digo1660!"
        self.ids.confirma_senha.text = "Digo1660!"

    def cadastrar_novo_usuario(self, nome, usuario, email, senha, confirma_senha):
        valemail, valuser, valsenha = validate_email_basic(email), validate_username(usuario), validate_senha(senha)

        if not valemail:
            self.ids.email.error = True
            self.ids.email.helper_text = "Digite um email válido"
            self.ids.email.helper_text_mode = "on_error"
        if not valuser:
            self.ids.username_cadastro.error = True
            self.ids.username_cadastro.helper_text = "Digite um nome de usuário válido"
            self.ids.username_cadastro.helper_text_mode = "on_error"
        if not valsenha:
            self.ids.senha_cadastro.error = True
            self.ids.senha_cadastro.helper_text = "Digite uma senha válida"
            self.ids.senha_cadastro.helper_text_mode = "on_error"
        if senha == confirma_senha:
            conferem = True
        else:
            self.ids.confirma_senha.error = True
            self.ids.confirma_senha.helper_text = "Senhas não conferem!"
            self.ids.confirma_senha.helper_text_mode = "on_error"
            conferem = False
        if conferem and valemail and valuser and valsenha:
            pacote = {
                "email": email,
                "username": usuario,
                "senha": senha,
                "nome": nome
            }
            novarequisicao = RequisicoesFunc()
            resultado = novarequisicao.criar_cadastro(pacote)
            if resultado.status_code == 201:
                toast("Usuário cadastrado com sucesso")
                self.manager.current = "menu"
                DogsApp.logged = usuario


class Menu(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.entrar)

    def entrar(self, dttime):
        DogsApp.show_add_dog_dialog(DogsApp(), tela=self)
        if len(self.ids.gridmenu.children) == 0:
            botoes = {'Chegadas': 'chegadas', 'Hotel':'hotel', 'Creche': 'creche', 'Day Care': 'daycare'}
            for key, value in botoes.items():
                btn1 = Button(text=key, on_release=lambda x: (self.callbtn(botoes[x.text])))
                _btn = self.ids.gridmenu.add_widget(btn1)

    def callbtn(self, nome_screen):
        print(nome_screen)
        self.manager.current = nome_screen


class PresencasHotel(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.entrar)

    def entrar(self, dttime):
        novareq = Requisicoes()
        listacaes = novareq.caes_ativos()
        if len(self.ids.scrolllist.children) == 0:
            for i in listacaes:
                self.ids.scrolllist.add_widget(TwoItemWithCheck(text=f'{i["NOME_CAO"]} ({i["RACA"]})',
                                                                secondary_text=f'{i["TUTOR"]}'))

    def caes_no_hotel(self):
        lista_caes_no_hotel = []

        for i in self.ids.scrolllist.children:
            if i.children[0].children[0].state == 'down':
                lista_caes_no_hotel.append(i.children[1].children[2].text)

        try:
            resposta = {"hotel":lista_caes_no_hotel, "funcionario": DogsApp.logged}
            novarequ = Requisicoes()
            novarequ.postar_caes_hotel(resposta)
            self.manager.current = 'menu'
            toast('Enviado com sucesso!', duration=3.5)
        except Exception as err:
            toast(f"Algo deu errado: {err}")
        return lista_caes_no_hotel

    def on_leave(self, *args):
        self.ids.scrolllist.clear_widgets()


class AddCaoPop(BoxLayout):
    pass


class PresencasCreche(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.popular_lista)

    def popular_lista(self, ddtime):
        novareq = Requisicoes()
        listacaes = novareq.caes_ativos()
        for i in listacaes:
            self.ids.scrolllist.add_widget(TwoItemWithCheck(text=f'{i["NOME_CAO"]} ({i["RACA"]})',
                                                            secondary_text=f'{i["TUTOR"]}'))

    def caes_na_creche(self):
        lista_caes_na_creche = []

        for i in self.ids.scrolllist.children:
            if i.children[0].children[0].state == 'down':
                lista_caes_na_creche.append(i.children[1].children[2].text)

        try:
            resposta = {"creche": lista_caes_na_creche, "funcionario": DogsApp.logged}
            novarequ = Requisicoes()
            novarequ.postar_caes_creche(resposta)
            self.manager.current = 'menu'
            toast('Enviado com sucesso!', duration=3.5)
        except Exception as err:
            toast(f"Algo deu errado: {err}")
        return lista_caes_na_creche

    def on_leave(self, *args):
        self.ids.scrolllist.clear_widgets()

class PresencasDayCare(Screen):
    pass


class Chegadas(Screen):
    pass


class Banhos(Screen):
    pass


class AddDogManually(MDDialog):
    pass


class DogsApp(MDApp):
    dialog = None
    logged = None

    def show_add_dog_dialog(self, tela):
        if self.dialog:
            self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                title='Adicione o nome do Cão',
                type='custom',
                content_cls=AddCaoPop(),
                auto_dismiss=False
                # buttons=[
                #     MDRoundFlatButton(
                #         text='Cancelar',
                #         on_release=lambda x: self.dialog.dismiss()
                #     ),
                #     MDFillRoundFlatButton(
                #         text='Ok',
                #         on_release=lambda x: self.on_popok(tela)
                #     )
                # ]
            )
            self.dialog.open()

    def on_popok(self, tela):

        for scrolllist in tela.ids:
            exec(f"tela.ids.{scrolllist}.add_widget("
                 f"TwoItemWithCheck(text=self.dialog.content_cls.ids.addcaopop.text,"
                 f"secondary_text='Adicionado Manualmente'))")

        self.dialog.dismiss()
    def on_pause(self):
        return True

    def build(self):
        self.logged = None
        popadddog = None


if __name__ == '__main__':
    aplicativo = DogsApp()
    aplicativo.run()
