# tor-crawler

Tor network crawler that saves URL and HTML in SQLite DB.




### Usage
Install requirements

`pip3 install -r requirements.txt`

`sudo apt install tor`

Run

`sudo service tor start`

`python3 main.py `

## TODO
	
 - [ ] Remove crawled urls from list
 - [x] Url parsing remove local paths (#id)
 - [ ] Make it multithreaded
 - [ ] Index the db and make a simple search engine
