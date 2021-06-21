#!/usr/bin/env python3
r"""# A CLI tool for making 'crusts': .py files from a template

This module provides a CLI interface for  making  a  .py  file  'skeleton'
with   commonly  used  import  statements, a number of named blocks marked
off by comment bars, and a __main__ block.  Current  options   allow   for
specifying  block  length  and width, adjusting how each name bar is made,
and using FIGlet to make pretty headers for  each  block,  as  well  as  a
pretty  footer  placed  at the end of the crust.

The  module  defaults in 'setup' can be changed to customize the hashbang,
which import statements are used, and how the __main__ function is defined
and  called.  The module functions can be imported and used outside of the
Command Line Interface, providing various text elements or the entire text
of a crust.  The CLI interface will create a crust as instructed, and save
the output to the given filepath,  asking  before  overwriting an existing
file (the -r option will quietly replace an existing file without asking).

## A quick look at the functions

figlet(message, /, opt='std', *opts, prefix='##', pad=2, def_len=3,
        no_skip=False, width=80)
    Runs figlet,  passing in the *message*.  Other  options may be
    given using *opt* or *opts*. *opt* is a key used to access a tuple
    of options from a dict of defaults.  If *opts* are given, they
    take priority over *opt*.  If  figlet  executes without error,
    the  output  lines  are  returned  with the *prefix* and *pad*
    space prepended to them. A default value of *def_len* lines
    made  of  the  *prefix*,  *pad*, and a newline is returned if an
    error occurs or *no_skip* is True.  The *width* determines the
    maximum width of the figlet output

section(name, /, lines=1, prefix='\n', width=80, char='#', pad=1,
            tags='    ', head='\n', foot='', headlen=1, footlen=0,
            *fig_args, **fig_kwds)
    Returns  a  block of lines surrounded by '### *name* ###' bars
    that are *width* long. If *lines* is a string,  it  will  be  
    inserted  between  the  name   bars  as-is.  If *lines* is  an
    integer, the body of the section will be `prefix  *  lines`.
    *char* is the character used for the bars.
    
    The *tags* string and  *pad*  number specify the  characters
    and  amount  of  space  to be placed around the name in each
    namebar.
    
    *head* and *foot* are the strings that get added  above  and
    below the block *headlen* and *footlen* times, respectively.
    If using figlet,  the header and footer will instead be made
    according to the *fig_args* and *fig_kwds* passed in.

dough(name, /, blocks=('setup', 'helpers'), length=5, width=80,
        tags='   ', pad=1, use_fig=False, use_ego=False,
        use_main=True, use_foot=False)
    *name* is used in the docstring, and footer if using figlet.
    *blocks*  are the names of the body's  code  blocks.  Figlet
    will also use these names to make a block's header. *length*
    is the number of blank lines in each code block.  *tags* and
    *pad* are passed into *section*.

    *use_fig*,  *use_ego*,  *use_main*, and *use_foot* determine
    whether figlet is used, or whether  the  ego  snippet,  main
    block, or footer are inserted.

cat(*strings)
    A Simple helper for string concatenation.

## CLI Interface

    usage:
            crust [ -h ] [ -femorA ] [ -l length ]
            [ -t tags ] [ -w width ] [ -p padding ]
            file [ blocknames ... ]
    
    crust - A CLI tool for for creating .py files from a template.
    
    positional arguments:
        file
            Name or path of the file to make - a .py extention
            will be added if none is included

        blocknames
            names of comment blocks to insert
    
    optional arguments:
        -h, --help
            Show this help message and exit

        -r, --force
            Quietly replace the target file if it already exists

        -f, --figlet
            Use figlet when making headers/footers

        -e, --ego
            Add global variable 'ego' set to 'pathlib.Path(file)'

        -m, --main
            Add a simple '__main__' block

        -l LEN, --len LEN
            Set the number of lines in each comment block (default is 5)

        -o, --foot
            Place a footer at the end of the file

        -A, --all
            Equivalent to -gemo

        -t TAGS, --tags TAGS  
            Characters to be placed around the name in each namebar

        -w WIDTH, --width WIDTH
            Max column width to use for text

        -p padding, --pad padding
            Number of spaces to pad around the name in each namebar

Version 1.0.0
"""

