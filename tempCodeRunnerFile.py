
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