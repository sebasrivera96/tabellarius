# Tabellarius

## Description

Tabellarius is a Face Recognition engine to learn new faces and later detect them on unknown pictures.

## Development Tools

- Ubuntu 16.04 LTS
- Python 3
- [face_recognition module](https://github.com/ageitgey/face_recognition)
- [Pyrebase](https://github.com/thisbejim/Pyrebase)

Note: The supported image files that can be used are: jpg, png, jpeg, JPG.

## How to use it

1. Clone this repository by using the following command:

``` bash
git clone https://github.com/sebasrivera96/tabellarius
```

2. To start the system, run this command:

``` bash
python3 main.py
```

3. A menu with the different functionalities of the system will be shown.

``` bash
************************************************
Please type a CHARACTER to execute an action:

        - [C] ==> Register people from a directory
        - [D] ==> Print the registered people
        - [F] ==> Erase a person given his/her name
        - [G] ==> Look for known people in pictures of a given directory
        - [H] ==> Remove the paths to images of ALL the registered users
        - [I] ==> Remove ALL people registered
        - [exit] ==> Exit
************************************************
```

## Register people

### Multiple registration

1. Organize all the images on a single folder. The image must contain exactly one face, otherwise the registration wouldn't be completed successfully. Following, an example of the organization of the files is shown.

```bash
- facesToRegister/
    - Manuel_Almazan.jpg
    - Aaron_Fernandez.jpg
    - Irasema_Hernandez.jpg
    - Alejandra_Juarez.jpg
```

2. The name of the image must correspond to the name of the person you want to register. For instance, if the name of the person is **Juan de la Cruz** the name of the image must be **_Juan_de_la_Cruz.jpg_** (or any other file extension from the supported ones).

3. Look for the complete path to the directory. It must be copied once the option **[C] - Register people from a directory** is selected from the interactive menu.

<!-- #### Single registration -->

## Identify people

## Delete people & information

## Future development

In the file called [TODO](./TODO.md), one can find the features that could be added to this system.