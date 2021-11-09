# long-watch
CLI program to track how much time has passed since events you specify.

Requirements: 
- click
- python >= 3.5

Example output:
```
NoFap:             4 days, 21:17:42
Gameing:           08:45:42
Movies and Series: 10:47:42
Youtube:           09:12:42
```
Output of `long-watch --help`
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create tracker
  list    List active trackers
  remove  Delete tracker
  update  Update tracker
```
