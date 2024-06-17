#!/bin/zsh
mkdir -p $MYDISSVAULT/utilities/obsidian/latex/latex_suite
mkdir -p $MYDISSVAULT/utilities/obsidian/templater
ln -s $MYOBSIDIANPATH/package_settings/.latex_suite/snippets $MYDISSVAULT/utilities/obsidian/latex/latex_suite/snippets
ln -s $MYOBSIDIANPATH/package_settings/.latex $MYDISSVAULT/utilities/obsidian/latex/preambles
ln -s $MYOBSIDIANPATH/package_settings/.templater/templates $MYDISSVAULT/utilities/obsidian/templater/templates
ln -s $MYOBSIDIANPATH/package_settings/.templater/scripts $MYDISSVAULT/utilities/obsidian/templater/scripts
ln -s $MYOBSIDIANPATH/css $MYDISSVAULT/.obsidian/snippets