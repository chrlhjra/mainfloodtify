from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.config import Config
from kivy_garden.graph import LinePlot
from kivy.clock import Clock
import pyrebase
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')





class SplashScreen(Screen):
	pass

class Onboarding(Screen):
	pass

class Home(Screen):
    pass

class ChuchuApp(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.value = 0
		self.date = ''
		self.screen = None
		self.touched = ''
		self.sm = ScreenManager(transition = FadeTransition())
		self.stream = None
		self.mid = 29
		self.high = 49
		self.counter = 0
		self.root = self.sm
		self.xmax = 60
		self.low_color = (13/255, 95/255, 7/255, 1)
		self.mid_color = (95/255, 82/255, 7/255, 1)
		self.high_color = (95/255, 7/255, 28/255, 1)
		self.plot_color = self.low_color
		self.img_url = 'images/dribbble-loader-green.gif'
		config = {
			"apiKey": "AIzaSyAbn0O55Rl5ndKYYgM3tIw1z0Ut4kqPRtY",
			"authDomain": "floodtify.firebaseapp.com",
			"databaseURL": "https://floodtify-default-rtdb.firebaseio.com",
			"projectId": "floodtify",
			"storageBucket": "floodtify.appspot.com",
			"messagingSenderId": "1064857342609",
			"appId": "1:1064857342609:web:c2cba06784d4f404566530",
			"measurementId": "G-7RX9RNTT2B"
		}
		firebase = pyrebase.initialize_app(config)
		self.db = firebase.database()
		self.auth = firebase.auth()

	def stream_handler(self, message):
		self.update_val(message['data']['area'], message['data']['date'], message['data']['image'])
	def format_time(self, date):
		time_from_date = date.split('_')[1]
		hour = int(time_from_date.split('-')[0])
		minute = time_from_date.split('-')[1]
		time_indicator = 'AM'
		if hour > 12:
			hour = str(hour - 12)
			time_indicator = 'PM'
		formatted_time = f"{hour}:{minute}-{time_indicator}"
		return formatted_time
	def format_date(self, date):
		date_from_date = date.split('_')[0]
		month = date_from_date.split('-')[0]
		day = date_from_date.split('-')[1]
		year = date_from_date.split('-')[2]
		formatted_date = f"{month}/{day}/{year}"
		return formatted_date
	def update_val(self, value, date, img_url):
		card = self.root.get_screen('home').ids.card
		value_label = self.root.get_screen('home').ids.value
		description = self.root.get_screen('home').ids.desc
		time_label = self.root.get_screen('home').ids.time
		formatted_time = self.format_time(date)
		self.value = value
		self.date = date
		if value > 0 and value <= self.mid:
			description.text = 'Low'
			description.color = self.low_color
			self.plot_color = self.low_color
			card.md_bg_color = 210/255, 251/255, 208/255, 1
		elif value > self.mid and value <= self.high:
			description.text = 'Caution'
			description.color = self.mid_color
			self.plot_color = self.mid_color
			card.md_bg_color = 251/255, 245/255, 208/255, 1
		elif value > self.high:
			description.text = 'Danger'
			description.color = self.high_color
			self.plot_color = self.high_color
			card.md_bg_color = 251/255, 208/255, 218/255, 1
		value_label.color = description.color
		value_label.text = f"{value}%"
		time_label.text = formatted_time
		self.img_url = img_url
		self.graph.background_color = card.md_bg_color
		self.plot.points.append((self.counter, value))
		self.graph.label_options.color = description.color
		self.counter += 1
		Clock.schedule_once(self.set_axis_color)
		self.graph.add_plot(self.plot)
		Clock.schedule_once(self.add_history_list)
		if len(self.plot.points) > self.xmax:
			self.plot.points = self.plot.points[1:]
			self.graph.xmax += 1
			self.graph.xmin += 1
			Clock.schedule_once(self.remove_last_history_list)
	def set_axis_color(self, dt):
		self.graph.border_color = self.plot_color
	def add_history_list(self, dt):
		history_list = self.root.get_screen('home').ids.history_list
		one_list_item = OneLineListItem()
		his_val_label = MDLabel(text=f"{self.value}%", pos_hint = {"center_x": .55, "center_y": .55}, font_name='Fonts/Poppins-SemiBold.ttf', font_size=16)
		his_date_label = MDLabel(text=f"{self.format_date(self.date)} {self.format_time(self.date)}", pos_hint = {"center_x": 1, "center_y": .55}, font_name='Fonts/Poppins-Regular.ttf', font_size=16)
		one_list_item.add_widget(his_val_label)
		one_list_item.add_widget(his_date_label)
		history_list.add_widget(one_list_item, index=-1)
	def remove_last_history_list(self, dt):
		history_list = self.root.get_screen('home').ids.history_list
		history_list.remove_widget(history_list.children[-1])
	def on_start(self):
		self.sm.current = 'splash'
		Clock.schedule_once(self.change_screen, 2)
	def on_request_close(self, *args):
		self.stream.close()
	def change_screen(self, dt):
		self.sm.current = 'home'
	def build(self):
		# screen_width = Window.size[0]
		# screen_height = Window.size[1]
		
		Window.size = (421, 939)



		Builder.load_file('kivy_files/splashscreen.kv')
		Builder.load_file('kivy_files/onboarding.kv')
		Builder.load_file('kivy_files/home.kv')
		self.theme_cls.primary_palette = "Cyan"

		self.sm.add_widget(SplashScreen(name='splash'))
		self.sm.add_widget(Home(name='home'))
		self.stream = self.db.child('data').stream(self.stream_handler)
		Window.bind(on_request_close=self.on_request_close)
		
		self.plot = LinePlot(line_width=1.2, color=[0,0,0,1])
		self.graph = self.root.get_screen('home').ids.graph
		self.graph.add_plot(self.plot)
		self.graph.xlabel = 'Time'
		self.graph.x_ticks_minor = 1
		self.graph.x_ticks_major = 10
		self.graph.x_grid_label = True
		self.graph.xmin = 0
		self.graph.xmax = self.xmax

		Clock.schedule_interval(self.update_image_source, 10.0)
		return self.sm
	
	def update_image_source(self, dt):
		my_image = self.root.get_screen('home').ids.my_image
		my_image.source = self.img_url
	
		
if __name__ == '__main__':
	ChuchuApp().run()

