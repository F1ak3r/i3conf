#!/bin/bash
i3status --config ~/.i3/status.conf | (while :
do
  read line
  id=$(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}')
  if [ x$id != x ]; then
    name=$(xprop -id $id | awk '/_NET_WM_NAME/{$1=$2="";print}' | cut -d'"' -f2)
    name=${name//\\/\\\\}
    name=${name//\"/\\\"}
    dat="[{\"name\":\"title\",\"full_text\":\"$name\"},"
    echo "${line/[/$dat}" || exit 1
  else
    echo "$line "  || exit 1
  fi
done)
