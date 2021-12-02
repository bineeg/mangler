from itertools import permutations
from optparse import OptionParser

data_list = []
output_file = ''
verbose = False


def get_order_of_attack(number):
    unorderd_list = []
    order_list = []
    variable_count = number
    if variable_count >= 1:
        index_list = list(range(1, variable_count+1))

        for i in range(1, variable_count):
            unorderd_list.append(list(permutations(index_list, i)))
        for lists_val in unorderd_list:
            for j in lists_val:
                u = list(j)
                u.sort()
                if u not in order_list:
                    order_list.append(u)
        order_list.append(index_list)
    return order_list


def file_write(data):
    try:
        with open(output_file, 'w') as writer:
            writer.write(data)
            print(bcolors.WARNING+'\nOutput file : '+output_file+bcolors.ENDC)
    except Exception as e:
        print("Exception in file write "+str(e))


def handle_data():
    global data_list

    payload_buffer = ''
    order = get_order_of_attack(len(data_list))
    print(bcolors.OKGREEN+'\nPayloads creating.....\n'+bcolors.ENDC)
    for parameter in order:
        payload = ''

        for index in parameter:
            if len(payload) > 0:
                payload += '&'+str((data_list[index-1]))

            else:
                payload += str((data_list[index-1]))
        if verbose:
            print(payload)
        if len(payload_buffer) > 0:
            payload_buffer += '\n'+payload

        else:
            payload_buffer += payload

    file_write(payload_buffer)


def parse_options():
    global data_list, output_file, verbose
    usage = "Usage: use : python mangler.py -d data [-o output_file_name]\nTool for mangle data and create payloads"

    parser = OptionParser(
        usage=usage)

    # add options
    parser.add_option('-d', '--data', dest='data', metavar="data",
                      type='string',
                      help='data in double quotes , more than one parameter',)
    parser.add_option('-o', '--output', metavar='output_file', dest='out_file',
                      type='string',
                      help='output file name',)
    parser.add_option('-v', "--verbose", action="store_true",
                      dest="verbose", default=False, help="stdout payloads")

    (options, args) = parser.parse_args()
    if (options.data == None):
        print(parser.usage)
        exit(0)
    data_list = (options.data).split('&')
    if len(data_list) <= 1:
        print(parser.usage)
        exit(0)
    output_file = options.out_file if options.out_file != None else 'payloads.txt'

    if options.verbose:
        verbose = True


class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


if __name__ == "__main__":
    print(bcolors.BOLD + bcolors.HEADER +
          '\nMangler'+bcolors.ENDC)
    parse_options()
    handle_data()
