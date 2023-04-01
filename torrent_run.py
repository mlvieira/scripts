#!/usr/bin/env python3

'''
    Script to copy subtitle from movies or tv shows using the REGEX_SUBTITLE pattern 
    following rarbg folder format and jellyfin subtitle format
    rarbg format:
        movies: <title>/Subs/<regex pattern>.<ext>
        tv show: <title>/Subs/<episode name>/<regex pattern>.<ext>
    jellyfin subtitle format:
        subtitle: <video>.<language>.<ext>
'''

from argparse import ArgumentParser
from shutil import copy2
from sys import exit
from re import match, compile, IGNORECASE
from os import listdir, EX_OSFILE
import logging

REGEX_SUBTITLE = compile(pattern=r"^(\d+_(?P<language>En)g(?:lish)?\.\w{3})$", flags=IGNORECASE) # https://regex101.com/r/8dE1R8/1
VIDEO_FORMATS = ("mkv", "avi", "mp4")
SUBTITLE_FORMATS = ("srt", "ass")


def parseArgs():
    parser = ArgumentParser(prog="RARBG Subtitles Extractor",
                            description="Script to copy subtitle from movies or tv shows using the REGEX_SUBTITLE pattern following rarbg folder format and jellyfin subtitle format")
    parser.add_argument('-r', '--root', help="Root of the folder", required=True)
    return parser.parse_args()

def listDirTry(path):
    try:
        return listdir(path)
    except OSError:
        logging.error("Folder: %s doesn't exist" % path)
        exit(EX_OSFILE) # die

def findVideo(name):
    if name.endswith(VIDEO_FORMATS):
        return name
    else:
        logging.warning("Didn't find any video with the following name: %s" % name)

def isTvShow(name):
    for i in name:
        if i.endswith(SUBTITLE_FORMATS):
            return False
        else:
            return True
    
def sortRegexList(ls):
    return sorted(list(filter(REGEX_SUBTITLE.match, listDirTry(ls))))[0]

def extractLanguage(str):
    lang = match(REGEX_SUBTITLE, str)
    try:
        return lang.group('language').lower()
    except IndexError:
        logging.error("Couldn't determine language with current regex, falling back to english")
        return "en"

def copyFile(src, dest):
    try:
        copy2(src, dest)
        logging.info("Sucessfully copied subtitle %s to %s" % (src, dest))
    except OSError:
        logging.error('Failed to copy file: %s to %s' % (src, dest))

def main():
    logging.basicConfig(filename='.subtitle_torrent.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    args = parseArgs()
    logging.info("Grabbing subtitles for folder: %s" % args.root)
    root_videos_no_ext = [x for x in listDirTry(args.root) if findVideo(x)][0][:-4]
    sub_dict = dict(folder_path = args.root + "/Subs/")
    sub_dict['listDir'] = listDirTry(sub_dict['folder_path'])
    flg_tvshow = isTvShow(sub_dict['listDir']) 
    if flg_tvshow:
        for i in sub_dict['listDir']: # we are on <title>/Subs/
            filtered = sortRegexList(sub_dict['folder_path'] + i) # we are on <title>/Subs/<episode>/<subtitle>. filter subtitles while they are in lists
            sub_dict['language'] = extractLanguage(filtered) 
            sub_dict['og_path_formatted'] = f"{sub_dict['folder_path']}{i}/{filtered}"
            sub_dict['new_path_formatted'] = f"{args.root}/{i}.{sub_dict['language']}.{filtered[-3:]}"
            copyFile(sub_dict["og_path_formatted"], sub_dict["new_path_formatted"])
    else:
        filtered = sortRegexList(sub_dict['folder_path']) # we are on <title>/Subs/
        sub_dict['language'] = extractLanguage(filtered) 
        sub_dict['og_path_formatted'] = f"{sub_dict['folder_path']}{filtered}"
        sub_dict['new_path_formatted'] = f"{args.root}/{root_videos_no_ext}.{sub_dict['language']}.{filtered[-3:]}"
        copyFile(sub_dict["og_path_formatted"], sub_dict["new_path_formatted"])
    
if __name__ == '__main__':
    main()