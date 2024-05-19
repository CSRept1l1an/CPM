import sqlite3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


class NetDataDisplay(App):
    def build(self):
        conn = sqlite3.connect('management.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Network_KPIs WHERE Category ='critical'")
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

        labels = ['ID', 'Timestamp', 'Bandwidth Utilization', 'Latency', 'Packet Loss', 'Network Errors',
                  'Network Availability', 'Status']
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


class ITDataDisplay(App):
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

        labels = ['ID, Timestamp', 'CPU Utilization', 'Memory Utilization', 'Disk IO', 'Disk Usage',
                  'System Uptime', 'Status']

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


class AppDataDisplay(App):
    def build(self):
        conn = sqlite3.connect('management.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Application_KPIs WHERE Category ='critical'")
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

        labels = ['ID, Timestamp', 'Response Time', 'Error Rate', 'Throughput', 'Resource Usage (CPU)',
                  'Resource Usage (Memory)', 'Database Performance (Query Execution Time)',
                  'Database Performance (Throughput)', 'Category']

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


if __name__ == '__main__':
    Window.size = (600, 600)
    AppDataDisplay().run()
    NetDataDisplay().run()
    ITDataDisplay().run()
