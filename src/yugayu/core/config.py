import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class ayuModel:
    name: str
    path: str
    origin: Optional[str] = None
    type: str = "base"

@dataclass
class ayuEntry:
    name: str
    path: str
    origin: Optional[str] = None
    status: str = "active"

@dataclass
class LabConfig:
    lab_root: str
    nas_path: Optional[str] = None
    hf_token: Optional[str] = None
    max_log_size_mb: int = 1024
    ayus: List[ayuEntry] = field(default_factory=list)
    models: List[ayuModel] = field(default_factory=list)

# REMOVED: CONFIG_PATH = Path.home() / ".yugayu" / "config.yaml"

def get_config_path() -> Path:
    """Dynamically fetch the config path so Pytest can mock it."""
    return Path.home() / ".yugayu" / "config.yaml"

def load_config() -> LabConfig:
    """Reads ~/.yugayu/config.yaml and returns a LabConfig object."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return LabConfig(lab_root=str(Path.home() / "yugayu-lab"))
    
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
        
    ayus = [ayuEntry(**p) for p in data.get("ayus", [])]
    models = [ayuModel(**m) for m in data.get("models", [])]
    
    return LabConfig(
        lab_root=data.get("lab_root", "~/yugayu-lab"),
        nas_path=data.get("nas_path"),
        hf_token=data.get("hf_token"),
        max_log_size_mb=data.get("max_log_size_mb", 1024),
        ayus=ayus,
        models=models
    )

def save_config(config: LabConfig):
    """Saves the LabConfig object back to the filesystem."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(asdict(config), f, default_flow_style=False)

def get_lab_root() -> Path:
    cfg = load_config()
    return Path(cfg.lab_root).expanduser()
