class Clean_Data(object):
    def __init__(self):
        """ 
            Class initialization
            Intitialised class attributes
        """
        self.parent_directory = "..\csv\\"
        self.file_parse_error_msg = "An error occurred while paring the file"

    def update_file(self, file_name):
        """
            :parameters: name of the file. datatype = string 
            Replace:
                a. Commas with blankspaces
                b. Semi-Colons with Commas
            
            Updates the files with above changes

            Returns a boolean value
                True: File updated succesfully
                False: File not updated successfully

            Note: Please change the parent directory accordingly
        """
        try:
            new_str = ""
            success = True
            with open(self.parent_directory + file_name, mode='r') as file_data:
                for line in file_data:
                    line = line.replace(",", ".")
                    line = line.replace(";",",")
                    new_str += line
            
            with open(self.parent_directory + file_name, mode='w') as file_data:
                file_data.write(new_str)
            return success
        except:
            print(self.file_parse_error_msg)
            success = False
        finally:
            if file_data != None:
                file_data.close()
            return success

    def print_data(self, file_name):
        """ 
            :parameters: name of the file. datatype = string
            Prints the file data
        """
        try:
            print(f'Contents of the file {file_name}')
            print('-'*20)
            with open(self.parent_directory + file_name, mode='r') as file_data:
                for line in file_data:
                    print(line)
        except:
            print(self.file_parse_error_msg)
        finally:
            if file_data != None:
                file_data.close()

    def get_filename(self):
        return input('Enter filename: ')

clean_mode = True
clean_data_object = Clean_Data()
while clean_mode:
    print('-'*20)
    print('Agata_Retail_Data_Clean Utility')
    print('1. Update file')
    print('2. Print Contents of the file')
    print('3. Exit')
    print('-'*20)
    choice = input('Enter your choice:')

    if choice == "1":
        file_name = clean_data_object.get_filename()
        if clean_data_object.update_file(file_name):
            print(f'File {file_name} updated successfully')
    elif choice == "2":
        clean_data_object.print_data(clean_data_object.get_filename())
    elif choice == "3":
        clean_mode = False
    else:
        print('Invalid input. Please select from the above options only')
