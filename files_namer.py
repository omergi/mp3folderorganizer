#!/usr/bin/pyhton

# ---------------------- imports ------------------------------------------------
import eyed3
import os
import shutil
import argparse

# ---------------------- internal imports ------------------------------------------
import main as dir_organizer

# ---------------------- implementaion ------------------------------------------

def input_validator(func):
    def wrapper(input_type, default):
        input_str = func(input_type, default)
        while input_str == '':
            print "The input you've entered is illeagl please enter a correct one or exit (Ctrl + C)"
            input_str = func(input_type, default)
        return repr(input_str)
    return wrapper

@input_validator
def user_input(input_type, default):
    input_msg = u'Please enter %s' % (input_type,)
    if default:
        input_msg += u' [default: %s]' % (default)
    input_msg += u': '
    return raw_input(input_msg)

def get_field_to_set(field_name, mp3_file):
    field_default = getattr(dir_organizer, 'get_%s' % (field_name))(mp3_file)
    field_to_set = user_input(field_name, field_default)
    return field_to_set

def argparser():
    parser = argparse.ArgumentParser(description='Set artist and title tags to supplied mp3 file')
    parser.add_argument("file_name", help="The file name which we want to set")

    return parser.parse_args()

def process_file(file_name):
    mp3_file = eyed3.load(file_name)
    artist_to_set = get_field_to_set('artist', mp3_file)
    title_to_set = get_field_to_set('title', mp3_file)
    mp3_file.tag.artist = artist_to_set
    mp3_file.tag.title = title_to_set
    mp3_file.tag.save()
    print u'Updated file %s to artist %s and title %s' % (os.path.basename(mp3_file.path), artist_to_set, title_to_set)

def main():
    args = argparser()
    process_file(args.file_name)

if __name__ == "__main__":
    main()

