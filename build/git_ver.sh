# file name: git_ver.sh
#!/bin/bash 
VER_FILE=Version.xml
BASEPATH=$(cd `dirname $0`; pwd)
VER_FILE=$BASEPATH/$VER_FILE
LOCALVER=`git rev-list HEAD | wc -l | awk '{print $1}'`
VER=r$LOCALVER
VER="${VER}_$(git rev-list HEAD -n 1 | cut -c 1-7)"
GIT_VERSION=$VER
echo \<?xml version=\"1.0\" encoding=\"UTF-8\"?\> >$VER_FILE
echo "<info>" >>$VER_FILE
echo "	<entry>" >>$VER_FILE
echo "		<relative-url></relative-url>" >>$VER_FILE
echo "		<commit revision=\"$GIT_VERSION\"></commit>" >>$VER_FILE
echo "	</entry>" >>$VER_FILE
echo "</info>" >>$VER_FILE