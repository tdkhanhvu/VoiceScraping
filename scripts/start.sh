#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# Enable strict mode.
set -euo pipefail

# Temporarily disable strict mode and activate conda:
set +euo pipefail
conda activate VoiceScraping

# Re-enable strict mode:
set -euo pipefail

# exec the final command:
exec python src/main.py