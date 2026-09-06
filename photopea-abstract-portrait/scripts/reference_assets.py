"""Validate/list reference records, prepare a session, fetch explicit artwork images."""
import argparse
import copy
import io
import json
from pathlib import Path
import re
import sys
import time
import urllib.parse
import urllib.request

from select_artist import DEFAULT_CATALOG, now, read_json, resolve_artist, write_json


def public_url(url):
    p = urllib.parse.urlparse(url or '')
    return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password


def validate(catalog, root):
    errors = []
    artists, works = catalog.get('artists', []), catalog.get('artworks', [])
    artist_ids, work_ids = [a.get('id') for a in artists], [w.get('id') for w in works]
    if len(artist_ids) != len(set(artist_ids)) or None in artist_ids:
        errors.append('Duplicate/missing artist ID')
    if len(work_ids) != len(set(work_ids)) or None in work_ids:
        errors.append('Duplicate/missing artwork ID')
    index = {w.get('id'): w for w in works}
    aliases = {}
    from select_artist import normal
    for artist in artists:
        aid = artist.get('id')
        for value in [aid, artist.get('name_zh'), artist.get('name_en'), *artist.get('aliases', [])]:
            if not isinstance(value, str) or not value.strip():
                errors.append(f'{aid}: empty identity field'); continue
            key = normal(value)
            if key in aliases and aliases[key] != aid:
                errors.append(f'Ambiguous alias: {value}')
            aliases[key] = aid
        guide = (root / artist.get('guide_path', '')).resolve()
        if not guide.is_relative_to(root.resolve()) or not guide.is_file():
            errors.append(f'{aid}: missing/out-of-package guide')
        directions = artist.get('directions', [])
        dids = [d.get('id') for d in directions]
        if len(dids) != len(set(dids)) or artist.get('default_direction_id') not in dids:
            errors.append(f'{aid}: invalid/default direction')
        for direction in directions:
            refs = direction.get('work_ids', [])
            if len(refs) != len(set(refs)):
                errors.append(f'{aid}/{direction.get("id")}: duplicate references')
            if direction.get('reference_set_ready') and not 3 <= len(refs) <= 5:
                errors.append(f'{aid}/{direction.get("id")}: ready set needs 3-5 works')
            if direction.get('id') == artist.get('default_direction_id') and not direction.get('reference_set_ready'):
                errors.append(f'{aid}: default direction has no prepared reference set')
            for wid in refs:
                if wid not in index or index[wid].get('artist_id') != aid:
                    errors.append(f'{aid}: wrong/missing artwork {wid}')
                elif direction.get('id') not in index[wid].get('direction_ids', []):
                    errors.append(f'{wid}: direction membership mismatch')
    for work in works:
        wid = work.get('id')
        for key in ('title_original', 'date_display', 'collection_url', 'metadata_source'):
            if not work.get(key): errors.append(f'{wid}: missing {key}')
        if work.get('artist_id') not in artist_ids: errors.append(f'{wid}: unknown artist')
        if not public_url(work.get('collection_url')): errors.append(f'{wid}: invalid collection URL')
        image = work.get('image', {})
        if image.get('url') and not public_url(image['url']): errors.append(f'{wid}: invalid image URL')
        if image.get('url') and not image.get('provenance'): errors.append(f'{wid}: image provenance missing')
    return errors


