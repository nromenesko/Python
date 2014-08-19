#/usr/bin/env python
#
# Downloads a YouTube Video or Song from either a URL or a line-separated list of URLs.
# The file(s) are downloaded to a directory given by user input.
#
################################
import os, shutil, subprocess, sys

def main():
    base_dir = os.path.dirname(os.path.realpath(__file__)) + '\\dependencies\\'
    tmp_path = base_dir + 'tmp\\'
    tmp_path = encap_str(tmp_path)

    # Update downloader if available
    update_cmd = encap_str(base_dir + 'youtube-dl.exe')
    update_cmd = update_cmd + ' -U'
    subprocess.call(update_cmd, shell=True)
    
    dst = input('\nWhere should the files be saved? Enter full path, or leave empty for current\ndirectory: ')
    isAudio = input('\nConvert file(s) to audio?  (1 = Yes,  0 = No): ')
    isList = input('\nDownload multiple YouTube videos from a list?  (1 = Yes,  0 = No): ')
    verify_dir(dst)     # If no '\' at end of dst, add one.
    
    try:
        isList = int(isList)
        isAudio = int(isAudio)
    except ValueError:
        sys.exit('Invalid Input: "1" for Yes, "0" for No.')
    
    # If dst field left empty, default to current working directory
    if dst == "": 
        dst = os.getcwd() + '\\'
        
    
    dst = encap_str(dst)
    
    # If video, no temp folder required. If audio, make temp folder.
    if not isAudio:
        tmp_path = dst
    else:
        if not os.path.isdir(tmp_path):
            tmp_path = decap_str(tmp_path)  # Remove quotes temporarily for mkdir command
            os.mkdir(tmp_path)
            tmp_path = encap_str(tmp_path)
    
    
    if not isList:
        url = input('\nEnter YouTube URL:  ')
        download(url, tmp_path)
        
    elif isList:

        list_path = input('\nEnter Path to list of YouTube URLs:   ')
        list_path = encap_str(list_path)
        
        try:
            list_path = decap_str(list_path)
            url_list = open(list_path, 'r')
            list_path = encap_str(list_path)
        except OSError:
            sys.exit('Error: Unable to open list of URLs.')

        # Download each URL in list
        for line in url_list:
            download(line, tmp_path)   
   
    else:
        sys.exit('Invalid Input: "1" for Yes, "0" for No.')

    # If audio, convert files in temp folder and remove temp afterwards
    if isAudio:
        mp3_convert(tmp_path, dst)
        shutil.rmtree(decap_str(tmp_path))
        
        
    # Exit successfully
    sys.exit(0)

#   
# Uses youtube-dl.exe to download a video from the parameter Youtube 'url'. 
# Places videos in the directory given by the string 'dst'.
#
def download(url, dst):
    base_dir = os.path.dirname(os.path.realpath(__file__)) + '\\dependencies\\'
    ytdl_path = encap_str(base_dir + 'youtube-dl.exe')

    cmd = ytdl_path + ' -i -o "' + decap_str(dst) + '%(title)s.%(ext)s" ' + url
    cmd = cmd + ' --restrict-filenames'  #Removes illegal characters from title
    subprocess.call(cmd, shell=True)
    
    
#
# Uses ffmpeg to convert a directory of video files to audio. 
# (Workaround for a youtube-dl bug)
#
def mp3_convert(src, dst):
    base_dir = os.path.dirname(os.path.realpath(__file__)) + '\\dependencies\\'
    ffmpeg_path = encap_str(base_dir + 'ffmpeg\\bin\\ffmpeg.exe')
    
    # If there are quotes, remove them to append filename to directory
    src = decap_str(src)
    dst = decap_str(dst)
    
    # Extract audio using FFMPEG
    for file in os.listdir(src):
        vid_path = encap_str(src + file)
        mp3_path = encap_str(dst + os.path.splitext(file)[0] + '.mp3')
        cmd = ffmpeg_path + ' -i ' + vid_path + ' -vn -acodec libmp3lame ' + mp3_path
        subprocess.call(cmd, shell=True)
   

#
# Takes a string containing the path to a directory and verifies it exists.
# Appends a '\' to the end of the path if not already present.
#
def verify_dir(dir_path):
    path = dir_path
    if not os.path.isdir(dir_path):
        sys.exit('Error: Directory creation not supported yet. Directories must exist prior to execution.')
    if not path.endswith('\\'):
        path = dir_path + '\\'
    return path


#
# Places double quotations around parameter string if they are not already present.
#
def encap_str(str):
    if not str.startswith('"'):
        str = '"' + str
    
    if not str.endswith('"'):
        str = str + '"'
        
    return str
    
    
#
# Removes double quotations around parameter string if they are present.
#
def decap_str(str):
    if str.startswith('"'):
        str = str[1:len(str)]
    
    if str.endswith('"'):
        str = str[0:len(str) - 1]
        
    return str
  
if __name__ == '__main__':
    main()