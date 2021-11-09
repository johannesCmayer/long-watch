# long-watch
CLI program to track how much time has passed since events you specify.

Requirements: 
- click
- python >= 3.5

One use can be to track how long you manaed to not procrastinte. Example output:
```
NoFap:             51 days, 21:17:42
Youtube:           09:12:42
Gameing:           40 days, 08:45:42
Movies and Series: 12 days10:47:42
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
