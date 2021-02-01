# coding=utf-8
from installer import check_checksum
import sys
from tkinter import *
from tkinter import messagebox as mb


if not check_checksum("license.key"):
    print("You don't have a license!")
    mb.showerror("error", "You don't have a license!")
    sys.exit()
else:
	print("well,you have access to control this programme..!!")