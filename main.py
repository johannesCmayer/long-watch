import datetime
import click
import os
import json
import re
from pathlib import Path
import math

#TODO Have tracker groups, that are visually seperated in the output and can be ordered
#TODO allow to change the ordering of trackers
#TODO Unhardcode goal display
#TODO Save the history of all updates in a file
#TODO Allow to different kinds of input as dates (not just one hardcoded one, e.g. allow to specify seconds, and have a shortcut for now, and allow to add to now[possibly without having to specify the now e.g. +1d10:00:00])
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
    """Delete tracker"""
    d_dict = ctx.obj
    del d_dict[name]
    with open(SAVE_FILE, 'w') as f:
        json.dump(d_dict, f, indent=4)
    print(f"Removed tracker {name}")

@cli.command()
@click.pass_context
@click.option('-n', '--name', required=True, help="The name of the tracker")
@click.option('-d', '--date', required=True, help="The start tracking date")
def create(ctx, name, date):
    """Create tracker"""
    regex = r'^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$'
    if not re.search(regex, date):
        print(f"Invalid format. Use format: {regex}")
        exit(1)

    d_dict = ctx.obj
    if name in d_dict:
        print(f"Tracker {name} already exists.")
        return
    d_dict[name] = date
    with open(SAVE_FILE, 'w') as f:
        json.dump(d_dict, f, indent=4)
    print(f"Creating tracker {name}")

@cli.command()
@click.pass_context
@click.option('-n', '--name', required=True, help="The name of the tracker")
@click.option('-d', '--date', required=True, help="The start tracking date")
def update(ctx, name, date):
    """Update tracker"""
    regex = r'^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$'
    if not re.search(regex, date):
        print(f"Invalid format. Use format: {regex}")
        exit(1)

    d_dict = ctx.obj
    if name not in d_dict:
        print(f"Tracker {name} does not exsist.")
        return
    d_dict[name] = date
    with open(SAVE_FILE, 'w') as f:
        json.dump(d_dict, f, indent=4)
    print(f"Updating tracker {name}")

#TODO fix if the event is more than a year away
@cli.command()
@click.pass_context
@click.option('-n', '--name', required=False, help="The name of the tracker")
def list(ctx, name):
    """List active trackers"""
    if len(ctx.obj) == 0:
        print(f"{SAVE_FILE} contains no trackers.")
    else:
        print_list = []
        for item_name, date in ctx.obj.items():
            if name != None and name != item_name:
                continue
            time = (datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            negative_days = time.days < 0

            years = math.floor(abs(time.days / 365))
            days = abs(time.days) % 365
            #TODO fix the countdown of time (it seems to be offset by an hour)
            total_seconds = (60*60*24 - time.seconds) if negative_days else time.seconds
            hours = total_seconds // 60**2
            minutes = abs(total_seconds // 60) % 60
            seconds = abs(total_seconds) % 60

            print_list.append([
                item_name,
                "- " if negative_days else "",
                f"{years}y " if years != 0 else '', 
                f"{days}d " if days != 0 else '', 
                f"{hours:02.0f}:",
                f"{minutes:02.0f}:",
                f"{seconds:02}"
            ])
        for j, e in enumerate(print_list):
            for i, arg in enumerate(e):
                max_len = max([len(x[i]) for x in print_list])
                postfix = ": " if i == 0 else ""
                print(arg + postfix + " " * (max_len - len(arg)), end='')
            print()

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
