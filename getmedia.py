import os
import sys
import configparser
from gfycat.client import GfycatClient
from imgurpython import ImgurClient
from PIL import Image
import urllib.request
import requests
import re
import hashlib

import logging


# Function for opening file as string of bytes
def file_as_bytes(file):
    with file:
        return file.read()


# Function for downloading images from a URL to media folder
def save_file(img_url, file_path):
    resp = requests.get(img_url, stream=True)
    if resp.status_code == 200:
        with open(file_path, 'wb') as image_file:
            for chunk in resp:
                image_file.write(chunk)
        # Return the path of the image, which is always the same since we just overwrite images
        image_file.close()
        return file_path
    else:
        logging.error(f'File failed to download. Status code: ' +
                      str(resp.status_code))
        return


# Function for obtaining direct image URLs from popular image hosts
def get_media(img_url, IMGUR_CLIENT, IMGUR_CLIENT_SECRET):
    # Make sure config file exists
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
    except BaseException as e:
        logging.exception('Error while reading config file:')
        sys.exit()
    # Make sure media folder exists
    IMAGE_DIR = config['MediaSettings']['MediaFolder']
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        logging.info('Media folder not found, created a new one')
    # Download and save the linked image
    if any(s in img_url
           for s in ('i.redd.it',
                     'i.reddituploads.com')):  # Reddit-hosted images
        file_name = os.path.basename(urllib.parse.urlsplit(img_url).path)
        file_extension = os.path.splitext(img_url)[-1].lower()
        # Fix for issue with i.reddituploads.com links not having a file extension in the URL
        if not file_extension:
            file_extension += '.jpg'
            file_name += '.jpg'
            img_url += '.jpg'
        # Grab the GIF versions of .GIFV links
        # When Tweepy adds support for video uploads, we can use the MP4 versions instead
        if (file_extension == '.gifv'):
            file_extension = file_extension.replace('.gifv', '.gif')
            file_name = file_name.replace('.gifv', '.gif')
            img_url = img_url.replace('.gifv', '.gif')
        # Download the file
        file_path = IMAGE_DIR + '/' + file_name
        logging.info(f'Downloading file at URL ' + img_url + ' to ' +
                     file_path + ', file type identified as ' + file_extension)
        img = save_file(img_url, file_path)
        return img
    elif ('imgur.com' in img_url):  # Imgur
        try:
            client = ImgurClient(IMGUR_CLIENT, IMGUR_CLIENT_SECRET)
        except BaseException as e:
            logging.exception('Error while authenticating with Imgur:')
            return
        # Working demo of regex: https://regex101.com/r/G29uGl/2
        regex = r"(?:.*)imgur\.com(?:\/gallery\/|\/a\/|\/)(.*?)(?:\/.*|\.|$)"
        m = re.search(regex, img_url, flags=0)
        if m:
            # Get the Imgur image/gallery ID
            id = m.group(1)
            if any(s in img_url
                   for s in ('/a/', '/gallery/')):  # Gallery links
                images = client.get_album_images(id)
                # Only the first image in a gallery is used
                imgur_url = images[0].link
            else:  # Single image
                imgur_url = client.get_image(id).link
            # If the URL is a GIFV link, change it to a GIF
            file_extension = os.path.splitext(imgur_url)[-1].lower()
            if (file_extension == '.gifv'):
                file_extension = file_extension.replace('.gifv', '.gif')
                img_url = imgur_url.replace('.gifv', '.gif')
            # Download the image
            file_path = IMAGE_DIR + '/' + id + file_extension
            logging.info(f'Downloading Imgur image at URL ' + imgur_url +
                         ' to ' + file_path)
            imgur_file = save_file(imgur_url, file_path)
            # Imgur will sometimes return a single-frame thumbnail instead of a GIF, so we need to check for this
            if (file_extension == '.gif'):
                # Open the file using the Pillow library
                img = Image.open(imgur_file)
                # Get the MIME type
                mime = Image.MIME[img.format]
                if (mime == 'image/gif'):
                    # Image is indeed a GIF, so it can be posted
                    img.close()
                    return imgur_file
                else:
                    # Image is not actually a GIF, so don't post it
                    logging.error(
                        f'Imgur has not processed a GIF version of this link, so it can not be posted'
                    )
                    img.close()
                    # Delete the image
                    try:
                        os.remove(imgur_file)
                    except BaseException as e:
                        logging.exception('Error while deleting media file:')
                    return
            else:
                return imgur_file
        else:
            logging.error(
                f'Could not identify Imgur image/gallery ID in this URL:',
                img_url)
            return
    elif ('gfycat.com' in img_url):  # Gfycat
        gfycat_name = os.path.basename(urllib.parse.urlsplit(img_url).path)
        client = GfycatClient()
        gfycat_info = client.query_gfy(gfycat_name)
        # Download the 2MB version because Tweepy has a 3MB upload limit for GIFs
        gfycat_url = gfycat_info['gfyItem']['max2mbGif']
        file_path = IMAGE_DIR + '/' + gfycat_name + '.gif'
        logging.info(f'Downloading Gfycat at URL ' + gfycat_url + ' to ' +
                     file_path)
        gfycat_file = save_file(gfycat_url, file_path)
        return gfycat_file
    elif ('giphy.com' in img_url):  # Giphy
        # Working demo of regex: https://regex101.com/r/o8m1kA/2
        regex = r"https?://((?:.*)giphy\.com/media/|giphy.com/gifs/|i.giphy.com/)(.*-)?(\w+)(/|\n)"
        m = re.search(regex, img_url, flags=0)
        if m:
            # Get the Giphy ID
            id = m.group(3)
            # Download the 2MB version because Tweepy has a 3MB upload limit for GIFs
            giphy_url = 'https://media.giphy.com/media/' + id + '/giphy-downsized.gif'
            file_path = IMAGE_DIR + '/' + id + '-downsized.gif'
            logging.info(f'Downloading Giphy at URL ' + giphy_url + ' to ' +
                         file_path)
            giphy_file = save_file(giphy_url, file_path)
            # Check the hash to make sure it's not a GIF saying "This content is not available"
            # More info: https://github.com/corbindavenport/tootbot/issues/8
            hash = hashlib.md5(file_as_bytes(open(giphy_file,
                                                  'rb'))).hexdigest()
            if (hash == '59a41d58693283c72d9da8ae0561e4e5'):
                logging.error(
                    f'Giphy has not processed a downsized GIF version of this link, so it can not be posted'
                )
                return
            else:
                return giphy_file
        else:
            logging.error(f'Could not identify Giphy ID in this URL:', img_url)
            return
    else:
      return