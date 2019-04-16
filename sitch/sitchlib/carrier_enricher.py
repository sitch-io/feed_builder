"""Enrich carrier information."""


class CarrierEnricher:  # NOQA
    """This class gets the carrier name for MCC + MNC combination."""

    def __init__(self, mcc_mnc_carrier_list):
        """Initialize with carrier list."""
        self.reference = mcc_mnc_carrier_list

    def get_carrier(self, mcc, mnc):
        """Return carrier for MCC + MNC."""
        retval = "UNKNOWN"
        for carrier in self.reference:
            if carrier["mnc"] == mnc and carrier["mcc"] == mcc:
                retval = carrier["carrier"]
                break
        return retval