import argparse
import subprocess
import re

from pathlib import Path

###############################################################################
##
##              _                 
##   ___   ___ | |_  _   _  _ __  
##  / __| / _ \| __|| | | || '_ \
##  \__ \|  __/| |_ | |_| || |_) |
##  |___/ \___| \__| \__,_|| .__/
##                         |_|    
################################### !setup  ###################################

# Hashbang that gets placed on the
# first line
hashbang = '#!/usr/bin/env python3\n'
# A simple docstring is created in
# the body of __main__ to be
# placed on the line after

# Common import statements, commented
imports_basic = """\
# import string
# import re
# import math
# import random
# import itertools
# import functools
# import pathlib
# import os
# import time
# import argparse
# import json
# import collections
# import timeit\n\n"""

# Skeleton of a __main__()
# function and __name__ call
mainbody = """\



def __main__():
    print('running main...')

if __name__ == '__main__':
    __main__()

"""

################################### @setup  ###################################
##
##   _            _                         
##  | |__    ___ | | _ __    ___  _ __  ___
##  | '_ \  / _ \| || '_ \  / _ \| '__|/ __|
##  | | | ||  __/| || |_) ||  __/| |   \__ \
##  |_| |_| \___||_|| .__/  \___||_|   |___/
##                  |_|                     
################################## !helpers  ##################################

def cat(*strings):
    'Concatenate strings s1 + ... + sn, or an iterable of strings'
    if len(strings) == 0:
        return ''
    elif len(strings) == 1:
        # If only one strings is given and
        # it is a string, return it
        if type(strings[0]) is str:
            return strings[0]
        # Otherwise, assume it is an
        # iterable of strings and join
        # them
        return ''.join(strings[0])
    else:
        return ''.join(strings)

def figlet(
         message, /
        ,opt='std', *opts
        ,prefix='##'
        ,pad=2
        ,def_len=3
        ,no_skip=False
        ,width=80
        ):
    r"""figlet - Wrapper function to run FIGlet as a shell subprocess.

    Runs  figlet, passing in the message.  Other  options may be
    given using opt or opts. opt is a key used to access a tuple
    of  options  from  a  dict of default options.  If opts  are  
    given, they take priority over opt.                                    

    If  the subprocess's returncode == 0,  the bytes object that
    represents figlet's output is converted to a str.  If given,  
    the prefix is prepended to each line in the output, followed
    by `' ' * pad`.                              

    A default  return  value is created from the prefix and pad,
    followed by a newline. If no_skip is False or the returncode  
    is an error value,  the function returns a string consisting
    of default * def_len.

    From the figlet man page:                                  

        NAME:                                           
            'FIGlet - display  large  characters  made up of
            ordinary screen characters'                     

        SYNOPSIS:                                       
            figlet [ -cklnoprstvxDELNRSWX ]
            [ -d fontdirectory ]
            [ -f fontfile ] [ -m layoutmode ]
            [ -w outputwidth ] [ -C controlfile ]
            [ -I infocode ] [ message ]                        

        DESCRIPTION:                                    
            'FIGlet prints its input using large  characters
            (called   FIGcharacters)  made  up  of  ordinary
            screen characters (called subcharacters). FIGlet
            output is generally reminiscent of the sort   of
            signatures  many  people  like  to  put  at  the
            end of e-mail  and  UseNet  messages. It is also
            reminiscent  of  the   output   of  some  banner
            programs, although it is oriented normally,  not
            sideways.'
        (...)
    """
    prefix += ' '*pad
    default = prefix + '\n'
    # quickly return the defaults
    # if instrucred to skip
    if no_skip is False:
        # return the default string
        # prepended by the prefix
        # repeated def_len times
        defaults = (default)*def_len
        return defaults
    width = str(width - len(prefix))
    default_options = {
        'std': ['-k', '-w', width],
        'big': ['-k','-f','big','-w', width]
        }
    # any args passed in take
    # priority
    if not opts:
        # otherwise use a key
        opts = default_options[opt]
    # run figlet with the options and
    # message to be processed
    compro = subprocess.run(['figlet', *opts, message], capture_output=True)
    # returncode of 0 means
    # subprocess finished without
    # error
    if compro.returncode == 0:
        # stdout is of type bytes,
        # decode  it to type str
        decoded = compro.stdout.decode()
        # Split the decoded string by
        # line ends without discarding the
        # line ends
        lines = decoded.splitlines(True) # True = keep line ends
        # Re-join the lines with the
        # prefix  prepended to each line
        fig = cat(prefix + line for line in lines)
        return fig
    # non-0 returncode means the
    # subprocess finished with an
    # error    
    else:
        defaults = (default)*def_len
        return defaults

