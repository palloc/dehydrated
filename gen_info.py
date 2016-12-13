#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

if len(sys.argv) < 3:
    print("Error: few arguments")
    exit(1)
    
with open("APIfile.data", "wb") as file:
    user = sys.argv[1]
    password = sys.argv[2]

    file.write(user + '\n')
    file.write(password)





