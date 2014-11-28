def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file
       system.
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="filename",
                        type=lambda x: is_valid_file(parser, x),
                        help="write report to FILE", metavar="FILE")
    parser.add_argument("-n", 
                        dest="n", default=10, type=int, 
                        help="how many lines get printed")
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    args = parser.parse_args()