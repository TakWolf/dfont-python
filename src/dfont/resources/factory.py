from typing import Final

from dfont.resources.fond import FondResource
from dfont.resources.nfnt import NfntResource
from dfont.resources.sfnt import SfntResource

RESOURCE_TYPE_REGISTRY: Final = {
    'sfnt': SfntResource,
    # 'NFNT': NfntResource,
    # 'FOND': FondResource,
}
