# Open alex tools

Basic tools to download [OpenAlex](openalex.org) data and export it.
Currently, it is possible to download by

* Specifying an initial paper, then recursively downloading all papers referenced by it

It is also possible to export the data as

* Standard JSON
* JSON formatted for use with VOS viewer
	* Can then be used to make various visualizations of the data

## Usage

To start using the code

* Ensure you have Python 3.7+ installed
* Make a virtual environment with `python -m venv .venv`
* Activate the environment with `source .venv/bin/activate`
* Install the requirements with `pip install -r requirements.txt`
* Add the URL for your base paper and email into the `download.py` file
* Execute the script with `python -m download`

