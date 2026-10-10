"""Locate ZIPs 28202 and 28215 on the paper's Fig 24 image, for slide labels.

The deck keeps the paper's Mecklenburg map (output/figures/fig-24-heatmap-
mecklenburg.png) unchanged and overlays two ZIP labels on the slide. This
script finds where to put them: it reads the raw ZCTA and county boundaries,
projects them to the map's CRS (NC State Plane, as in
src/analysis/phase3_county_heatmaps.py), clips the two ZIPs to the county, and
maps a point inside each ZIP onto the image using the county outline drawn in
the PNG. Read-only; nothing is recomputed from the study's results.

Run from the repo root:

    uv run python src/paper/seinforms_deck/fig24_labels.py

Output: src/paper/seinforms_deck/assets/fig24-labels.json (positions as
fractions of the image width and height).

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
from PIL import Image

from evpulse.constants import TARGET_CRS

REPO = Path(__file__).resolve().parents[3]
PNG = REPO / "output" / "figures" / "fig-24-heatmap-mecklenburg.png"
ZCTA = REPO / "data" / "raw" / "nc-zcta-boundaries.geojson"
COUNTY = REPO / "data" / "raw" / "nc-county-boundaries.geojson"
OUT = Path(__file__).resolve().parent / "assets" / "fig24-labels.json"
MECKLENBURG = "37119"
ZIPS = ("28202", "28215")


def outline_bbox(img: np.ndarray) -> tuple[int, int, int, int]:
    """Pixel bbox of the county outline (pure black line, left 85% of image).

    The colour bar on the right has a grey frame, and the navy fills are blue,
    so near-black pixels with no blue cast belong to the county outline (and
    the black edges of the station triangles, which lie inside it).
    """
    rgb = img[:, :, :3].astype(int)
    black = (rgb.max(axis=2) < 60) & (np.abs(rgb[:, :, 2] - rgb[:, :, 0]) < 25)
    black[:, int(img.shape[1] * 0.85) :] = False
    ys, xs = np.nonzero(black)
    return xs.min(), ys.min(), xs.max(), ys.max()


def main() -> None:
    img = np.asarray(Image.open(PNG).convert("RGB"))
    h, w = img.shape[:2]
    px0, py0, px1, py1 = outline_bbox(img)

    county = gpd.read_file(COUNTY)
    county = county[county["GEOID"] == MECKLENBURG].to_crs(TARGET_CRS)
    zcta = gpd.read_file(ZCTA).to_crs(TARGET_CRS)
    zcta = zcta[zcta["ZCTA5CE20"].isin(ZIPS)]
    clipped = gpd.clip(zcta, county)
    gx0, gy0, gx1, gy1 = county.total_bounds

    labels = {
        "image_px": [w, h],
        "outline_px": [int(px0), int(py0), int(px1), int(py1)],
    }
    for _, row in clipped.iterrows():
        pt = row.geometry.representative_point()
        fx = (px0 + (pt.x - gx0) / (gx1 - gx0) * (px1 - px0)) / w
        fy = (py0 + (gy1 - pt.y) / (gy1 - gy0) * (py1 - py0)) / h
        labels[row["ZCTA5CE20"]] = [round(fx, 4), round(fy, 4)]
    OUT.write_text(json.dumps(labels, indent=2) + "\n")
    print(json.dumps(labels))


if __name__ == "__main__":
    main()
