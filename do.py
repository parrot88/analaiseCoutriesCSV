# coding: utf-8
"""
パラメータからnhentaiのurlを渡す
"""

import sys
import funcs

args = sys.argv

googlePlayURL = "https://play.google.com/store/apps/details?id=com.kuwagata.timestamp&hl=ja"
funcs = funcs.Functions(googlePlayURL)
#funcs = funcs.Functions(args[1])
funcs.get_all()
