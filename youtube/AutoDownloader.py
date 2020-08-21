import subprocess
import ssl
import pytube


def paste():
    p = subprocess.Popen(['pbpaste', 'r'], stdout=subprocess.PIPE, close_fds=True)
    return p.communicate()[0].decode('utf-8')


class NotYoutubeURLError(Exception):
    pass


class YoutubeURL(object):
    def __init__(self, _val: str):
        if _val.startswith('https://www.youtube.com/watch') is False:
            raise NotYoutubeURLError
        else:
            self.val = _val


def download_mp4_from_youtube(_url: YoutubeURL):
    ssl._create_default_https_context = ssl._create_unverified_context
    yt = pytube.YouTube(_url.val)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()


def main():
    try:
        clipboard = paste()
        youtube_url = YoutubeURL(clipboard)
        download_mp4_from_youtube(youtube_url)

    except NotYoutubeURLError:
        pass


if __name__ == '__main__':
    main()
