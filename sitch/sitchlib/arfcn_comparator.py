"""ARFCN comparison logic."""
from . import arfcn_ref


class ArfcnComparator:
    """Initialization requires no arguments.

    There are two attributes you want to pay attention to
    uplink_to_arfcn and downlink_to_arfcn, which are generated on
    instantiation.  You'll use these as the reference input for the
    class method get_arfcn_list_by_range.  We are currently only building for
    GSM850 and PCS1900.  To add bands, improve on reference_list components
    below.

    """

    def __init__(self):  # NOQA
        self.reference_list = arfcn_ref.GSM_850 + arfcn_ref.PCS_1900
        self.uplink_to_arfcn = self.get_up_to_arfcn()
        self.downlink_to_arfcn = self.get_down_to_arfcn()

    def get_up_to_arfcn(self):
        """Return uplink frequency for ARFCN reference."""
        uplink_to_arfcn = {}
        for arfcn in self.reference_list:
            uplink_to_arfcn[arfcn["uplink"]] = arfcn["arfcn"]
        return uplink_to_arfcn

    def get_down_to_arfcn(self):
        """Return downlink to ARFCN reference."""
        downlink_to_arfcn = {}
        for arfcn in self.reference_list:
            downlink_to_arfcn[arfcn["downlink"]] = arfcn["arfcn"]
        return downlink_to_arfcn

    def arfcn_from_uplink_range(self, start, end):
        """Unlikely to ever be used."""
        reference = self.uplink_to_arfcn
        arfcn_list = ArfcnComparator.get_arfcn_list_by_range(reference,
                                                             start, end)
        return sorted(arfcn_list)

    def arfcn_from_downlink_range(self, start, end):
        """Use this for getting ARFCN list by tower TX."""
        reference = self.downlink_to_arfcn
        arfcn_list = ArfcnComparator.get_arfcn_list_by_range(reference,
                                                             start, end)
        return sorted(arfcn_list)

    @classmethod
    def get_arfcn_list_by_range(cls, reference, start, end):
        """Return list of ARFCNs for a frequency range.

        The reference var should look like this:
        {frequency: arfcn, frequency: arfcn}
        """
        arfcn_list = []
        try:
            starting = float(start)
            ending = float(end)
        except ValueError:
            msg = "Unable to set float from %s and %s" % (str(start), str(end))
            print(msg)
            starting = float(0)
            ending = float(1)
        for freq in reference.items():
            target = float(freq[0])
            if starting < target < ending:
                arfcn_list.append(freq[1])
        return arfcn_list
