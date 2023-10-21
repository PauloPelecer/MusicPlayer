import JyPyUI
from mutagen.mp3 import MP3
'''
Toda Vez Que Usar o JyPyUI comente #import pygame para que o JyPyUI possa usalo para criar seus elementos 
'''
#import pygame


class Music:
	def __init__(self):
		if os.path.exists('Music'):
			self.musics = os.listdir('Music')
			self.music_reverse = self.musics[::-1]
		else:
			os.mkdir('Music')
			Music()
		self.music = JyPyUI.Interface().app.mixer.music
		self.paused = False
		self.reverse = False
	def Play(self,count):
		if self.reverse:
			self.music.load(os.path.join('Music',self.music_reverse[count]))
			self.music.play()
		else:
			self.music.load(os.path.join('Music',self.musics[count]))
			self.music.play()
	def Pause(self):
		if self.paused:
			self.music.unpause()
			self.paused = False
		else:
			self.music.pause()
			self.paused = True
		
class main:
		def __init__(self):
			self.app = JyPyUI.Interface().app
			self.name = 'Player Music - v1.0.0'
			self.size_screen = (720,1500)
			self.gui = JyPyUI.Interface().Window(self.size_screen,self.name)
			
			self.bg = JyPyUI.Image(self.gui,os.path.join('static','img','background.png'))
			self.bg.pos = {'x':0,'y':0}
			self.bg.padding = {'x':769,'y':1200}
			
			self.pres_play = True
			self.play = JyPyUI.Image(self.gui,os.path.join('static','img','pause.png'))
			self.play.pos = {'x':300,'y':1200}
			self.play.padding = {'x':150,'y':150}
			
			self.anterior = JyPyUI.Image(self.gui,os.path.join('static','img','anterior.png'))
			self.anterior.pos = {'x':130,'y':1225}
			self.anterior.padding = {'x':100,'y':100}
			
			self.proximo = JyPyUI.Image(self.gui,os.path.join('static','img','proximo.png'))
			self.proximo.pos = {'x':500,'y':1225}
			self.proximo.padding = {'x':100,'y':100}
			
			self.div = JyPyUI.Div(self.gui)
			self.div.pos= {'x':0,'y':1050}
			self.div.padding = {'x':769,'y':300}
			
			
			self.div2 = JyPyUI.Div(self.gui)
			self.div2.pos= {'x':120,'y':350}
			self.div2.padding = {'x':500,'y':500}
			
			self.disc = JyPyUI.Animation.MultImage(os.path.join('static','img','Disc'))
			self.disc.pos = {'x':260,'y':480}
			self.disc.padding = {'x':200,'y':200}
			
			
			self.Group = JyPyUI.Animation.GroupAnimation(self.disc).Group
			self.div3 = JyPyUI.Div(self.gui)
			self.div3.pos= {'x':0,'y':0}
			self.div3.padding = {'x':769,'y':100}
			
			
			
			self.name_music = JyPyUI.Label(self.gui)
			self.name_music.text_color = 'white'
			self.anim_name = -400
			self.name_music.pos = {'x':self.anim_name,'y':50}
			
			
			self.music = Music()
			self.music.Play(0)
			self.list_names = os.listdir('Music')
			
			
			self.time_label = JyPyUI.Label(self.gui)
			self.time_label.text_color = 'white'
			
			self.time_label.pos = {'x':230,'y':750}
			self.time_music = MP3(os.path.join('Music',self.list_names[0]))
			self.duration = self.time_music.info.length
			self.duration_min = self.time_music.info.length /60
			self.progress = 0 
			self.view_bar = JyPyUI.Progress_Bar(self.gui,self.progress)
			self.view_bar.pos = {'x':50,'y':1100}
			self.view_bar.color = '#A61515'
			self.view_bar.background = '#6E4F4F'
			self.name_music.text = self.list_names[0]
			self.skip = 0
			self.current = 0
			self.bar_run = 0
			
			self.disc.ActiveAnimation()
			self.disc.sprites = self.disc.sprites[::-1]
		def run(self):
			while True:
				self.real_time = self.music.music.get_pos()/1000
				self.time = self.duration - self.real_time
				self.time = self.time / 60
				self.current += 1
				
				self.view_bar.progress = self.real_time*4.6
				if self.view_bar.progress >= 610:
					self.view_bar.progress = 610
				self.time_label.text = f' Tempo Estimado: {self.time:.2f}'
				self.name_music.text = self.list_names[self.skip]
				
				if not self.music.music.get_busy():
					self.skip += 1
					if self.skip >= len(self.music.musics):
						self.skip = 0
					if self.pres_play:
						self.music.Play(self.skip)
						self.time_music = MP3(os.path.join('Music',self.music.musics[self.skip]))
						self.duration = self.time_music.info.length
						self.duration_min = self.time_music.info.length /60
					if self.pres_play == False:
						self.disc.DefaultAnimation()
				
				self.anim_name += 5
				if self.anim_name >= 769:
					self.anim_name = -400
					self.name_music.pos = {'x':self.anim_name,'y':50}
				self.name_music.pos = {'x':self.anim_name,'y':50}
				self.play_pause = 'pause.png'
				self.bg.Draw()
				
				
				events = JyPyUI.Interface().Event_init()
				dirs_event = JyPyUI.Interface().Events(events)
				if dirs_event != None:
					if dirs_event['click']:
						if self.play.rect.collidepoint(dirs_event['event'].pos):
							if self.pres_play == False:
								self.play.image = self.play.app.image.load(os.path.join('static','img','pause.png'))
								self.pres_play = True
								self.music.Pause()
								self.disc.ActiveAnimation()
								
							else:
								self.play.image = self.play.app.image.load(os.path.join('static','img','play.png'))
								self.music.Pause()
								self.pres_play = False
								self.disc.DefaultAnimation()
						if self.proximo.rect.collidepoint(dirs_event['event'].pos):
							self.skip += 1 
							musics = os.listdir('Music')
							if self.skip >= len(musics):
								self.skip = 0
							if self.pres_play == False:
								self.music.Play(self.skip)
								self.music.music.pause()
								self.time_music = MP3(os.path.join('Music',self.music.musics[self.skip]))
								self.duration = self.time_music.info.length
								self.duration_min = self.time_music.info.length /60
								
							else:
								self.music.Play(self.skip)
								self.time_music = MP3(os.path.join('Music',self.music.musics[self.skip]))
								self.duration = self.time_music.info.length
								self.duration_min = self.time_music.info.length /60
						if self.anterior.rect.collidepoint(dirs_event['event'].pos):
							self.skip -= 1 
							musics = os.listdir('Music')
							if self.skip <= 0:
								self.skip = 0
							if self.skip >= len(musics):
								self.skip = 0
							if self.pres_play == False:
								self.music.Play(self.skip)
								self.music.music.pause()
								self.time_music = MP3(os.path.join('Music',self.music.musics[self.skip]))
								self.duration = self.time_music.info.length
								self.duration_min = self.time_music.info.length /60
								
							else:
								self.music.Play(self.skip)
								self.time_music = MP3(os.path.join('Music',self.music.musics[self.skip]))
								self.duration = self.time_music.info.length
								self.duration_min = self.time_music.info.length /60
							
				self.div.Draw()
				self.play.Draw()
				self.anterior.Draw()
				self.proximo.Draw()
				self.div2.Draw()
				
				self.div3.Draw()
				self.time_label.Draw()
				self.name_music.Draw()
				self.view_bar.Draw()
				self.Group.draw(self.gui)
				self.Group.update()
				JyPyUI.Interface().Run(fps=60)
				JyPyUI.Interface().app.time.delay(20)
			
				
				
main().run()