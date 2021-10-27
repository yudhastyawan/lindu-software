import sys
import os
from pathlib import Path
sys.path.append(os.path.join(Path(__file__).resolve().parent.parent, "src"))

import lindu

lindu.run()