# -*- coding: utf-8 -*-
##################################################
#
# Created by Davor Baric
# email: davorbaric1@hotmail.com
#
# Description:
#       Read BigData from .gid files and create figures
# Usage:
#      run cmd in folder -> python main.py -c channel_name -p path_to_gid_file1 path_to_gid_file2
#
##################################################

# import modules
import argparse
import matplotlib.pyplot as plt
import statistics


def get_user_input():
    """Function used to get value from user input with ArgumentParser class

    Args:
        no args

    Returns:
        user_channel (str): channel from .gid file that the user requests

        path (str/list):  path where .gid file/ files stored
    """
    print('\n')
    print("=" * 100)
    print("\t\t Created by: Davor Baric")
    print("\t\t e-mail: davorbaric1@hotmail.com")
    print("\t\t Description: Read BigData from .gid files and create figures")
    print("=" * 100)

    argPars = argparse.ArgumentParser(description="Enter arguments:")
    argPars.add_argument('-c', '--channel', type=str, help="Name of channel in .gid file")
    argPars.add_argument('-p', '--path', metavar='N', nargs='+', type=str, help="Input .gid file/files")
    args = argPars.parse_args()

    path = args.path
    user_channel = args.channel

    if path and user_channel:
        print("USER INPUT [Path] -->", path)
        print("USER INPUT [channel] --> ", user_channel)
        print("-" * 100)
        return path, user_channel
    else:
        print("-" * 100)
        print("ERROR: Use -p path_to_gid_file1 path_to_gid_file2 !!!")
        print("ERROR: Use -c cannel_name !!!")
        print("-" * 100)
        exit()


def get_index_channel_from_gid(path, user_channel):
    """Function used to get position(index) of channel from .gid file that the user requests

    Args:
        path (str):  path where .gid file stored

        user_channel(str): channel from .gid file that the user requests

    Returns:
        index_CAngle (int): index of Crank Angle

        index_mass (int): index of :flow:total_mass values
    """

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
            #  if Comments  appear on line between CHANNEL and UNIT blocks.
            if item.startswith('#'):
                continue
            else:
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

    index_mass = ''
    index_CAngle = ''
    if user_channel in channels:
        index_mass = int(channels.index(user_channel))

    else:
        print("\nERROR: %s channel not exists in .gid file" % user_channel)
        exit()

    if 'Crank_Angle' in channels:
        index_CAngle = int(channels.index('Crank_Angle'))

    else:
        print("\nERROR: Crank_Angle not exists in .gid file")
        exit()

    return index_CAngle, index_mass


def get_value_index_channel_from_gid(path, index_CAngle, index_mass):
    """Function used to get value on position(index) in END chapter

     Args:
         path (str):  path to the .gid file

        index_CAngle (int): index of Crank Angle

        index_mass (int): index of :flow:total_mass values

     Returns:
         crank_values (list): values of Crank Angle (deg)

         mass_values(list): values of :flow:total_mass (grams)
     """

    with open(path, 'r') as f:
        content = f.readlines()

    flag_end = 0
    end_items = list()
    for item in content:
        if item.startswith('END'):
            flag_end = 1
            continue
        #  if comments appear after line END
        if item.startswith('#'):
            continue
        if flag_end == 1:
            end_items.append(item.split())

    crank_values = list()
    mass_values = list()
    for first in end_items:
        crank_values.append(float(first[index_CAngle]))
        # 0. ITEM JE crank_angle - predati poziciju na kojoj se nalazi

    for second in end_items:
        mass_values.append(float(second[index_mass]) * 1000)  # *1000 kg in grams
        # 27. ITEM JE flow:total_mass - predati poziciju na kojoj se nalazi

    return crank_values, mass_values


def display_single_curve(crank_values, mass_values, ylabel_name, tittle_name):
    """Function used for create figure with matplotlib module

    Args:
        crank_values (list): all Crank Angle values from .gid file

        mass_values (list): all :flow:total_mass values from .gid file OR values for channel which user get

        ylabel_name (str): name of y axis

        tittle_name (str): tittle name of figure

    Returns:
        crank_values (list): all Crank Angle values from .gid file

        mass_values (list): all flow:total_mass values from .gid file
    """

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


def display_average_curve(crank_values, mass_list, ylabel_name):
    """Function used for create AVERAGE figure with matplotlib module

    Args:
        crank_values (list): all Crank Angle values from .gid file

        mass_list (list): AVERAGE of :flow:total_mass values from .gid files OR values for channel which user get

        ylabel_name (str): name of y axis

    Returns:
        crank_values (str/None): call Crank Angle values from .gid file

        avg_result (list):  values of :flow:total_mass

        ylabel_name (str): name of y axis
    """

    avg_result = [statistics.mean(k) for k in zip(*mass_list)]

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
    """Function used for create Summary_Average_Curve.txt file with values from AVERAGE figure

     Args:
         crank_values (list):  Crank Angle values from Average figure

         avg_result (list):  :flow:total_mass values from Average figure

         ylabel_name (str): name of y axis

     Returns:
         no return
     """

    f = open("Summary_Average_Curve.txt", "w")
    f.write('Crank Angle\t|\t' + ylabel_name + '\n')
    f.write('_' * 45 + '\n')
    for crank, avg in zip(crank_values, avg_result):
        f.write(str(crank) + '\t\t|\t' + str(avg) + '\n')
        f.write('-' * 45 + '\n')

    f.close()


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
        exit()

    crank_values, avg_result, ylabel_name = display_average_curve(crank_values, mass_list, user_channel)
    create_summary_file(crank_values, avg_result, ylabel_name)


if __name__ == '__main__':
    main()
