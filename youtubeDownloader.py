from pytube import YouTube
import os
import time
import subprocess
import pyperclip


def downloadYouTube(audiourl, path):
    """Saves a youtube video as a mp4 file at the path, in the highest quality availible"""
    yt = YouTube(audiourl)

    # Picks the highest quality video format from the url
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()

    # Saves the mp4
    yt.download(path)
    return yt


def getNewFiles(old, new):
    """Returns the difference between the folder contents, the difference between the 2 lists"""
    newFiles = []
    for item in new:
        if item not in old:
            newFiles.append(item)
    return newFiles

# -------------------------------------------MAIN-PROGRAM----------------------------------------------------------------


# Only runs if this module is run directly, not imported
if __name__ == '__main__':

    path = "./Downloaded"

    # If the file path doesn't excist, make it excist
    if not os.path.exists(path):
        os.makedirs(path)

    # Saves the files that are already in the Downloaded folder
    oldDirFiles = os.listdir(path)

    print('Grabbing url')
    # Gets the clipboard content to the python program
    url = pyperclip.paste()

    # If it is not a youtube link, change it to the legend hype man video url
    if 'youtube' not in url:
        print('URL invalid, url is set to the video that anyone must have seen')
        url = 'https://www.youtube.com/watch?v=xK3yuxrmCac'

    yt = downloadYouTube(url, path)

    subprocess.run(['ffmpeg', '-i',
                    os.path.join(path, yt.default_filename),
                    os.path.join(path, time.strftime(
                        "Audio-%Y-%m-%d-%H-%M-%S" + ".mp3"))
                    ])

    # Saves the files that are already in the Downloaded folder, there are more files now since downloading has been completed
    newDirFiles = os.listdir(path)
    # Looks up what is new
    newClips = getNewFiles(oldDirFiles, newDirFiles)
    if len(newClips) == 0:
        print('Youtube video was already downloaded')

    elif len(newClips) == 1:
        print('Download Finished, saved as: %s' % newClips[0])
    # Will not happen in this program, since downloadYouTube downloads one file at a time
    else:
        print('Download Finished, saved as %s' % ', '.join(newClips))
