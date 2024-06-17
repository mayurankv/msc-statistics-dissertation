#!/bin/zsh
DISSERTATION_PATH=~/Documents/Mayuran/Programming/Projects/Academic/Imperial\ College\ London/MSc\ Statistics/Dissertation

mkdir -p $MYDISSVAULT/utilities/obsidian/latex_suite
mkdir -p $MYDISSVAULT/utilities/obsidian/templater
ln -s $MYOBSIDIANPATH/package_settings/.latex_suite/snippets $MYDISSVAULT/utilities/obsidian/latex_suite/snippets
ln -s $MYOBSIDIANPATH/package_settings/.templater/templates $MYDISSVAULT/utilities/obsidian/templater/templates
ln -s $MYOBSIDIANPATH/package_settings/.templater/scripts $MYDISSVAULT/utilities/obsidian/templater/scripts
ln -s $MYOBSIDIANPATH/css $MYDISSVAULT/.obsidian/snippets