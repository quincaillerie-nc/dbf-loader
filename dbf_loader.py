# -*- coding: utf-8 -*-
"""
================================================================================
MODULE : dbf-loader / dbf_loader.py
================================================================================
Charge un fichier .DBF depuis un partage réseau SMB.
- Windows : lecture directe via chemin UNC
- Linux   : copie temporaire via smbclient puis lecture locale
================================================================================
"""

import platform
import subprocess
import os
from pathlib import Path
from dbfread import DBF
import pandas as pd
from dotenv import load_dotenv

# Charge le .env depuis la racine dev/
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# =====================================================
# CONFIG SMB  (lues depuis .env)
# =====================================================
SMB_HOST     = os.getenv("SMB_HOST",     "//192.168.0.250/bases")
SMB_USER     = os.getenv("SMB_USER",     "supportserv")
SMB_PASSWORD = os.getenv("SMB_PASSWORD", "")

# Chemin réseau Windows (UNC)
WINDOWS_BASE = os.getenv("SMB_WINDOWS_BASE", r"\\192.168.0.250\Bases")

# Dossier temporaire Linux
LINUX_TMP = "/tmp"


# =====================================================
# DÉTECTION OS
# =====================================================
def is_windows() -> bool:
    return platform.system() == "Windows"


# =====================================================
# POINT D'ENTRÉE PUBLIC
# =====================================================
def get_dbf(chemin_relatif: str) -> pd.DataFrame:
    """
    Charge un fichier .DBF depuis le réseau et retourne un DataFrame pandas.

    Paramètres
    ----------
    chemin_relatif : str
        Chemin depuis la racine du partage SMB.
        Exemple : "qc/article.dbf"

    Retourne
    --------
    pandas.DataFrame
    """
    if is_windows():
        return _load_windows(chemin_relatif)
    else:
        return _load_linux(chemin_relatif)


# =====================================================
# FONCTIONS INTERNES
# =====================================================
def _load_windows(chemin_relatif: str) -> pd.DataFrame:
    chemin_win = chemin_relatif.replace("/", "\\")
    full_path  = Path(WINDOWS_BASE) / chemin_win

    print(f"[DBF_LOADER] Windows → lecture directe : {full_path}")

    if not full_path.exists():
        raise FileNotFoundError(f"[DBF_LOADER] Fichier introuvable : {full_path}")

    return _read_dbf(str(full_path))


def _load_linux(chemin_relatif: str) -> pd.DataFrame:
    nom_fichier = Path(chemin_relatif).name
    tmp_path    = os.path.join(LINUX_TMP, nom_fichier)

    print(f"[DBF_LOADER] Linux → copie SMB vers {tmp_path}")

    cmd = [
        "smbclient", SMB_HOST,
        "-U", f"{SMB_USER}%{SMB_PASSWORD}",
        "-c", f'get "{chemin_relatif}" "{tmp_path}"'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"[DBF_LOADER] Échec smbclient :\n{result.stderr}"
        )

    print(f"[DBF_LOADER] Fichier copié : {tmp_path}")
    return _read_dbf(tmp_path)


def _read_dbf(path: str) -> pd.DataFrame:
    table = DBF(path, load=True, encoding="cp1252", char_decode_errors="ignore")
    df    = pd.DataFrame(iter(table))
    print(f"[DBF_LOADER] {len(df)} lignes chargées depuis {Path(path).name}")
    return df
