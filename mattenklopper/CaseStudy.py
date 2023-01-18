from flashtext import KeywordProcessor
from pathlib import Path
from tqdm.auto import tqdm
from typing import Callable

from lxml import etree as ET

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

    def filter(self, xpath: str, secondary_processing: Callable = None) -> int:
        """Filter Alpino XML files with the given xpath string

        Args:
            xpath (str): the xpath string which matches the desired syntactic phenomena
            secondary_processing (Callable): the function which should be applied to extract data when a sentence match has been found

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

        # Recursively find all Alpino XML files
        files = list(Path(self.corpus_directory).rglob("*.xml"))

        for pfin in tqdm(files, unit="file", position=0):
            # print(pfin.stem)
            with pfin.open("rb") as fhin:
                for _, element in ET.iterparse(fhin, tag="alpino_ds", events=("end", )):
                    # Extract the full sentence from the tree
                    sentence = element.find('sentence').text
                    # We check using flash text whether it's worth running xpath on this sentence
                    if len(self.keyword_processor.extract_keywords(sentence)) == 0:
                        continue

                    # If the xpath matches, it means that the syntactic structure is the one we're looking for
                    if element.xpath(xpath):
                        if secondary_processing is not None:
                            secondary_data = secondary_processing(element)
                            total_hits.append((sentence, secondary_data))

                    element.clear()

        return total_hits
