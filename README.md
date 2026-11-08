# NAUX (party aux player)

Hindi and Punjabi party songs that drop straight into each song's best part and crossfade into the next.

## Run locally
    npx serve          # or: python3 -m http.server 3000
Open http://localhost:3000 (YouTube will not play from file://).

## First-time setup
1. Open **Song library**. Songs come from `songs.json` (about 570 songs in 3 categories) with NAUX-style best-part start times, but **no YouTube links yet**.
2. Click **Auto-find links** (works best with a YouTube Data API key; the free search quota is about 100 songs a day, so it may take a few days). You can also paste a link per song, or use the "find" link on a row.
3. Pick a category in **Play from** and press **Start the aux**.

## Making changes permanent
- Everything you change (links, drags, categories, deletes, added songs) is saved in your browser immediately.
- To keep it for every device: **Download songs.json** and commit it, or enter your repo and a fine-grained GitHub token (Contents: read and write) in Song library and use **Save to GitHub** (optional auto-save).

## Host on GitHub Pages
Push all files to a repo, then Settings > Pages > Deploy from branch `main`, folder `/ (root)`.

## Hooks
- Drag the start or end line on the waveform: saved as your own cue and always wins.
- **Default hook** (player) or **reset** (library row) clears your cue, back to the NAUX or YouTube most-replayed hook, else an automatic start.
- Optional: `pip install yt-dlp` then `python scripts/fetch_hooks.py`. Songs with no hook get start and end from YouTube's Most replayed graph. Songs with a NAUX start keep it and only get an END (where replays drop off). Hand-tuned songs are never touched. Use `--force` to recompute. Songs without a Most replayed graph keep the "seconds per hook" cut. `.github/workflows/hooks.yml` runs it on GitHub when you push `songs.json`.

## Files
- `index.html`: the whole app
- `songs.json`: songs and categories (`id, t, a, e, yt, hook, end, cat, hs`)
- `naux-*.json`: the separate list files (re-import with "Import songs file")
- `scripts/fetch_hooks.py`, `.github/workflows/hooks.yml`: optional hook fetching

## Auto links and quick delete
- Add a song by name (artist optional) and its YouTube link is found automatically.
- Press **Start the aux** and any song picked for the set that has no link gets one found first, so you never need to fill the library by hand. Found links are saved.
- **Delete song** in the player removes the current song from your library and moves on. **Undo** stays for 10 seconds.

## Using it from any device
1. Host on GitHub Pages (see above).
2. On each device, open the site once, go to Song library, enter `your-user/your-repo` and your GitHub token, and tick auto-save. Without the token a device can play but changes stay on that device.
3. Changes (new songs, links, categories, deletes, start/end cues) are merged into `songs.json` in your repo, so devices do not overwrite each other. Devices that have the repo entered read the latest `songs.json` straight from GitHub; others see it after the Pages cache refreshes (a few minutes).
