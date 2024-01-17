# ![logo](https://github.com/Mr-Bilal-Ashraf/PySharer/blob/master/static/img/short_logo.png) PySharer

This is a flask app use to share files from your machine on the **LAN** (Local Area Network). Just clone the repo and
run the setup.py file. It will show all your system files and folders on system **IPV4 Address**.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/fe57a018-1341-49e8-bd1c-5090211c0be7)

You can go to **localhost:5050** on your browser to see your files. Your **IPV4 address** is also shown there!

## Dependencies

* `Python 3`
* `Flask`

## Run App

Open terminal in the project directory and run the following command,

`python setup.py`

You can also use following flags while running the app.

## Flags

| Flag        | Default |        Expected        |                           Behavior |
|-------------|:-------:|:----------------------:|-----------------------------------:|
| --port      | `5050`  | Any Port (e.g., 5000)  |     app will run on the given port |
| --dot_files |   `0`   | other than 0 (e.g., 1) | to see files starting with dot "." |
| --download  |   `1`   |           0            |        to disable file downloading |
| --upload    |   `1`   |           0            |          to disable file uploading |

`python setup.py --port 8000`

`python setup.py --dot_files 1`

`python setup.py --download 0`

`python setup.py --upload 0`

`python setup.py --port 8080 --dot_files 2 --upload 0`

## Upload File

Just open the **IPV4 address** from any mobile OR other machines in the **LAN** (Local Area Network). You can now see
the whole file structure from that device. You can also upload files from your devices to the sharing machine. Just
click on the **upload** button.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/b1265629-315d-4b4f-9337-e651becad48f)

Now click on the **cloud** icon to select the desired file.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/112c1fc6-4b89-4d24-aeb4-61ddef07c19a)

Now click on the upload button and it will start uploading the file to the system. You can also cancel the file
uploading.

![image](https://github.com/Mr-Bilal-Ashraf/PySharer/assets/92203535/4a66d2ad-424a-4b4b-8c7b-2e3def005808)

All the uploaded files will be saved in **Downloads** Folder.

## Download File

To **download** any file, just **click** on the file and it will start downloading the file in your system. You can *
*hover over** the file to see the file **full name** and its **size**.


