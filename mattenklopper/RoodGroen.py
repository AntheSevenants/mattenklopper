from .CaseStudy import CaseStudy
from .Constants import Constants
from tqdm.auto import tqdm
from lxml import etree as ET

class RoodGroen(CaseStudy):
    def filter(self, order: str) -> list[tuple]:
        """Apply the filtering operation for the RoodGroen case study

        Args:
            order (str): either "red" or "green"

        Raises:
            Exception: if order other than "red" or "green" is specified

        Returns:
            list[tuple]: list of tuples containing: (sentence, (participle, auxiliary, participle lemma, auxiliary lemma), filename)
        """

        if order not in ["red", "green"]:
            raise Exception(
                "Unrecognised order. Specify either 'red' or 'green' as the requested order.")

        # The general xpath is the xpath that will decide whether a sentence adheres to the syntax we want
        # In this case, we want to find subordinate clauses with a perfective verb cluster (red or green depends on the setting)
        general_xpath = Constants.GENERAL_XPATHS[order]

        self.order = order

        return super().filter(general_xpath)

    def secondary_processing(self, element : ET) -> tuple:
        """Apply secondary processing for the RoodGroen case study

        Args:
            element (ET): the element containing the matched sentence

        Returns:
            tuple: a tuple containing the participle, auxiliary, participle lemma and auxiliary lemma
        """

        # The following two xpaths are used to find the specific participles and auxiliaries
        # The query is the same for both orders, only the operators are different
        participle_xpath = Constants.SPECIFIC_XPATHS["participle"].replace(
            "$SIGN$", Constants.OPERATORS["participle"][self.order])
        auxiliary_xpath = Constants.SPECIFIC_XPATHS["auxiliary"].replace(
            "$SIGN$", Constants.OPERATORS["auxiliary"][self.order])

        participle = element.xpath(participle_xpath)[0].get('word')
        participle_lemma = element.xpath(participle_xpath)[0].get('lemma')
        auxiliary = element.xpath(auxiliary_xpath)[0].get('word')
        auxiliary_lemma = element.xpath(auxiliary_xpath)[0].get('lemma')

        return participle, auxiliary, participle_lemma, auxiliary_lemma
