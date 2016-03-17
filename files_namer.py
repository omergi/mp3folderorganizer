#!/usr/bin/pyhton

# ---------------------- imports ------------------------------------------------
import eyed3
import os
import shutil
import argparse

# ---------------------- internal imports ------------------------------------------
import main as dir_organizer

# ---------------------- implementaion ------------------------------------------

CODING_TYPE = 'utf-8'

def input_validator(func):
    def wrapper(input_type, default):
        input_str = func(input_type, default)
        if input_str == default or input_str.strip() == '':
            msg = "No input was entered, using default: %s" % (default,)
            print msg.encode(CODING_TYPE)
        return input_str
    return wrapper

def str_to_unicode(str_in):
    if type(str_in) is str:
        return unicode(str_in, CODING_TYPE)
    else:
        return str_in

@input_validator
def user_input(input_type, default):
    input_msg = u'Please enter %s' % (input_type,)
    if default:
        input_msg += ' [default: %s]' % (default)
    input_msg += u': '
    user_input = raw_input(input_msg.encode(CODING_TYPE))
    if user_input == '':
        user_input = default
    return user_input

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
    mp3_file.tag.artist = str_to_unicode(artist_to_set)
    mp3_file.tag.title = str_to_unicode(title_to_set)
    mp3_file.tag.save()
    done_msg = 'Updated file %s to artist %s and title %s' % (os.path.basename(mp3_file.path), 
                                                              artist_to_set.encode(CODING_TYPE),
                                                              title_to_set.encode(CODING_TYPE))
    print done_msg

def main():
    args = argparser()
    process_file(args.file_name)

if __name__ == "__main__":
    main()

