import argparse
import os
from filereader import FileReader
from simple_text_parser import SimpleTextParser


class ArgumentParser:

    @staticmethod
    def check_file(file):
        if not os.path.exists(file):
            raise argparse.ArgumentError("{0} does not exist".format(file))
        return file

    @staticmethod
    def setup_parser(file_type):
        parser = argparse.ArgumentParser(description='Check duplicate lines in files: ' + file_type)

        parser.add_argument('--srcdir', type=ArgumentParser.check_file, required=True,
                            help='a folder where search for ' + file_type + 's takes place')
        parser.add_argument('--destdir', required=True,
                            help='destination dir where result files will be created')

        parser.add_argument('--delete-duplicate-lines-from', nargs='*', type=ArgumentParser.check_file,
                            help="Found duplicate lines will be deleted from the provided list of files in all cases.",
                            default=None)
        return parser

    @staticmethod
    def create_args_dict(arg_parser):
        args = arg_parser.parse_args()
        print(args)

        args_dict = vars(args)
        # deletes null keys
        args_dict = dict((k, v) for k, v in args_dict.items() if v)
        print("args dict: " + str(args_dict))
        return args_dict


if __name__ == "__main__":
    arg_parser = ArgumentParser.setup_parser(SimpleTextParser.extension)
    args = ArgumentParser.create_args_dict(arg_parser)
    reader = FileReader(SimpleTextParser(), args['srcdir'], args['destdir'])
    reader.collect_and_print_lines()

    if 'delete_duplicate_lines_from' in args:
        processable_file_names = args['delete_duplicate_lines_from']
        filenames_to_line_numbers_mapping = SimpleTextParser.get_deletable_line_numbers(processable_file_names,
                                                                                        reader.parser.hashed_lines)
        reader.delete_lines_from(filenames_to_line_numbers_mapping)