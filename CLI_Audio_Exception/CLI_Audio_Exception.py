'''
This class handles errors reports for the CLI Audio. It contains
two sublcasses off of CLI_Audio_Exception for sceen size errors
along with file reading errors

@author Kehlsey Lewis
@version Fall 2018

'''

#child class of pythons exception class
class CLI_Audio_Exception(Exception):
    def __init__(self, err):
        self.err = err

#subclass of CLI_Audio_Exception for file reading errors
class CLI_Audio_File_Exception(CLI_Audio_Exception):
    def __init__(self, err):
        super(CLI_Audio_Exception, self).__init__(err)

#subclass of CLI_Audio_Exception for errors related to screen size  
class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    def __init__(self, err):
        super(CLI_Audio_Exception, self).__init__(err)