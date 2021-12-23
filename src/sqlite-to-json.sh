db="$1";
key=$( /usr/local/bin/jq -r '."key"' $2 );

/usr/local/bin/sqlcipher -list -noheader "$db" "PRAGMA key = \"x'"$key"'\";select json from messages;" | tail -n +2 | jq -R -s -c 'split("\n")'