import logging
logging.basicConfig(level=logging.INFO)
import subprocess

logger = logging.getLogger(__name__)

def main():
	logger.info('Starting extract process')
	subprocess.run(['python3.8', 'extract.py'], cwd='.')
	logger.info('Starting transform process')
	subprocess.run(['python3.8', 'process.py'], cwd='.')
	logger.info('Starting Analysis process')
	print('\n\n')
	print(' Ready ')
	print('\n\n')


if __name__=='__main__':
	
	main()
