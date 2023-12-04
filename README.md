# PhotogScreener
by Lyjia

PhotogScreener automatically identifies blurry photos and makes it easy to delete them. Many photographers shoot hundreds or thousands of photos in a single photoshoot, which can occupy significant amounts of disk space. PhotogScreener makes it easy to identify bad shots and delete them.

THIS SOFTWARE IS CURRENTLY A PROTOTYPE. Not recommended for regular use at this time.

## How to Use

1. Open PhotogScreener and go to File > Scan Folder...
2. Point it towards a folder of potentially bad images.
3. PhotogScreener will scan the folder and present its results in the right-side pane.
4. Hover the mouse over an image to see a tooltip with the results of the scan.
5. Use the filters in the left pane to narrow down the different kinds of scan results (e.g. blurry images only)
6. Check the images that you wish to delete
7. Hit the "Remove" button to either delete the image or send it to the recycle bin (this can be changed in the options)

## Getting the code running

### From a prepackaged build:

TBA

### From source:
1. download the code
1. (OPTIONAL) create a virtual environment for this code in a subfolder called "venv" by running `python -m venv venv`
1. (OPTIONAL) activate the venv using your platform's activation script (refer to the table at https://docs.python.org/3/library/venv.html#how-venvs-work for the command for your platform)
1. run `python -m pip install -r requirements.txt`
1. run `python main.py`
