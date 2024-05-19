import hashlib
import sqlite3

from kivy.uix.gridlayout import GridLayout

from criticalData import ITDataDisplay, NetDataDisplay, AppDataDisplay
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from GraPhics import create_graph


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

    def get_texture(self, color):
        texture = Texture.create(size=(1, 1))
        buf = bytes([int(c * 255) for c in color])
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture


class LoginPage(Screen):
    MAX_LOGIN_ATTEMPTS = 5

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.login_attempts = 0
        self.add_widget(GradientWidget())
        self.dark_theme = False
        layout = BoxLayout(orientation='vertical', padding=(40, 40, 40, 40), spacing=20)
        self.logo_label = Label(text='XTI Mobile', font_size='24sp', color=(1, 1, 1, 1), size_hint=(1, 0.2))
        layout.add_widget(self.logo_label)
        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint=(0.8, None), height=40,
                                        pos_hint={'center_x': 0.5})
        layout.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False, size_hint=(0.8, None),
                                        height=40, pos_hint={'center_x': 0.5})
        layout.add_widget(self.password_input)
        self.login_button = Button(text='Login', size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
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
        if self.login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            self.message_label.text = "Maximum login attempts reached. Please try again later."
            return

        username = self.username_input.text
        password = self.password_input.text

        # Hash the entered password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username == 'kali' and hashed_password == '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2':
            self.message_label.text = 'Login successful!'
            self.message_label.color = (0, 1, 0, 1)
            app = App.get_running_app()
            app.root.current = 'main_page'
            anim = Animation(color=(1, 1, 1, 1), background_color=(1, 1, 1, 1))
            anim.cancel(self.login_button)
        else:
            self.login_attempts += 1
            attempts_left = self.MAX_LOGIN_ATTEMPTS - self.login_attempts
            self.message_label.text = f'Authentication error. {attempts_left} attempts left.'
            self.message_label.color = (1, 0, 0, 1)

            anim = Animation(color=(1, 0, 0, 1)) + Animation(color=(0, 0, 0, 1))
            anim.start(self.message_label)

            anim = Animation(background_color=(1, 0, 0, 1)) + Animation(background_color=(1, 1, 1, 1))
            anim.repeat = True

            anim.cancel(self.login_button)
            anim.start(self.login_button)


def switch_to_cpu_graph_page(instance, touch):
    if touch.is_double_tap and instance.collide_point(*touch.pos):
        app = App.get_running_app()
        app.root.current = 'cpu_graph_page'


def switch_to_throughput_graph_page(instance, touch):
    if touch.is_double_tap and instance.collide_point(*touch.pos):
        app = App.get_running_app()
        app.root.current = 'throughput_graph_page'


def switch_to_about(instance):
    app = App.get_running_app()
    app.root.current = 'about_page'


def quit_app(instance):
    App.get_running_app().stop()


def switch_to_bandwidth_graph_page(instance, touch):
    if touch.is_double_tap and instance.collide_point(*touch.pos):
        app = App.get_running_app()
        app.root.current = 'bandwidth_graph_page'


def switch_to_alert(instance):
    app = App.get_running_app()
    app.root.current = 'alert_page'


class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)

        self.top_bar = None
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
        self.menu.add_widget(Label(text='Menu', color=(1, 1, 1, 1)))
        self.menu.add_widget(Button(text='Dashboard'))
        self.menu.add_widget(Button(text='Alert', on_press=switch_to_alert))
        self.menu.add_widget(Button(text='About', on_press=switch_to_about))
        quit_button = Button(text='Quit')
        quit_button.bind(on_press=quit_app)
        self.menu.add_widget(quit_button)
        self.layout.add_widget(self.menu)

        self.main_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 1),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.create_bandwidth_graph()
        self.create_cpu_graph()
        self.create_throughput_graph()

    def create_bandwidth_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, bandwidth_utilization FROM Network_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('Bandwidth Utilization', data, 'Bandwidth Utilization')

        graph_layout = BoxLayout(size_hint=(None, None), size=(400, 250), spacing=50, padding=50)
        graph_layout.add_widget(graph)
        graph_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.6}

        self.layout.add_widget(graph_layout)
        connection.close()

        graph_layout.bind(on_touch_down=switch_to_bandwidth_graph_page)

    def create_cpu_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, cpu_utilization FROM IT_Node_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('CPU Utilization', data, 'CPU Utilization')

        graph_layout = BoxLayout(size_hint=(None, None), size=(400, 250), spacing=50, padding=50)
        graph_layout.add_widget(graph)
        graph_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.4}

        self.layout.add_widget(graph_layout)
        connection.close()

        graph_layout.bind(on_touch_down=switch_to_cpu_graph_page)

    def create_throughput_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, throughput FROM Application_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('Throughput', data, 'Throughput')

        graph_layout = BoxLayout(size_hint=(None, None), size=(400, 250), spacing=50, padding=50)
        graph_layout.add_widget(graph)
        graph_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.2}

        self.layout.add_widget(graph_layout)
        connection.close()

        graph_layout.bind(on_touch_down=switch_to_throughput_graph_page)

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.layout.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)

        xti_app_label = Label(text='XTI App', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def add_vertical_layout(self, title, on_press_callback):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 0.33))
        button = Button(text=title, size_hint=(1, None), height=40)
        button.bind(on_press=on_press_callback)
        box.add_widget(button)
        self.main_layout.add_widget(box)

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


