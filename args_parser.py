import argparse


class ArgsParser:
    acc_username, acc_password, output_verbose, input_urls_file = None, None, None, None

    def __init__(self):
        arg_parser = argparse.ArgumentParser(description="Download audiobooks from scribd.")
        arg_parser.add_argument('--username', '-u', type=str, help='Account username')
        arg_parser.add_argument('--password', '-p', type=str, help='Account password')
        arg_parser.add_argument('--input', '-i', type=str, help='Specify the file that contains'
                                                                ' book/audiobooks url list',
                                default=None)
        arg_parser.add_argument('--verbose', '-v', help='Increase output verbosity',
                                action='store_true')

        args = arg_parser.parse_args()
        self.acc_username = args.username
        self.acc_password = args.password
        self.output_verbose = args.verbose
        self.input_urls_file = args.input
