from .CaseStudy import CaseStudy
from .Constants import Constants
from lxml import etree as ET

class Adjectives(CaseStudy):
    def filter(self) -> list[tuple]:
        """Apply the filtering operation for adjectives search

        Returns:
            list[tuple]: list of tuples containing: (sentence, (participle, participle lemma), filename)
        """

        # We use the general XPATH to look for sentences with an adjective
        general_xpath = Constants.GENERAL_XPATHS["adjectives"]

        return super().filter(general_xpath)

    def secondary_processing(self, element : ET) -> list[tuple]:
        """Apply secondary processing for the participles search

        Args:
            element (ET): the element containing the matched sentence

        Returns:
            tuple: a tuple containing the participle and participle lemma
        """

        # The following two xpaths are used to find the specific participles and auxiliaries
        # The query is the same for both orders, only the operators are different
        adjective_xpath = Constants.SPECIFIC_XPATHS["adjectives"]

        matches = []

        for adjective_match in element.xpath(adjective_xpath):
            adjective = adjective_match.get('word')
            adjective_lemma = adjective_match.get('lemma')

            matches.append((adjective, adjective_lemma))

        return matches
