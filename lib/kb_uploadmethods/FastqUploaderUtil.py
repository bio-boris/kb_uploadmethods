import os
from pprint import pprint
import subprocess
import shutil
import urllib2
from contextlib import closing
import ftplib
import re
import gzip
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ftp_service.ftp_serviceClient import ftp_service

def log(message):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(message)

class FastqUploaderUtil:

	def __init__(self, config):
		log('--->\nInitializing FastqUploaderUtil instance:\n config:')
		log(config)
		self.scratch = config['scratch']
		self.callback_url = config['SDK_CALLBACK_URL']
		self.token = config['KB_AUTH_TOKEN']
		self.token_user = self.token.split('client_id=')[1].split('|')[0]

	"""
	upload_fastq_file: upload single-end fastq file or paired-end fastq files to workspace as read(s)
	                   source file can be either from user's staging area or web

	params: 
	first_fastq_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
	second_fastq_file_name: reverse/right paired-end fastq file name user's staging area
	sequencing_tech: sequencing technology
	reads_file_name: output reads file name
	workspace_name: workspace name/ID that reads will be stored to
	download_type: download type for web source fastq file
	first_fastq_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
	second_fastq_file_url: reverse/right paired-end fastq file URL

	"""
	def upload_fastq_file(self, params):
		log('--->\nrunning upload_fastq_file:\nparams:\n')
		log(params)

		self.validate_upload_fastq_file_parameters(params)

		if 'second_fastq_file_name' in params:
			# process paried-end fastq files from user's staging area
			returnVal = self._upload_file_path(
							fwd_file=params.get('first_fastq_file_name'), 
							rev_file=params.get('second_fastq_file_name'),
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params.get('reads_file_name'),
							workspace_name_or_id=params.get('workspace_name')
						)
		elif 'first_fastq_file_name' in params and 'second_fastq_file_name' not in params:
			# process single-end fastq file from user's staging area
			returnVal = self._upload_file_path(
							fwd_file=params.get('first_fastq_file_name'), 
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params.get('reads_file_name'),
							workspace_name_or_id=params.get('workspace_name')
						)
		
		if 'second_fastq_file_url' in params:
			# process paried-end fastq file URLs
			returnVal = self._upload_file_url(
							download_type=params.get('download_type'),
							fwd_file_url=params.get('first_fastq_file_url'), 
							rev_file_url=params.get('second_fastq_file_url'),
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params.get('reads_file_name'),
							workspace_name_or_id=params.get('workspace_name')
						)
		elif 'first_fastq_file_url' in params and 'second_fastq_file_url' not in params:
			# process single-end fastq file URL
			returnVal = self._upload_file_url(
							download_type=params.get('download_type'),
							fwd_file_url=params.get('first_fastq_file_url'), 
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params.get('reads_file_name'),
							workspace_name_or_id=params.get('workspace_name')
						)

		return returnVal


	"""
	validate_upload_fastq_file_parameters: validates params passed to upload_fastq_file method

	"""
	def validate_upload_fastq_file_parameters(self, params):

		# check for required parameters
		for p in ['reads_file_name', 'workspace_name']:
			if p not in params:
				raise ValueError('"' + p + '" parameter is required, but missing')	

		# check for invalidate both file path and file URL parameters
		upload_file_path = False
		upload_file_URL = False

		if 'first_fastq_file_name' in params or 'second_fastq_file_name' in params:
			upload_file_path = True

		if 'first_fastq_file_url' in params or 'second_fastq_file_url' in params:
			upload_file_URL = True

		if upload_file_path and upload_file_URL:
			raise ValueError('Cannot upload Reads for both file path and file URL')	

		# check for file path parameters
		if 'second_fastq_file_name' in params:
			self._validate_upload_file_path_availability(params["second_fastq_file_name"])
		elif 'first_fastq_file_name' in params:
			self._validate_upload_file_path_availability(params["first_fastq_file_name"])
		
		# check for file URL parameters
		if 'first_fastq_file_url' in params:
			self._validate_upload_file_URL_availability(params)

	"""
	_validate_upload_file_path_availability: validates file availability in user's staging area

	"""
	def _validate_upload_file_path_availability(self, upload_file_name):
		list = ftp_service(self.callback_url).list_files() #get available file list in user's staging area
		if upload_file_name not in list:
			raise ValueError("Target file: %s is NOT available. Available files: %s" % (upload_file_name, ",".join(list)))

	"""
	_validate_upload_file_URL_availability: validates param URL format/connection 

	"""
	def _validate_upload_file_URL_availability(self, params):
		if 'download_type' not in params:
			raise ValueError("Download type parameter is required, but missing")

		# parse URL prefix
		if 'second_fastq_file_url' in params:
			first_url_prefix = params['first_fastq_file_url'][:5].lower()
			second_url_prefix = params['second_fastq_file_url'][:5].lower()
		elif 'first_fastq_file_url' in params and 'second_fastq_file_url' not in params:
			url_prefix = params['first_fastq_file_url'][:5].lower()

		# check URL prefix
		if 'second_fastq_file_url' in params:
			if params['download_type'] == 'Direct Download' and (first_url_prefix[:4] != 'http' or second_url_prefix[:4] != 'http'):
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] in ['DropBox', 'Google Drive']  and (first_url_prefix != 'https' or second_url_prefix != 'https'):
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] == 'FTP' and (first_url_prefix[:3] != 'ftp' or second_url_prefix[:3] != 'ftp'):
				raise ValueError("Download type and URL prefix do NOT match")
		elif 'first_fastq_file_url' in params and 'second_fastq_file_url' not in params:
			if params['download_type'] == 'Direct Download' and url_prefix[:4] != 'http':
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] in ['DropBox', 'Google Drive'] and url_prefix != 'https':
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] == 'FTP' and url_prefix[:3] != 'ftp':
				raise ValueError("Download type and URL prefix do NOT match")

	"""
	_get_file_path: return staging area file path

	directory pattern: /data/bulk/user_name/file_name

	"""
	def _get_file_path(self, upload_file_name):
		return '/data/bulk/%s/%s' % (self.token_user, upload_file_name)

	"""
	_upload_file_path: upload fastq file as reads from user's staging area

	params:
	fwd_file: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
	sequencing_tech: sequencing technology
	output_file_name: output reads file name
	workspace_name_or_id: workspace name/ID that reads will be stored to
	rev_file: reverse/right paired-end fastq file name user's staging area

	"""
	def _upload_file_path(self, fwd_file, sequencing_tech, output_file_name, workspace_name_or_id, rev_file=None):
		fwd_file_path = self._get_file_path(fwd_file)

		# copy single-end fastq or forward/left paired-end fastq file from starging area to local tmp folder
		dstdir = os.path.join(self.scratch, 'tmp')
		if not os.path.exists(dstdir):
			os.makedirs(dstdir)
		shutil.copy2(fwd_file_path, dstdir)
		copy_fwd_file_path = os.path.join(dstdir, fwd_file)
		log('--->\ncopied file from: %s to: %s\n' % (fwd_file_path, copy_fwd_file_path))

		upload_file_params = {
			'fwd_file': copy_fwd_file_path,
			'sequencing_tech': sequencing_tech,
			'name': output_file_name
		}

		# copy reverse/right paired-end fastq file from starging area to local tmp folder
		if rev_file:
			rev_file_path = self._get_file_path(rev_file)
			shutil.copy2(rev_file_path, dstdir)
			copy_rev_file_path = os.path.join(dstdir, rev_file)
			log('--->\ncopied file from: %s to: %s\n' % (rev_file_path, copy_rev_file_path))
			upload_file_params['rev_file'] = copy_rev_file_path

		if str(workspace_name_or_id).isdigit():
			upload_file_params['wsid'] = int(workspace_name_or_id)
		else:
			upload_file_params['wsname'] = str(workspace_name_or_id)

		log('--->\nReadsUtils upload_reads params:\n')
		log(upload_file_params)

		ru = ReadsUtils(self.callback_url)
		result = ru.upload_reads(upload_file_params)

		log('--->\nremoving folder: %s' % dstdir)
		shutil.rmtree(dstdir)

		return result

	"""
	_upload_file_url: upload fastq file as reads from web

	params:
	download_type: download type for web source fastq file
	fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
	sequencing_tech: sequencing technology
	output_file_name: output reads file name
	workspace_name_or_id: workspace name/ID that reads will be stored to
	rev_file_url: reverse/right paired-end fastq file URL

	"""
	def _upload_file_url(self, download_type, fwd_file_url, sequencing_tech, output_file_name, workspace_name_or_id, rev_file_url=None):

		# prepare local copy file path for fwd_file
		tmp_fwd_file_name = 'tmp_fwd_fastq.fq'
		dstdir = os.path.join(self.scratch, 'tmp')
		if not os.path.exists(dstdir):
			os.makedirs(dstdir)
		copy_fwd_file_path = os.path.join(dstdir, tmp_fwd_file_name)

		self._download_file(download_type, fwd_file_url, copy_fwd_file_path)

		upload_file_params = {
			'fwd_file': copy_fwd_file_path,
			'sequencing_tech': sequencing_tech,
			'name': output_file_name
		}

		if rev_file_url:
			# prepare local copy file path for rev_file
			tmp_rev_file_name = 'tmp_rev_fastq.fq'
			copy_rev_file_path = os.path.join(dstdir, tmp_rev_file_name)
			self._download_file(download_type, rev_file_url, copy_rev_file_path)
			upload_file_params['rev_file'] = copy_rev_file_path

		if str(workspace_name_or_id).isdigit():
			upload_file_params['wsid'] = int(workspace_name_or_id)
		else:
			upload_file_params['wsname'] = str(workspace_name_or_id)

		log('--->\nReadsUtils upload_reads params::\n')
		log(upload_file_params)

		ru = ReadsUtils(self.callback_url)
		result = ru.upload_reads(upload_file_params)

		log('--->\nremoving folder: %s' % dstdir)
		shutil.rmtree(dstdir)

		return result

	"""
	_download_file: download execution distributor 

	params:
	download_type: download type for web source fastq file
	file_url: file URL
	copy_file_path: output file saving path
	
	"""
	def _download_file(self, download_type, file_url, copy_file_path):
		if download_type == 'Direct Download':
			self._download_direct_download_link(file_url, copy_file_path)
		elif download_type == 'DropBox':
			self._download_dropbox_link(file_url, copy_file_path)
		elif download_type == 'FTP':
			self._download_ftp_link(file_url, copy_file_path)
		elif download_type == 'Google Drive':
			self._download_google_drive_link(file_url, copy_file_path)

	"""
	_download_direct_download_link: direct download link handler 

	params:
	file_url: direct download URL
	copy_file_path: output file saving path

	"""
	def _download_direct_download_link(self, file_url, copy_file_path):
		try: online_file = urllib2.urlopen(file_url)
		except urllib2.HTTPError as e:
			raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
		except urllib2.URLError as e:
			raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
		else:
			with closing(online_file):
				with open(copy_file_path, 'wb') as output:
					shutil.copyfileobj(online_file, output)

	"""
	_download_dropbox_link: dropbox download link handler
	                        file needs to be shared publicly 

	params:
	file_url: dropbox download link
	copy_file_path: output file saving path

	"""
	def _download_dropbox_link(self, file_url, copy_file_path):
		# translate dropbox URL for direct download
		if "?" not in file_url:
			force_download_link = file_url + '?raw=1'
		else:
			force_download_link = file_url.partition('?')[0] + '?raw=1'

		try: online_file = urllib2.urlopen(force_download_link)
		except urllib2.HTTPError as e:
			raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
		except urllib2.URLError as e:
			raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
		else:
			with closing(online_file):
				with open(copy_file_path, 'wb') as output:
					shutil.copyfileobj(online_file, output)

	"""
	_download_ftp_link: FTP download link handler
	                    URL fomat: ftp://user_name:password@ftp_link or ftp://ftp_link
	                    defualt user_name: 'anonymous'
	                    		password: 'anonymous@domain.com'

	params:
	file_url: FTP download link
	copy_file_path: output file saving path

	"""
	def _download_ftp_link(self, file_url, copy_file_path):

		# process ftp credentials 
		ftp_url_format = re.match(r'ftp://.*:.*@.*/.*', file_url)
		if ftp_url_format:
			self.ftp_user_name = re.search('ftp://(.+?):', file_url).group(1)
			self.ftp_password = file_url.rpartition('@')[0].rpartition(':')[-1]
			self.ftp_domain = re.search('ftp://.*:.*@(.+?)/', file_url).group(1)
			self.ftp_file_path = file_url.partition('ftp://')[-1].partition('/')[-1].rpartition('/')[0]
			self.ftp_file_name = re.search('ftp://.*:.*@.*/(.+$)', file_url).group(1)
		else:
			self.ftp_user_name = 'anonymous'
			self.ftp_password = 'anonymous@domain.com'
			self.ftp_domain = re.search('ftp://(.+?)/', file_url).group(1)
			self.ftp_file_path = file_url.partition('ftp://')[-1].partition('/')[-1].rpartition('/')[0]
			self.ftp_file_name = re.search('ftp://.*/(.+$)', file_url).group(1)

		self._check_ftp_connection(self.ftp_user_name, self.ftp_password, self.ftp_domain, self.ftp_file_path, self.ftp_file_name)
		
		ftp_connection = ftplib.FTP(self.ftp_domain)
		ftp_connection.login(self.ftp_user_name, self.ftp_password)
		ftp_connection.cwd(self.ftp_file_path)

		# .gz file handler 
		# TODO: create separate zip file handler for all download types 
		if self.ftp_file_name.endswith('.gz'):
			with open(copy_file_path + '.gz', 'wb') as output:
				ftp_connection.retrbinary('RETR %s' % self.ftp_file_name, output.write)
			with gzip.open(copy_file_path + '.gz', 'rb') as in_file:
				with open(copy_file_path, 'w') as f:
					f.write(in_file.read())
		else:
			with open(copy_file_path, 'wb') as output:
				ftp_connection.retrbinary('RETR %s' % self.ftp_file_name, output.write)

	"""
	_check_ftp_connection: ftp connection checker

	params:
	user_name: FTP user name
	password: FTP user password
	domain: FTP domain
	file_path: target file directory
	file_name: target file name 

	"""
	def _check_ftp_connection(self, user_name, password, domain, file_path, file_name):

		try: ftp = ftplib.FTP(domain)
		except ftplib.all_errors, error:
			raise ValueError("Cannot connect: %s" % error)
		else:
			try: ftp.login(user_name, password)
			except ftplib.all_errors, error:
				raise ValueError("Cannot login: %s" % error)
			else:
				ftp.cwd(file_path)
				if file_name in ftp.nlst():
					pass
				else:
					raise ValueError("File %s does NOT exist in FTP path: %s" % (file_name, domain + '/' + file_path))

	"""
	_download_google_drive_link: Google Drive download link handler
	                    		 file needs to be shared publicly 

	params:
	file_url: Google Drive download link
	copy_file_path: output file saving path

	"""
	def _download_google_drive_link(self, file_url, copy_file_path):
		# translate Google Drive URL for direct download
		force_download_link_prefix = 'https://drive.google.com/uc?export=download&id='
		file_id = file_url.partition('/d/')[-1].partition('/')[0]
		force_download_link = force_download_link_prefix + file_id

		try: online_file = urllib2.urlopen(force_download_link)
		except urllib2.HTTPError as e:
			raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
		except urllib2.URLError as e:
			raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
		else:
			with closing(online_file):
				with open(copy_file_path, 'wb') as output:
					shutil.copyfileobj(online_file, output)	

