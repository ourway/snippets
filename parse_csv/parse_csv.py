import csv
import os
import sys


def main(input, output):
    user = {}
    pre_user = None
    with open(input, 'r', newline='') as raw_file, \
            open(output, 'w', newline='') as parsed_file:
        csv_raw = csv.reader(raw_file)
        csv_parsed = csv.writer(parsed_file)
        for row in csv_raw:
            if pre_user == row[0]:
                user[row[1]] = row[2]
            else:
                if pre_user is not None:
                    write_line(csv_parsed, pre_user, user)
                user = {}
                user[row[1]] = row[2]
                pre_user = row[0]
        else:
            write_line(csv_parsed, pre_user, user)


def write_line(fd, user, values):
    line = [user]
    line += ['{0}:{1}'.format(key, val) for key, val in values.items()]
    fd.writerow(line)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