def section(
         name, /
        ,lines=1
        ,prefix='\n'
        ,width=80
        ,char='#'
        ,pad=1
        ,tags='    '
        ,head='\n'
        ,foot=''
        ,headlen=1
        ,footlen=0
        ,*fig_args
        ,**fig_kwds
    ):
    r"""section - Make a new '###  section  ###'

    Returns  a  block   of   lines   surrounded   by  '###  name
    ###'  bars  that  are  *width*  long.  The  head  string  is
    added   before   the   top   namebar  *headlen*  times,  and
    defaults  to `'\n'   *   1`.  The   foot   string  is  added
    below the  bottom  namebar  footlen  times,  and defaults to
    `'\n' * 0`. If figlet is used, *fig_args* and *fig_kwds* are 
    passed to it.
    
    If *lines* is  a  string, it  will  be  inserted between the
    name bars  as-is.  If  *lines*  is  an  integer,  the  body of
    the section will be `prefix  *  lines`.  The  char string is
    used  to  make  the  namebars - '$' would produce '$$$  name  $$$' 
    If  using  a  str  longer  than  one character,  adjust  the
    width  accordingly.  The  *pad*  integer specifies the  amount
    of  spaces  '  '  to  put  around  the  name  in  each  bar.
    
    The *tags*  string  specifies  the  characters  to be placed
    around  the  name  in  each  namebar,  which  are spaces ' '
    by default. The tags can  be  given in a few different ways.
    An  empty  string  will  result  in no extra padding in  the 
    namebars.  A  single  character or three characters will  be 
    filled in with spaces ' '.  If  two  characters  are  given,
    a  space  ' ' will be placed after each character.
    
    Examples of tags:
        ''
        -> '### name ###', '### name ###'

        '!!@@'
        -> '### !name! ###', '### @name@ ###'

        '@!' -> '@ ! '
        -> '### @name  ###', '### !name  ###'

        '@' -> '@   '
        -> '### @name  ###', '###  name  ###'

        '@!@' -> '@!@ '
        -> '### @name! ###', '### @name ###'

        
    """
    if not type(tags) == str:
        raise TypeError("tags must be type str")

    # parse the tags
    tag_len = len(tags)
    if tag_len == 1:
        tags = tag + '   '
    elif tag_len == 2:
        tags = tag[0] + ' ' + tag[1] + ' '
    elif tag_len == 3:
        tags = tags + ' '
    elif tag_len > 4:
        tags = tags[:4]

    # Make the header and footer
    if fig_kwds['no_skip']:
        head = figlet(name, width=width, *fig_args, **fig_kwds)
    else:
        head = head*3
    if foot:
        foot = foot*footlen

    # Find how long the chars in
    # the bars should be
    less = width - len(name) - pad*2 - 3
    right = less//2
    left = less - right


    # Make the left and right bars
    l, r = '#'*left, '#'*right
    t1, t2, t3, t4 = tags
    pad = ' '*pad
    # Join the namebar parts
    start = cat(l, pad, t1, name, t2, pad, r, '\n')
    end = cat(l, pad, t3, name, t4, pad, r, '\n')

    # If the user provides a string
    # for the lines, fill the block
    # with them
    if type(lines) is str:
        contents = lines
    # Otherwise use comments or empty
    # lines as directed
    else:
        contents = prefix*(lines+1)

    # Join everything together
    dough = cat(head, start, contents, end, foot)
    return dough

################################## @helpers  ##################################
##
##       _                       _     
##    __| |  ___   _   _   __ _ | |__  
##   / _` | / _ \ | | | | / _` || '_ \
##  | (_| || (_) || |_| || (_| || | | |
##   \__,_| \___/  \__,_| \__, ||_| |_|
##                        |___/        
################################### !dough  ###################################

