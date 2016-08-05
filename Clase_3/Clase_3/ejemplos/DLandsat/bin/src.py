#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
DLandsat main modules such as download metadata or image.
"""

from __future__ import print_function, division, unicode_literals

import xml.etree.ElementTree as ET
import sys
import math
import time
import datetime
import os
import socket
# To import urllib2 in Python 2 and 3
try:
    from urllib.parse import urlencode
    import urllib.request as urllib2
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    import urllib2
    from urllib2 import HTTPError, URLError

def connect_earthexplorer_proxy(proxy_info, usgs, quiet=False, qquiet=False):
    """Connect to Earth Explorer with proxy

    Parameters
    ----------
    proxy_info: dic
      Dictionary with four arguments (keys): 'user', 'pass', 'host' and 'port' of the proxy.
    usgs: dic
      Dictionary with two arguments (keys) 'account' and 'passwd' to loggin in the Earth Exprorer.
    quiet: bool, optional
      Only print the download progress and errors.
    qquiet: bool, optional
      Only print errors.
    """
    if not (quiet or qquiet):
        sys.stdout.write("Establishing connection to Earthexplorer with proxy: ...")
        sys.stdout.flush()

    #building an "opener" that used a proxy connection with authorization
    proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)s" \
                                          % proxy_info, "https" : \
                                          "http://%(user)s:%(pass)s@%(host)s:%(port)s" %proxy_info})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor)

    #Installation
    urllib2.install_opener(opener)

    #Connection parameters
    params = urlencode(dict(username=usgs['account'], password=usgs['passwd'])).encode("utf-8")

    #Connection timeout
    try:
        open_url = opener.open('https://ers.cr.usgs.gov/login', params)
    except socket.timeout:
        print('\n\nConection time out')
        sys.exit(-1)

    data = open_url.read()
    open_url.close()

    text_return = 'You must sign in as a registered user to download' \
                  ' data or place orders for USGS EROS products'

    data_str = str(data)
    if data_str.find(text_return) > 0:
        print("Authentification failed")
        sys.exit(-1)

    if not (quiet or qquiet):
        sys.stdout.write("\rEstablishing connection to Earthexplorer with proxy: Ready\n")
        sys.stdout.flush()

    return


def connect_earthexplorer_no_proxy(usgs, quiet=False, qquiet=False):
    '''Connection to Earth Explorer without proxy

    Parameters
    ----------
    usgs: dic
      Dictionary with two arguments (keys) 'account' and 'passwd' to loggin in the Earth Exprorer.
    quiet: bool, optional
      Only print the download progress and errors.
    qquiet: bool, optional
      Only print errors.
    '''
    if not (quiet or qquiet):
        sys.stdout.write("Establishing connection to Earthexplorer without proxy: ...")
        sys.stdout.flush()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    params = urlencode(dict(username=usgs['account'], password=usgs['passwd'])).encode("utf-8")

    #Connection timeout
    try:
        open_url = opener.open("https://ers.cr.usgs.gov/login", params)
    except socket.timeout:
        print('\n\nConection time out')
        sys.exit(-1)

    data = open_url.read()
    open_url.close()

    text_return = 'You must sign in as a registered user to' \
                  ' download data or place orders for USGS EROS products'

    #type(data)
    #>>> <class 'str'>
    data_str = str(data)
    if data_str.find(text_return) > 0:
        print("Authentification failed")
        sys.exit(-1)

    if not (quiet or qquiet):
        sys.stdout.write("\rEstablishing connection to Earthexplorer without proxy: Ready\n")
        sys.stdout.flush()

    return


def download_metadata(config_dict):
    '''Download metadata of a path and row between start_date and end_date specified in config-dict.
       Aditional, you can put specified cloud_cover.

    Parameters
    ----------
    config_dic: dict
      Dictionary with the folow structure:
        config_dic = {'path': ..., 'row': ..., 'start_date': ..., 'end_date': ...}
    quiet: bool
      If true, only print errors (not progress).

    Return
    ------
    metadata_xml: str
      Str with all metadata.
    '''
    str2replace1 = 'xmlns=\'http://upe.ldcm.usgs.gov/schema/metadata\'\nxmlns:xsi=\'http://www.w3.org/2001/XMLSchema-instance\'\nxsi:schemaLocation=\'http://upe.ldcm.usgs.gov/schema/metadata http://earthexplorer.usgs.gov/EE/metadata.xsd\''

    str2replace2 = '\n\n<returnStatus value="success">Completed Successfully</returnStatus>\n'

    if not config_dict['qq']:
        sys.stdout.write('Downloading metadata: ...')
        sys.stdout.flush()

    url = 'http://earthexplorer.usgs.gov/EE/InventoryStream/pathrow'
    values = {'start_path' : config_dict['path'],
              'end_path' : config_dict['path'],
              'start_row' : config_dict['row'],
              'end_row' : config_dict['row'],
              'sensor' : config_dict['real_name'],
              'start_date': config_dict['date_start'],
              'end_date' : config_dict['date_end']}

    if config_dict['cloudcover'] != 0:
        values['cc'] = config_dict['cloudcover']

    data = urlencode(values).encode("utf-8")
    req = urllib2.Request(url, data)

    #Connection timeout
    try:
        response = urllib2.urlopen(req)
    except socket.timeout:
        print('\n\nConection time out')
        sys.exit(-1)

    metadata_xml = response.read()

    #In python3, metadata_xml is <class='bytes'>
    #Change to utf-8
    if sys.version_info > (3,):
        metadata_xml = str(metadata_xml, encoding='utf-8')

    #Replace the string str2replace1 and str2replace2 with ''
    #to read more aesy the xml file after.

    metadata_xml = metadata_xml.replace(str2replace1, '')
    metadata_xml = metadata_xml.replace(str2replace2, '')

    if not config_dict['qq']:
        sys.stdout.write('\rDownloading metadata: Ready\n')
        sys.stdout.flush()

    return metadata_xml


def ids2download(metadata_xml):
    '''Return a list with the sceneID to download

    Parameters
    ----------
    metadata_xml : str
      Xml metadata

    Return
    ------
    scene_id : list
      List with all the sceneID to download
    '''
    root = ET.fromstring(metadata_xml)

    scene_id = []
    for scene  in root.iter('sceneID'):
        scene_id.append(scene.text)

    if not scene_id:
        print('No images were found to download')
        sys.exit(-1)

    return scene_id


def sizeof_h(num):
    '''File size in a unit such that the value is less than 1024 on that unit.
    _h is for 'in human format'.

    Parameter
    ---------
    num: int
      Size in bytes of a file.

    Return
    ------
    return: str
      Size and unit of the file.
    '''
    for b_size in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, b_size)
        num /= 1024.0

    print("The file is more big than TB")
    sys.exit(-1)


def part2targz(download_path, file_size):
    """
    Change the file name from .tar.gz.part to .tar.gz
    if the file was downloaded correctly.

    Parameters
    ----------
    download_path: str
      Path where the file was downloaded.
    file_size: str
      Size of the file to download.
      Get by urllib2.urlopen(url-file-2-download).info()['Content-Length']
    """
    download_size = os.path.getsize(download_path)

    if download_size == file_size:
        os.rename(download_path, download_path[:-5])
    else:
        print('The file %s in not downloaded correctly' %download_path)


def progress_bar(total_size, chunk_size, start_time, done, downloaded):
    """
    Download progress bar
    """
    time_steep = time.time() - start_time
    rate = chunk_size // time_steep
    porcent = math.floor((downloaded / total_size) * 100)
    done_equal = '=' * done
    need_equal = ' ' * (50 - done)
    need_time_seg = int((total_size*time_steep)/chunk_size)
    time_remaining = str(datetime.timedelta(seconds=need_time_seg))

    sys.stdout.write('\r[{1}{2}]{0:3.0f}% {3}/s {4}  '.format(porcent, done_equal, \
                                                                need_equal, sizeof_h(rate), \
                                                                time_remaining))
    sys.stdout.flush()

def download_chunks(url, file_name, file_path, qquiet=False):
    '''Download file in chunks

    Parameters
    ----------
    url: str
      Url to download file.
    file_name: str
      File name to save.
    file_path: str
      Path to save the download file.
    quiet: bool
      If true, only print errors (not progress).
    '''
    try:
        #Connection timeout
        try:
            response = urllib2.urlopen(url)
        except socket.timeout:
            print('\n\nConection time out')
            sys.exit(-1)

        #If type(url) == 'text/html' then it is not a image
        if response.info()['Content-Type'] == 'text/html':
            print("error: the file is in html format, not a image")
            lignes = response.read()
            if lignes.find('Download Not Found') > 0:
                raise TypeError
            else:
                print(lignes)
                print(sys.exit(-1))

        #Size of the file
        total_size = int(response.info()['Content-Length'].strip())
        downloaded = 0
        total_size_h = sizeof_h(total_size)

        total_path = os.path.join(file_path, file_name) + '.tar.gz.part'

        with open(total_path, 'wb') as download_file:

            if not qquiet:
                sys.stdout.write('\nDownloading {0} ({1}):\n'.format(file_name, total_size_h))
                sys.stdout.flush()

            while True:
                start = time.time()

                #Download the file in chunk
                CHUNK = 256*1024

                #Check connection time out
                try:
                    chunk = response.read(CHUNK)
                except socket.timeout:
                    print('\n\nConection time out')
                    sys.exit(-1)

                downloaded += len(chunk)
                done = int(50 * downloaded / total_size)

                if not chunk:
                    break

                download_file.write(chunk)

                if not qquiet:
                    progress_bar(total_size, CHUNK, start, done, downloaded)

            part2targz(total_path, os.path.getsize(total_path))

    except HTTPError as err:
        print("HTTP Error:", err.code, url)
        return False

    except URLError as err:
        print("URL Error:", err.reason, url)
        return False
