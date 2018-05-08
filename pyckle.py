#!/usr/bin/env python3

import os, sys, configparser, subprocess
from tempfile import TemporaryFile

def error (reasons):
    print("error")
    for r in reasons:
        print(r)
    print("exiting")
    sys.exit(0)  

def parse_config ():
    print("checking config.ini... ", end = '')
    missing = []
    config = configparser.ConfigParser()

    if os.path.isfile('./config.ini'):
        config.read('./config.ini')
    else:
        error(["config.ini is missing from this directory"])
    if 'default' not in config:
        error(["[default] section missing from config.ini"])

    keys = ['layouts', 'public', 'markdowns', 'domain']
    for key in keys:
        if key not in config['default']:
            missing.append("\"%s\" key missing from config.ini" % key)
    if missing:
        error(missing)

    conf = {}
    for key in keys:
        conf[key] = config['default'][key]
         
    print("done")
    return conf

def find_markdown (root):
    print("finding markdown files... ", end = '')
    md = []
    for dirName, subdirList, fileList in os.walk(root):
        for fname in fileList:
            if fname.endswith(".md"):
                md.append((dirName+"/"+fname)[len(root):-3])
    print("done")
    return md

def generate_website (f, conf):
    if os.path.isfile(conf['public'] + f + ".html"):
        print("updating ", end = '')
    else:
        print("creating ", end = '')
    print ("website.com" + f + ".html... ", end = '')

    md_file, tags = parse_markdown(conf['markdowns'] + f + ".md")
    # check tags in template
    # build page

    print("done")

def parse_markdown (markdown_file):
    md_file = TemporaryFile()
    md = open(markdown_file,"r")
    tags = {}
    for ln in md:
        if ln.startswith("@"):
            try:
                i = ln[1:-1].split(': ')
                tags[i[0]] = i[1]
            except:
                error(["\""+i[0]+"\" variable in "+markdown_file+" formatted incorrectly"])
        else:
            md_file.write(bytes(ln, 'UTF-8'))

    #tags = infer_tags(md_file, tags)

    return md_file, tags

def main ():
    conf = parse_config()
    files = find_markdown(conf['markdowns'])
    for f in files:
        generate_website(f, conf)
    print("finished successfully")

if __name__ == "__main__":
    main()