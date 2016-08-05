#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
DLandsat utilitis modules like parse_arg and read4file
"""

from __future__ import print_function, division, unicode_literals

import tarfile
import sys
import os
import datetime
import argparse

def satellite_specs(sat):
    """
    Some specs of the satellite like the right name to download the metadata, rep, etc.
    """
    if sat == 'LC8':
        repert = '4923'
        real_name = 'LANDSAT_8'
    elif sat == 'LE7_SLC_OFF':
        repert = '3373'
        real_name = 'LANDSAT_ETM_SLC_OFF'
    elif sat == 'LE7_SLC_ON':
        repert = '3372'
        real_name = 'LANDSAT_ETM'
    elif sat == 'LT4_5_TM':
        repert = '3119'
        real_name = 'LANDSAT_TM'
    elif sat == 'LT4_5_MSS':
        repert = '3119'
        real_name = 'LANDSAT_MSS2'

    return repert, real_name


def read4file(file_path):
    """
    Read the initial parameter for a file.
    The file can have multiple lines of comments, always, starting with "" "and end with" "".

    Parameters
    ----------
    file_path : str
        Path to the file

    Returns
    -------
    usgs_param: dict
      Dictionary with 'user' and 'passwd' to connect with Eart Explorer.
    proxy_param: dict
      If given the proxy configurations in the file, return a dictionary with
      'usser' (proxy_user), 'pass' (proxy_pass), 'host' and 'port'.
      Else, return an empy dictionary.
    """
    config_file = open(file_path, 'r')

    usgs_param = {}
    proxy_param = {}

    while True:
        line_file = config_file.readline()

        #salteo todo los comentarios que usan """
        if '"""' in line_file:
            while True:
                line_file = config_file.readline()
                if '"""' in line_file:
                    line_file = config_file.readline()
                    break

        #salteo todo los comentarios que usan '''
        elif "'''" in line_file:
            while True:
                line_file = config_file.readline()
                if "'''" in line_file:
                    line_file = config_file.readline()
                    break

        if line_file == '\n':
            line_file = config_file.readline()

        if line_file == '':
            break

        #Remove all spaces
        line_file = ''.join(line_file.split())

        #Split the text and the value
        text, val = line_file.split('=')

        #variables
        if text == 'account':
            usgs_param['account'] = val
        elif text == 'password':
            usgs_param['passwd'] = val
        elif text == 'proxy_user':
            proxy_param['user'] = val
        elif text == 'proxy_pass':
            proxy_param['pass'] = val
        elif text == 'proxy_host':
            proxy_param['host'] = val
        elif text == 'proxy_port':
            proxy_param['port'] = val
        else:
            print('No es nada de esto')

    config_file.close()

    if not 'account' in usgs_param:
        print('You forget the account')
        return sys.exit(-3)

    if not 'passwd' in usgs_param:
        print('You forget the password')
        return sys.exit(-3)

    if len(proxy_param) > 1 and len(proxy_param) != 6:
        print('Missing any of the following parameters: proxy_user,' \
              ' proxy_pass, proxy_host and/or proxy_port')
        return sys.exit(-3)

    return usgs_param, proxy_param


def args_options():
    """
    Parce arguments from CLI.
    """
    parser = argparse.ArgumentParser(description='Download Landsat Images')

    parser.add_argument("-o", "--option", choices=['scene', 'liste', 'catalog'],
                        help="scene or liste", default='scene')

    parser.add_argument("-l", "--liste",
                        help="list filename", default=None)

    parser.add_argument("-s", "--scene",
                        help="WRS2 coordinates of scene (ex 198030)", default=None)

    parser.add_argument("-d", "--start_date",
                        help="start date, yyyymmdd")

    parser.add_argument("-f", "--end_date",
                        help="end date, yyyymmdd",
                        default=datetime.datetime.now().strftime("%Y%m%d"))

    parser.add_argument("-c", "--cloudcover", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9], type=int,
                        help="Set a limit to the cloud cover of the image where 1 is 10 percent," \
                        " 2 is 20 percent ... 9 is 90 percent. The default option no set limit.",
                        default=0)

    parser.add_argument("--config",
                        help="USGS earthexplorer account and password file. Optional," \
                        " you can put the proxy usser, pass, host and port",
                        default='user.config')

    parser.add_argument("-z", "--unzip", action='store_true',
                        help="Unzip downloaded .tar.gz file")

    parser.add_argument("-b", "--sat", dest="bird",
                        choices=['LT4_5_MSS', 'LT4_5_TM', 'LE7_SLC_OFF', 'LE7_SLC_ON', 'LC8'],
                        help="Which satellite are you looking for", default='LC7_SLC_OFF')

    parser.add_argument("--output",
                        help="Where to download files", default='/tmp/LANDSAT')

    parser.add_argument("-t", "--timeout", type=int,
                        help="Set the conection time out in seconds. Default = 60 seg.", default=60)

    parser.add_argument("-q", action='store_true',
                        help="Only print the download progress and errors.")

    parser.add_argument("-qq", action='store_true',
                        help="Only print errors.")

    args = parser.parse_args()

    #Check all necessary inputs
    if args.option == 'scene':
        if not args.start_date:
            parser.error('In scene, start date is requiered')
        if not args.scene:
            parser.error('In scene, scene is requiered')
    elif args.option == 'liste':
        if not args.liste:
            parser.error('In liste, liste is requiered')

    return args


def un_tar(download_path, file_name, quiet=False):
    """
    Untar a file using tools from the standar library.

    Parameters
    ----------
    download_path: str
      Path where the file was downloaded.
    file_name: str
      File name.
    quiet: bool, optinal
      If True, no progress will be indicated.
    """
    #If not exist, created the directory where the images will extract
    directory = os.path.join(download_path, file_name)
    full_path = directory + '.tar.gz'
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not quiet:
        sys.stdout.write('Decompressing files: ...')
        sys.stdout.flush()

    tfile = tarfile.open(full_path, 'r:gz')
    tfile.extractall(directory)
    tfile.close()

    if not quiet:
        sys.stdout.write('\rDecompressing files: Ready\n')
        sys.stdout.flush()
