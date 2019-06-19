# Password-Manager-

A CLI based password manager for personal use. It generates cryptographically secure passwords, encrypts them, and stores them in an embedded database.

<!--![compressed_example](https://user-images.githubusercontent.com/44934000/52548221-52ddec80-2d9a-11e9-8f07-50920cdc8b02.gif)-->

## Encryption
It is essential that account data is encrypted before it is stored. This program uses the `cryptography` library built on AES-128 in conjunction with PBKDF2 (SHA256) to generate keys. The passwords are salted using the secure random number generator from `urandom`.

## Getting Started
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

It is recommended for future convenience to a shell script to run the program.<br/>

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
<img src="https://user-images.githubusercontent.com/44934000/52547424-94b86400-2d95-11e9-8fdb-46779f75612c.png" width="400"><img src="https://user-images.githubusercontent.com/44934000/52547415-8ec28300-2d95-11e9-8d79-6dbc7cf5f789.png" width="400">

#### Fuzzy searching


*project by Felix Zhou.*
