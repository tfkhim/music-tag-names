music-tag-names
===============

Python program for renaming audio files based on song meta data. There
aren't any options to adjust the renaming. So this is only useful for my
personal use or anyone with the same naming schema for their audio
library. The output is all lower case and uses the following pattern for
the file name:

    {artist}-{tracknumber:02d}-{title}

The tool relies on properly tagged audio files to extract the required
values used in the pattern. Reading the meta data is done using the
[mutagen](https://pypi.org/project/mutagen/) library.

With minor changes to the source code a different naming schema can be
achieved. See [Configure section](#Configure) for more details.

Setup
-----

Clone the repository and install it.

    python setup.py install

Consider creating a virtual environment to install the module in
isolation.

Examples
--------

You can pass a single file to the script to change its name

    music_tag_names.py <audio-file>

You may also pass a directory. The script will then recursively
rename all audio files

    music_tag_names.py <directory>

Files for which mutagen isn't able to detect the file type will
be skipped.

Configure
---------

The global variable `PATTERN` contains the file name pattern. You may use
any tag names supported by mutagen.

Add or change the `CHAR_MAP` dictionary for converting some undesired
characters contained in the tags.

Change the `toLower` constructor argument of the `TagStringFilter` class
instantiation to `False` if you do not want all lower case file names.
