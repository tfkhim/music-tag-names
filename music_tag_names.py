#!/usr/bin/env python

import sys
import os
import itertools

import mutagen

CHAR_MAP = {" " : "_", 
            "/" : "_",
            "?" : ""}

PATTERN = "{artist}-{tracknumber:02d}-{title}"

def leadingIntegerParse(intStr):
    intStr = intStr.strip()
    intStr = itertools.takewhile(lambda x: x.isdigit(), intStr)
    return int("".join(intStr))

class TagStringFilter(object):
    def __init__(self, charMap, toLower=False):
        self.toLower = toLower
        self.charMap = charMap

    def __call__(self, inputStr):
        def mapFunc(value):
            return self.charMap.get(value, value)
        mappedStr = "".join(map(mapFunc, inputStr))
        return mappedStr.lower() if self.toLower else mappedStr

class FilenameBuilder(object):
    def __init__(self, tagFilter, pattern):
        self.tagFilter = tagFilter
        self.pattern = pattern

    def __call__(self, inputFile):
        tagInfo = mutagen.File(inputFile, easy=True)
        if not tagInfo:
            return os.path.basename(inputFile)
        
        def mapTagData(keyValue):
            key, values = keyValue
            if len(values) > 0:
                return (key, self.tagFilter(values[0]))
            else:
                return None

        tagInfo = dict(filter(None, map(mapTagData, tagInfo.items())))

        trackNum = tagInfo.get("tracknumber", "0")
        tagInfo["tracknumber"] = leadingIntegerParse(trackNum)

        try:
            formatedFilename = self.pattern.format(**tagInfo)
        except KeyError:
            return os.path.basename(inputFile)

        extension = os.path.splitext(inputFile)[1]
        return "{0}{1}".format(formatedFilename, extension)

class FileRenamer(object):
    def __init__(self, nameBuilder, dryRun=False):
        self.nameBuilder = nameBuilder
        self.doRename = self.doDryRun if dryRun else self.doRenameImpl

    def doDryRun(self, source, destination):
        print("{0} -> {1}".format(source, destination))

    def doRenameImpl(self, source, destination):
        os.rename(source, destination)

    def recurseDirectory(self, directory):
        for path, _unused, files in os.walk(os.path.abspath(directory)):
            for file in files:
                filename = os.path.join(path, file)
                newName = self.nameBuilder(filename)
                self.doRename(filename, os.path.join(path, newName))

    def renameFile(self, filename):
        newName = self.nameBuilder(filename)
        path = os.path.dirname(os.path.abspath(filename))
        self.doRename(filename, os.path.join(path, newName))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {0} <audio file>".format(sys.argv[0]))
        sys.exit(2)

    fileOrDir = sys.argv[1]

    tagFilter = TagStringFilter(CHAR_MAP, True)
    builder = FilenameBuilder(tagFilter, PATTERN)
    fileRenamer = FileRenamer(builder)

    if os.path.isdir(fileOrDir):
        fileRenamer.recurseDirectory(fileOrDir)
    else:
        fileRenamer.renameFile(fileOrDir)

