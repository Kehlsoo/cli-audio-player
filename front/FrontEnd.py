import curses
import curses.textpad
import os, shutil, sys
from CLI_Audio_Exception.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception
from CLI_Audio_Exception.CLI_Audio_Exception import CLI_Audio_File_Exception

'''

This is the front end of the command line interface. It displays
infromation such as songs in the library, playlists, as well as
displaying the current song playing. The different options are all listed.

@author Kehlsey Lewis
@version Fall 2018

'''

class FrontEnd:
    def __init__(self, player, library):
        self.player = player
        self.library = library
        #self.player.play("./media/bensound-slowmotion.wav")
        curses.wrapper(self.menu)      
    def menu(self, args):
            self.stdscr = curses.initscr()
            self.stdscr.border()

            #checking for appropriate screensize
            y,x = self.stdscr.getmaxyx()
            if (y < 20 and x < 80):
                raise CLI_Audio_Screen_Size_Exception("screen is to small")
            else:
                self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
                self.stdscr.addstr(5,10, "c - Change current song")
                self.stdscr.addstr(6,10, "p - Play/Pause")
                self.stdscr.addstr(7,10, "s - Create Playlist")
                self.stdscr.addstr(8,10, "t - Play Playlist")
                self.stdscr.addstr(9,10, "ESC - Quit")
                self.displayLibrary(self.library)
                self.updateSong()
                self.stdscr.refresh()
                while True:
                    c = self.stdscr.getch()
                    if c == 27:
                        self.quit()
                    elif c == ord('p'): #when p key is pressed
                        self.player.pause()
                    elif c == ord('c'): #when c key is pressed
                        self.changeSong()
                        self.updateSong()
                        self.stdscr.touchwin()
                        self.stdscr.refresh()
                    elif c == ord('s'): #when s key is pressed
                        self.createPlaylist()
                    elif c == ord('t'): #when t key is pressed
                        self.playPlaylist()
#
#updates current song display
#
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())
#       
#changes the song to the one passed in
#
    def changeSong(self): 
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "Enter song number", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        try:
            self.player.play("./media/"+ self.library.getSong(path.decode(encoding="utf-8")))
        except:
           raise CLI_Audio_File_Exception("file not found or player problem") 
        return
#
#exits the interface
#
    def quit(self): 
        self.player.stop()
        exit()
#
#displays the library on the screen
#
    def displayLibrary(self, lib):
        list = []
        list = lib.getLibrary() #gets the library
        locY = 17
        locX = 10
        count = 0
        self.stdscr.addstr(locY,locX, "---- Library ----")
        for i in list: #iterates and displays the song titles
            locY += 1
            self.stdscr.addstr(locY,locX, str(count) + ". " + i)
            count = count + 1
#
#displays current playlists
#
    def displayPlaylist(self): 
        locY = 17
        locX = 45
        self.stdscr.addstr(locY,locX, "---- Playlists ----")
        for i in os.listdir('./playlists'): #iterates through the playlists directory
            locY += 1
            self.stdscr.addstr(locY,locX, str(i))
#			
#makes a file for the requested playlist
#
    def createPlaylist(self):
        #asking user to name the playlist
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "Name the playlist", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        name = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

        #making a text file named the specified playlist
        text_file = open('./playlists/' + name.decode(encoding="utf-8"), "w")
        text_file.close()
        
        #sending the playlist to be written to
        self.writeToFiles(name.decode(encoding="utf-8")) 
#      
#plays the playlist
#
    def playPlaylist(self):
        self.displayPlaylist()

        #asking user for playlist to played
        scr = curses.initscr()
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "Enter playlist to play", curses.A_REVERSE)
        curses.echo()
        playlist = changeWindow.getstr(1,1, 30)
        del changeWindow

        #opens the playlist file
        text_file = open('./playlists/' + playlist.decode(encoding="utf-8"), "r")
        content = text_file.read()
        s = str(content)
        data = []
        data = s.split(",") #splits the track numbers into own string

        #display the playlist
        locY = 17
        locX = 70
        self.stdscr.addstr(locY,locX, "----Songs in Playlist: " + playlist.decode(encoding="utf-8")+ " ---")
        for i in data:
            locY += 1
            self.stdscr.addstr(locY,locX, self.library.getSong(int(i)))
        try:
            self.player.play("./media/" + self.library.getSong[data[0]])
        except:
            raise CLI_Audio_File_Exception("file not found or player problem")
#
#asks the user which songs to add to playlist along with writes to the file (playlist)
#
    def writeToFiles(self, playListName):

        #now asking user for songs add to playlist
        nWindow = curses.newwin(5, 40, 5, 50)
        nWindow.border()
        nWindow.addstr(0,0, "Enter songs to add to playlist", curses.A_REVERSE)
        nWindow.addstr(1,0, "Enter song numbers seperated by commas", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        string = nWindow.getstr(3,1, 30)
        curses.noecho()
        del nWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        
        #writing to playlist file
        text_file = open('./playlists/' + playListName, "w")
        text_file.write(string.decode(encoding="utf-8"))
        text_file.close()