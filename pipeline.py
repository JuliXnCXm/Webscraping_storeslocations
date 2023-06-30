from fileinput import filename
import logging
logging.basicConfig(level=logging.INFO)
import subprocess

logger = logging.getLogger(__name__)
delivery_sites_uid = ['']

def main():
    for i in range(20):
        _init()
    _extract()
    _transform()

def _init():
    logger.info('Starting setup process')
    subprocess.run(['python3', 'extract.py'], cwd='./extract')
    logger.info('Process finished')

def _extract():
    for i in range(38):
        try:
            logger.info('Starting extract process')
            subprocess.run(
                ['python3', 'main.py', '{}'.format(delivery_sites_uid[0]), str(i)], cwd='./extract')
            subprocess.run(['find', '.', '-name', '{}*'.format(delivery_sites_uid[0]), '-exec' , 'mv' , '{}' , '../raw/{}_{}_.csv'.format(delivery_sites_uid[0],i), ';'], cwd='./extract')
        except print(i):
            print("error with data")

def _transform():
    for i in range(38):
        try:
            logger.info('Starting transform process')
            dirty_data_filename = '{}_{}_.csv'.format(delivery_sites_uid[0], i)
            clean_data = '{}_{}_clean'.format(delivery_sites_uid[0],i)
            subprocess.run(['python3', 'main.py', '../raw/{}'.format(dirty_data_filename)], cwd='./transform')
            subprocess.run(['mv', '../raw/{}.csv'.format(clean_data) , '../transform/{}{}.csv'.format(delivery_sites_uid[0],i)], cwd='./transform')
            subprocess.run(['rm', '../raw/{}'.format(dirty_data_filename)], cwd='./transform')
            logger.info('Process finished')
        except print(i):
            print("error with the data")


if __name__ == '__main__':
    main()
