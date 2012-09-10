#! /bin/sh
# returns the address of the first ethernet interface found
# (stops at eth10 to avoid endless loop)
i=0
found=FALSE
while [ $found = FALSE ]
do
  if ip addr show eth${i} >/dev/null 2>&1
  then
    found=TRUE
    ip addr show dev eth${i} | grep "inet " | sed -E "s/ +inet +([^/]+).+/\1/"
  else
    i=$((i+1))
    if [ $i -eq 10 ]
    then
      echo 0.0.0.0
      echo "No ethernet interface" >&2
      exit 1
    fi
  fi
done
