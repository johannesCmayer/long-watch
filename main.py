import datetime
import click
import os
import json
import re
from pathlib import Path

#TODO Save the history of all updates in a file
#TODO Allow to different kinds of input as dates (not just one hardcoded one, e.g. allow to specify seconds)
#TODO Allow teh user to specify the save file location (possibly with config in same dir or in .config)

SAVE_FILE = f"{Path.home()}/.config/tracker/tracker.json"

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.pass_context
@click.option('-n', '--name', required=True, help="The name of the tracker")
def remove(ctx, name):
    """Delete trackers"""
    d_dict = ctx.obj
    del d_dict[name]
    with open(SAVE_FILE, 'w') as f:
        json.dump(d_dict, f, indent=4)
    print(f"Removed tracker {name}")

@cli.command()
@click.pass_context
@click.option('-n', '--name', required=True, help="The name of the tracker")
@click.option('-d', '--date', required=True, help="The start tracking date")
def update(ctx, name, date):
    """Update and create trackers"""
    regex = r'^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$'
    if not re.search(regex, date):
        print(f"Invalid format. Use format: {regex}")
        exit(1)

    d_dict = ctx.obj
    d_dict[name] = date
    with open(SAVE_FILE, 'w') as f:
        json.dump(d_dict, f, indent=4)
    print(f"Updating tracker {name}")

@cli.command()
@click.pass_context
def list(ctx):
    """List active trackers"""
    if len(ctx.obj) == 0:
        print(f"{SAVE_FILE} contains no trackers.")
    else:
        print_list = []
        for name, date in ctx.obj.items():
            time = (datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            time = re.sub(r'\.\d+$', '', str(time))
            print_list.append([
                f"{name}: ", 
                f"{time}"
            ])
        max_len = max([len(x) for x, _ in print_list])
        for name, time in print_list:
            print(name + " " * (max_len - len(name)) + time)

def main():
    data_dir = os.path.dirname(SAVE_FILE)
    if not os.path.isdir(data_dir):
        a = ''
        while a != 'y' and a != 'n':
            a = input(f"{SAVE_FILE} config file does not exsist. Create it? y/n: ")
        if a == 'y':
            os.makedirs(data_dir)
        elif a == 'n':
            print("No config file. Aborting.")
            exit(1)
    data = {}
    if os.path.isfile(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            json_d = f.read()
            if json_d != '':
                data = json.loads(json_d)
    cli(obj=data)

if __name__ == "__main__":
    main()
