 
# Obfuscator for C Source code
### Author: Filip Januška

**Full repo link: https://github.com/Captain00180/CScrambler**

This project implements a python class **Scrambler**, which obfuscates source code in C language.

The class provides three simple methods of obfuscation: Obfuscating identifiers, string and integer literals and whitespace removal. 

Basic usage of the class is demonstrated in the **main.py** script. 

### Dependencies
The project depends on an external python module **pycparser**, which can be installed from pip. 

### Limitations
This project is merely a demo of some obfuscation methods. It only works on simple C programs and doesn't support all C constructs or programs using any external modules with the #include directive . 
The obfuscated code should however remain fully functional. 
