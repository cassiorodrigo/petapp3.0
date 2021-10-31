from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.button import Button
from kivymd.uix.list import IRightBodyTouch, TwoLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
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
    pass


class NewUser(Screen):
    pass


class Menu(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.entrar)

    def entrar(self, dttime):
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
        if len(self.ids.scrolllist.children) == 0:
            for i in range(5):
                self.ids.scrolllist.add_widget(TwoItemWithCheck(text=f'Dog{i}', secondary_text='raça'))

    def caes_no_hotel(self):
        lista_caes_no_hotel = []
        for i in self.ids.scrolllist.children:
            if i.children[0].children[0].state == 'down':
                lista_caes_no_hotel.append(i.children[1].children[2].text)

        self.manager.current = 'menu'

        toast('Enviado com sucesso!', duration=3.5)

        return lista_caes_no_hotel


class AddCaoPop(BoxLayout):
    pass


class PresencasCreche(Screen):
    pass


class PresencasDayCare(Screen):
    pass


class Chegadas(Screen):
    pass


class AddDogManually(MDDialog):
    pass


class DogsApp(MDApp):
    dialog = None

    def show_add_dog_dialog(self, tela):
        if self.dialog:
            self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                title='Adicione o nome do Cão',
                type='custom',
                content_cls=AddCaoPop(),
                auto_dismiss=False,
                buttons=[
                    MDRoundFlatButton(
                        text='Cancelar',
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFillRoundFlatButton(
                        text='Ok',
                        on_release=lambda x: self.on_popok(tela)
                    )
                ]
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
        logged = None
        popadddog = None


if __name__ == '__main__':
    aplicativo = DogsApp()
    aplicativo.run()
