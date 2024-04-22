# HLTB Extractor

## How to Use
---
### 1. Requirements
- **Install Python 3.10 or higher**  
- **[Install Poetry (required)](https://python-poetry.org/docs/)**

---
### 2. Install project and dependencies
```sh
git clone git@github.com:brunurd/hltb-extractor.git ./hltb-extractor
cd hltb-extractor
poetry install
```
---
### 3. Run the "start" script with game titles
Example:
```sh
poetry run start "Inside" "home" "Doom" "mario 64"
```
Output of this example:
```sh
Title           Main Story    Main + Extra    Completionist
--------------  ------------  --------------  ---------------
Inside          3½            4               4½
Home (2012)     1             1½              3
Doom (2016)     11½           16½             27
Super Mario 64  12            17              20
```
Also it create a `.csv` file in the project folder `./out/`.
