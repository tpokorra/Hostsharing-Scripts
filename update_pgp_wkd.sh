#!/bin/bash

# siehe https://wiki.hostsharing.net/index.php/WKD_einrichten

if [ -z $1 ]
then
    echo "Bitte den Pfad für die Datei mit dem öffentlichen Key mitgeben: z.B. $0 ~/public.txt"
    exit
fi
publickeyfile=$(realpath $1)

if [ ! -f $publickeyfile ]
then
    echo "Kann den öffentlichen Schlüssel nicht finden: $publickeyfile"
    exit
fi

DOMAIN=$(find ~/doms/openpgpkey.*/htdocs-ssl | head -n 1 | awk -F/ '{ print $8 }' | sed -e 's/openpgpkey.//g')

if [ -z $DOMAIN ]
then
    echo "Zuerst muss die subdomain openpgpkey.$DOMAIN im HSAdmin eingerichtet werden!"
    exit
fi

cd ~/doms/openpgpkey.$DOMAIN
cat > .htaccess  <<FINISH
ForceType application/octet-stream;
<IfModule mod_headers.c>
   Header set Access-Control-Allow-Origin "*"
</IfModule>
FINISH
cd ~/doms/openpgpkey.$DOMAIN/htdocs-ssl/
rm -f .htaccess
mkdir -p .well-known/openpgpkey
cd .well-known
gpg --import < $publickeyfile
gpg --list-options show-only-fpr-mbox  -k "@$DOMAIN" | /usr/lib/gnupg/gpg-wks-client --install-key
touch openpgpkey/$DOMAIN/policy
chmod a+x openpgpkey/$DOMAIN/
chmod a+x openpgpkey/$DOMAIN/hu/
touch openpgpkey/$DOMAIN/hu/index.html
