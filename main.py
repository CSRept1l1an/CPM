from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.animation import Animation


class GradientWidget(Widget):
    def __init__(self, **kwargs):
        super(GradientWidget, self).__init__(**kwargs)
        self.color_1 = (0.5, 0, 0.5, 1)
        self.color_2 = (0.5, 0, 0.5, 1)
        self.color_3 = (0.5, 0, 0.5, 1)
        self.anim_duration = 5
        with self.canvas.before:
            self.rect1 = Rectangle(pos=self.pos, size=(self.width, self.height))
            self.bind(pos=self.update_rect, size=self.update_rect)
            self.update_texture()

    def update_rect(self, instance, value):
        self.rect1.pos = instance.pos
        self.rect1.size = (instance.width, instance.height)

    def update_texture(self):
        self.rect1.texture = self.get_texture(self.color_1)

    @staticmethod
    def get_texture(color):
        texture = Texture.create(size=(1, 1))
        buf = bytes([int(c * 255) for c in color])
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.add_widget(GradientWidget())
        self.dark_theme = False
        layout = BoxLayout(orientation='vertical', padding=(40, 40, 40, 40), spacing=20)
        self.logo_label = Label(text='XTI Mobile', font_size='24sp', color=(1, 1, 1, 1), size_hint=(1, 0.2))
        layout.add_widget(self.logo_label)
        self.username_input = TextInput(hint_text='Имя пользователя', multiline=False, size_hint=(0.8, None), height=40, pos_hint={'center_x': 0.5})
        layout.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Пароль', password=True, multiline=False, size_hint=(0.8, None), height=40, pos_hint={'center_x': 0.5})
        layout.add_widget(self.password_input)
        self.login_button = Button(text='Войти', size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        self.login_button.bind(on_press=self.login)
        layout.add_widget(self.login_button)
        self.message_label = Label(size_hint=(1, None), height=40)
        layout.add_widget(self.message_label)
        self.add_widget(layout)
        self.animate_elements()

    def animate_elements(self):
        for widget in self.children:
            widget.opacity = 0
            Animation(opacity=1, duration=0.5).start(widget)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.logo_label.color = (1, 0.2, 0.2, 1)
            self.username_input.background_color = (0.2, 0.2, 0.2, 1)
            self.password_input.background_color = (0.2, 0.2, 0.2, 1)
            self.login_button.background_color = (0.8, 0.2, 0.2, 1)
            self.message_label.color = (1, 0, 0, 1)
        else:
            self.logo_label.color = (0, 0.5, 1, 1)
            self.username_input.background_color = (1, 1, 1, 1)
            self.password_input.background_color = (1, 1, 1, 1)
            self.login_button.background_color = (0, 0.5, 1, 1)
            self.message_label.color = (0, 0, 0, 1)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == 'kali' and password == 'root':
            self.message_label.text = 'Вход выполнен успешно!'
            self.message_label.color = (0, 1, 0, 1)
            app = App.get_running_app()
            app.root.current = 'main_page'
            anim = Animation(color=(1, 1, 1, 1), background_color=(1, 1, 1, 1))
            anim.cancel(self.login_button)  # Остановка анимации кнопки входа
        else:
            self.message_label.text = 'Ошибка аутентификации'
            self.message_label.color = (1, 0, 0, 1)

            anim = Animation(color=(1, 0, 0, 1)) + Animation(color=(0, 0, 0, 1))
            anim.start(self.message_label)

            anim = Animation(background_color=(1, 0, 0, 1)) + Animation(background_color=(1, 1, 1, 1))
            anim.repeat = True
            anim.cancel(self.login_button)  # Остановка предыдущей анимации
            anim.start(self.login_button)


class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)

        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)
        self.add_top_bar()

        with self.layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(size=(Window.width, Window.height), pos=self.layout.pos)
            self.layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        self.menu_button = Button(text='≡', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'top': 1})
        self.menu_button.bind(on_press=self.toggle_menu)
        self.layout.add_widget(self.menu_button)

        self.menu = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200, pos_hint={'x': -1})
        self.menu.add_widget(Label(text='Меню', color=(1, 1, 1, 1)))
        self.menu.add_widget(Button(text='Dashboard'))
        self.menu.add_widget(Button(text='Alert', on_press=self.switch_to_alert))
        self.menu.add_widget(Button(text='About', on_press=self.switch_to_about))
        quit_button = Button(text='Quit')
        quit_button.bind(on_press=self.quit_app)
        self.menu.add_widget(quit_button)
        self.layout.add_widget(self.menu)

        message_label = Label(text='Добро пожаловать на главную страницу!', size_hint=(1, 1), color=(0, 0, 1, 1),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(message_label)

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.layout.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)

        xti_app_label = Label(text='XTI App', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_menu(self, instance):
        if self.menu.pos_hint['x'] == -1:
            anim = Animation(pos_hint={'x': 0}, duration=0.3)
        else:
            anim = Animation(pos_hint={'x': -1}, duration=0.3)
        anim.start(self.menu)

    @staticmethod
    def switch_to_alert(instance):
        app = App.get_running_app()
        app.root.current = 'alert_page'

    @staticmethod
    def switch_to_about(instance):
        app = App.get_running_app()
        app.root.current = 'about_page'

    @staticmethod
    def quit_app(instance):
        App.get_running_app().stop()


class AlertPage(Screen):
    def __init__(self, **kwargs):
        super(AlertPage, self).__init__(**kwargs)

        self.rect = None
        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)
        self.add_top_bar()

        with self.layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(size=(Window.width, Window.height), pos=self.layout.pos)
            self.layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        self.menu_button = Button(text='≡', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'top': 1})
        self.menu_button.bind(on_press=self.toggle_menu)
        self.layout.add_widget(self.menu_button)

        self.menu = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200, pos_hint={'x': -1})
        self.menu.add_widget(Label(text='Меню', color=(1, 1, 1, 1)))
        self.menu.add_widget(Button(text='Dashboard', on_press=self.switch_to_main))
        self.menu.add_widget(Button(text='Alert'))
        self.menu.add_widget(Button(text='About', on_press=self.switch_to_about))
        quit_button = Button(text='Quit')
        quit_button.bind(on_press=self.quit_app)
        self.menu.add_widget(quit_button)
        self.layout.add_widget(self.menu)

        message_label = Label(text='Это страница Alert', size_hint=(1, 1), color=(1, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(message_label)

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.layout.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1,0, 0, 1)  # Red color
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)

        xti_app_label = Label(text='XTI App', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_menu(self, instance):
        if self.menu.pos_hint['x'] == -1:
            anim = Animation(pos_hint={'x': 0}, duration=0.3)
        else:
            anim = Animation(pos_hint={'x': -1}, duration=0.3)
        anim.start(self.menu)

    @staticmethod
    def switch_to_main(instance):
        app = App.get_running_app()
        app.root.current = 'main_page'

    @staticmethod
    def switch_to_about(instance):
        app = App.get_running_app()
        app.root.current = 'about_page'

    @staticmethod
    def quit_app(instance):
        App.get_running_app().stop()


class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)

        self.rect = None
        self.top_bar = None
        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)

        self.add_top_bar()

        with self.layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(size=(Window.width, Window.height), pos=self.layout.pos)
            self.layout.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        self.menu_button = Button(text='≡', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'top': 1})
        self.menu_button.bind(on_press=self.toggle_menu)
        self.layout.add_widget(self.menu_button)

        self.menu = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200, pos_hint={'x': -1})
        self.menu.add_widget(Label(text='Меню', color=(1, 1, 1, 1)))
        self.menu.add_widget(Button(text='Dashboard', on_press=self.switch_to_main))
        self.menu.add_widget(Button(text='Alert', on_press=self.switch_to_alert))
        self.menu.add_widget(Button(text='Home', on_press=self.switch_to_main))



        quit_button = Button(text='Quit')
        quit_button.bind(on_press=self.quit_app)
        self.menu.add_widget(quit_button)
        self.layout.add_widget(self.menu)

        about_scroll = ScrollView(size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        about_text = (
            "Команда Ibrahim, Xadica и Telman участвует в хакатоне с целью разработки нового мобильного приложения "
            "для управления личными финансами. Мы стремимся к созданию удобного и интуитивно понятного интерфейса, "
            "который поможет пользователям эффективно управлять своими финансами в повседневной жизни."
        )
        about_label = Label(
            text=about_text,
            size_hint=(1, None),
            color=(0, 0, 0, 1)
        )
        about_label.bind(texture_size=about_label.setter('size'))
        about_scroll.add_widget(about_label)
        self.layout.add_widget(about_scroll)

    def update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.layout.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)

        xti_app_label = Label(text='XTI App', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def toggle_menu(self, instance):
        if self.menu.pos_hint['x'] == 0:
            anim = Animation(pos_hint={'x': -1}, duration=0.3)
        else:
            anim = Animation(pos_hint={'x': 0}, duration=0.3)
        anim.start(self.menu)

    @staticmethod
    def switch_to_main(instance):
        app = App.get_running_app()
        app.root.current = 'main_page'

    @staticmethod
    def switch_to_alert(instance):
        app = App.get_running_app()
        app.root.current = 'alert_page'

    @staticmethod
    def quit_app(instance):
        App.get_running_app().stop()


class AuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login_page'))
        sm.add_widget(MainPage(name='main_page'))
        sm.add_widget(AlertPage(name='alert_page'))
        sm.add_widget(AboutPage(name='about_page'))
        return sm


if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    AuthApp().run()

