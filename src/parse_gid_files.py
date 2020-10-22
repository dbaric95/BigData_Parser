# -*- coding: utf-8 -*-
##################################################
#
# Created by Davor Baric
# email: davorbaric1@hotmail.com
#
# Description:
#       Read gid files and create figures
# Usage:
#      run cmd in folder -> python main.py -c channel -p path_to_gid_file1 path_to_gid_file2
#
##################################################

# import modules
import argparse
import matplotlib.pyplot as plt
import statistics
import itertools


def get_user_input():
    print("-" * 50)
    print("Created by: Davor Baric")
    print("e-mail: davorbaric1@hotmail.com")
    print("-" * 50)

    argPars = argparse.ArgumentParser(description="Enter arguments:")
    argPars.add_argument('-c', '--channel', type=str, help="name of channel in gid file")
    argPars.add_argument('-p', '--path', metavar='N', nargs='+', type=str, help="Input .gid file/files")
    args = argPars.parse_args()

    path = args.path
    user_channel = args.channel

    if path and user_channel:
        print("-" * 50)
        print("Path of gid file/files -> ", path)
        print("Channel -> ", user_channel)
        print("-" * 50)
    else:
        print("-" * 50)
        print("ERROR: Use -p path_to_gid_file1 path_to_gid_file2 !!!")
        print("ERROR: Use -c cannel_name !!!")
        print("-" * 50)
        exit()

    return path, user_channel


def display_single_curve(crank_values, mass_values, ylabel_name, tittle_name):
    plt.title('Total Mass @ ' + tittle_name)
    plt.xlabel('Crank Angle (deg)')
    plt.ylabel(ylabel_name + ' (grams)')
    plt.plot(crank_values, mass_values, 'k')
    plt.legend(('Value: ' + ylabel_name, 'Total'),
               loc='upper center')
    plt.grid(True)
    plt.savefig(tittle_name + '.pdf')
    plt.close()
    return crank_values, mass_values


def display_average_curve(crank_values, avg_mass, ylabel_name):
    avg_result = [statistics.mean(k) for k in zip(*avg_mass)]

    plt.title('Average Total Mass')
    plt.xlabel('Crank Angle (deg)')
    plt.ylabel(ylabel_name + ' (grams)')
    plt.plot(crank_values, avg_result, 'k--')
    plt.legend(('Average: ' + ylabel_name, 'Total'),
               loc='upper center')
    plt.grid(True)
    plt.savefig('Average_Total.pdf')
    plt.close()
    return crank_values, avg_result, ylabel_name


def create_summary_file(crank_values, avg_result, ylabel_name):
    f = open("Summary_Average_Curve.txt", "w")
    f.write('Crank Angle\t|\t' + ylabel_name + '\n')
    f.write('_' * 45 + '\n')
    for crank, avg in zip(crank_values, avg_result):
        f.write(str(crank) + '\t\t|\t' + str(avg) + '\n')
        f.write('-' * 45 + '\n')

    f.close()


def get_value_index_channel_from_gid(path, index_CAngle, index_mass):
    with open(path, 'r') as f:
        content = f.readlines()

    flag_end = 0
    end_items = list()
    for item in content:
        if item.startswith('END'):
            flag_end = 1
            continue
        if item.startswith('#'):
            continue
        if flag_end == 1:
            end_items.append(item.split())

    # print(len(end_items))
    crank_values = list()
    mass_values = list()
    for first in end_items:
        crank_values.append(float(first[index_CAngle]))
        # 0. ITEM JE crank_angle - predati poziciju na kojoj se nalazi

    for second in end_items:
        mass_values.append(float(second[index_mass]) * 1000)  # *1000 kg in grams
        # 27. ITEM JE flow:total_mass - predati poziciju na kojoj se nalazi

    return crank_values, mass_values


def get_index_channel_from_gid(path, user_channel):
    with open(path, 'r') as f:
        content = f.readlines()

    channels_key = 'CHANNELNAME'
    flag_channel = 0
    all_content_channels = list()
    for item in content:
        if item.startswith(channels_key):
            flag_channel = 1
        if item.startswith('UNIT'):
            flag_channel = 0
            break
        if flag_channel == 1:
            all_content_channels.append(item)

    temp_channels = list()
    word = ''
    for value_chn in all_content_channels:
        for item in value_chn:
            if '=' in item or '&' in item or '[' in item or '\n' in item or ']' in item:
                word += ''
            else:
                word += item

    temp_channels.append(word.split())
    channels = list()

    for channel in temp_channels:
        for chan in channel:
            if chan == channels_key:
                pass
            else:
                channels.append(chan.replace(',', '').replace('\'', ''))

    channels[0:2] = ['_'.join(channels[0:2])]
    # print("All channels from file: ", channels)

    index_mass = ''
    index_CAngle = ''
    if user_channel in channels:
        index_mass = int(channels.index(user_channel))
        # print(index_mass)
    else:
        print("\nERROR: %s channel not exists in .gid file" % user_channel)
        exit()

    if 'Crank_Angle' in channels:
        index_CAngle = int(channels.index('Crank_Angle'))
        # print(index_CAngle)
    else:
        print("\nERROR: Crank_Angle not exists in .gid file")
        exit()
    return index_CAngle, index_mass


def main():
    path, user_channel = get_user_input()
    mass_list = list()

    if len(path) > 1:
        for p in path:
            index_CAngle, index_mass = get_index_channel_from_gid(path=p,
                                                                  user_channel=user_channel)
            crank_values, mass_values = get_value_index_channel_from_gid(path=p,
                                                                         index_CAngle=index_CAngle,
                                                                         index_mass=index_mass)
            full_path = p.split('\\')
            figure_name = full_path[-1].split('_')

            display_single_curve(crank_values=crank_values,
                                 mass_values=mass_values,
                                 ylabel_name=user_channel,
                                 tittle_name=figure_name[-2]
                                 )
            mass_list.append(mass_values)

    else:
        index_CAngle, index_mass = get_index_channel_from_gid(path=path[0])
        crank_values, mass_values = get_value_index_channel_from_gid(path=path[0],
                                                                     index_CAngle=index_CAngle,
                                                                     index_mass=index_mass
                                                                     )
        full_path = path.split('\\')
        figure_name = full_path[-1].split('_')
        display_single_curve(crank_values=crank_values,
                             mass_values=mass_values,
                             ylabel_name=user_channel,
                             tittle_name=figure_name[-2]
                             )

    crank_values, avg_result, ylabel_name = display_average_curve(crank_values, mass_list, user_channel)
    create_summary_file(crank_values, avg_result, ylabel_name)


if __name__ == '__main__':
    main()
