import sys
from proveit._core_.context import Theorems
sys.modules[__name__] = Theorems(__name__, __file__)
