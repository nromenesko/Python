#!/usr/bin/env python
#
# Takes an exported list of bookmarks in .html format and parses
# them. Places each YouTube URL into a separate file "youtube_list.txt"
# with one URL per line.
#
# Intended for use with list_dl.py, which downloads a list of YouTube
# video URLs in mp3 format.
################################

import argparse
import sys

def main():

    parser = argparse.ArgumentParser(description='Parses YouTube urls from bookmarks file into a line-separated list in .txt format')
    parser.add_argument('bookmark_path', metavar='bookmark_path', type=str, help='Path to HTML file of exported bookmarks')
    argvs = parser.parse_args()
    
    bookmark_path_str  = argvs.bookmark_path
    bookmarks = open(bookmark_path_str, 'r', encoding="UTF-8")
    youtube_list = open('youtube_list.txt', 'w', encoding="UTF-8")
    url_count = 0
    
    #FOR REFERENCE: Python string index starts at 0
    for line in bookmarks:
        
        start_url = line.find("http")
        
        # If the line in the html file contains a link
        if start_url != -1:
            
            #If that link is a youtube video link
            if line.find("www.youtube.com/watch?v") != -1:
                
                #Maybe need to subtract one from end_url index
                end_url = line.find('" ')
                
                #Write YouTube
                youtube_list.write(line[start_url:end_url] + "\n")
                url_count +=1 
    
    print("Wrote %d URLS to file youtube_list.txt in current directory" %(url_count))
    sys.exit(0)

if __name__ == '__main__':
    main()