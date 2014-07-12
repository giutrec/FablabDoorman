opkg update
opkg install libsqlite3 sqlite3-cli python-sqlite3 php5-mod-sqlite3 php5-cgi zoneinfo-europe zoneinfo-simple
uci set uhttpd.main.interpreter=.php=/usr/bin/php-cgi
uci commit

uncomment extension=sqlite.so in /etc/php.ini