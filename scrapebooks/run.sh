#! /bin/bash

scrapy crawl books -o books.json

pyhton json2sqlite.py

echo "DONE!"

pause