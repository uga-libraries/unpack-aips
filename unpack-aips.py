"""AIP Unpacker

This script identifies AIPs and unpacks them into folders named with the AIP IDs containing only the collections
material. It iterates through a directory, identifies tarred and zipped AIPs (tar.bz2 files), unpacks the contents
of the objects folder into a new directory with the AIP number, then deletes the bag metadata. It leaves the
compressed AIP files in the folder so that the script can be run again and the files re-extracted if needed.

Script usage: python /path/to/unpack-aips.py /path/to/aipdirectory
"""

import os
import shutil
import sys
import tarfile

aip_dir = sys.argv[1]


def find_aips(aip_dir):
    """Walks a directory tree and identifies compressed AIP files with the '.tar.bz2' extension

    Parameters
    -----------
    aip_dir : str
        The path of the directory containing AIPs to unpack

    Returns
    -----------
    aips_list : list
        The list of AIP file paths in the directory
    """
    aips_list = []
    for root, dirs, files in os.walk(aip_dir):
        for file in files:
            if str(file).endswith(".tar.bz2"):
                aip_path = os.path.join("\\\\?\\", root, file)
                aips_list.append(aip_path)

    return aips_list


def find_bags(aip_dir):
    """Walks a directory tree and identifies files packed according to the BagIt file packaging format

    BagIt standards: https://datatracker.ietf.org/doc/html/rfc8493

    Parameters
    -----------
    aip_dir : str
        The path of the directory containing AIPs to unpack

    Returns
    -----------
    bags_list : list
        The list of file paths for bagged materials
    """


    bags_list = []
    for root, dirs, files in os.walk(aip_dir):
        for dir in dirs:
            if '_bag' in str(dir):
                aip_bag = os.path.join("\\\\?\\", root, dir)
                bags_list.append(aip_bag)

    return bags_list


def extract_aip_contents(aip_path):
    """Extracts all files from a compressed AIP file with tar.bz2 extension

    Parameters
    -----------
    aip_path : str
        The file path of the compressed AIP file

    Returns
    -----------
    none
    """
    unpacked_file = tarfile.open(aip_path, 'r:bz2')
    unpacked_file.extractall()
    unpacked_file.close()


def unbag_aip(aip_bag):
    """Moves all files from the bag objects folder to a new directory with the AIP ID. Checks that source objects folder
    is empty and then deletes source bag directory.

    Parameters
    -----------
    aip_bag : str
        The file path of the AIP bag directory

    Returns
    -----------
    none
    """

    for root, dirs, files in os.walk(aip_bag):
        for dir in dirs:
            if str(dir) == 'objects':
                dir_path = os.path.join("\\\\?\\", root, dir)
                parent = os.path.dirname(dir_path)
                bag_folder = os.path.dirname(parent)
                no_bag = str(bag_folder).split('_bag')[0]
                aip_id = os.path.basename(no_bag)
                new_folder = f'{aip_dir}\\{aip_id}\\'
                if os.path.isdir(new_folder) is False:
                    os.mkdir(new_folder)
                files = os.listdir(dir_path)
                for file in files:
                    file_path = os.path.join("\\\\?\\", dir_path, file)
                    shutil.move(file_path, new_folder)
                if not os.listdir(dir_path):
                    shutil.rmtree(bag_folder)


if __name__ == "__main__":

    # Change CWD so contents are unbagged to the AIP dir
    os.chdir(aip_dir)

    dirlist = os.listdir(aip_dir)

    # Find all AIPs in the directory and extract their contents
    aips = find_aips(aip_dir)
    print(f'Finding and unpacking AIPs...')

    for aip in aips:
        aip_file = aip.split('\\')[-1]
        aip_id = aip_file.split('_bag')[0]

        # Check to see if AIP has already been unpacked - if so, skip
        if aip_id in dirlist:
            print(f' > {aip_id}: SKIPPED - This folder already exists. To unpack it again, delete the folder and '
                  f're-run the script.')
        else:
            print(f' > {aip_id}')
            extract_aip_contents(aip)

    # Unbag the extracted files
    bags = find_bags(aip_dir)
    if bags:
        print(f'Unbagging...')
    else:
        print(f'ERROR: No bags found.')
        exit()
    for bag in bags:
        unbag_aip(bag)

    print(f'Script is finished running.')

