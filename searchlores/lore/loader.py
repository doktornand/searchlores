from pathlib import Path
import yaml
from .models import Lore

def load_lore(path: str | Path) -> Lore:
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Lore.model_validate(data)