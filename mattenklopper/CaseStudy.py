from flashtext import KeywordProcessor
from pathlib import Path
from tqdm.auto import tqdm
from typing import Callable
from io import BytesIO
from lxml import etree as ET

import concurrent.futures

import os.path


def get_tree_count(pfin: Path) -> int:
    """Count the number of "alpino_ds" nodes in a given file. We use iterparse to avoid OOM issues but that makes
     it slow!

    Args:
        pfin (Path): input file to query for alpino_ds nodes

    Returns:
        int: number of alpino_ds nodes in the given file
    """
    el_count = 0
    with pfin.open("rb") as fhin:
        for _, element in tqdm(ET.iterparse(fhin, tag="alpino_ds", events=("end", )),
                               unit="trees", leave=False, desc="Counting no. trees"):
            el_count += 1

            # Clean up to save memory
            element.clear()

    return el_count

class CaseStudy:
    def __init__(self, corpus_directory: str, closed_class_items: dict) -> None:
        """Case study object which provides an abstraction for individual case studies

        Args:
            corpus_directory (str): the directory where the Alpino-compatible corpus is stored, all XML files in here will be processed
            closed_class_items (dict): a dictionary specifying the lexical items that should definitely be part of the sentence in order for a match to occur
        """

        # Check if corpus directory exists
        if not os.path.exists(corpus_directory):
            raise FileNotFoundError(corpus_directory)

        # Save the corpus directory
        self.corpus_directory = corpus_directory

        # Keyword processor
        self.keyword_processor = KeywordProcessor()
        self.keyword_processor.add_keywords_from_dict(closed_class_items)

    def filter(self, xpath: str) -> int:
        """Filter Alpino XML files with the given xpath string

        Args:
            xpath (str): the xpath string which matches the desired syntactic phenomena

        Returns:
            int: the number of hits
        """

        total_hits = []

        # Make xpath query relative, because we will be executing it on subnodes if low_memory_usage
        # Cf. https://stackoverflow.com/a/74798156/1150683
        xpath = f".{xpath}"

        # Rewrite Gretel XML query to be lxml compatible
        # Cf. https://stackoverflow.com/a/74797463/1150683
        xpath = xpath.replace("number(@begin)", "@begin")

        self.xpath = xpath

        # Recursively find all Alpino XML files
        files = list(Path(self.corpus_directory).rglob("*.xml"))

        if len(files) == 0:
            raise Exception("Corpus directory contains no XML files")

        # Turn all files into Paths
        files = [ Path(file) for file in files]

        # Register a tqdm progress bar
        progress_bar = tqdm(total=len(files), desc='Query progress')

        # Start a processing pool
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # For each file, spawn a new process
            futures = [ executor.submit(self.filter_single, file) for file in files ]

            output = []
            # Loop over future results as they become available
            for future in concurrent.futures.as_completed(futures):
                progress_bar.update(n=1)  # Increments counter

                result = future.result()
                # The result of the filter_single method can be empty
                # We check for an empty result and only save actual results
                if len(result) == 0:
                    continue
                
                output.append(result)

        return output

    def filter_single(self, pfin):
        total_hits = []

        buffer_open = False
        parse_OK = False

        with pfin.open("rt") as reader:
            buf = []

            for line in reader:
                # Open the buffer for writing when sentence opening tag has been found
                if line.startswith("<alpino_ds"):
                    buffer_open = True
                # Close the buffer when closing tag is found
                # In addition, parse the current buffer and get its hits
                elif line.startswith("  <sentence"):
                    # We check using flash text whether it's worth even parsing this sentence
                    # We can already do this in the buffer stage so we skip parsing
                    # (which is expensive)
                    if len(self.keyword_processor.extract_keywords(line)) > 0:
                        parse_OK = True
                elif line.startswith("</alpino_ds"):
                    buf.append(line)

                    if parse_OK:
                        total_hits = total_hits + self.filter_xml_buffer("\n".join(buf), pfin.stem)

                    buffer_open = False
                    parse_OK = False
                    
                    # Reset buffer
                    buf = []

                # Only add lines if the buffer is open
                if buffer_open:
                    buf.append(line)

        return total_hits

    def filter_xml_buffer(self, xml, filename):
        total_hits = []

        # Parse the XML from string
        for _, element in ET.iterparse(BytesIO(xml.encode("UTF-8")), tag="alpino_ds", events=("end", )):
            # If the xpath matches, it means that the syntactic structure is the one we're looking for
            if element.xpath(self.xpath):
                if self.secondary_processing is not None:
                    # Extract the full sentence from the tree
                    sentence = element.find('sentence').text

                    secondary_data = self.secondary_processing(element)
                    total_hits.append((sentence, filename, secondary_data))

            element.clear()

        return total_hits
