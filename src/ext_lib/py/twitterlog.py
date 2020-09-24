import traceback
from dateutil import tz
import datetime
import sys

UTC_TZ = tz.gettz('UTC')
TWEET_TIME_FMT = "%a %b %d %H:%M:%S %z %Y"
TWEET_TIME_TZ = tz.gettz('UTC')

STOCK_TIME_FMT = "%Y-%m-%d %H:%M:%S"
STOCK_TIME_TZ = tz.gettz('Europe/Warsaw')

def open_twitterlog_fn(path, gzipped = True):
    """
    Returns a function, which when called, returns a readable file object.

    Arguments:
    - `path`: path to file
    - `gzipped`: if true, we assume the file is compressed uzing gzip
    """
    if gzipped:
        import gzip
        import codecs
        reader = codecs.getreader("utf-8")
        return lambda: reader(gzip.open(path, 'r'), errors="ignore")
    elif path == '':
        import fileinput
        return lambda: fileinput.input()
    else:
        return lambda: open(path, 'r', errors="ignore")

def twitterlog_w_kw(open_fn):
    """
    Returns a touple containing keyword for the file and generator for json values for the stream.

    Arguments:
    - `open_fn`: function that, when called, should return readable file object (see open_twitterlog_fn)
    """
    kw = kw_from_file(open_fn)
    return kw, twitterlog_gen(open_fn())

def print_err(msg):
    '''
    Standardní chybová hláška
    '''
    sys.stderr.write("ERR: ")
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")

def logToStdErr(*args):
    '''
    Standardní logovací hláška
    '''
    sys.stderr.write('LOG:')
    for i, k in enumerate(args):
        sys.stderr.write(' ')
        sys.stderr.write(str(k))
    sys.stderr.write('\n')


def kw_from_file(open_fn):
    """
    Returns a keyword for given file.

    Arguments:
    - `open_fn`: function that, when called, should return readable file object (see open_twitterlog_fn)
    """

    with open_fn() as f:
        for ln in f:
            return ln.split(':')[-1].strip()

def twitterlog_gen(file):
    """
    Returns a generator for given file

    Arguments:
    - `file`: File with the data.
    """
    return safe_gen(json_gen(skip_empty_ln(skip_first(file))))

def safe_gen(gen):
    """
    gzip is being written to, so it might explode with 'no eof' found ... this should make sure that script doesn't end on such error
    """
    try:
        for g in gen:
            yield g
    except Exception as e:
        print_err(traceback.format_exc())
        print_err(e)

def json_gen(gen):
    import json
    for g in gen:
        try:
            yield json.loads(g, encoding = "utf-8")
        except Exception as e:
            print_err("json parsing error: {},\nsource:\n{}".format(e, g))

def skip_empty_ln(gen):
    """
    Returns generator of all non-empty elements

    Arguments:
    - `gen`: Data generator.
    """
    for g in gen:
        gg = g.strip()
        if len(gg) != 0:
            yield g

def skip_first(gen):
    """
    Skips first element of the generator (usually a keyword i.e. not json) and returns generator of all other elements

    Arguments:
    - `gen`: Data generator.
    """
    for idx, g in enumerate(gen):
        if idx != 0:
            yield g

def parse_tweet_time_as_UTC(timestr):
    return parse_and_convert_time(timestr, TWEET_TIME_FMT, TWEET_TIME_TZ, UTC_TZ)

def parse_stocks_time_as_UTC(timestr):
    return parse_and_convert_time(timestr, STOCK_TIME_FMT, STOCK_TIME_TZ, UTC_TZ)


def parse_and_convert_time(timestr, fmt, tzin, tzout):
    parsed = parse_time_w_timezone(timestr, fmt, tzin)
    return convert_to_tz(parsed, tzout)

def parse_time_w_timezone(time,fmt, tz):
    parsed = datetime.datetime.strptime(time, fmt)
    return parsed.replace(tzinfo = tz)

def convert_to_tz(time, tz_out):
    if time.tzinfo != tz_out:
        return time.astimezone(tz_out)
    else:
        return time

def round_to_next_5min(time):
    """
    Returns datetime with time changed to the start of the next five-minute interval.

    Arguments:
    `time`: Datetime to be rounded.
    """
    rounded = time.replace(second = 0)
    delta = datetime.timedelta(minutes = (5 - (rounded.minute % 5)))
    added_delta = rounded + delta
    return added_delta

def round_to_next_min(time):
    """
    Returns datetime with time changed to the start of the next minute.

    Arguments:
    `time`: Datetime to be rounded.
    """
    time = time.replace(second = 0)
    time = time + datetime.timedelta(minutes = 1)
    return time

def datetime_to_int(dtime):
    """
    Convert datetime datetime structure into an int (unix timestamp). Works fine for UTC times.

    Arguments:
    `dtime`: datetime time to be converted to unix timestamp
    """
    return int((dtime - datetime.datetime(1970,1,1,tzinfo=UTC_TZ)).total_seconds())

def datetimeToNormalStr(dtime, tzinfo=UTC_TZ):
    '''
    Vrati cas ve formatu, kterz povazujeme za "normalni" (ve smyslu standardniho formatu)
    '''
    if dtime.tzinfo is None:
        dtime = dtime.replace(tzinfo=tzinfo)
    return dtime.strftime(TWEET_TIME_FMT)