def prepare(args, catalog):
    session = read_json(args.session)
    artist = resolve_artist(catalog['artists'], session['selection']['artist_id'])
    did = args.direction or session.get('direction_id') or artist['default_direction_id']
    direction = next((d for d in artist['directions'] if d['id'] == did), None)
    if not direction: raise ValueError(f'Unknown direction: {did}')
    ids = args.works or direction.get('work_ids', [])
    if len(set(ids)) != len(ids) or not 3 <= len(ids) <= 5:
        raise ValueError('Prepare exactly 3-5 distinct works; supplement an incomplete alternate direction first')
    index = {w['id']: w for w in catalog['artworks']}
    for wid in ids:
        if wid not in index or index[wid]['artist_id'] != artist['id'] or did not in index[wid]['direction_ids']:
            raise ValueError(f'Artwork not in selected artist/direction: {wid}')
    if args.out.resolve() == args.session.resolve(): raise ValueError('Manifest must differ from session')
    if args.out.exists() and not args.replace:
        old = read_json(args.out)
        if old.get('artist_id') != artist['id'] or old.get('direction_id') != did or [w['id'] for w in old.get('artworks', [])] != ids:
            raise ValueError('Existing manifest differs; --replace is required for an intentional change')
        session['direction_id'] = did
        session['reference_manifest'] = str(args.out.resolve())
        write_json(args.session, session)
        return {'reused': True, 'manifest': str(args.out.resolve()), 'work_count': len(ids)}
    manifest = {
        'schema_version': 1, 'artist_id': artist['id'], 'artist_name': artist['name_zh'],
        'direction_id': did, 'direction_name': direction['name'], 'created_at': now(),
        'catalog_version': catalog.get('version'), 'guide_path': artist['guide_path'],
        'artworks': [copy.deepcopy(index[wid]) for wid in ids],
        'viewing_note': 'Downloaded files are not visually inspected. Record actual viewing and reference roles separately.',
    }
    write_json(args.out, manifest)
    session['direction_id'] = did
    session['reference_manifest'] = str(args.out.resolve())
    write_json(args.session, session)
    return {'reused': False, 'manifest': str(args.out.resolve()), 'work_count': len(ids)}


def fetch(args):
    from PIL import Image, UnidentifiedImageError
    manifest = read_json(args.manifest)
    destination = args.out_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    results = []
    for work in manifest['artworks']:
        wid = work['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', wid): raise ValueError(f'Unsafe artwork ID: {wid}')
        info = work.get('image', {})
        url = info.get('url')
        result = {'artwork_id': wid, 'checked_at': now(), 'visually_inspected': False}
        prior = work.get('fetch_result', {})
        cached = Path(prior['local_path']) if prior.get('local_path') else None
        try:
            if cached and cached.is_file() and cached.resolve().is_relative_to(destination) and prior.get('source_url') == url and not args.refresh:
                with Image.open(cached) as img:
                    img.load(); size = list(img.size)
                result.update(status='cached', local_path=str(cached.resolve()), pixels=size, source_url=url)
            elif not url:
                result.update(status='needs-browser', reason=info.get('status', 'No verified image URL'), collection_url=work['collection_url'])
            else:
                if not public_url(url): raise ValueError('Only explicit public HTTPS image URLs are supported')
                req = urllib.request.Request(url, headers={'User-Agent': 'portrait-reference-library/1.0', 'Accept': 'image/*'})
                with urllib.request.urlopen(req, timeout=args.timeout) as response:
                    if not public_url(response.geturl()): raise ValueError('Unexpected non-HTTPS redirect')
                    payload = response.read(args.max_mb * 1024 * 1024 + 1)
                    if len(payload) > args.max_mb * 1024 * 1024: raise ValueError('Image exceeds download size limit')
                    resolved_url = response.geturl()
                with Image.open(io.BytesIO(payload)) as img:
                    fmt = img.format; img.verify()
                with Image.open(io.BytesIO(payload)) as img:
                    img.load(); size = list(img.size)
                ext = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'TIFF': '.tif', 'GIF': '.gif'}.get(fmt)
                if not ext: raise ValueError(f'Unsupported reference raster format: {fmt}')
                path = destination / (wid + ext)
                path.write_bytes(payload)
                result.update(status='downloaded', local_path=str(path), pixels=size, format=fmt, source_url=url, resolved_url=resolved_url)
                if min(size) < 500: result['quality_note'] = 'Small image: seek a larger source for local brush/edge inspection.'
        except (OSError, ValueError, UnidentifiedImageError) as exc:
            result.update(status='unavailable', reason=str(exc), collection_url=work['collection_url'])
        work['fetch_result'] = result
        results.append(result)
        write_json(args.manifest, manifest)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        if url and result['status'] not in ('cached', 'needs-browser'):
            time.sleep(1.0 if 'artic.edu' in url else 0.25)
    if args.contact_sheet:
        make_sheet(manifest, args.contact_sheet)
    return {'manifest': str(args.manifest.resolve()), 'downloaded_or_cached': sum(r['status'] in ('downloaded', 'cached') for r in results), 'total': len(results), 'all_available': all(r['status'] in ('downloaded', 'cached') for r in results)}


