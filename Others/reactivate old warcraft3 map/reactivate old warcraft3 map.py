import os

directory_path = r'C:\Users\kenkot\OneDrive\桌面\war3\OK-20230904T112735Z-001\OK'  # replace with your directory path

for filename in os.listdir(directory_path):
    if os.path.isfile(os.path.join(directory_path, filename)):
        new_filename = "000" + filename
        source = os.path.join(directory_path, filename)
        destination = os.path.join(directory_path, new_filename)

        os.rename(source, destination)  # rename the file