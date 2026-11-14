"""SmartQC settings: config.example.yaml (defaults, in Git) + config.local.yaml (this computer only).

Use it anywhere like this:
    from engine.config import load_settings
    settings = load_settings()
    port = settings.get("serial.port")
"""

import difflib                     # built-in: finds similar words, for "did you mean...?"
import json                        # built-in: only used to print the settings neatly
import logging                     # built-in: our black box (Lesson 1.4)
import sys                         # built-in: sys.exit() ends the program with a status code
from dataclasses import dataclass  # built-in: the @dataclass shortcut (Lesson 1.2)
from pathlib import Path           # built-in: file locations that work on any computer

import yaml                        # pyyaml package: reads YAML files (Lesson 1.3)

log = logging.getLogger(__name__)  # this file's post box (Lesson 1.4)

REPO_ROOT = Path(__file__).parent.parent             # engine\config.py → engine → F:\Smart-QC
EXAMPLE_FILE = REPO_ROOT / "config.example.yaml"     # the standard form (in Git)
LOCAL_FILE = REPO_ROOT / "config.local.yaml"         # this computer's notes (not in Git)


class ConfigError(Exception):      # ours: a new error type, "a kind of Exception"
    """Raised when the settings files have a problem we can explain."""


def _read_yaml(path):
    """Read one YAML file and return a dict (an empty dict if the file is empty)."""
    try:
        with open(path, encoding="utf-8") as f:   # open, read, always close (Lesson 1.3)
            data = yaml.safe_load(f)              # YAML text → dict
    except yaml.YAMLError as err:                 # the file exists but is badly written
        raise ConfigError(f"{path.name} is not valid YAML:\n{err}") from None
        # ↑ path.name = just the file name, e.g. "config.local.yaml"
        #   "from None" = show only our clear message, not two tangled tracebacks
    if data is None:          # an empty file gives None, not a dict
        return {}             # so treat it as "no settings"
    if not isinstance(data, dict):   # e.g. the file contains just a list or one word
        raise ConfigError(f"{path.name} must contain sections like 'camera:' at the top level")
    return data


def _suggest(word, choices):
    """Return ' Did you mean ...?' if a similar word exists, else an empty string."""
    close = difflib.get_close_matches(word, list(choices), n=1)   # e.g. "prot" → ["port"]
    if close:                                    # the list has something in it
        return f" Did you mean '{close[0]}'?"    # close[0] = the first (best) match
    return ""                                    # nothing similar: add nothing


def _merge(defaults, local):
    """Write local values over the defaults, refusing any unknown section or setting."""
    for section, values in local.items():        # e.g. section="serial", values={"port": "COM5"}
        if section not in defaults:              # e.g. "serail:" typo
            raise ConfigError(
                f"config.local.yaml: unknown section '{section}'."
                + _suggest(section, defaults.keys())
            )
        if not isinstance(values, dict):         # e.g. "serial: COM5" written on one line
            raise ConfigError(
                f"config.local.yaml: '{section}' must have its settings indented under it"
            )
        for key, value in values.items():        # e.g. key="port", value="COM5"
            if key not in defaults[section]:     # e.g. "prot" typo
                raise ConfigError(
                    f"config.local.yaml: unknown setting '{section}.{key}'."
                    + _suggest(key, defaults[section].keys())
                )
            defaults[section][key] = value       # known setting: local value wins
    return defaults


@dataclass
class Settings:                   # ours: the one settings object every program uses
    data: dict                    # all settings, after merging
    local_used: bool              # True if config.local.yaml was found

    def get(self, dotted_key):
        """Return one setting by 'section.key', e.g. settings.get('serial.port')."""
        section, _, key = dotted_key.partition(".")   # "serial.port" → "serial", ".", "port"
        if section not in self.data:
            raise ConfigError(
                f"No settings section '{section}'." + _suggest(section, self.data.keys())
            )
        if key not in self.data[section]:
            raise ConfigError(
                f"No setting '{dotted_key}'." + _suggest(key, self.data[section].keys())
            )
        return self.data[section][key]


def load_settings():
    """Read both files and return one Settings object. Raises ConfigError on any problem."""
    if not EXAMPLE_FILE.exists():     # the standard form must always be there
        raise ConfigError(f"Missing {EXAMPLE_FILE}. It belongs in the repo: try 'git pull'.")
    data = _read_yaml(EXAMPLE_FILE)   # start from the defaults

    local_used = LOCAL_FILE.exists()
    if local_used:                    # this computer has its own notes: apply them
        data = _merge(data, _read_yaml(LOCAL_FILE))
        log.info("Loaded %s with local changes from %s", EXAMPLE_FILE.name, LOCAL_FILE.name)
    else:                             # a fresh computer: defaults are fine, but say so
        log.warning("No %s found, using defaults only. Copy config.example.yaml to make one.",
                    LOCAL_FILE.name)
    return Settings(data, local_used)


if __name__ == "__main__":            # self-test: python -m engine.config
    from engine.log import setup_logging   # our Lesson 1.4 file
    setup_logging("config")                # screen + logs\config_....log
    try:
        settings = load_settings()
        print(json.dumps(settings.data, indent=2))   # print every setting, neatly
        print("Local file used:", settings.local_used)
        print("Serial port:", settings.get("serial.port"))
        print("Camera index:", settings.get("camera.index"))
    except ConfigError as err:        # only OUR explained problems are caught here
        print("SETTINGS PROBLEM:", err)
        sys.exit(1)                   # stop, and tell Windows it ended with a problem