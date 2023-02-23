from .CaseStudy import CaseStudy
from .Constants import Constants
from lxml import etree as ET

class Participles(CaseStudy):
    def filter(self) -> list[tuple]:
        """Apply the filtering operation for participles search

        Returns:
            list[tuple]: list of tuples containing: (sentence, (participle, participle lemma), filename)
        """

        # We use the general XPATH to look for sentences with a past participle
        general_xpath = Constants.GENERAL_XPATHS["participles"]

        return super().filter(general_xpath)

    def secondary_processing(self, element : ET) -> tuple:
        """Apply secondary processing for the participles search

        Args:
            element (ET): the element containing the matched sentence

        Returns:
            tuple: a tuple containing the participle and participle lemma
        """

        # The following two xpaths are used to find the specific participles and auxiliaries
        # The query is the same for both orders, only the operators are different
        participle_xpath = Constants.SPECIFIC_XPATHS["participles"]

        participle = element.xpath(participle_xpath)[0].get('word')
        participle_lemma = element.xpath(participle_xpath)[0].get('lemma')

        return participle, participle_lemma
