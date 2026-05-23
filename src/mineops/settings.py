from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path("config/config.yaml")

def load_settings(
config_path: Path = DEFAULT_CONFIG_PATH,
) -> dict[str, Any]:

```
if not config_path.exists():
    raise FileNotFoundError(
        f"Config file not found: {config_path}"
    )

with config_path.open(
    "r",
    encoding="utf-8",
) as file:
    data = yaml.safe_load(file)

return data or {}
```

