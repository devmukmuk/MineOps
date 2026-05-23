from mineops.settings import load_settings

def test_load_settings() -> None:
settings = load_settings()

```
assert "app" in settings
```

