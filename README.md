# Password-Manager-

A python based password manager for personal use. It generates crytographically secure passwords, encrypts them, and stores them in an embedded database.

![compressed_example](https://user-images.githubusercontent.com/44934000/52548221-52ddec80-2d9a-11e9-8f07-50920cdc8b02.gif)

## Encryption
It is essential that account data is encrypted before it is stored. This program uses the 'cryptography' library built on AES-128 in conjunction with PBKDF2 (SHA256) to generate keys. The passwords are salted using the secure random number generator from 'urandom'.

## Getting Started
### Setup and Dependencies
It is recommended to use Python3.6.1+. The following dependencies are necessary:
```
$ pip3 install py-bcrypt
$ pip3 install cryptography
$ pip3 install sqlalchemy
$ pipe install pyperclip
```
Then clone the repository by doing:

```
$ git clone https://github.com/zhoufel1/Password-Manager-.git
```
### How To Use
To run the program, ensure permissions with:
```
$ chmod u+x main.py
```
and run:
```
$ ./main.py
```
On first startup, the program will initialize an embedded database and prompt the user to create a password.

Onwards, the program will prompt the user for that created password.

<img src="https://user-images.githubusercontent.com/44934000/52547424-94b86400-2d95-11e9-8fdb-46779f75612c.png" width="400"><img src="https://user-images.githubusercontent.com/44934000/52547415-8ec28300-2d95-11e9-8d79-6dbc7cf5f789.png" width="400">

Since this program doesn't have a GUI, input numbers to access the various options.

For ease, when querying for accounts by website, you can enter keywords (e.g., entering gmail rather than ht<span>tp</span>://w<span>ww.gm</span>ail.com)

*project by Felix Zhou.*
