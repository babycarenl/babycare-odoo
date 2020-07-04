# coding: utf-8
from openerp import api, fields, models, tools, _
from openerp.exceptions import Warning
from io import open

import base64
import os
import re
import time
try:
    import pysftp
except ImportError:
    raise ImportError(
        'This module needs pysftp to write files through SFTP. Please install pysftp on your system. (sudo pip install pysftp)')

import logging

_logger = logging.getLogger(__name__)


class SftpExport(models.Model):
    _name = 'sftp.export'
    _rec_name = 'export_type'

    export_type = fields.Selection(
        [('ups', 'UPS')], 'Export Type', required=True)
    export_extension = fields.Selection(
        [('csv', 'CSV')], 'Export Extension', required=True, default='csv')
    folder = fields.Char('Local SFTP File Directory', help='Absolute path for storing the SFTP files', required='True',
                         default='/odoo/sftp-files')

    # Columns for external server (SFTP)
    sftp_path = fields.Char(
        'Path external server',
        help='The location to the folder where the files should be written to. For example /sftpuser/files/.\nFiles will then be written to /sftpuser/files/ on your remote server.')
    sftp_host = fields.Char(
        'IP Address SFTP Server',
        help='The IP address from your remote server. For example 192.168.0.1')
    sftp_port = fields.Integer(
        'SFTP Port', help='The port on the FTP server that accepts SSH/SFTP calls.', default=22)
    sftp_user = fields.Char(
        'Username SFTP Server',
        help='The username where the SFTP connection should be made with. This is the user on the external server.')
    sftp_password = fields.Char(
        'Password User SFTP Server',
        help='The password from the user where the SFTP connection should be made with. This is the password from the user on the external server.')

    _sql_constraints = [
        ('field_unique',
         'unique(export_type)',
         'Export Type has to be unique!')
    ]

    @api.multi
    def test_sftp_connection(self, context=None):
        self.ensure_one()

        # Check if there is a success or fail and write messages
        messageTitle = ""
        messageContent = ""

        for rec in self:
            try:
                pathToWriteTo = rec.sftp_path
                ipHost = rec.sftp_host
                portHost = rec.sftp_port
                usernameLogin = rec.sftp_user
                passwordLogin = rec.sftp_password
                # Connect with external server over SFTP, so we know sure that everything works.
                srv = pysftp.Connection(
                    host=ipHost, username=usernameLogin, password=passwordLogin, port=portHost)
                srv.close()
                # We have a success.
                messageTitle = _("Connection Test Succeeded!")
                messageContent = _(
                    "Everything seems properly set up for exporting files via SFTP!")
            except Exception, e:
                messageTitle = _("Connection Test Failed!")
                if len(rec.sftp_host) < 8:
                    messageContent += _("\nYour IP address seems to be too short.\n")
                messageContent += _("Here is what we got instead:\n")
        if "Failed" in messageTitle:
            raise Warning(_(messageTitle + '\n\n' +
                            messageContent + "%s") % tools.ustr(e))
        else:
            raise Warning(_(messageTitle + '\n\n' + messageContent))

    @api.multi
    def sftp_export(self, filecontent, type):
        conf_ids = self.search([('export_type', '=', type)])
        for rec in conf_ids:

            # Create Local Backup Directory if not exists
            try:
                if not os.path.isdir(rec.folder):
                    os.makedirs(rec.folder)
            except:
                raise

            # Create name for file
            file_name = 'import%s.%s' % (type.lower(), rec.export_extension)
            file_path = os.path.join(rec.folder, file_name)
            # Decode base64 to csv output and write to file
            csv_output = base64.decodestring(filecontent)
            csv_output = csv_output.decode("utf-8")
            with open(file_path, 'w+', encoding='utf-8') as fp:
                fp.write(csv_output)

            try:
                # store all values in variables
                pathToWriteTo = rec.sftp_path
                ipHost = rec.sftp_host
                portHost = rec.sftp_port
                usernameLogin = rec.sftp_user
                passwordLogin = rec.sftp_password

                # Connect with external server over SFTP
                srv = pysftp.Connection(
                    host=ipHost, username=usernameLogin, password=passwordLogin, port=portHost)
                # Set keepalive to prevent socket closed / connection dropped error
                srv._transport.set_keepalive(30)
                # Move to the correct directory on external server.
                # If the user made a typo in his path with multiple slashes (/sftpuser//files/) it will be fixed by this regex.
                pathToWriteTo = re.sub('([/]{2,5})+', '/', pathToWriteTo)
                _logger.debug('sftp remote path: %s' % pathToWriteTo)
                try:
                    srv.chdir(pathToWriteTo)
                except IOError:
                    # Create directory and subdirs if they do not exist.
                    currentDir = ''
                    for dirElement in pathToWriteTo.split('/'):
                        currentDir += dirElement + '/'
                        try:
                            srv.chdir(currentDir)
                        except:
                            _logger.info(
                                '(Part of the) path didn\'t exist. Creating it now at ' + currentDir)
                            # Make directory and then navigate into it
                            srv.mkdir(currentDir, mode=777)
                            srv.chdir(currentDir)
                            pass
                srv.put(file_path)

                # Close the SFTP session.
                srv.close()

            except Exception, e:
                _logger.debug(
                    'Exception! We couldn\'t transfer to the SFTP server..')
