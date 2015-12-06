from backend import blockhain_info as bi

class LinkabilityTest:
    def __init__(self):
        self.name = "LinkabilityTest"
        self.verbose = False

    def test(self, addr1, addr2, blocks):
        """
        """

        print("LinkabilityTest: test()")

        return -1

class TotalAmountSentTest(LinkabilityTest):
    """This compares the total amount sent and received between two addresses.
    If two addresses have similar amounts sent and received, we consider those
    addresses as being linked.
    """

    def test(self, addr1, addr2, blocks):
        """We assume addr1 sends BTC to addr2. We return a value which is 1 if
        the amount sent is equal to the amount received. As these amounts become
        more different, the value we return approaches 0.

        The range of values we return is 0 -> 1, inclusive.
        """

        addr1_total_sent = bi.get_addr(addr1)["total_sent"]
        addr2_total_received = bi.get_addr(addr2)["total_received"]

        return 1 - abs(addr1_total_sent - addr2_total_received) / \
            max(addr1_total_sent, addr2_total_received)

class IndividualAmountSentTest(LinkabilityTest):
    """This compares the transactions from two addresses. 
    """

    def test(self, addr1, addr2, blocks):
        """
        """

        print("IndividualAmountSentTest: test()")

class DirectLinkExistsTest(LinkabilityTest):
    """
    """

    def test(self, addr1, addr2, blocks):
        """
        """

        print("DirectLinkTest: test()")

class TransactionFrequencyTest(LinkabilityTest):
    """
    """
    


