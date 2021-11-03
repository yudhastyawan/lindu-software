import sys
import os
from pathlib import Path
sys.path.append(os.path.join(Path(__file__).resolve().parent.parent, "src"))

import lindu

def test_run():
    lindu.run()
    assert True

if __name__ == "__main__":
    test_run()