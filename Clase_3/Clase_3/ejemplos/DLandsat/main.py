#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Landsat-Download
================

Parameters
----------
option: str
  Choices between scene, liste or catalog
liste: str
  List filename
scene: str
  WRS2 coordinates of scene. Example, if the path is 198 and the row is 030, scene = 198030
start_date: str
  Start date in format yyyymmdd
end_date: str, optional
  End date in format yyyymmdd. If not given, it is taken as the current date.
cloudcover: int, optional
  Set a limit to the cloud cover of the image where 1 is 10%,
    2 is 20% ... 9 is 90%. The default option no set limit.
conf:
  USGS earthexplorer account and password file.
  Optional, you can put the proxy usser, pass, host and port.
unzip: bool, optional
  Unzip downloaded tgz file. Default = False
sat:
  Which satellite are you looking for. You can choise between ['LT4_5_MSS', 'LT4_5_TM', 'LE7_SLC_OFF', 'LE7_SLC_ON', 'LC8'].
output:
  Path to where download files.
updatecatalogfiles:
  Update catalog metadata files
q: bool, optional
  Only print the download progress and errors.
qq: bool, optional
  Only print errors.
"""
from __future__ import print_function, division
import os
import socket

import bin.src as src
import bin.utilitis as utilitis

def main():
    args = utilitis.args_options()
    config_dict = vars(args)

    #Create the output directory
    output_path = config_dict['output']
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    #Path, row, start and end date from the initial configuration
    config_dict['path'] = args.scene[0:3]
    config_dict['row'] = args.scene[3:6]

    #Start and end date
    config_dict['date_start'] = args.start_date[0:4] + '-' + \
                                args.start_date[4:6] + '-' + args.start_date[6:8]

    config_dict['date_end'] = args.end_date[0:4] + '-' + \
                              args.end_date[4:6] + '-' + args.end_date[6:8]

    repert, real_name = utilitis.satellite_specs(config_dict['bird'])
    config_dict['repert'] = repert
    config_dict['real_name'] = real_name

    #Time_out in seconds
    socket.setdefaulttimeout(config_dict['timeout'])

    #Connect to Earth Explorer
    usgs_dic, proxy_dic = utilitis.read4file(config_dict['config'])
    if len(proxy_dic) == 4:
        src.connect_earthexplorer_proxy(proxy_dic, usgs_dic)
    else:
        src.connect_earthexplorer_no_proxy(usgs_dic)

    metadata_xml = src.download_metadata(config_dict)

    scene_id = src.ids2download(metadata_xml)

    print("Number of images to download: %d" %len(scene_id))

    for scene in scene_id:
        url = "http://earthexplorer.usgs.gov/download/%s/%s/STANDARD/EE" \
              %(config_dict['repert'], scene)
        src.download_chunks(url, scene, output_path)

        if config_dict['unzip']:
            utilitis.un_tar(output_path, scene)


if __name__ == "__main__":
    main()
