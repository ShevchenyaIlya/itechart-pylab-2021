# iTechArt Python labs 2021

Each folder consists of files written in Python for solving laboratory tasks.

## Tasks

- [x] Python script using the Beautiful Soup library to collect data from www.reddit.com for posts in the 
Top -> This Month category.

- [x] Parser data is not saved directly to a file, but through a separate RESTful service available at 
http://localhost:8087/, which in turn provides a simple API for working with basic file operations.

- [ ] Additional challenge: implement parallel post processing using asyncio.

[More information](assignment2/README.md)

## Setup hooks

- Make _setup.sh_ executable
```bash
chmod +x setup.sh
```

- Run _setup.sh_ to copy hooks, install and config postgresql
```bash
./setup.sh
```

### PostgreSQL basic connection
- name: reddit_db
- username: postgres
- password: postgres