def dough(
         name, /
        ,blocks=('setup', 'helpers')
        ,length=5
        ,width=80
        ,tags='   '
        ,pad=1
        ,use_fig=False
        ,use_ego=False
        ,use_main=True
        ,use_foot=False
    ):
    """dough - Generate the the contents of a new .py file

    Returns the entire text of a crust.
    *name* is the name of the file to be made.  The name is used
    to make the docstring,  and a pretty footer if using figlet.
    *blocks* is a sequence of the names of the code blocks to be
    placed into the body.  Figlet  will also make pretty headers
    that go above each  block.  *length*  is the number of blank
    lines in the code blocks.
    
    *tags*  are  wrapped  around  the names in the namebars that
    enclose each block. *pad* is the number of spaces the tagged
    names are padded with inside the namebar.
    
    *use_fig*,  *use_ego*,  *use_main*, and *use_foot* determine
    whether figlet is used, or whether  the  ego  snippet,  main
    block, or footer are inserted.

    """
    # Horizontal bar
    bar = '#'*(width-1) + '\n'
    # make a basic docstring
    doc = '"""docstring for {}"""\n\n'.format(name)
    # assemble the file header
    dough = [hashbang, doc, imports_basic]

    # add ego snippet to the header
    if use_ego:
        ego = ('from pathlib import Path\nego = Path("{}")\n\n'
            .format(name)
            )
        dough.append(ego)

    # Place a bar at the start of the body
    dough.append(bar)

    # Create and add the body sections
    blocks = cat(
        section(
            name, length
            ,no_skip=use_fig
            ,tags=tags
            ,width=width
            ,pad=pad
            )
        for name in blocks
        )
    dough.append(blocks)

    # Add the __main__ skeleton
    if use_main:
        main = section(
             'main'
            ,lines=mainbody
            ,no_skip=use_fig
            ,tags=tags
            ,width=width
            ,pad=pad
            )
        dough.append(main)

    # Make a footer with the file name
    if use_foot:
        foot = figlet(
             name, 'big'
            ,def_len=3
            ,no_skip=use_fig
            ,width=width
            )
        foot = bar + foot + bar
    # or not
    else:
        foot = ''

    # Add the finishing touches
    dough += foot, '#EOF'
    # Join it all together
    crust = cat(dough)
    return crust

################################### @dough  ###################################
##
##                                       
##   _ __    __ _  _ __  ___   ___  _ __
##  | '_ \  / _  || '__|/ __| / _ \| '__|
##  | |_) || (_| || |   \__ \|  __/| |   
##  | .__/  \__,_||_|   |___/ \___||_|   
##  |_|                                  
################################### !parser  ##################################

parser = argparse.ArgumentParser(
    description=('crust - A CLI tool for for creating '
                 '.py files from a template.\n')
    ,usage=("\n        crust [ -h ] [ -femorA ] [ -l length ]\n"
            "        [ -t tags ] [ -w width ] [ -p padding ]\n"
            "        file [ blocknames ... ]\n")
    )
parser.add_argument(
     'file'
    ,metavar='file'
    ,type=str
    ,help=("Name or path of the file to make - a"
           " .py extention will be added if none "
           "is included")
    )
parser.add_argument(
     '-r', '--force'
    ,action='store_true'
    ,help="Quietly replace the target file if it already exists"
    )
parser.add_argument(
     '-f', '--figlet'
    ,dest='use_fig'
    ,action='store_true'
    ,help="Use figlet when making headers/footers"
    )
parser.add_argument(
     '-e', '--ego'
    ,dest='use_ego'
    ,action='store_true'
    ,help="Add global variable 'ego' set to 'pathlib.Path(file)'"
    )
parser.add_argument(
     '-m', '--main'
    ,dest='use_main'
    ,action='store_true'
    ,help="Add a simple '__main__' block"
    )
parser.add_argument(
     '-l', '--len'
    ,action='store'
    ,help="Set the number of lines in each comment block (default is 5)"
    ,default=5
    ,type=int
    )
parser.add_argument(
     '-o', '--foot'
    ,dest='use_foot'
    ,action='store_true'
    ,help="Place a footer at the end of the file"
    )
