#!/usr/bin/env python3

import os
import sys
import shutil
import json

# Location of the resource directory from the home directory.
MPD_RESDIR_FROM_HOME = "/Documents/computing/python/projects/MPD/code/test/LaTeX/"
####################################################################

class ProjDirMaker:
    """Generates a project directory based on a set of templates.

    The path to a directory containing the template subdirectories
    is set during object initialization. The resource directory
    must also contain a single file with the json describing the
    directory layout. The object can then be used to query the user
    for which template to use from each template subdirectory. The
    project directory can then be built in the current working
    directory. If the project directory and any subdirectories
    already exist, they are simply populate with the necessary files.
    If a file already exists, no action is taken, and a notification
    is displayed.
    """

    def __init__(self, res_path):
        """Get dicts for the file keys and dir struct.

        Args:
          res_path (string): Path to the template directory.
        """
        try:
            res_files = [x for x in os.listdir(res_path)
                         if os.path.isfile(os.path.join(res_path, x))]
            # List of the template subdirectories.
            self.temp_dirs = [x for x in os.listdir(res_path)
                              if os.path.isdir(os.path.join(res_path, x))]
            # Make sure there is only one file in the resource dir.
            if(len(res_files) == 1):
                res_json_file = os.path.join(res_path, res_files[0])
                with open(res_json_file) as openFile:
                    json_file_dict = json.load(openFile)
                if(not "FILE_KEYS" in json_file_dict):
                    sys.exit("No FILE_KEYS object in json file!")
                if(not "DIR_STRUCT" in json_file_dict):
                    sys.exit("No DIR_STRUCT object in json file!")
                # Dict associates template dirs with file names
                self.file_names = json_file_dict["FILE_KEYS"]
                # Dict describes the structure of the dir to be made
                self.dir_struct = json_file_dict["DIR_STRUCT"]
            else:
                sys.exit("Too many resource json files!")
        except FileNotFoundError:
            sys.exit("Cannot find resource directory!")
        except Exception as e:
            print(sys.exc_info())
            sys.exit("Failed to read json file!")
        self.res_path = res_path

    def query_proj_name(self):
        """Ask the user for the project name and return it.

        Args:
          None.

        Returns:
          string: Name of the project entered.
        """
        proj_name = input("Enter project name: ")
        return proj_name

    def proj_dir_exists(self, proj_name):
        """Check if the project dir already exists in the cwd.
    
        Args:
          proj_name (string): Name of the project.

        Returns:
          bool: True if directory exists, False otherwise.
        """
        proj_dir = os.path.join(os.getcwd(), proj_name)
        return os.path.exists(proj_dir)

    def set_selections(self):
        """Determine which template files to use.

        Args:
          None.

        Returns:
          None.

        User is queried about which template files are to be used and
        these are stored as paths in the self.selections member
        variable referenced versus their template directory names
        as the keys. If user skips a template the value "NO_TEMPLATE"
        is used.
        """
        self.selections = {}
        for temp_dir in self.temp_dirs:
            temp_path = os.path.join(self.res_path, temp_dir)
            temp_files = [x for x in os.listdir(temp_path)
                          if os.path.isfile(os.path.join(temp_path, x))]
            num_files = len(temp_files)
            if(temp_dir in self.file_names and num_files > 0):
                self.__disp_menu(temp_files, temp_dir)
                selection, valid = self.__query_selection(num_files)
                if(not valid or selection < 0):
                    sys.exit("No project built.")
                elif(selection == 0):
                    self.selections[temp_dir] = "NO_TEMPLATE"
                else:
                    selection -= 1
                    self.selections[temp_dir] =\
                            os.path.join(temp_path, temp_files[selection])

    def create(self, proj_name):
        """Create and populate the project directory.
            
        Args:
        proj_name (string): Name of the project.

        Returns:
          None.
        """
        if(not self.proj_dir_exists(proj_name)):
            try:
                os.mkdir(proj_name)
            except:
                print(sys.exc_info())
                sys.exit("Cannot create project directory!")
        proj_path = os.path.join(os.getcwd(), proj_name)
        sys.stdout.write("******\n")
        self.__populate(proj_path, self.dir_struct)

    def __disp_menu(self, temp_file_list, temp_dir):
        """Display a menu for choosing between files in a directory.

        Args:
          temp_file_list (list of strings): Files to choose from.
          temp_dir (string): Name of dir containing the files.

        Returns:
          None.
        """
        header_str = "Choose template for "
        header_str += self.file_names[temp_dir] + " in the "
        header_str += temp_dir + " directory.\n"
        sys.stdout.write(header_str)
        for i, n in enumerate(temp_file_list):
            sys.stdout.write("    " + str(i + 1) + ": " + n + "\n")
        sys.stdout.write("    0: Do not create this template\n")
        sys.stdout.write("    q: Quit\n")
        sys.stdout.flush()

    def __query_selection(self, max_selection):
        """Obtain a menu selection.

        Args:
          max_selection (int > 0): Maximum index of selection values.

        Returns:
          int: Index of the selection.
          bool: Flag indicating whether the selection is valid.

        Method prompts user for a selection, checks to make sure it
        is an integer in the appropriate range and returns the value
        along with a flag indicating whether a valid selection was
        entered. The user is given three opportunities to enter a
        valid selection before the methods returns invalid.
        """
        attempt = 0
        selection_valid = False
        while(attempt < 3):
            try:
                response = input("Selection: ")
                selection = 0
                if(response != "q"):
                    selection = int(response)
                else:
                    selection_valid = True
                    selection = -1
                    break
                if(selection > max_selection or selection < 0):
                    sys.stderr.write("Invalid selection\n")
                    attempt += 1
                else:
                    selection_valid = True
                    break
            except ValueError:
                sys.stderr.write("Invalid selection\n")
                attempt += 1
        return selection, selection_valid

    def __populate(self, cur_dir_path, dir_struct, level=0):
        """Populate a directory according to a directory layout.

        Args:
          cur_dir_path (string): Path to the directory to populate.
          dir_struct (dict): Subdir name keys, subdir layout vals.
          level (int, default 0): Subdir level.

        Returns:
          None.

        Method populates a directory tree recursively. If a
        subdirectory already exists, it is simply populated. If a
        subdirectory does not exist, it is created and then
        populated. If a file exists, nothing is done. If a file does
        not exist and has a template, the template is copied to the
        given subdirectory. If the template path is "NO_TEMPLATE",
        then no file is created. If the file does not exist, and
        there is no template, an empty file is created.
        """
        for json_key in dir_struct:
            indent = "    " * level
            if(type(dir_struct[json_key]) == type(dict())):
                # These are the directories to create.
                new_dir_path = os.path.join(cur_dir_path, json_key)
                if(not os.path.exists(new_dir_path)):
                    try:
                        os.mkdir(new_dir_path)
                        message = indent + "Directory \""
                        message += os.path.basename(new_dir_path)
                        message += "/\" created\n"
                        sys.stdout.write(message)
                    except:
                        print(sys.exc.info())
                        sys.exit("Cannot create subdirectories!")
                else:
                    message = indent + "Directory \""
                    message += os.path.basename(new_dir_path)
                    message += "/\" already exists\n"
                    sys.stdout.write(message)
                self.__populate(new_dir_path, dir_struct[json_key], level + 1)
            elif(type(dir_struct[json_key]) == type(list())):
                # These are the files to create.
                if(len(dir_struct[json_key]) != 0):
                    for new_file in dir_struct[json_key]:
                        # These are new files.
                        if(new_file in self.file_names):
                            new_file_name = self.file_names[new_file]
                        else:
                            new_file_name = new_file
                        new_file_path = os.path.join(cur_dir_path,
                                                     new_file_name)
                        if(os.path.exists(new_file_path)):
                        # File already exists, so leave it alone.
                            message = indent + "File \"" + new_file_name
                            message += "\" already exists (no overwrite)\n"
                            sys.stdout.write(message)
                        elif(new_file in self.selections):
                        # File is new and has a template.
                            if(self.selections[new_file] != "NO_TEMPLATE"):
                                shutil.copy(self.selections[new_file],
                                            new_file_path)
                                message = indent + "File \"" + new_file_name
                                message += "\" created from template "
                                message += os.path.basename(
                                               self.selections[new_file])
                                message += "\n"
                                sys.stdout.write(message)
                            else:
                            # No template should be created.
                                continue
                        else:
                        # Create a new empty file.
                            try:
                                open(new_file_path, 'a').close()
                                message = indent + "New file \""
                                message += new_file + "\" created\n"
                                sys.stdout.write(message)
                            except:
                                print(sys.exc_info())
                                sys.exit(
                                    "Cannot create " + new_file + " stopping")

# Main script ######################################################

if __name__ == "__main__":
    # Build complete path to the resource directory.
    str_list = [os.path.expanduser("~"), MPD_RESDIR_FROM_HOME]
    mpd_resdir = "".join(str_list)

    proj_maker = ProjDirMaker(mpd_resdir)
    proj_maker.set_selections()
    proj_name = proj_maker.query_proj_name()
    proj_maker.create(proj_name)

