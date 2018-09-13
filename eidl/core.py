import os
import string
import tempfile
import getpass
import subprocess

import requests
import bs4
import brightway2 as bw


class EcoinventDownloader:
    def __init__(self, username=None, password=None, version=None,
                 system_model=None, outdir=None, **kwargs):
        self.username = username
        self.password = password
        self.version = version
        self.system_model = system_model
        self.outdir = outdir

    def run_interactive(self):
        if self.username is None or self.password is None:
            self.username, self.password = self.get_credentials()
        print('logging in to ecoinvent homepage...')
        self.login()
        self.db_dict = self.get_available_files()
        print('login successful!')
        if (self.version, self.system_model) not in self.db_dict.keys():
            self.version, self.system_model = self.choose_db()
        print('downloading {} {} ...'.format(self.system_model, self.version))
        self.download()
        self.file_name = '{}{}.7z'.format(
            self.system_model, self.version.replace('.', '')
        )
        if self.outdir:
            self.out_path = os.path.join(self.outdir, self.file_name)
        else:
            self.out_path = os.path.join(os.path.abspath('.'), self.file_name)

        with open(self.out_path, 'wb') as out_file:
            out_file.write(self.file_content)
        print('download finished!: {}\n'.format(self.out_path))

    def get_credentials(self):
        un = input('ecoinvent username: ')
        pw = getpass.getpass('ecoinvent password: ')
        return un, pw

    def login(self):
        self.session = requests.Session()
        logon_url = 'https://v33.ecoquery.ecoinvent.org/Account/LogOn'
        post_data = {'UserName': self.username,
                     'Password': self.password,
                     'IsEncrypted': 'false',
                     'ReturnUrl': '/'}
        self.session.post(logon_url, post_data, timeout=20)
        if not len(self.session.cookies):
            print('Login failed')
            self.username, self.password = self.get_credentials()
            self.login()

    def get_available_files(self):
        files_url = 'https://v33.ecoquery.ecoinvent.org/File/Files'
        files_res = self.session.get(files_url)
        soup = bs4.BeautifulSoup(files_res.text, 'html.parser')
        file_list = [l for l in soup.find_all('a', href=True) if
                     l['href'].startswith('/File/File?')]
        link_dict = {f.contents[0]: f['href'] for f in file_list}
        db_dict = {
            tuple(k.replace('ecoinvent ', '').split('_')[:2:]): v for k, v in
            link_dict.items() if k.endswith('.7z') and 'lc' not in k.lower()}
        return db_dict

    def choose_db(self):
        versions = {k[0] for k in self.db_dict.keys()}
        version_dict = dict(zip(string.ascii_lowercase,
                                sorted(versions, reverse=True)))
        print('\n', 'available versions:')
        for k, version in version_dict.items():
            print(k, version)
        while True:
            version = input('version: ')
            if version in versions or version in version_dict.keys():
                break
            else:
                print('Enter version number or letter')
        system_models = {k[1] for k in self.db_dict.keys()}
        sm_dict = dict(zip(string.ascii_lowercase, sorted(system_models)))
        print('\n', 'system models:')
        for k, sm in sm_dict.items():
            print(k, sm)
        while True:
            sm = input('system model: ')
            if sm in system_models or sm in sm_dict.keys():
                break
            else:
                print('Enter system model or letter')
        dbkey = (version_dict.get(version, version),
                 sm_dict.get(sm, sm))
        return dbkey

    def download(self):
        url = 'https://v33.ecoquery.ecoinvent.org'
        db_key = (self.version, self.system_model)
        self.file_content = self.session.get(
            url + self.db_dict[db_key]).content


def get_ecoinvent(db_name=None, auto_write=False, download_path=None, *args, **kwargs):

    """
    Download and import ecoinvent to current brightway2 project
    Optional kwargs:
        db_name: name to give imported database (string) default is downloaded filename
        auto_write: automatically write database if no unlinked processes (boolean) default is False (i.e. prompt yes or no)
        download_path: path to download .7z file to (string) default is download to temporary directory (.7z file is deleted after import)
    """
    with tempfile.TemporaryDirectory() as td:
        if download_path is None:
            download_path = td

        downloader = EcoinventDownloader(*args, outdir=download_path, **kwargs)
        downloader.run_interactive()

        extract = '7za x {} -o{}'.format(downloader.out_path, td)
        subprocess.call(extract.split())
        if not db_name:
            db_name = downloader.file_name.replace('.7z', '')
        datasets_path = os.path.join(td, 'datasets')
        importer = bw.SingleOutputEcospold2Importer(datasets_path, db_name)

    if 'biosphere3' not in bw.databases:
        if auto_write:
            bw.bw2setup()
        else:
            print('No biosphere database present in your current ' +
                  'project: {}'.format(bw.projects.current))
            print('You can run "bw2setup()" if this is a new project. Run it now?')
            if input('[y]/n ') in {'y', ''}:
                bw.bw2setup()
            else:
                return

    importer.apply_strategies()
    datasets, exchanges, unlinked = importer.statistics()

    if auto_write and not unlinked:
        print('\nWriting database {} in project {}'.format(
            db_name, bw.projects.current))
        importer.write_database()
    else:
        print('\nWrite database {} in project {}?'.format(
            db_name, bw.projects.current))
        if input('[y]/n ') in {'y', ''}:
            importer.write_database()


def get_ecoinvent_cli():
    downloader = EcoinventDownloader()
    downloader.run_interactive()
