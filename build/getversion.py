#!/usr/bin/evn python 
#coding:utf-8

if __name__ == "__main__":
    try: 
        import xml.etree.cElementTree as ET
    except ImportError: 
        import xml.etree.ElementTree as ET
    import sys
        
    try:
        tree = ET.parse(sys.argv[1])            #打开xml文档
        root = tree.getroot()                   #获得root节点
        entry = root.find('entry')
        commit = entry.find('commit')
        revision = commit.get('revision')
        sys.exit(revision)
    except Exception, e:
        print "Error:cannot parse file:Version.xml."
        sys.exit(1)
  
