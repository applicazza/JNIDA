### About

Helps to rename and restore C signatures of JNI native methods

### Installation

Download latest copy of the software and drop into your IDA `plugins` folder.

### Usage

> **DO NOT FORGET TO MAKE A DATABASE SNAPSHOT AND/OR BACKUP YOUR CURRENT PROJECT**

Currently this plugin has been tested under IDA 7.4 with Python 2.7 on Windows and armeabi-v7a shared library.

1. Analyze your binary
2. Proceed to `.data` section and select appropriate lines with function name, function signature and pointer to function.
3. Press `Ctrl + /` and enter desired prefix to be added to function names.

