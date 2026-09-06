"""Check exported raster files and report missing human observations without inventing them."""
import argparse
import json
from pathlib import Path
import sys
import urllib.parse

from select_artist import now, read_json, write_json


def verify(session, image_path, min_long_edge=2000):
    from PIL import Image
    errors, pending = [], []
    path = Path(image_path).resolve()
    if not path.is_file(): raise ValueError(f'Export does not exist: {path}')
    with Image.open(path) as image:
        fmt = image.format; image.verify()
    with Image.open(path) as image:
        image.load(); width, height = image.size
    if fmt not in ('PNG', 'JPEG'): errors.append('Expected final PNG or JPEG image')
    if max(width, height) < min_long_edge: errors.append(f'Long edge below {min_long_edge}px')
    canvas = session.get('canvas', {})
    if canvas.get('width') and canvas.get('height'):
        cw, ch = float(canvas['width']), float(canvas['height'])
        if cw <= 0 or ch <= 0: errors.append('Canvas dimensions must be positive')
        elif abs(width / height - cw / ch) > 0.01: errors.append('Export aspect ratio differs from recorded canvas')
    else: pending.append('Record intended canvas dimensions')
    canva = session.get('canva', {})
    url = canva.get('design_url', '')
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in ('www.canva.com', 'canva.com') or not parsed.path.startswith('/design/') or len(parsed.path.split('/')) < 3 or not parsed.path.split('/')[2]:
        errors.append('Missing or invalid Canva design URL (a recorded editor URL is required)')
    if not canva.get('save_observed_at') or not canva.get('save_observation'): pending.append('Observe Canva UI save success')
    if not canva.get('editable_elements'): pending.append('Individually select and inspect key editable elements')
    if canva.get('reference_underlay_status') not in ('removed', 'hidden', 'not_used'): pending.append('Record final reference-underlay status')
    checks = session.get('quality_checks', [])
    for scale in ('thumbnail', 'normal', 'detail'):
        if not any(c.get('scale') == scale and c.get('checked_at') and c.get('observation') for c in checks):
            pending.append(f'Perform and record {scale} visual inspection')
    review = session.get('export_review', {})
    if not review.get('viewed_at') or not review.get('observation'): pending.append('Open and visually inspect the actual exported file')
    return {
        'checked_at': now(), 'image': str(path), 'format': fmt, 'width': width, 'height': height,
        'bytes': path.stat().st_size, 'canva_design_url': url, 'mechanical_checks_passed': not errors,
        'errors': errors, 'missing_manual_records': pending,
        'manual_records_present': not pending,
        'scope': 'Checks image decoding, dimensions, URL structure and presence of reports. Does not verify Canva save, permissions, layer editability, source attribution or aesthetic quality.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--min-long-edge', type=int, default=2000)
    args = parser.parse_args()
    try:
        if args.min_long_edge < 1: raise ValueError('Minimum image size must be positive')
        if args.out.resolve() in (args.image.resolve(), args.session.resolve()): raise ValueError('Report must not overwrite image or session')
        report = verify(read_json(args.session), args.image, args.min_long_edge)
        write_json(args.out, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report['errors']: return 2
        return 3 if report['missing_manual_records'] else 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
