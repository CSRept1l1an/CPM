from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.garden.graph import Graph, LinePlot
from kivy.core.window import Window
import sqlite3


def create_graph(title, data, ylabel):
    graph = Graph(xlabel='Time', ylabel=ylabel, x_ticks_minor=5, x_ticks_major=25, y_ticks_minor=1,
                  y_ticks_major=5, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                  xmin=0, xmax=len(data) - 1, ymin=min(data), ymax=max(data))

    # Set the title color to blue
    graph.title_color = [0, 0, 1, 1]  # Blue color

    plot = LinePlot(line_width=2, color=[1, 0, 0, 1])
    plot.points = [(i, value) for i, value in enumerate(data)]
    graph.add_plot(plot)

    return graph


class GraphPage(Screen):
    def __init__(self, **kwargs):
        super(GraphPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.create_bandwidth_graph()
        self.create_cpu_graph()
        self.create_throughput_graph()
        self.add_widget(self.layout)

    def create_bandwidth_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, bandwidth_utilization FROM Network_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('Bandwidth Utilization', data, 'Bandwidth Utilization')
        self.layout.add_widget(graph)
        connection.close()

    def create_cpu_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, cpu_utilization FROM IT_Node_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('CPU Utilization', data, 'CPU Utilization')
        self.layout.add_widget(graph)
        connection.close()

    def create_throughput_graph(self):
        connection = sqlite3.connect('management.db')
        cursor = connection.cursor()
        cursor.execute('SELECT timestamp, throughput FROM Application_KPIs')
        data = [row[1] for row in cursor.fetchall()]
        graph = create_graph('Throughput', data, 'Throughput')
        self.layout.add_widget(graph)
        connection.close()


class AuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GraphPage(name='graph_page'))
        return sm


if __name__ == '__main__':
    Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Set background color to white
    AuthApp().run()
