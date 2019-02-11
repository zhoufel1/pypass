# Password-Manager- 

A python-based password manager for personal use. It automatically creates secure randomly generated passwords, encrypts them, and stores account information in an embedded database. The account information is then decrypted when retrieved. 

## Getting Started 
### Setup and Dependencies 
Program is tested on Python 3.6. It is recommended you initialize a python virtual environment and do:
```
$ pip3 install py-bcrypt
$ pip3 install cryptography 
$ pip3 install sqlalchemy
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
On first startup, the program will initialize an embedded database and prompt the user to create a password. Onwards, the program will prompt the user for that created password. 

