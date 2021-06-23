# FoodTruckFinder

Are you hungry? Do you love buying food from trucks? Do you live in San Francisco? Are you a huge fan of CLIs?

If this sounds like you, brace yourself. Earth-shattering developments in mobile food facility locator technology are about to change your life forever!

Enter the FoodTruckFinder: a concise Python script which, when given your current latitude and longitude coordinates, will find you the ten closest food trucks or push carts in San Francisco.

# Quickstart

## Prerequisites

- NOTE: These instructions assume you are running Windows!
- Download and install Python >= 3.9.5 (@ https://www.python.org/downloads/)
- Open Windows Terminal or your favorite CLI and navigate to the root of this repository.

## Create and activate a virtual environment for this project
```
py -m venv .venv
.\.venv\Scripts\activate
```

## Install required dependencies
```
pip install -r requirements.txt
```

## Run FoodTruckFinder
```
Expected usage: py ftf.py [your_latitude] [your_longitude]
          e.g., py ftf.py 37.7775 -122.416389
```

# Development

First, ensure you have fulfilled all the prerequisites above.

To get going quickly, we recommend using VS Code and its Python extension. If you don't already have these installed, the [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) guide has excellent instructions.

Next, you'll want to open the project folder in VS Code. If your current working directory is the root of this repo, you can do this from the CLI with
```
code .
```

## Selecting the right Python interpreter

Because you already created a virtual environment (`.venv`) and because our `.vscode\settings.json` already knows to look for an environment with that name, you shouldn't need to manually select the Python interpreter used by VS Code.

If you're curious, you can learn more about manually selecting a Python interpreter [here](https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter).


## Running and debugging FoodTruckFinder
Open `ftf.py` and select `Run > Start Debugging` or `Run > Run Without Debugging` in VS Code. This will run the script based on our configuration in `.vscode\launch.json` which specifies a known good set of lat/long coordinates (taken from San Francisco's Wikipedia page) as arguments.

## Adding or updating packages
If you modify the set of packages this project depends on, remember to update our list of dependencies with the below command before committing:
```
pip freeze > requirements.txt
```

## Testing

TODO

# Context

This project is my submission to CSE's Take Home Engineering Challenge.

Above all else, you should know I have zero prior experience with Python and its tooling. But, in keeping with the organization's spirit of learning as a core competency, I decided to have some fun and try something new.

Why Python, though? I recently took Andrew Ng's (somewhat dated) Machine Learning open courseware, and while the material and assignments were fantastic, all the coding was in MATLAB. So, knowing that Python is a favorite language of modern ML & AI practitioners, it's been on my short list of tech to explore. This project proved an excellent opportunity to get a little experience working with the language (and even the pandas data analysis library!).


# Some parting thoughts

## Known items which merit further investigation/consideration
- Expand README instructions for multiple platforms
- Add an auto-formatter and linter
- Investigate how to package this script as a proper module and distribute it on Python Package Index (PyPI), or perhaps as an all-in-one single executable
- Read through popular open-source Python projects to get a better idea of common conventions and best practices which could be applied here
- Investigate parsing user input as Decimals (using the decimal module) instead of floats; this may be totally overkill, but would be good to confirm we're not sacrificing accuracy by storing lat/long coordinates in floats


## Potential new features
- Add support for a "force refresh" flag to cause food truck data to be downloaded even when it's already present on disk
- Allow users to mark food trucks as "visited" or "ignored" so they can optionally be filtered out of future searches when the user wants to try something new
- For food trucks missing lat/long data, approximate these coordinates based on the given address
- Currently, depending on the lat/long the user provides, it is possible to see multiple entries/permits for the same type of truck which have only minor variations in their locations. Support a new CLI argument to trim these similar options when presenting results
- Only show trucks currently open/on-site when a user is searching. (This would likely be difficult; though the dataset contains a "dayshours" column and some trucks have schedule info here, the field is not consistently populated)