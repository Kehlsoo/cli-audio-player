'''

This class handles the library functionality.

@author Kehlsey Lewis
@version Fall 2018

'''
import curses
import curses.textpad
import sys
import pyaudio
import wave
import time
import os

class Library:

#
# Constructor method creates a readable library that can be displayed
#
	def __init__(self):
		#reads the wav files and creates a library containing them
		self.songs = []
		for i in os.listdir('./media'):
			self.songs.append(i)
#
#returns the library with songs
#
	def getLibrary(self):
		return self.songs;
#
#returns the requested song
#
	def getSong(self, songNum):
		return self.songs[songNum]