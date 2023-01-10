import os

class FileManager():
    def __init__(self, location_file, destination_file):
        self.location_file = location_file
        self.destination_file = destination_file

        self.directory_list_file = ["texts", "images", "codes", "other"]

    def Main_file(self):
        all_file = os.listdir(path=self.location_file)
        
        for fileName in all_file:
            self.get_extension(os.path.splitext(fileName))

    def get_extension(self, fileName):
        extension_file = fileName[1]
        file_name = fileName[0] + fileName[1]

        path_location = os.path.join(self.location_file, file_name)

        if extension_file == ".txt":
            path_destination = os.path.join(self.destination_file, "texts", file_name)
            print("Transfert fichier ", file_name)
            os.replace(path_location, path_destination)

        elif extension_file == ".png" or ".jpg":
            path_destination = os.path.join(self.destination_file, "images", file_name)
            print("Transfert fichier ", file_name)
            os.replace(path_location, path_destination)

        else:
            path_destination = os.path.join(self.destination_file, "other", file_name)
            print("Transfert fichier ", file_name)
            os.replace(path_location, path_destination)


    def verify_integrity(self):
        for path in os.listdir(self.destination_file):
            if not os.path.isfile(os.path.join(self.destination_file, path)):
                self.directory_list_file.remove(path)

        for element in self.directory_list_file:
            file_destination_path = os.path.join(self.destination_file, element)
            os.mkdir(file_destination_path)
            
    def Lauch(self):
        self.verify_integrity()
        self.Main_file()