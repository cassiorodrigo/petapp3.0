from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.button import Button

class Gerenciador(ScreenManager):
    pass


class BaseScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once()


class Login(Screen):
    pass


class NewUser(Screen):
    pass


class Menu(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.entrar)

    def entrar(self, dttime):
        botoes = {'Chegadas': 'chegadas', 'Hotel':'hotel', 'Creche': 'creche', 'Day Care': 'daycare'}
        for key, value in botoes.items():
            btn1 = Button(text=key, on_release=lambda x: (self.callbtn(botoes[x.text])))
            _btn = self.ids.gridmenu.add_widget(btn1)
            # btn = self.ids.gridmenu.add_widget(Button(text=f'{key}'))
            # btn.bind(on_release=lambda x: self.callbtn(print(value)))

    def callbtn(self, nome_screen):
        print(nome_screen)
        self.manager.current = nome_screen


class PresencasHotel(Screen):
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
    def on_pause(self):
        return True

    def build(self):
        logged = None
        popadddog = None
        ger = Gerenciador()
        ger.add_widget(Login(name='login'))
        ger.add_widget(NewUser(name='newuser'))
        ger.add_widget(PresencasHotel(name='presencas'))
        ger.add_widget(Chegadas(name='chegadas'))
        ger.add_widget(Menu(name='menu'))


if __name__ == '__main__':
    aplicativo = DogsApp()
    aplicativo.run()
