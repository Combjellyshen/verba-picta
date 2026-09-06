"""Check exported raster files and report missing human observations without inventing them."""
import argparse
import json
from pathlib import Path
import sys

from select_artist import now, read_json, write_json


def verify(session, image_path, min_long_edge=2000, project_path=None):
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
    photopea = session.get('photopea', {})
    project_value = project_path or photopea.get('project_path')
    project = {'path': None, 'decoded': False, 'layer_count': 0}
    if not project_value:
        errors.append('Missing layered PSD project')
    else:
        project_file = Path(project_value).resolve()
        project['path'] = str(project_file)
        if project_file == path or project_file.suffix.lower() != '.psd' or not project_file.is_file():
            errors.append('Expected an existing PSD project separate from the raster export')
        else:
            from psd_tools import PSDImage
            try:
                document = PSDImage.open(project_file)
                layers = [layer for layer in document.descendants() if not layer.is_group()]
                for layer in layers:
                    if layer.has_pixels():
                        layer.topil()
                project.update(decoded=True, width=document.width, height=document.height,
                               layer_count=len(layers), bytes=project_file.stat().st_size)
                if len(layers) < 2: errors.append('PSD must retain at least two independent content layers')
                if document.size != (width, height): errors.append('PSD dimensions differ from raster export')
            except Exception as exc:
                errors.append(f'PSD decoding failed: {exc}')
    if not photopea.get('save_observed_at') or not photopea.get('save_observation'): pending.append('Observe Photopea PSD download')
    if not photopea.get('reopened_at') or not photopea.get('reopen_observation'): pending.append('Reopen the saved PSD in Photopea and inspect layers')
    if not photopea.get('editable_layers'): pending.append('Individually select and inspect key editable layers and masks')
    if photopea.get('reference_underlay_status') not in ('removed', 'hidden', 'not_used'): pending.append('Record final reference-underlay status')
    study = session.get('technique_study', {})
    if not study.get('targets') or not study.get('trials') or not study.get('decision'): pending.append('Record technique targets, UI trials and chosen method')
    checks = session.get('quality_checks', [])
    for scale in ('thumbnail', 'normal', 'detail'):
        if not any(c.get('scale') == scale and c.get('checked_at') and c.get('observation') for c in checks):
            pending.append(f'Perform and record {scale} visual inspection')
    review = session.get('export_review', {})
    if not review.get('viewed_at') or not review.get('observation'): pending.append('Open and visually inspect the actual exported file')
    return {
        'checked_at': now(), 'image': str(path), 'format': fmt, 'width': width, 'height': height,
        'bytes': path.stat().st_size, 'project': project, 'mechanical_checks_passed': not errors,
        'errors': errors, 'missing_manual_records': pending,
        'manual_records_present': not pending,
        'scope': 'Checks raster and PSD decoding, dimensions, layer count and presence of reports. Does not verify Photopea UI actions, meaningful layer editability, source attribution or aesthetic quality.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--project', type=Path, help='Layered PSD; defaults to photopea.project_path in session')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--min-long-edge', type=int, default=2000)
    args = parser.parse_args()
    try:
        if args.min_long_edge < 1: raise ValueError('Minimum image size must be positive')
        session = read_json(args.session)
        project_value = args.project or session.get('photopea', {}).get('project_path')
        protected = [args.image.resolve(), args.session.resolve()]
        if project_value: protected.append(Path(project_value).resolve())
        if args.out.resolve() in protected: raise ValueError('Report must not overwrite image, project or session')
        report = verify(session, args.image, args.min_long_edge, project_value)
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
