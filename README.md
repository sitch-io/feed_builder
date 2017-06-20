# Sitch feed builder
## Another stab at verifying the GSM network around us

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


## What it does

This tool runs in a Docker container and requires the following environment
variables to be passed in:

| Variable Name  | Purpose                      |
|----------------|------------------------------|
| OCID_KEY       | OpenCellID API key           |
| TWILIO_SID     | Twilio SID, for API access   |
| TWILIO_TOKEN   | Twilio token, for API access |

You should also mount your web root directory into the container's filesystem
at ```/var/production/```.  This will ensure that when the container dies, it
will leave behind your feed files to be served by your web server.  Make sure
you remove the container after it's run, or you kick the job off with --rm in
the arguments for ```docker run```.  If not, you'll quickly subscribe the disk
in your instance running the Docker engine.  This takes quite a while to run.  
See below for details.

You can run the feed builder process after checking out this repo by doing
something like the following (change `/opt/shared/feed` to some Docker-writable
output directory on your machine):

    docker build --pull -t feed_builder .
    docker run -it --rm \
       -e OCID_KEY=$OCID_KEY \
       -e TWILIO_SID=$TWILIO_SID \
       -e TWILIO_TOKEN=$TWILIO_TOKEN \
       -v /opt/shared/feed:/var/ \
       feed_builder

While the Docker image itself is a humble <64MB, the running container
can use beyond 12.5GB of disk storage and nearly 2GB of RAM as it creates the
feed files.  It seems less than ideal, but without this process the individual
download size of the intel feed would be multiple gigabytes per sensor, per
feed refresh.  This is an unfortunate but necessary evil.  The feed data will be
dropped at /opt/shared/feed/production.
