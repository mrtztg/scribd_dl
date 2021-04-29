import argparse


class ArgsParser:
    acc_username, acc_password, output_verbose, __input_urls_file = None, None, None, None

    def __init__(self):
        arg_parser = argparse.ArgumentParser(description="Download audiobooks from scribd.")
        arg_parser.add_argument('-u', '--username', type=str, help='Account email/username')
        arg_parser.add_argument('-p', '--password', type=str, help='Account password')
        arg_parser.add_argument('-i', '--input', type=str, help='Specify the file that contains'
                                                                ' book/audiobooks url list', )
        arg_parser.add_argument('-v', '--verbose', help='Increase output verbosity',
                                action='store_true')

        args = arg_parser.parse_args()
        self.acc_username = args.username
        self.acc_password = args.password
        self.output_verbose = args.verbose
        self.__input_urls_file = args.input

    def get_books_url(self):
        with open(self.__input_urls_file) as input_file:
            return input_file.read().splitlines()
