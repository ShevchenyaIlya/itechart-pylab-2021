## What does the program do?
- _parser.py_ - main fail that collect reddit post information such as: 
username, user karma, user cake day, post karma, comment karma, post date, number of comment, number of votes,
 post category  
 
- _server.py_ - server implementation using Python standard library tools without third-party libraries and frameworks.

- _cache.py_ - simple cache for server

- _xpath_config.json_ - xpath templates for basic html blocks

- _file_management.py_ - processing and communication with files

- _url_processing.py_ - functions for managing request url

- _parser_async_page_opening.py_ - analog of _parser.py_ but user pages are opened and parsed asynchronously
## How do I start the program? 
### Run parser.py
```bash
python parser.py 
usage: parser.py [-h] [--path path] [--log_level log_level]
                 [--post_count post_count]

Reddit parser

optional arguments:
  -h, --help            show this help message and exit
  --path path           Chromedriver path
  --log_level log_level
                        Minimal logging level('DEBUG', 'INFO', 'WARNING',
                        'ERROR', 'CRITICAL')
  --post_count post_count
                        Parsed post count
```

### Start server
```bash
python server.py
usage: server.py [-h] [--port port] [--log_level log_level]

Simple http server

optional arguments:
  -h, --help            show this help message and exit
  --port port
  --log_level log_level
                        Minimal logging level('DEBUG', 'INFO', 'WARNING',
                        'ERROR', 'CRITICAL')

```

### How to connect to server?

- Change setting in _db_connection_setting.json_ file for your own
