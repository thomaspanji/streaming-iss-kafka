import argparse
from producer import run


ORBIT_MINUTE = 95
STREAM_MINUTE = 0


parser = argparse.ArgumentParser(
    description="""
    Streaming ISS position data for certain time.
    If no argument supplied, the stream will run forever.
    """
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-o',
    '--orbit',
    type=int,
    help="""
    Specify a number of orbit you want to fetch the data.
    Time to take an orbit is approximately 90-93 minutes,
    but we are rounding it to 95 minutes.
    So, argument `--orbit 2` will stream the data for 190 minutes.
    """ 
)
group.add_argument(
    '-m',
    '--minutes',
    type=int,
    help='Specify how long the stream will run in minutes.'
)

args = parser.parse_args()


if args.orbit:
    len_stream = args.orbit * ORBIT_MINUTE
elif args.minutes:
    len_stream = args.minutes + STREAM_MINUTE
else:
    len_stream = None

run(len_stream)