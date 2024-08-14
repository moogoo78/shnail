import argparse
from pathlib import Path
import shutil
from datetime import datetime
import logging

__version__ = '0.0.1'


class Shnail(object):
    '''Suhian's image utils'''

    AVAILABLE_IMAGE = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
    AVAILABLE_MOVIE = ['.mov', '.mp4', '.m4v']

    args = None
    logger = None
    stats = {
        'counter': {
            'not-media': 0,
            'media-image': 0,
            'media-movie': 0,
        },
        'process': {
            'action': '',
            'media-image': 0,
            'media-movie': 0,
            'last_date': None,
        },
    }

    def __init__(self, args):
        self.args = args
        self.set_logger(args.verbose)
        self._print(f'action: {args.action}')

    def set_logger(self, verbose_level):
        logger = logging.getLogger('shnail')
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        # level_map = {
        #     'critical': logging.CRITICAL,
        #     'error': logging.ERROR,
        #     'warning': logging.WARNING,
        #     'info': logging.INFO,
        #     'debug': logging.DEBUG,
        # }
        if not verbose_level:
            console_handler.setLevel('ERROR')
        elif args.verbose == 1:
            console_handler.setLevel('WARNING')
            self._print('log level: WARNING')
        elif args.verbose == 2:
            console_handler.setLevel('INFO')
            self._print('log level: INFO')
        elif args.verbose >= 3:
            console_handler.setLevel('DEBUG')
            self._print('log level: DEBUG')

        formatter = logging.Formatter('[%(levelname)s] %(asctime)s | %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger

    def _print(self, s):
        print(f'shnail @ {s}')

    def process_media(self, file_path, mtime):
        media = self.check_media(file_path)

        todo = True
        if media == 'image':
            self.stats['counter']['media-image'] += 1
        elif media == 'movie':
            self.stats['counter']['media-movie'] += 1
        else:
            self.stats['counter']['not-media'] += 1
            self.logger.debug(f'skip: {file_path}')
            todo = False

        self.stats['process']['action'] = self.args.action
        if todo:
            if self.stats['process']['last_date'] is None or \
               mtime.date() > self.stats['process']['last_date']:
                self.stats['process']['last_date'] = mtime.date()
            if self.args.action == 'copy':
                date_dir = mtime.date().strftime('%y%m%d')
                target_dir = Path(args.target_path, date_dir)
                target_path = Path(target_dir, file_path.name)
                if not self.args.dry_run and not target_dir.exists():
                    target_dir.mkdir(parents=True)
                    self.logger.info(f'create new dir: {date_dir}')

                self.stats['process'][f'media-{media}'] += 1
                if not self.args.dry_run:
                    shutil.copyfile(file_path, target_path)

            elif self.args.action == 'thumbnail':
                #is_done = make_thumb(path, name, path_out, size, x)
                pass


    def check_media(self, file_path):
        """Validate the media file"""
        # check extension only now

        if file_path.suffix.lower() in self.AVAILABLE_IMAGE:
            return 'image'
        elif file_path.suffix.lower() in self.AVAILABLE_MOVIE:
            return 'movie'

        return ''

    def run(self):
        src_path = Path(self.args.source_path)
        for root, dirs, files in src_path.walk(top_down=True):
            #print(root, dirs, files)
            for filename in files:
                file_path = Path(root, filename)

                atime = datetime.fromtimestamp(file_path.stat().st_atime)
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                ctime = datetime.fromtimestamp(file_path.stat().st_ctime)
                self.logger.debug(f'{file_path}, atime: {atime}, mtime: {mtime}, ctime: {ctime}')

                if start_date := args.start_date:
                    try:
                        sd = start_date.split('-')
                        y = f'20{sd[0]}'if len(sd[0]) == 2 else sd[0]
                        m = sd[1]
                        d = sd[2]

                        if ctime.date() >= datetime(int(y), int(m), int(d)).date():
                            self.process_media(file_path, mtime)
                    except Exception as err_msg:
                        self.logger.error(f'date format error: {err_msg}')
                else:
                    self.process_media(file_path, mtime)

        print(self.stats)
        return self.stats

def make_thumb(path, fn, tgt_dir, sz, prefix):
    size = (sz, sz)
    """Make image thumbnail"""
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
    infile = os.path.join(path, fn)
    out_filename = 'tn_{}'.format(fn) if prefix == 'y' else fn
    outfile = os.path.join(tgt_dir, out_filename)
    print('Making thumbnail: ' + infile, '=> ', outfile)
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.LANCZOS)
        im.save(outfile, "JPEG")
        return True
    except IOError:
        print('Failed: ', infile)
        return False


def main(args):
    shnail = Shnail(args)
    shnail.run()


def set_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--source_path', type=Path, default='.', help='source directory', required=True)
    parser.add_argument('-t', '--target_path', type=Path, default='./out', help='target directory')
    parser.add_argument('-z', '--size', type=int, default=650, help='resolution size ("1024" or "s:200,m:600")')
    parser.add_argument('-c', '--config', type=Path, default='.shnail', help='config file for copy')
    parser.add_argument('-a', '--action', default='copy', help='process action {copy|thumbnail}')
    parser.add_argument('-s', '--start_date', default=None, help='process start from')
    parser.add_argument('-v', '--verbose', action='count', help="verbose level. v...vvv", default=2)
    parser.add_argument('-d', '--dry_run', type=bool, action=argparse.BooleanOptionalAction, default=False, help="dry run")
    return parser.parse_args()


if __name__ == '__main__':
    args = set_argparse()
    main(args)
    #print(args)
