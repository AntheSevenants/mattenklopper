from flashtext import KeywordProcessor
from pathlib import Path
from tqdm.auto import tqdm
from typing import Callable
from io import BytesIO
from lxml import etree as ET

import concurrent.futures

import os.path

class CaseStudy:
    def __init__(self, corpus_directory: str, closed_class_items: dict=None) -> None:
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
        if closed_class_items is not None:
            self.keyword_processor = KeywordProcessor()
            self.keyword_processor.add_keywords_from_dict(closed_class_items)
        else:
            self.keyword_processor = None

    def filter(self, xpath: str) -> list[tuple]:
        """Filter Alpino XML files with the given xpath string

        Args:
            xpath (str): the xpath string which matches the desired syntactic phenomena

        Raises:
            Exception: if corpus directory contains no XML files

        Returns:
            list[tuple]: list of corpus hits with the given syntactic structure
        """

        # Make xpath query relative, because we will be executing it on subnodes if low_memory_usage
        # Cf. https://stackoverflow.com/a/74798156/1150683
        xpath = f".{xpath}"

        # Rewrite Gretel XML query to be lxml compatible
        # Cf. https://stackoverflow.com/a/74797463/1150683
        xpath = xpath.replace("number(@begin)", "@begin")

        # Set the xpath that we will be using
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
                
                # Add the found results to the current results
                output = output + result

        return output

    def filter_single(self, pfin: Path) -> list[tuple]:
        """Filter a single Alpino XML file and return all hits

        Args:
            pfin (Path): a Path object pointing to the Alpino XML file to check

        Returns:
            list[tuple]: list of corpus hits in the given file with the given syntactic structure
        """

        total_hits = []

        buffer_open = False # controls whether lines can be added to the buffer
        parse_OK = False # controls whether the buffer should be parsed at all

        with pfin.open("rt") as reader:
            buf = []

            for line in reader:
                # Open the buffer for writing when sentence opening tag has been found
                if line.startswith("<alpino_ds"):
                    buffer_open = True
                # We check using flash text whether it's worth even parsing this sentence
                # We can already do this in the buffer stage so we skip parsing
                # (which is expensive)
                elif line.startswith("  <sentence"):
                    # If keyword processing is not available, always parse
                    if self.keyword_processor is None:
                        parse_OK = True
                    # Else, go for it
                    elif len(self.keyword_processor.extract_keywords(line)) > 0:
                        parse_OK = True
                # Close the buffer when closing tag is found
                # In addition, parse the current buffer and get its hits (if allowed)
                elif line.startswith("</alpino_ds"):
                    buf.append(line)

                    # Only parse if anything interesting was found using flashtext
                    if parse_OK:
                        total_hits = total_hits + self.filter_xml_buffer("\n".join(buf), pfin.stem)

                    # Reset flags
                    buffer_open = False
                    parse_OK = False
                    
                    # Reset buffer
                    buf = []

                # Only add lines if the buffer is open
                if buffer_open:
                    buf.append(line)

        return total_hits

    def filter_xml_buffer(self, xml: str, filename:str)-> list[tuple]:
        """Filter a single Alpino sentence buffer and return the specified information

        Args:
            xml (str): a string containing a single Alpino sentence (i.e. one <alpino_ds> element)
            filename (str): the filename of the file the Alpino sentence came from

        Returns:
            list[tuple]: list of corpus hits in the given file with the given syntactic structure
        """
        total_hits = []

        # Parse the XML from string
        alpino_ds = ET.fromstring(xml)
        
        # Extract the full sentence from the tree
        sentence_element = alpino_ds.find('sentence')
        sentence = sentence_element.text
        sentence_id = None

        # Don't worry, this is a surprise
        words = sentence.split(" ")

        if "sentid" in sentence_element.attrib:
            sentence_id = sentence_element.get("sentid")

        # Let's find different subordinate clauses
        for element in alpino_ds.xpath(self.xpath):
            # If the xpath matches, it means that the syntactic structure is the one we're looking for
            
            # DEBUG print the words of this node
            # print(" ".join(words[int(element.get("begin")) : int(element.get("end"))]))

            if self.secondary_processing is not None:
                # Secondary processing is set by children of the CaseStudy type
                # This method will run processing to find lexical elements in the syntactic structure
                secondary_data = self.secondary_processing(element)
                # print(secondary_data)

                if secondary_data is None:
                    with open("errors.txt", "at") as writer:
                        writer.write(f"{filename},{sentence_id}\n")
                    continue

                if type(secondary_data) == tuple:
                    # With the lexical elements obtained, add them to our list of hits
                    total_hits.append((sentence, filename, sentence_id, secondary_data))
                elif type(secondary_data) == list:
                    for secondary_data_tuple in secondary_data:
                        total_hits.append((sentence, filename, sentence_id, secondary_data_tuple))

            # Performance/memory improvement
            element.clear()

        return total_hits