class NetworkPage(Screen):
    def __init__(self, **kwargs):
        super(NetworkPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text='Network Page'))
        back_button = Button(text='Back to Main Page', size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        back_button.bind(on_press=self.back_to_main)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def back_to_main(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_page'


class ITNodesPage(Screen):
    def __init__(self, **kwargs):
        super(ITNodesPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text='IT Nodes Page'))
        back_button = Button(text='Back to Main Page', size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        back_button.bind(on_press=self.back_to_main)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def back_to_main(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_page'


class AppPage(Screen):
    def __init__(self, **kwargs):
        super(AppPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text='App Page'))
        back_button = Button(text='Back to Main Page', size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        back_button.bind(on_press=self.back_to_main)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def back_to_main(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_page'


def switch_to_main(instance):
    app = App.get_running_app()
    app.root.current = 'main_page'


class AlertPage(Screen):
    def __init__(self, **kwargs):
        super(AlertPage, self).__init__(**kwargs)

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
        self.menu.add_widget(Label(text='Menu', color=(1, 1, 1, 1)))
        self.menu.add_widget(Button(text='Dashboard', on_press=switch_to_main))
        self.menu.add_widget(Button(text='Alert'))
        self.menu.add_widget(Button(text='About', on_press=switch_to_about))
        quit_button = Button(text='Quit')
        quit_button.bind(on_press=quit_app)
        self.menu.add_widget(quit_button)
        self.layout.add_widget(self.menu)

        message_label = Label(text='The Alert Page', size_hint=(1, 1), color=(1, 0, 0, 1),
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


class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)
        self.bg_rect = None
        self.menu = None
        self.add_background()
        self.add_top_bar()
        self.add_menu()
        self.add_about_content()

    def add_background(self):
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

    def update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def add_top_bar(self):
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        top_bar.add_widget(Label(text='XTI App', color=(1, 1, 1, 1), font_size='20sp'))
        self.add_widget(top_bar)

    def add_menu(self):
        menu_button = Button(text='≡', size_hint=(None, None), size=(50, 50))
        menu_button.bind(on_press=self.toggle_menu)
        self.add_widget(menu_button)

        menu = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200)
        menu.add_widget(Label(text='Меню', color=(1, 1, 1, 1)))
        menu.add_widget(Button(text='Dashboard', on_press=switch_to_main))
        menu.add_widget(Button(text='Alert', on_press=switch_to_alert))
        menu.add_widget(Button(text='Home', on_press=switch_to_main))
        quit_button = Button(text='Quit', on_press=quit_app)
        menu.add_widget(quit_button)
        self.add_widget(menu)

        self.menu = menu

    def toggle_menu(self, instance):
        if self.menu.x == 0:
            anim = Animation(x=-self.menu.width, duration=0.3)
        else:
            anim = Animation(x=0, duration=0.3)
        anim.start(self.menu)

    def add_about_content(self):
        about_scroll = ScrollView(size_hint=(None, None), size=(Window.width * 0.8, Window.height * 0.8),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        about_text = (
            "The team of Ibrahim, Xadica, and Telman is participating in a hackathon with the aim of developing a new mobile "
            "application for managing personal finances. We aspire to create a convenient and intuitively understandable interface "
            "that will help users efficiently manage their finances in everyday life.\n\n"
            "We pay special attention to the details and functionality of the application to provide our users with the best "
            "possible features. Our goal is to make financial planning accessible and simple for everyone.\n\n"
            "Join us on this exciting journey to create a new application that will help you better manage your finances and "
            "achieve your financial goals!"
        )

        about_label = Label(
            text=about_text,
            size_hint=(1, None),
            color=(0, 0, 0, 1)
        )
        about_label.bind(size=about_label.setter('text_size'))
        about_scroll.add_widget(about_label)
        self.add_widget(about_scroll)


def go_to_main_page(instance):
    app = App.get_running_app()
    app.root.current = 'main_page'


class BandwidthGraphPage(Screen):
    def __init__(self, **kwargs):
        super(BandwidthGraphPage, self).__init__(**kwargs)
        self.rect = None
        self.add_top_bar()

        # Add a label to the page
        self.add_widget(Label(text='Bandwidth Graph Page'))

        home_button = Button(size_hint=(None, None), size=(120, 70), pos=(10, self.height - 80),
                             background_normal='', background_color=(0, 0, 0, 0))
        home_button.bind(on_press=go_to_main_page)

        with home_button.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Gray color
            self.bg_rect = Rectangle(size=home_button.size, pos=home_button.pos)

        button_layout = BoxLayout(orientation='horizontal', spacing=5)

        home_button_image = Image(source='graph_icon.jpg', size_hint=(None, None), size=(40, 40))
        button_layout.add_widget(home_button_image)

        home_button_text = Label(text='Home', size_hint=(None, None), size=(60, 50), font_size=18)
        button_layout.add_widget(home_button_text)

        home_button.add_widget(button_layout)

        self.add_widget(home_button)

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)
        xti_app_label = Label(text='BandwidthGraphPage', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CPUGraphPage(Screen):
    def __init__(self, **kwargs):
        super(CPUGraphPage, self).__init__(**kwargs)
        self.rect = None
        self.top_bar = None
        self.add_top_bar()
        self.top_bar = None

        self.add_widget(Label(text='CPUGraphPage'))

        home_button = Button(size_hint=(None, None), size=(120, 70), pos=(10, self.height - 80),
                             background_normal='', background_color=(0, 0, 0, 0))
        home_button.bind(on_press=go_to_main_page)

        with home_button.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.bg_rect = Rectangle(size=home_button.size, pos=home_button.pos)

        button_layout = BoxLayout(orientation='horizontal', spacing=50)

        home_button_image = Image(source='graph_icon.jpg', size_hint=(None, None), size=(40, 40))
        button_layout.add_widget(home_button_image)

        home_button.add_widget(button_layout)

        self.add_widget(home_button)

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)
        xti_app_label = Label(text='CPUGraphPage', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ThroughputGraphPage(Screen):

    def add_top_bar(self):
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.add_widget(self.top_bar)

        with self.top_bar.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=self.top_bar.size, pos=self.top_bar.pos)
            self.top_bar.bind(size=self.update_rect, pos=self.update_rect)
        xti_app_label = Label(text='ThroughputGraphPage', color=(1, 1, 1, 1), font_size='20sp')
        self.top_bar.add_widget(xti_app_label)

    def __init__(self, **kwargs):
        super(ThroughputGraphPage, self).__init__(**kwargs)
        self.rect = None
        self.top_bar = None
        self.add_top_bar()

        self.add_widget(Label(text='Throughput Graph Page'))

        home_button = Button(size_hint=(None, None), size=(120, 70), pos=(10, self.height - 80),
                             background_normal='', background_color=(0, 0, 0, 0))
        home_button.bind(on_press=go_to_main_page)

        # Set button background color to gray
        with home_button.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.bg_rect = Rectangle(size=home_button.size, pos=home_button.pos)

        # Create a layout for button content
        button_layout = BoxLayout(orientation='horizontal', spacing=50)

        # Add image to the button layout
        home_button_image = Image(source='graph_icon.jpg', size_hint=(None, None), size=(40, 40))
        button_layout.add_widget(home_button_image)

        home_button.add_widget(button_layout)

        self.add_widget(home_button)

        data_layout = self.build()
        self.add_widget(data_layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def build(self):
        conn = sqlite3.connect('management.db')
        c = conn.cursor()

        c.execute("SELECT * FROM IT_Node_KPIs WHERE Category ='critical'")
        rows = c.fetchall()
        conn.close()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title_label = Label(
            text="Data Display",
            font_size='24sp',
            bold=True,
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        layout.add_widget(title_label)

        grid = GridLayout(cols=2, spacing=20, size_hint_y=None, padding=[10, 10, 10, 10])
        grid.bind(minimum_height=grid.setter('height'))

        labels = ['ID', 'Timestamp', 'CPU Utilization', 'Memory Utilization', 'Disk IO', 'Disk Usage', 'System Uptime',
                  'Status']

        for row in rows:
            for label, value in zip(labels, row):
                grid.add_widget(Label(
                    text=label,
                    font_size='18sp',
                    halign='left',
                    valign='middle',
                    size_hint_y=None,
                    height=40
                ))
                value_label = Label(
                    text=str(value),
                    font_size='18sp',
                    halign='left',
                    valign='middle',
                    size_hint_y=None,
                    height=40
                )
                value_label.bind(size=value_label.setter('text_size'))
                grid.add_widget(value_label)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(grid)

        layout.add_widget(scroll_view)

        return layout


class AuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login_page'))
        sm.add_widget(MainPage(name='main_page'))
        sm.add_widget(BandwidthGraphPage(name='bandwidth_graph_page'))  # Добавление BandwidthGraphPage
        sm.add_widget(CPUGraphPage(name='cpu_graph_page'))  # Добавление CPUGraphPage
        sm.add_widget(ThroughputGraphPage(name='throughput_graph_page'))  # Добавление ThroughputGraphPage
        sm.add_widget(AlertPage(name='alert_page'))
        sm.add_widget(AboutPage(name='about_page'))
        return sm


if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    AuthApp().run()
