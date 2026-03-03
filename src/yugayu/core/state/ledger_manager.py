import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Protocol

@dataclass
class ayuModel:
    name: str
    path: str
    origin: Optional[str] = None
    type: str = "base"
    shareable: bool = True  # NEW: Defines if it can be symlinked globally

@dataclass
class ayuEntry:
    name: str
    path: str
    origin: Optional[str] = None
    status: str = "active"
    capabilities: List[str] = field(default_factory=list) # NEW: E.g., ["image-generation-fp8"]
    inference_command: str = ""  # NEW: The agnostic execution instruction

@dataclass
class LabConfig:
    lab_root: str
    nas_path: Optional[str] = None
    hf_token: Optional[str] = None
    max_log_size_mb: int = 1024
    os_source_path: Optional[str] = None # NEW: Stores the repo root for dev commands
    admin_identities: List[str] = field(default_factory=lambda: ["admin-cli"])
    ayus: List[ayuEntry] = field(default_factory=list)
    models: List[ayuModel] = field(default_factory=list)
    os_capabilities: List[str] = field(default_factory=list)

def get_config_path() -> Path:
    return Path.home() / ".yugayu" / "config.yaml"

def load_config() -> LabConfig:
    config_path = get_config_path()
    if not config_path.exists():
        return LabConfig(lab_root=str(Path.home() / "yugayu-lab"))
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    if data is None:
        data = {}
    ayus = [ayuEntry(**p) for p in data.get("ayus", [])]
    models = [ayuModel(**m) for m in data.get("models", [])]
    return LabConfig(
        lab_root=data.get("lab_root", "~/yugayu-lab"),
        nas_path=data.get("nas_path"),
        hf_token=data.get("hf_token"),
        max_log_size_mb=data.get("max_log_size_mb", 1024),
        os_source_path=data.get("os_source_path"), # NEW
        admin_identities=data.get("admin_identities", ["admin-cli"]),
        ayus=ayus,
        models=models
    )

def save_config(config: LabConfig):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(asdict(config), f, default_flow_style=False)

@dataclass
class SessionState:
    session_id: str
    shared_secret: bytes
    is_active: bool

class StateStore(Protocol):
    def save_session(self, ayu_name: str, state: SessionState) -> None: ...
    def load_session(self, ayu_name: str) -> SessionState | None: ...

class MemoryStateStore:
    def __init__(self):
        self._store = {}
    def save_session(self, ayu_name: str, state: SessionState) -> None:
        self._store[ayu_name] = state
    def load_session(self, ayu_name: str) -> SessionState | None:
        return self._store.get(ayu_name)