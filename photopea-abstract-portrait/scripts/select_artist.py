"""Uniform artist selection with persistent, explicit resume semantics. Stdlib only."""
import argparse
import json
import os
from pathlib import Path
import random
import re
import sys
import tempfile
import time
import unicodedata
from datetime import datetime, timezone

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'references' / 'artist-catalog.json'


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict):
        raise ValueError(f'Expected JSON object: {path}')
    return data


def write_json(path, data):
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
        for attempt in range(6):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.1)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def normal(value):
    text = unicodedata.normalize('NFKD', value).casefold()
    return re.sub(r'[\W_]+', '', ''.join(c for c in text if not unicodedata.combining(c)))


def resolve_artist(artists, value):
    key = normal(value)
    matches = [a for a in artists if key in {normal(v) for v in
               [a['id'], a['name_zh'], a['name_en'], *a.get('aliases', [])]}]
    if len(matches) != 1:
        raise ValueError(f'Unknown or ambiguous artist: {value}')
    return matches[0]


def choose(catalog, session, artist=None, excluded=(), seed=None, redraw=False):
    artists = catalog['artists']
    ids = [a['id'] for a in artists]
    if not artists or len(ids) != len(set(ids)):
        raise ValueError('Catalog must contain unique artists')
    excluded_ids = {resolve_artist(artists, value)['id'] for value in excluded}
    specified = resolve_artist(artists, artist) if artist else None
    old = session.get('selection')
    if old and not redraw:
        prior = resolve_artist(artists, old['artist_id'])
        if prior['id'] in excluded_ids or (specified and prior['id'] != specified['id']):
            raise ValueError('Existing selection conflicts with request. Use --redraw only after user requests a new selection.')
        return old, True
    pool = [a for a in artists if a['id'] not in excluded_ids]
    if not pool:
        raise ValueError('No eligible artists remain')
    if specified and specified['id'] in excluded_ids:
        raise ValueError('Specified artist is also excluded')
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    chosen = specified or rng.choice(pool)
    result = {
        'artist_id': chosen['id'], 'artist_name': chosen['name_zh'],
        'mode': 'specified' if specified else 'random',
        'method': 'user-specified' if specified else ('seeded-random' if seed is not None else 'system-random'),
        'eligible_artist_ids': [a['id'] for a in pool],
        'excluded_artist_ids': sorted(excluded_ids),
        'probability': None if specified else f'1/{len(pool)}',
        'seed': seed if not specified else None,
        'catalog_version': catalog.get('version'), 'selected_at': now(),
        'guide_path': chosen['guide_path'],
        'default_direction_id': chosen['default_direction_id'],
    }
    if old:
        session.setdefault('selection_history', []).append(old)
        invalidated = {key: session[key] for key in ('direction_id', 'reference_manifest', 'visual_interpretation', 'technique_study', 'quality_checks', 'export_review') if key in session}
        if isinstance(session.get('photopea'), dict):
            invalidated['photopea'] = dict(session['photopea'])
        if invalidated:
            session.setdefault('revision_history', []).append({'invalidated_at': now(), **invalidated})
        for key in ('direction_id', 'reference_manifest', 'visual_interpretation', 'technique_study', 'quality_checks', 'export_review'):
            session.pop(key, None)
        if isinstance(session.get('photopea'), dict):
            for key in ('save_observed_at', 'save_observation', 'reopened_at', 'reopen_observation', 'editable_layers', 'reference_underlay_status', 'ui_state'):
                session['photopea'].pop(key, None)
    session['selection'] = result
    session.setdefault('schema_version', 1)
    return result, False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--artist')
    parser.add_argument('--exclude', action='append', default=[])
    parser.add_argument('--seed', type=int, help='Explicit reproducible/test mode; otherwise system randomness')
    parser.add_argument('--redraw', action='store_true', help='Only when the user has explicitly requested re-selection')
    args = parser.parse_args()
    try:
        catalog = read_json(args.catalog)
        session = read_json(args.session) if args.session.exists() else {}
        selection, reused = choose(catalog, session, args.artist, args.exclude, args.seed, args.redraw)
        if not reused:
            write_json(args.session, session)
        print(json.dumps({'reused': reused, 'session': str(args.session.resolve()), 'selection': selection}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
