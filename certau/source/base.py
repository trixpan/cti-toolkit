import logging
import os
import warnings

import ramrod
from stix.core import STIXPackage
from stix.utils.parser import UnsupportedVersionError

LATEST_STIX_VERSION = "1.2"

class StixSourceItem(object):
    """A base class for STIX package containers."""

    def __init__(self, source_item):
        self.source_item = source_item
        self._logger = logging.getLogger()
        try:
            self.stix_package = STIXPackage.from_xml(self.io())
        except UnsupportedVersionError:
            updated = ramrod.update(self.io(), to_=LATEST_STIX_VERSION)
            document = updated.document.as_stringio()
            self.stix_package = STIXPackage.from_xml(document)
        except Exception:
            self._logger.error('error parsing STIX package (%s)',
                               self.file_name())
            self.stix_package = None

    def io(self):
        raise NotImplementedError

    def file_name(self):
        raise NotImplementedError

    def save(self, directory):
        try:
            stix_package = self.stix_package
            file_name = self.file_name()
            full_path = os.path.join(directory, file_name)
            self._logger.info('saving STIX package to file \'%s\'', full_path)
            with open(full_path, 'wb') as file_:
                file_.write(self.stix_package.to_xml())
        except Exception:
            self._logger.error('unable to save STIX package to file \'%s\'',
                               full_path)
