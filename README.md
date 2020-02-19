# SCUD - Server <- Curate 
#          \ 
#           *-------> Details

An absolutely trivial tool to store server details. By details I mean the usual jam - host, user/pass, identity file location (right, that's a big no no!). But anyway, this is a tool for the extreme lazy, who want to quickly connect to one of the insane amount of servers bestowed upon oneself to look after.

## Installation

```
git clone <repo>
cd <repo>
ln -s $PWD/scud.py ~/.local/bin/scud
```

## Usage

All the server details are stored as simple json, in a file called `scud`. The `default` location is `~/.config/scud.json`.

The sub-commands are similar to `git`, because you have one less thing to remember.

### commit

Add a new details to `scud` file. This command gathers details *interactively!*. Except *nickname*, you can pretty much skip all!

**Note:**

* If the file given doesn't exist or is ignored, a new one will be created.
* If the file isn't valid json, an error will be raised.

```
scud commit
scud commit -f /path/to/scud.json
```

### checkout

Finds one or more server details from the given `scud` file. The search text will match against *nickname*, *host* & *username* of a server detail. So, you can get multiple hits.

**Note:**

* If the file given doesn't exist or isn't valid json content, an error will be raised.
* If the search text is empty, all details will be returned.

```
scud checkout aws_staging
scud -f /path/to/scud.json checkout aws_staging

scud checkout ""
scud -f /path/to/scud.json checkout ""
```

### log

Displays all available server details from the given `scud` file.

**Note:** If the file given doesn't exist or isn't valid json content, an error will be raised.

```
scud log
scud -f /path/to/scud.json log
```

## Plans

Idea is to learn various python concepts and best practices. So, this tool will be updated to include,

* Tests
* Documentation
* Installation via PyPi
* PEP guidelines
* Add encryption - file level or just user/pass
* Backup (there's ideally nothing to backup, its a monolithic json file! compress maybe?)
