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

## Red and green word order in Dutch

mattenklopper has built-in functionality which can filter red and green word order in Dutch subordinate sentences. Of course, you need an Alpino-formatted corpus. In addition, you need a "closed set" of items which will definitely appear in all your desired examples. The [flashtext](https://arxiv.org/abs/1711.00046) algorithm (thanks, [@lemontheme](https://github.com/lemontheme)) is used to quickly filter all sentences which are *definitely* not part of that set. In the case of the red and the green order, this file should include all possible auxiliaries which allow for a red and green alternation. This file is already included in the repository under [data/RoodGroen/closed_items.json](https://github.com/AntheSevenants/mattenklopper/blob/main/data/RoodGroen/closed_items.json).

To recreate my dataset, run the following command. Make sure your virtual environment is enabled!

```bash
python3 RoodGroen.py "data/RoodGroen/closed_items.json" "/path/to/alpino/corpus/" --output_path "RoodGroen.csv"
```

* The argument `--output_path` is optional. If not supplied, the output file will be `RoodGroenAnthe.csv`.
* You need to change "/path/to/alpino/corpus/" to a path pointing to your own Alpino corpus, such as [Lassy Klein](https://taalmaterialen.ivdnt.org/download/lassy-klein-corpus6/) or [Lassy Groot](https://taalmaterialen.ivdnt.org/download/tstc-lassy-groot-corpus/).


## Future work

* Impement other case studies