### Obsidian-To-Anki Script

#### Demo
https://streamable.com/bhd3en

#### Description
This script helps convert revision/review questions in obsidian into a formatted csv file, which can then be easily imported into anki.

#### Setup
There is only one set up section in the obsidian_to_anki.py file. There are two paths that need to be filled in. The obsidian_path variable should be set to the absolute path to your obsidian vault folder, and the root_folder_path should be set to the absolute path of the folder containing this script. 

Some examples of paths are:  
/Users/user/Desktop/my_obsidian_vault   
C:/Users/user/Desktop/my_obsidian_vault  
C:\\Users\\user\\Desktop\\my_obsidian_vault  

To run the script simply run the obsidian_to_anki.py script.
When running the script, two folders should be created in the folder containing this script: logs and outputs. These will contain the logs and outputs of running the obsidian_to_anki.py script.

#### Note
For images to be picked up by this script, they have to be formatted as such: "\!\[\](imgur_link_here.png)". The script only works with imgur images, and other image links or .png files in your computer will not be detected by the script.
