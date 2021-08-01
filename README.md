# Sharkjack Payload Manager
This is a simple CLI tool created to easily switch sharkjack payloads from the command line without the tedious `ls` and `cp` commands.
There are 3 main commands,`set`, `get`, and `list`.
There are interactive elements to make it user friendly, while also providing cli arguments so you can swap payloads faster.


## Table of Contents
- [Commands](#commands)
- [Installation on Sharkjack](#install)
- [Development](#development)

## <a id="commands">Commands</a>

### pmset
Usage: `pmset [options]`
Description: Change the currently active payload on the sharkjack
Options:
- `-c string | --category=string` : Specify which category the payload is in
    - Optional
    - Default: ''
- `-p string | --payload=string` : Specify the name of the payload
    - Optional
    - Default: ''

Set payload interactively, without arguments
```bash
$~ pmset
No category provided
Please Select A Category:  (category1, category2) []: category1
No Payload Provided
Please Select A Payload:  (pay2cat1, pay1cat1) []: pay2cat1
Removing previous payload files
Moving the follwing files: payload.sh
Setting the current payload
pay2cat1 is now active
$~
```

Set payload with options, no interactivity
```bash
$~ pmset -c category1 -p pay1cat1
Removing previous payload files
Moving the follwing files: payload.sh
Setting the current payload
pay1cat1 is now active
$~
```

### pmget
Usage: `pmget`
Description: Prints the currently active payload to the console

```bash
$~ pmget
Current payload category: category1
Current payload: pay2cat1
$~
```

### pmlist
Usage: `pmlist [options]`
Description: Lists payloads and categories in sharkjack file system
- `-s | --show-payloads` : Show Payloads
    - Optional
    - Default: False
- `-c string | --category=string` : Show Payloads from specified category
    - Optional
    - Default: ''

Show categories
```bash
$~ pmlist
Categories:
category1
category2
```

Show All Categories and Payloads:
```bash
$~ pmlist -p
Showing Payloads
category1
pay2cat1
pay1cat1

category2
pay1cat2
pay2cat2
```

Show All Categories and Payloads:
```bash
$~ pmlist -c category2
Showing Payloads
category2
pay1cat2
pay2cat2
```

## <a id="install">Installation On the Sharkjack</a>

### Requirements
You must have the following packages installed on your sharkjack to continue:
- python3
- python3-pip
If you have not yet installed python, or other opkg packages on your sharkjack, refer to [this comment on the hak5 forum](https://forums.hak5.org/topic/50163-curl/?do=findComment&comment=324421) for ways to easily install packages


## <a id="development">Development</a>
