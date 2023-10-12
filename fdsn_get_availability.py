"""
Get the data availability of seismic stations from FDSN data centers.

Also see a related ObsPy issue request: https://github.com/obspy/obspy/pull/3002

Author: Dongdong Tian @ CUG
Inital Date: 2023/10/21
Repository: https://github.com/seisman/SeisDB-scripts/
"""
import sys
from io import StringIO

import pandas as pd
import requests


def usage():
    """
    Print usage information.
    """
    print(
        "Get the data availability of seismic stations from FDSN data centers.\n\n"
        f"Usage:\n    python {sys.argv[0]} network station\n\n"
        "    Station can be a single station name, a comma-separated list of station namesm\n"
        "    or a wildcard expression. For a wildcard expression, enclose it in quotes.\n\n"
        f"Example:\n    python {sys.argv[0]} IM 'TX*'\n"
        ""
    )


if len(sys.argv) != 3:
    usage()
    sys.exit(1)

network, station = sys.argv[1], sys.argv[2]
r = requests.get(
    "https://service.iris.edu/fdsnws/availability/1/extent",
    params={"net": network, "sta": station, "format": "request"},
    timeout=30,
)
if r.status_code != 200:
    print(f"Error: {r.status_code}")
    sys.exit(1)

df = pd.read_csv(
    StringIO(r.text),
    names=["network", "station", "location", "channel", "starttime", "endtime"],
    delim_whitespace=True,
)
df["starttime"] = pd.to_datetime(df["starttime"])
df["endtime"] = pd.to_datetime(df["endtime"])
print("Data availability:")
print(f"  network: {network}")
print(f"  station: {station}")
print("  Start time:", df["starttime"].min().strftime("%Y-%m-%d"))
print("  End time:", df["endtime"].max().strftime("%Y-%m-%d"))
