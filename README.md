# pypass

Pypass is a fast, secure, and user-friendly CLI based password manager written in Python.

# Table of Contents
1. [Features](#features)
2. [Encryption](#encryption)
3. [User Guide](#user-guide)

## Features
Pypass serves as an alternative to pricey and bloated GUI-based password managers as well as well written CLI solutions that are very functional but often hard to use. Some features include:

* Secure storage of passwords in an embedded database.
* SHA256 based encryption.
* Organized tree based visualization of account information.
* Fuzzy saerching for account information
* Copy to clipboard

## Encryption
It is essential that account data is encrypted before it is stored. This program uses the `cryptography` library built on AES-128 in conjunction with PBKDF2 (SHA256) to generate keys. The passwords are salted using the secure random number generator from `urandom`.

## User Guide
### Setup and Dependencies
It is recommended to use Python3.6.1+. The following dependencies are necessary:
```
$ pip3 install py-bcrypt
$ pip3 install cryptography
$ pip3 install sqlalchemy
$ pip3 install pyperclip
```
Then clone the repository by doing:

```
$ git clone https://github.com/zhoufel1/Password-Manager-.git
```
### Using
The program is executed through via the 'run' script:
```
$ ./run
```
The program will prompt for the creation of a master password which will be used to access the database on future use.

It is recommended for future convenience to have a shell script to run the program.<br/>

Here is an example script that will activate a virtual environment containing the dependencies, run the program, and deactivate the virtual environment on exit.
```
#!/bin/bash

# Activate venv called 'password' containing the dependencies
source $HOME/.virtualenvs/password/bin/activate

# Run program
cd $HOME/Other/Password-Manager-
./run

# Terminate venv on program close.
deactivate
```
<!--<img src="https://user-images.githubusercontent.com/44934000/52547424-94b86400-2d95-11e9-8fdb-46779f75612c.png" width="400"><img src="https://user-images.githubusercontent.com/44934000/52547415-8ec28300-2d95-11e9-8d79-6dbc7cf5f789.png" width="400">-->

#### Fuzzy searching
To aid with accessing items in the repository, the program has a fuzzy searcher which will return items associated with the user query.<br/>
<img src="https://user-images.githubusercontent.com/44934000/59738202-66103580-922e-11e9-8f1b-793cbbfe1cdd.png" width="350"><img src="https://user-images.githubusercontent.com/44934000/59738201-66103580-922e-11e9-9836-7fafbb7cc452.png" width="350">

#### Password Copying
Passwords are copied to the clipboard directly after query. The system
clipboard is purged after the program terminates.<br/>

_project by Felix Zhou._
