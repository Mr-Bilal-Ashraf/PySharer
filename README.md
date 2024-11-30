# ![logo](https://github.com/user-attachments/assets/42af0c02-001b-474c-9721-b394867554f3) PySharer

**PySharer** is a powerful and easy-to-use Python package for sharing and transferring data seamlessly between devices using **LAN** (Local Area Network).

## Installation Guide

You have multiple options to install **PySharer** on your machine:

### Option 1: Install via pip (Recommended)

The simplest way to install **PySharer** is by using `pip`. Open your terminal or command prompt and run:

```bash
pip install pysharer
```

### Option 2: Install from Source by Cloning the Repository

If you prefer to work with the source code or need to modify the package, you can clone the repository and install it locally.

1. First, clone the repository:
```bash
git clone https://github.com/Mr-Bilal-Ashraf/PySharer.git
```

2. Navigate to the project root directory and install the package using pip:
```bash
pip install .
```

### Option 3: Install from the Wheel Distribution
There is also **wheel** file in dist directory, you can also install the package using this **.whl** file.

1. Navigate to the dist/ directory where the .whl file is located:
```bash
cd dist
```

2. Install the .whl file with pip:
```bash
pip install PySharer-***.whl
```
This will install PySharer from the wheel file.

## Run PySharer

The package can be run from anywhere on the system. Just open terminal, type **pysharer** and hit enter...
```bash
pysharer
```
You can go to **localhost:5050** on your browser to see your files. Your **IPV4 address** is also shown there! Anyone from **LAN** can download and upload files using this **IPV4 address**.


![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/fe57a018-1341-49e8-bd1c-5090211c0be7)

## Upload File

Open the **IPV4 address** from any mobile OR other machines in the **LAN** (Local Area Network). Now
click on the **upload** button.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/b1265629-315d-4b4f-9337-e651becad48f)

Now click on the **cloud** icon to select the desired files.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/112c1fc6-4b89-4d24-aeb4-61ddef07c19a)

Now click on the upload button and it will start uploading the file to the system. You can also cancel the file
uploading.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/4a66d2ad-424a-4b4b-8c7b-2e3def005808)

All the uploaded files will be saved in **Downloads** Folder.

## Download File

To **download** any file, just **click** on the file and it will start downloading the file in your system. You can *
*hover over** the file to see the file **full name** and its **size**.

## Flags

You can also use following flags while running the app.

| Flag        | Default |        Expected        |                           Behavior |
|-------------|:-------:|:----------------------:|-----------------------------------:|
| --port      | `5050`  | Any Port (e.g., 5000)  |     app will run on the given port |
| --dot_files |   `0`   | other than 0 (e.g., 1) | to see files starting with dot "." |
| --download  |   `1`   |           0            |        to disable file downloading |
| --upload    |   `1`   |           0            |          to disable file uploading |
| --help      |         |                        |                 to see app details |

`pysharer --help`

`pysharer --port 8000`

`pysharer --dot_files 1`

`pysharer --download 0`

`pysharer --upload 0`

`pysharer --port 8080 --dot_files 2 --upload 0`

## Dependencies

* `Python 3`
* `Flask`
