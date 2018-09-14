import os
import glob

import appdirs


class EidlStorage():
    def __init__(self):
        self.eidl_dir = appdirs.user_data_dir(
            appname='EcoInventDownLoader',
            appauthor='EcoInventDownLoader'
        )

        if not os.path.isdir(self.eidl_dir):
            os.makedirs(self.eidl_dir)

    @property
    def stored_dbs(self):
        paths = glob.glob(os.path.join(self.eidl_dir, '*.7z'))
        db_dict = {os.path.split(p)[1]: p for p in paths}
        return db_dict

    def clear_stored_dbs(self):
        for db in self.stored_dbs.values():
            os.remove(db)


eidlstorage = EidlStorage()
