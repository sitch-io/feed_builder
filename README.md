# Sitch feed v3
# Another stab at vetting the GSM network around us

Given that cell phone companies are perfectly entitled to mess with their own
internal addressing, things like LAC and CID should be expected to change.

Without a relationship with each provider, it is nearly impossible to ascertain
the legitimacy of a BTS without programmatic access to each provider's asset
management system, in one way or another.  The OpenCellID project is compiled
from observations, not from an asset system; simply that it has been observed
before is not a great criteria for ascertaining that a BTS is trustworthy.  It
may just be persistent, and bad.

This approach is a little bit different.  We start with FCC records and
licensed frequencies.  From that we derive what ARFCNs we should see, as well
as the operators (allowed HNI, or MCC-MNC) that should be operating on those
licensed ARFCNs.  While this is a little looser, it does give us a clear picture
of where cell towers are licensed to operate and the frequencies they are
allowed to transmit on.  So we do a match based on geolocation and ARFCN, then
compare the HNI to the licensee to determine whether or not a BTS is evil.

This is intended to support the SITCH sensor Mk III.
