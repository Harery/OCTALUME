# Test dependencies
# Install with: pip install -e ".[test]"

import sys
from pathlib import Path

# Add src to path for local development
src_path = Path(__file__).parent.parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))
