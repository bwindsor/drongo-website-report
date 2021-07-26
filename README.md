## Project setup
1. Clone the git repository
1. Download the `chromedriver` executable suitable for your version of Chrome from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
1. Put the `chromedriver` executable in this directory
1. Create a Python virtual environment `virtualenv env`
1. Activate the virtual environment `venv/Scripts/activate`
1. Install dependencies `pip install -r requirements.txt`

## What the code does
### Inputs
* A text file containing the report. A new line indicates a new paragraph. Multiple new lines are treated as one.
* A directory containing photos to be uploaded
* The year of the report. This is used to know where to upload the photos to. Example: `2021`
* An upload directory name. This is the subdirectory of the `year` where photos will be uploaded to. For exapmle, `20210710MyEvent`
* Report title. This is the title for the report
* Username and password - used to log into the DrongO website

### Processing
* The image files are resized such that the maximum dimension is 1024px. A small version is also created with a maximum dimension of 200px. These are saved in a temporary directory which is deleted after when the script exits.
* The image files are uploaded to Web Images under the folder `<year>/<upload_directory_name>`. You specify the year and upload directory name as inputs to the script.
* The text file is split into paragraphs by looking for new line characters. Each paragraph is wrapped in a `<p>` tag.
* HTML tags for the image files are generated such that the small image is displayed as part of the report, and this is wrapped in a link such that clicking the image links to the large image displayed in a lightbox. The lightbox is given the same name as the image upload directory. The CSS class is set alternately to `FloatLeftImage` and `FloatRightImage` which has the effect of alternating images between appearing on the left and the right of the report.
* The photo HTML tags are interleaved with the text paragraphs such that there is one photo per paragraph (so if you have short paragraphs it may look strange). If there are more paragraphs than photos, trailing paragraphs do not have a photo. If there are more photos than paragraphs, trailing photos are just appended to the end, which may also look strange. 
* The interleaved HTML is uploaded to the website along with the report title

#### Idempotency
This is the ability to re-run the script without creating multiple reports. For example, if you decide to change the set of photos you use, or change the report text.

The script can be re-run without creating duplicate reports on the website provided that **the report title stays the same**. This is because the script searches reports by title to find out which one to edit if it already exists, otherwise it creates a new report.

When re-uploading images, existing ones are overwritten if they have the same name. Deleted images are not removed from the website however. To avoid two sets of images, **the year and upload directory name should stay the same** when re-running the script for the same report.

## Running the code

### From the command line
See usage by running 
```shell
python make_report.py --help
```

### From python
1. Copy `run_make_report.example.py` and rename as `run_make_report.py`
1. Fill in the inputs in `run_make_report.py` to suit your needs
1. Run the script with `python run_make_report.py`

`run_make_report.py` is excluded from Git to prevent you from committing your username and password.