parser.add_argument(
     '-A', '--all'
    ,action='store_true'
    ,help="Equivalent to -gemo"
    )
parser.add_argument(
     '-t', '--tags'
    ,default='    '
    ,help="Characters to be placed around the name in each namebar"
    )
parser.add_argument(
     '-w', '--width'
    ,default=80
    ,type=int
    ,help="Max column width to use for text"
    )
parser.add_argument(
     '-p', '--pad'
    ,metavar='padding'
    ,default=1
    ,type=int
    ,help="Number of spaces to pad around the name in each namebar"
    )
# parser.add_argument(
#      '-b', '--bar'
#     ,default='#'
#     ,help="Character(s) to use for bars and namebars"
#     )
# parser.add_argument(
#      '-c', '--comment'
#     ,default='#'
#     ,help='Character(s) to use for comments'
#     )
parser.add_argument(
     'blocks'
    ,metavar='blocknames'
    ,type=str
    ,nargs='*'
    ,help="Names of comment blocks to insert"
    ,default= ('setup', 'helpers')
    )

################################### @parser  ##################################
##
##                                  _                     
##                _ __ ___    __ _ (_) _ __               
##               | '_  _  \  / _  || || '_ \              
##               | | | | | || (_| || || | | |             
##   _____  _____|_| |_| |_| \__,_||_||_| |_|_____  _____
##  |_____||_____|                          |_____||_____|
################################### !main  ####################################


def __main__(*args):
    if args:
        rx = parser.parse_args(args)
    else:
        rx = parser.parse_args()
    # Find the target file
    them = Path(rx.file)
    if them.suffix != '.py':
        them = them.with_suffix('.py')
    # If the directory of the target
    # doesn't exist, complain.
    if not them.parent.exists():
        raise ValueError("{!s} does not exist".format(them.parent))
    # If the target already exists,
    # ask if it should be replaced.
    # Quit on 'no'
    if them.exists() and not rx.force:
        answer = ''
        # Input loop until answer
        # is yes or no
        while not answer:
            answer = input(
                cat(
                "Warning: File {!s} already exists, ".format(them)
                ,"do you want to replace it? [y/n]: "
                )
            )
        if answer == 'n' or answer == 'no':
            print(
                "File {!s} will be kept. Quitting...".format(them)
                )
            return 0
        elif answer == 'y' or answer == 'yes':
            print(
                "File {!s} will be replaced...".format(them)
                )

    crust = dough(
             them.stem
            ,blocks=rx.blocks
            ,length=rx.len
            ,width=rx.width
            ,tags=rx.tags
            ,pad=rx.pad
            ,use_fig=(rx.use_fig or rx.all)
            ,use_ego=(rx.use_ego or rx.all)
            ,use_main=(rx.use_main or rx.all)
            ,use_foot=(rx.use_foot or rx.all)
        )
    # 'create' mode if the file doesn't
    # exist, 'write' mode otherwise
    mode = 'xw'[them.exists()]
    with them.open(mode) as file:
        file.write(crust)

if __name__ == '__main__':
    __main__()

###################################  main  ####################################
###############################################################################
##``     .    "    `    .      '   |                                         ##
##  * ` _` .`  \_    +     ~      *|         Name: crust                     ##
##   \`(_)`+    *        -  `   "  |      Version: 1.0.0                     ##
## ~ ` ` `.` `   ,  -    /   _ `   |       Author: phials                    ##
##   \` `.``_  .   +   ' .  | |  . | Author email: phials@protonmail.com     ##
##    ___  _ __  _   _  ___ | |_   |  Description: Make .py templates        ##
## * / __|| '__|| |*| |/ __|| __|  |          url: https://github.com/       ## 
##  | (__ | |` *| |_| |\__ \| |_  `|               /phials/crust             ## 
##,  \___||_| ,  \____||___/ \__|  |      License: Unlicense                 ##
###################################|           OS: Linux, macOS              ##
## "Python  is to me what a flaky  |       Python: 3.9                       ##
##  crust is to a dog whose owner  |   Writted in: Sublime Text 4            ##
##  has  no  plates and loves pie" |                                         ##
###############################################################################
# EOF