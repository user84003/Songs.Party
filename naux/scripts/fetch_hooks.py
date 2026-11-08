"""Fill hook start/end from YouTube's "Most replayed" heatmap (via yt-dlp).

Usage: pip install yt-dlp && python scripts/fetch_hooks.py [--force]

- Songs with no hook: start AND end come from the heatmap peak (hs = "yt").
- Songs with a NAUX start (hs = "naux"): the start is kept, only the END is filled
  (where the replay level drops after the start).
- Songs you tuned by hand (hs = "manual") are never touched.
Songs without a Most replayed graph (low views) are skipped."""
import json, re, subprocess, sys
from pathlib import Path

FORCE = '--force' in sys.argv
P = Path(__file__).resolve().parent.parent / 'songs.json'


def vid(u):
    m = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})', u or '')
    return m.group(1) if m else None


def peak_hook(hm, dur):
    """Start and end around the highest replay peak (ignores the first 8% and last 10%)."""
    ok = [i for i, b in enumerate(hm) if .08 * dur <= b['start_time'] <= .9 * dur] or list(range(len(hm)))
    peak = max(ok, key=lambda i: hm[i]['value'])
    thr = hm[peak]['value'] * .8
    a = b = peak
    while a > 0 and hm[a - 1]['value'] >= thr: a -= 1
    while b < len(hm) - 1 and hm[b + 1]['value'] >= thr: b += 1
    start = max(0, round(hm[a]['start_time']) - 3)
    end = min(dur - 1, max(round(hm[b]['end_time']), start + 35), start + 90)
    return start, int(end)


def end_after(hm, dur, start):
    """End for a known start: first point (at least 30s in) where replays fall below 70% of the level at the start."""
    near = [b['value'] for b in hm if b['end_time'] >= start - 5 and b['start_time'] <= start + 15]
    ref = max(near) if near else max(b['value'] for b in hm)
    cut = next((b['start_time'] for b in hm if b['start_time'] >= start + 30 and b['value'] < ref * .7), None)
    end = cut if cut is not None else start + 60
    return int(min(dur - 1, max(start + 35, min(end, start + 90))))


def main():
    data = json.loads(P.read_text(encoding='utf-8'))
    changed = 0
    for s in data['songs']:
        v, hs = vid(s.get('yt')), s.get('hs')
        if not v or hs == 'manual':
            continue
        if hs == 'yt' and not FORCE:
            continue
        if hs == 'naux' and s.get('end') is not None and not FORCE:
            continue
        r = subprocess.run(['yt-dlp', '--skip-download', '--dump-single-json', '--no-warnings',
                            'https://www.youtube.com/watch?v=' + v], capture_output=True, text=True, timeout=120)
        try:
            info = json.loads(r.stdout)
        except Exception:
            print('FAILED  ', s['t'], (r.stderr or '')[:120].strip()); continue
        hm, dur = info.get('heatmap'), info.get('duration') or 0
        if not hm or not dur:
            print('NO DATA ', s['t'], '(video has no Most replayed graph)'); continue
        if hs == 'naux' and s.get('hook') is not None:
            s['end'] = end_after(hm, dur, s['hook'])
            print('END     ', s['t'], f"{s['hook']}s -> {s['end']}s (NAUX start kept)")
        else:
            s['hook'], s['end'] = peak_hook(hm, dur)
            s['hs'] = 'yt'
            print('OK      ', s['t'], f"{s['hook']}s -> {s['end']}s")
        changed += 1
    P.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'Updated {changed} song(s).')


if __name__ == '__main__':
    main()
