# coding=utf-8

import os


if __name__ == "__main__":
    command = "python " + os.getcwd() + "/" + "appmain.py proxy_1 config.json"
    os.system(command)
