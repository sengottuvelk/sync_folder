import gdata.docs.data
import gdata.docs.client

import mimetypes

import logging
import logging.config

from dbutils import DBConnect

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("reportsApp")


def upload_google(file_path, settings):
    """
    uploads document to google and return the link to that document
    """

    logger.info("Google Upload Call")
    # connect to database
    db = DBConnect()

    client = gdata.docs.client.DocsClient(source='rgu_v04')
    client.api_version = "3"
    client.ssl = True
    client.ClientLogin(
        "developer.egrove@gmail.com", "Egrdev@pwd23", client.source)

    # file_path = "/home/sengottuvel/two-scoops-django-best-practices-1.5.pdf"
    logger.info("Successfully logged In")
    file_name = file_path.split('/')[-1]

    my_resource = gdata.docs.data.Resource(file_path, file_name)
    my_media = gdata.data.MediaSource()
    my_media.SetFileHandle(file_path, mimetypes.guess_type(file_path)[0])

    # uploads the file here
    logger.info("Uploading the file %s" % file_name)
    my_document = client.CreateResource(
        my_resource,
        create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI,
        media=my_media
    )

    logger.info("Uploading Done!")
    document_link = my_document.GetAlternateLink().href
    logger.info("The Google Doc link is %s" % document_link)

    # log updation
    db.update_upload_path(settings['log_id'],
                          dropbox_path=None,
                          googledocs_path=document_link
                          )

    return document_link
