from .CaseStudy import CaseStudy
from .Constants import Constants
from tqdm.auto import tqdm


class RoodGroen(CaseStudy):
    def filter(self, order: str):
        """Apply the filtering operation for the RoodGroen case study

        Args:
            order (str): either "red" or "green"
        """

        if order not in ["red", "green"]:
            raise Exception(
                "Unrecognised order. Specify either 'red' or 'green' as the requested order.")

        # The general xpath is the xpath that will decide whether a sentence adheres to the syntax we want
        # In this case, we want to find subordinate clauses with a perfective verb cluster (red or green depends on the setting)
        general_xpath = Constants.GENERAL_XPATHS[order]

        # Secondary processing will be applied to the element containing a matched sentence
        # In this case, we want to get the auxiliary and participle from that node
        # We specify a lambda here with the correct order so the right xpaths will be used
        secondary_processing = lambda element: self.secondary_processing(element, order)

        return super().filter(general_xpath, secondary_processing=secondary_processing)

    def secondary_processing(self, element, order):
        # The following two xpaths are used to find the specific participles and auxiliaries
        # The query is the same for both orders, only the operators are different
        participle_xpath = Constants.SPECIFIC_XPATHS["participle"].replace(
            "$SIGN$", Constants.OPERATORS["participle"][order])
        auxiliary_xpath = Constants.SPECIFIC_XPATHS["auxiliary"].replace(
            "$SIGN$", Constants.OPERATORS["auxiliary"][order])

        participle = element.xpath(participle_xpath)[0].get('lemma')
        auxiliary = element.xpath(auxiliary_xpath)[0].get('lemma')

        return participle, auxiliary
