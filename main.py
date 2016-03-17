#!/usr/bin/pyhton
# ---------------------- imports ------------------------------------------------
import eyed3
import sys
import glob
import os
import shutil

# ---------------------- implementaion ------------------------------------------

def get_artist(audiofile):
    return audiofile.tag.artist

def create_dir(dir_name):
    full_dir_name = os.path.join('Music_Sort','%s' % (dir_name, ))
    if not os.path.exists(full_dir_name):
        os.makedirs(full_dir_name)
    return full_dir_name

def get_title(audiofile):
    if audiofile.tag.title is None:
        return ''
    return audiofile.tag.title.strip()

def main():
    if len(sys.argv) < 1:
        print 'No path given'
    path = sys.argv[1]
    files_list = glob.glob(os.path.join(path, '*.mp3'))
    audiofiles_lst = [eyed3.load(fname) for fname in files_list]
    for i in audiofiles_lst:
        artist = get_artist(i)
        dir_name = create_dir(artist)
        try:
            dest_path = os.path.join(dir_name, '%s - %s.mp3' % (artist, get_title(mp3_file)))
        except Exception:
            with open('log.txt', 'ab') as f:
                f.write(i.path)
        if not os.path.exists(dest_path):
            try:
                shutil.copy(i.path, dest_path)
            except Exception:
                with open('log.txt', 'ab') as f:
                    f.write(i.path)



if __name__ == "__main__":
    main()
