# mattenklopper

Alpino corpus search, out of necessity

mattenklopper is a corpus search engine tailor-made for the case studies in my PhD research. The goal of this program is to create specialised datasets from scratch (i.e. from corpus source files). The search engine is made specifically for quering [Alpino](https://www.let.rug.nl/vannoord/alp/Alpino/)-formatted corpora. It is based on the [xml_query](https://github.com/BramVanroy/xml_query) script by Bram Vanroy.

mattenklopper does *not* aim to be able to create datasets for every single research use case. However, the interface it provides can be useful for other researchers to extend the current functionality for their own case studies.

## Installing mattenklopper

### Preparation

These instructions only have to be run once.

1. Download and install [Python](https://www.python.org/).
2. `git clone https://github.com/AntheSevenants/mattenklopper.git`,   
    or download and unzip [this archive](https://github.com/AntheSevenants/mattenklopper/archive/refs/heads/main.zip).
3. Open a terminal window. Navigate to the `mattenklopper` directory:  
    `cd mattenklopper`
4. Create a new virtual environment:  
    `python -m venv venv` or `python3 -m venv venv`
5. Activate the virtual environment:  
    `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (unix)
6. Install all dependencies:  
    `pip install -r requirements.txt`

### Running

These instructions need to be followed every time you want to use the mattenklopper program.

1. Open a terminal window. Navigate to the `mattenklopper` directory:  
    `cd mattenklopper`
2. Activate the virtual environment:  
    `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (unix)
3. You can now run any of the case study scripts detailed below.

## Future work

* Impement other case studies
* Support parallel processing