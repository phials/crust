# crust - A CLI tool for making 'crusts': .py files from a template
*version 1.0.0*

This module provides a CLI interface for  making  a  .py  file  'skeleton'
with   commonly  used  import  statements, a number of named blocks marked
off by comment bars, and a \_\_main\_\_ block.  Current  options   allow   for
specifying  block  length  and width, adjusting how each name bar is made,
and using FIGlet to make pretty headers for  each  block,  as  well  as  a
pretty  footer  placed  at the end of the crust.

The  module  defaults in  the 'setup' section can be changed to customize
the hashbang, which import statements are used, and how the \_\_main\_\_ 
function is defined and  called.

The module functions can be imported  and used outside of the
Command Line Interface, providing the various text elements or the entire text
of a crust.  The CLI interface will create a crust as instructed, and save
the output to the given filepath,  asking  before  overwriting an existing
file (the **-r** option will quietly replace an existing file without asking).

## A quick look at the functions

```python
figlet(message, /, opt='std', *opts, prefix='##', pad=2, def_len=3,
       no_skip=False, width=80)
```

* Runs figlet,  passing in the *message*.  Other  options may be
 given using *opt* or *opts*. *opt* is a key used to access a tuple
 of options from a dict of defaults.  If *opts* are given, they
 take priority over *opt*.  
* If  figlet  executes without error, the  output  lines  are  returned 
 with the *prefix* and *pad* space prepended to them. A default value 
 of *def_len* lines made  of  the  *prefix*,  *pad*, and a newline is 
 returned if an error occurs or *no_skip* is True.  The *width* determines 
 the maximum width of the figlet output.

```python
section(name, /, lines=1, prefix='\n', width=80, char='#', pad=1,
            tags='    ', head='\n', foot='', headlen=1, footlen=0,
            *fig_args, **fig_kwds)
```

* Returns  a  block of lines surrounded by '### *name* ###' bars
 that are *width* long. If *lines* is a string,  it  will  be  
 inserted  between  the  name   bars  as-is.  If *lines* is  an
 integer, the body of the section will be `prefix  *  lines`.
 *char* is the character used for the bars.

* The *tags* string and  *pad*  number specify the  characters
 and  amount  of  space  to be placed around the name in each
 namebar.

* *head* and *foot* are the strings that get added  above  and
 below the block *headlen* and *footlen* times, respectively.
 If using figlet,  the header and footer will instead be made
 according to the *fig_args* and *fig_kwds* passed in.

```python
dough(name, /, blocks=('setup', 'helpers'), length=5, width=80,
        tags='   ', pad=1, use_fig=False, use_ego=False,
        use_main=True, use_foot=False)
```

* *name* is used in the docstring, and footer if using figlet.
 *blocks*  are the names of the body's  code  blocks.  Figlet
 will also use these names to make a block's header. *length*
 is the number of blank lines in each code block.  *tags* and
 *pad* are passed into *section*.
* *use_fig*,  *use_ego*,  *use_main*, and *use_foot* determine
 whether figlet is used, or whether  the  ego  snippet,  main
 block, or footer are inserted.

```python
cat(*strings)
```
* A Simple helper for string concatenation.

## CLI Interface

#### usage:

```
crust [ -h ] [ -gemofA ] [ -l length ]
[ -t tags ] [ -w width ] [ -p padding ]
file [ blocknames ... ]
```

#### positional arguments:

| argument | description |
|--|--|
| **file** | Name or path of the file to make - a .py extention will be added if none is included |
| **blocknames** | names of comment blocks to insert |

#### optional arguments:

|option| description |
|--|--|
| **-h, -\-help** | Show this help message and exit |
| **-r, -\-force** | Quietly replace the target file if it already exists |
| **-f, -\-figlet** | Use figlet when making headers/footers |
| **-e, -\-ego** | Add global variable 'ego' set to 'pathlib.Path(file)' |
| **-m, -\-main** | Add a simple '\_\_main\_\_' block |
| **-l LEN, -\-len LEN** | Set the number of lines in each comment block (default is 5) |
| **-o, -\-foot** | Place a footer at the end of the file |
| **-A, -\-all** | Equivalent to -gemo |
| **-t TAGS, -\-tags TAGS**   | Characters to be placed around the name in each namebar |
| **-w WIDTH, -\-width WIDTH** | Max column width to use for text |
| **-p PADDING, -\-pad PADDING** | Number of spaces to pad around the name in each namebar |

## Module Functions

#### figlet - Wrapper function to run FIGlet as a shell subprocess.

```python
figlet(message, /, opt='std', *opts, prefix='##', pad=2, def_len=3,
        no_skip=False, width=80)
```

Runs  figlet, passing in the *message*.  Other  options may be
given using *opt* or *opts*. *opt* is a key used to access a tuple
of  options  from  a  dict of default options.  If *opts*  are
given, they take priority over *opt*.

If  the subprocess's returncode == 0,  the bytes object that
represents figlet's output is converted to a str.  If given,
the *prefix* is prepended to each line in the output, followed
by `' ' * pad`.

A default  return  value is created from the *prefix* and pad,
followed by a newline. If no_skip is False or the returncode  
is an error value, a string consisting of `default * def_len`
is returned.

#### section - Make a new '###  section  ###'

```python
section(name, /, lines=1, prefix='\n', width=80, char='#', pad=1,
            tags='    ', head='\n', foot='', headlen=1, footlen=0,
            *fig_args, **fig_kwds)
```

Returns  a  block   of   lines   surrounded   by  '###  *name* ###' 
bars  that  are  *width*  long.  The  head  string  is
added   before   the   top   namebar  *headlen*  times,  and
defaults  to `'\n'   *   1`.  The   foot   string  is  added below the
bottom  namebar  *footlen*  times,  and defaults to `'\n' * 0`.
If figlet is used, *fig_args* and *fig_kwds* are passed to it.

If *lines* is  a  string, it  will  be  inserted between the
name bars  as-is.  If  *lines*  is  an  integer,  the  body of
the section will be `prefix  *  lines`.  The  char string is
used  to  make  the  namebars - '!' would produce '!!!  name  !!!'
If  using  a  str  longer  than  one character,  adjust  the
width  accordingly.  The  *pad*  integer specifies the  amount
of  spaces  '  '  to  put  around  the  name  in  each  bar.

The *tags*  string  specifies  the  characters  to  be  placed
around  the  name  in  each  namebar,  which  are spaces ' '
by default. The tags can  be  given in a few different ways.
An  empty  string  will  result  in no extra padding in  the 
namebars.  A  single  character or three characters will  be 
filled in with spaces ' '.  If  two  characters  are  given,
a  space  ' ' will be placed after each character.

Examples of tags:
> ''
> -> '### name ###', '### name ###'
> 
> '!!@@'
> -> '### !name! ###', '### @name@ ###'
> 
> '@!' -> '@ ! '
> -> '### @name  ###', '### !name  ###'
> 
> '@' -> '@   '
> -> '### @name  ###', '###  name  ###'
> 
> '@!@' -> '@!@ '
> -> '### @name! ###', '### @name ###'

#### dough - Generate the the contents of a new .py file

```python
dough(name, /, blocks=('setup', 'helpers'), length=5, width=80,
        tags='   ', pad=1, use_fig=False, use_ego=False,
        use_main=True, use_foot=False)
```

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