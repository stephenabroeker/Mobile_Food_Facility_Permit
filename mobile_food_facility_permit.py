#!/usr/bin/env python3
#
# pylint: disable=C0103
# pylint: disable=R0912
# pylint: disable=R0915
# pylint: disable=R0916


"""
Copyright (c) 2020 Stephen A. Broeker
All Rights Reserved.

:author: Stephen A. Broeker <steve_broeker@yahoo.com>

Find all Food Trucks that match a given (longitude, latitude) in a CSV file
(default = Mobile_Food_Facility_Permit.csv).
The following options is provided:

--applicant : Give details on a given Food Truck Applicant.

    This option is useful when you are interested in a given Food Truck and you
    want complete details.

--applicant_sort : Display all Food Trucks sorted by Applicant.

    This option is useful when you want to find out the location of a specific
    Food Truck.

(--latitude and --longitude) : Show all Food Trucks at a given location.

--latitude_sort : Display all Food Trucks sorted by Latitude.

    This option is useful when you want to check out the area around a specific
    location.

--longitude_sort : Display all Food Trucks sorted by Longitude.

    This option is useful when you want to check out the area around a specific
    location.

"""

import csv
import logging

from optparse import OptionParser # pylint: disable=W0402


def main():

    """
    Main function.
    """

    usage = """
%prog [options]

Find all food trucks that match a given (longitude, latitude) in a CSV.
    """.strip()

    parser = OptionParser(usage=usage)

    parser.add_option("", "--applicant",
                      dest="applicant",
                      help="Food truck applicant.")

    parser.add_option("", "--applicant_sort",
                      action="store_true", dest="applicant_sort",
                      default=False,
                      help="Show all trucks sorted by Applicant.")

    parser.add_option("", "--csv_file",
                      dest="csv_file",
                      default="Mobile_Food_Facility_Permit.csv",
                      type="string",
                      help="CSV input file " + \
                           "Mobile_Food_Facility_Permit.csv")

    parser.add_option("", "--latitude",
                      dest="latitude",
                      help="Food truck latitude.")

    parser.add_option("", "--latitude_sort",
                      action="store_true", dest="latitude_sort",
                      default=False,
                      help="Show all trucks sorted by Latitude.")

    parser.add_option("", "--longitude",
                      dest="longitude",
                      help="Food truck longitude.")

    parser.add_option("", "--longitude_sort",
                      action="store_true", dest="longitude_sort",
                      default=False,
                      help="Show all trucks sorted by Longitude.")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Display debug messages.")

    (g_opts, g_args) = parser.parse_args()

    invalid_arg_count = (len(g_args) != 0)

    if invalid_arg_count:
        raise parser.error("Invalid number of arguments.")

    if (g_opts.latitude) and (not g_opts.longitude):
        raise parser.error("--latitude option requires --longitude "
                           + "option.")

    if (g_opts.longitude) and (not g_opts.latitude):
        raise parser.error("--longitude option requires --latitude "
                           + "option.")

    if g_opts.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format=('%(filename)s: '
                                    '%(levelname)s: '
                                    '%(funcName)s(): '
                                    '%(lineno)d:\t'
                                    '%(message)s'))

    logging.debug("g_opts = %s" % (g_opts)) # pylint: disable=W1201

    logging.debug("g_args = %s" % (g_args)) # pylint: disable=W1201

    print()
    print()

    if g_opts.applicant:
        count = 0

        with open(g_opts.csv_file, 'r') as data:
            for line in csv.DictReader(data):
                if line['Applicant'] == g_opts.applicant:
                    for item in line:
                        print(str(item) + " : " + str(line[item]))
                    print()
                    count += 1

        if count == 0:
            print("No matching food trucks.")
        else:
            print(str(count) + " food trucks found.")

        print()
        print()

    if g_opts.applicant_sort:
        app_dict = {}

        with open(g_opts.csv_file, 'r') as data:
            for line in csv.DictReader(data):
                applicant = line['Applicant']
                if applicant in app_dict:
                    app_dict[applicant].append(line)
                else:
                    app_dict[applicant] = []
                    app_dict[applicant].append(line)

        for applicant in sorted(app_dict.keys()):
            print(applicant)
            for item in app_dict[applicant]:
                print("    " + str(item['Latitude']) + " " +
                      str(item['Longitude']))

        print()
        print()

    if g_opts.latitude:
        count = 0

        with open(g_opts.csv_file, 'r') as data:
            for line in csv.DictReader(data):
                if (line['Latitude'] == g_opts.latitude) and \
                   (line['Longitude'] == g_opts.longitude):
                    count += 1
                    for item in line:
                        print(str(item) + " : " + str(line[item]))
                    print()

        if count == 0:
            print("No matching food trucks.")
        else:
            print(str(count) + " food trucks found.")

        print()
        print()

    if g_opts.latitude_sort:
        lat_dict = {}

        with open(g_opts.csv_file, 'r') as data:
            for line in csv.DictReader(data):
                latitude = line['Latitude']
                if latitude in lat_dict:
                    lat_dict[latitude].append(line)
                else:
                    lat_dict[latitude] = []
                    lat_dict[latitude].append(line)

        for latitude in sorted(lat_dict.keys()):
            print(latitude)
            for item in lat_dict[latitude]:
                print("    " + str(item['Longitude']) + " " +
                      str(item['Applicant']))

        print()
        print()

    if g_opts.longitude_sort:
        long_dict = {}

        with open(g_opts.csv_file, 'r') as data:
            for line in csv.DictReader(data):
                longitude = line['Longitude']
                if line['Longitude'] in long_dict:
                    long_dict[longitude].append(line)
                else:
                    long_dict[longitude] = []
                    long_dict[longitude].append(line)

        for longitude in long_dict:
            print(longitude)
            for item in long_dict[longitude]:
                print("    " + str(item['Latitude']) + " " +
                      str(item['Applicant']))

    if (not g_opts.applicant) and \
       (not g_opts.applicant_sort) and \
       (not g_opts.latitude) and \
       (not g_opts.latitude_sort) and \
       (not g_opts.latitude_sort) and \
       (not g_opts.longitude_sort):
        raise parser.error("Must provide an option.")

if __name__ == '__main__':
    main()

# __eof__
