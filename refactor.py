#!/usr/bin/python
# -*- coding: utf-8 -*-

# refactor.py <oldPrefix> <newPrefix> <filePath>

from getopt import getopt
import os
import sys

def refactor_class_name():
    print("start refactor the class name")

def get_class_paths_and_names(root):
    file_paths = []
    class_names = []
    for base, dirs, files in os.walk(root):
        for name in files:
            file_path = os.path.join(base, name)
            file_paths.append(file_path)
            if ".m" in name:
                splits = name.split(".m")
                class_name = splits[0]
                class_names.append(class_name)
    return (file_paths, class_names)

def rename_file(file_path, old_prefix, new_prefix):
    splits = file_path.split("/")
    last = splits.pop()
    if last.startswith(old_prefix):
        new_last = new_prefix + last.lstrip(old_prefix)
        splits.append(new_last)
        new_file_path = "/".join(splits)
        os.rename(file_path, new_file_path)

def do_refactor(class_paths_and_names, old_prefix, new_prefix):
    class_paths = class_paths_and_names[0]
    class_names = class_paths_and_names[1]
    for class_path in class_paths:
        with open(class_path, "r") as file_reader:
            lines = file_reader.readlines()
        with open(class_path, "w") as file_writer:
            for line in lines:
                for class_name in class_names:
                    if class_name in line and class_name.startswith(old_prefix):
                        new_class_name = new_prefix + class_name.lstrip(old_prefix)
                        print("Replace " + class_name + " to " + new_class_name)
                        line = line.replace(class_name, new_class_name)
                        print("New Line: " + line)
                file_writer.write(line)
        rename_file(class_path, old_prefix, new_prefix)

def main():
    opts, args = getopt(sys.argv[1:], "h", "help")
    if len(args) != 3:
        print("Usage: refactor.py <oldPrefix> <newPrefix> <filePath>")
        return -1
    if os.path.exists(args[2]) != 1:
        print("ERROR: Your input file path <" + args[2] + "> is not exists!")
        return -2
    paths_and_names = get_class_paths_and_names(args[2])
    do_refactor(paths_and_names, args[0], args[1])

if __name__ == '__main__':
    sys.exit(main())
