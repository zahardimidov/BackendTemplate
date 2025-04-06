import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).parent.parent.resolve()

sys.path.insert(0, BASE_DIR.__str__())
sys.path.insert(0, BASE_DIR.joinpath('app').__str__())
