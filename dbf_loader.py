# modules/dbf_loader/dbf_loader.py

import platform
import subprocess
import os
from pathlib import Path
from dbfread import DBF
import pandas as pd

# =====================================================
# CONFIG SMB
# =====================================================
SMB_HOST     = "//192.168.0.250/bases"
SMB_USER     = "supportserv"
SMB_PASSWORD = "#Qu!ncal_2025"

# Chemin réseau Windows
WINDOWS_BASE = r"\\192.168.0.250\Bases"

# Dossier temp Linux
LINUX_TMP = "/tmp"

# =====================================================
# DETECTION OS
# =====================================================
def is_windows():
    return platform.system() == "Windows"

# =====================================================
# COPIE / ACCES DBF
# =====================================================
def get_dbf(chemin_relatif: str) -> pd.DataFrame:
    """
    Charge un DBF depuis le réseau.
    
    chemin_relatif : chemin depuis la base
    Ex: "qc/article.dbf"
    
    - Windows : lecture directe sur \\192.168.0.250\Bases\qc\article.dbf
    - Ubuntu  : copie via smbclient dans /tmp puis lecture
    
    Retourne un DataFrame pandas.
    """
    if is_windows():
        return _load_windows(chemin_relatif)
    else:
        return _load_linux(chemin_relatif)


def _load_windows(chemin_relatif: str) -> pd.DataFrame:
    # Convertit les / en \ pour Windows
    chemin_relatif_win = chemin_relatif.replace("/", "\\")
    full_path = Path(WINDOWS_BASE) / chemin_relatif_win

    print(f"[DBF_LOADER] Windows → lecture directe : {full_path}")

    if not full_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {full_path}")

    return _read_dbf(str(full_path))


def _load_linux(chemin_relatif: str) -> pd.DataFrame:
    # Nom du fichier seul pour le /tmp
    nom_fichier = Path(chemin_relatif).name
    tmp_path = os.path.join(LINUX_TMP, nom_fichier)

    print(f"[DBF_LOADER] Linux → copie SMB vers {tmp_path}")

    cmd = [
        "smbclient", SMB_HOST,
        "-U", f"{SMB_USER}%{SMB_PASSWORD}",
        "-c", f"get {chemin_relatif} {tmp_path}"
    ]

    subprocess.run(cmd, check=True)
    print(f"[DBF_LOADER] Fichier copié : {tmp_path}")

    return _read_dbf(tmp_path)


def _read_dbf(path: str) -> pd.DataFrame:
    table = DBF(path, load=True, encoding="cp1252", char_decode_errors="ignore")
    df = pd.DataFrame(iter(table))
    print(f"[DBF_LOADER] {len(df)} lignes chargées depuis {path}")
    return df
