from __future__ import with_statement
from couchpotato.core.downloaders.base import Downloader
from couchpotato.core.logger import CPLog
import os
import traceback

log = CPLog(__name__)


class Pneumatic(Downloader):

    protocol = ['nzb']
    strm_syntax = 'plugin://plugin.program.pneumatic/?mode=strm&type=add_file&nzb=%s&nzbname=%s'
    status_support = False

    def download(self, data = None, media = None, filedata = None):
        if not media: media = {}
        if not data: data = {}

        directory = self.conf('directory')
        if not directory or not os.path.isdir(directory):
            log.error('No directory set for .strm downloads.')
        else:
            try:
                if not filedata or len(filedata) < 50:
                    log.error('No nzb available!')
                    return False

                fullPath = os.path.join(directory, self.createFileName(data, filedata, media))

                try:
                    if not os.path.isfile(fullPath):
                        log.info('Downloading %s to %s.', (data.get('protocol'), fullPath))
                        with open(fullPath, 'wb') as f:
                            f.write(filedata)

                        nzb_name = self.createNzbName(data, media)
                        strm_path = os.path.join(directory, nzb_name)

                        strm_file = open(strm_path + '.strm', 'wb')
                        strmContent = self.strm_syntax % (fullPath, nzb_name)
                        strm_file.write(strmContent)
                        strm_file.close()

                        return self.downloadReturnId('')

                    else:
                        log.info('File %s already exists.', fullPath)
                        return self.downloadReturnId('')

                except:
                    log.error('Failed to download .strm: %s', traceback.format_exc())
                    pass

            except:
                log.info('Failed to download file %s: %s', (data.get('name'), traceback.format_exc()))
                return False
        return False