def make_sheet(manifest, path):
    from PIL import Image, ImageDraw, ImageOps
    ready = [(w['id'], w['fetch_result']['local_path']) for w in manifest['artworks'] if w.get('fetch_result', {}).get('status') in ('cached', 'downloaded')]
    if not ready: raise ValueError('No images available for contact sheet')
    panel_w, panel_h = 480, 540
    columns = min(3, len(ready))
    rows = (len(ready) + columns - 1) // columns
    sheet = Image.new('RGB', (panel_w * columns, panel_h * rows), '#ededeb')
    draw = ImageDraw.Draw(sheet)
    for n, (wid, file) in enumerate(ready):
        with Image.open(file) as src:
            item = ImageOps.contain(src.convert('RGB'), (440, 460))
        col, row = n % columns, n // columns
        x = col * panel_w + (panel_w - item.width) // 2
        sheet.paste(item, (x, row * panel_h + 35 + (460 - item.height) // 2))
        draw.text((col * panel_w + 12, row * panel_h + 510), wid, fill='black')
    path = Path(path).resolve(); path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() != '.png': raise ValueError('Contact sheet must use .png')
    sheet.save(path, 'PNG')


def table(catalog):
    def esc(value): return str(value or '').replace('|', '\\|').replace('\n', ' ')
    lines = ['# 艺术家与参考作品索引', '', f"资料版本：{catalog['version']}；整理日期：{catalog['updated_at']}。", '',
             '本表由 artist-catalog.json 生成；收录代表性创作研究方向。图像下载与实际人工审阅分别记录状态。', '',
             '| 艺术家 | 默认方向 | 其他研究方向 |', '|---|---|---|']
    for artist in catalog['artists']:
        default = next(d for d in artist['directions'] if d['id'] == artist['default_direction_id'])
        others = '；'.join(d['name'] for d in artist['directions'] if d['id'] != default['id'])
        lines.append(f"| {esc(artist['name_zh'])} | {esc(default['name'])} | {esc(others)} |")
    for artist in catalog['artists']:
        lines += ['', f"## {artist['name_zh']} / {artist['name_en']}", '', '| 作品 ID | 作品／年代 | 馆藏或资料方 | 图像获取 |', '|---|---|---|---|']
        for work in catalog['artworks']:
            if work['artist_id'] != artist['id']: continue
            img = work.get('image', {})
            access = f"[图像]({img['url']})" if img.get('url') else '需浏览器／补充图像来源'
            lines.append(f"| {work['id']} | [{esc(work['title_original'])}]({work['collection_url']}) · {esc(work['date_display'])} | {esc(work.get('institution'))} | {access} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    listing = sub.add_parser('list'); listing.add_argument('--artist')
    tab = sub.add_parser('table'); tab.add_argument('--out', type=Path, required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('--session', type=Path, required=True); prep.add_argument('--out', type=Path, required=True)
    prep.add_argument('--direction'); prep.add_argument('--works', nargs='+'); prep.add_argument('--replace', action='store_true')
    get = sub.add_parser('fetch')
    get.add_argument('--manifest', type=Path, required=True); get.add_argument('--out-dir', type=Path, required=True)
    get.add_argument('--refresh', action='store_true'); get.add_argument('--timeout', type=float, default=20)
    get.add_argument('--max-mb', type=int, default=25); get.add_argument('--contact-sheet', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'fetch':
            if args.timeout <= 0 or args.max_mb <= 0: raise ValueError('Positive timeout and size limit required')
            result = fetch(args)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result['all_available'] else 3
        catalog = read_json(args.catalog)
        if args.command == 'validate':
            errors = validate(catalog, args.catalog.resolve().parent.parent)
            result = {'valid': not errors, 'artists': len(catalog['artists']), 'artworks': len(catalog['artworks']), 'errors': errors}
            print(json.dumps(result, ensure_ascii=False, indent=2)); return 2 if errors else 0
        if args.command == 'prepare': result = prepare(args, catalog)
        elif args.command == 'list':
            result = resolve_artist(catalog['artists'], args.artist) if args.artist else catalog['artists']
        elif args.command == 'table':
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(table(catalog), encoding='utf-8')
            result = {'table': str(args.out.resolve())}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
