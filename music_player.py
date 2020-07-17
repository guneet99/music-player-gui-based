from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *

pygame.init()


class FrameApp(Frame):
    def __init__(self,master):

        super(FrameApp, self).__init__(master)

        self.grid()
        self.paused = False
        self.playlist = list()
        self.actual_song = 0

        self.b1 = Button(self, text="play", command=self.play_music, width=20)
        self.b1.grid(row=1, column=0)

        self.b2 = Button(self, text="previous", command=self.previous_song,
                         width=20)
        self.b2.grid(row=2, column=0)

        self.b3 = Button(self, text="toggle", command=self.toggle, width=20)
        self.b3.grid(row=3, column=0)

        self.b4 = Button(self, text="next", command=self.next_song, width=20)
        self.b4.grid(row=4, column=0)

        self.b5 = Button(self, text="add to list", command=self.add_to_list,
                         width=20)
        self.b5.grid(row=5, column=0)

        self.label1 = Label(self)
        self.label1.grid(row=6, column=0)

        self.output = Text(self, wrap=WORD, width=50)
        self.output.grid(row=8, column=0)
        
        self.SONG_END = pygame.USEREVENT + 1

        # TODO: Make progressbar, delete songs from playlist, amplify volume

    def add_to_list(self):
        
        directory = askopenfilenames()
       
        for song_dir in directory:
            print(song_dir)
            self.playlist.append(song_dir)
            
        self.output.delete(0.0, END)

        for key, item in enumerate(self.playlist):
           
            song = EasyID3(item)
            song_data = (str(key + 1) + ' : ' + song['title'][0] + ' - '
                         + song['artist'][0])
            self.output.insert(END, song_data + '\n')

    def song_data(self):
       
        song = EasyID3(self.playlist[self.actual_song])
        song_data = "Now playing: Nr:" + str(self.actual_song + 1) + " " + \
                    str(song['title']) + " - " + str(song['artist'])
        return song_data

    def play_music(self):
       
        directory = self.playlist[self.actual_song]
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.paused = False
        self.label1['text'] = self.song_data()

    def check_music(self):
       
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.next_song()

    def toggle(self):
       
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        elif not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def get_next_song(self):
        
        if self.actual_song + 2 <= len(self.playlist):
            return self.actual_song + 1
        else:
            return 0

    def next_song(self):
        
        self.actual_song = self.get_next_song()
        self.play_music()

    def get_previous_song(self):
        
        if self.actual_song - 1 >= 0:
            return self.actual_song - 1
        else:
            return len(self.playlist) - 1

    def previous_song(self):
        
        self.actual_song = self.get_previous_song()
        self.play_music()


root = Tk()
root.geometry("500x500")
app = FrameApp(root)

while True:
    
    app.check_music()
    app.update()

