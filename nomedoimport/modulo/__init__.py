from .module import OCR

all = ('__version__')
from pbr.version import VersionInfo
__version__ = VersionInfo('packagemeu').release_string()