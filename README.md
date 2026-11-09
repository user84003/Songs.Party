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

## Editing from any device
- Everything is editable in the app: add, edit (title/artist), delete and recategorise songs, add, rename and delete categories, set cues. 
- Open **Song library** on your first device, enter repo + token, then click **Copy setup link for other devices** and open that link once on your phone or another computer. It sets up the repo and token there (the link contains your token, keep it private). After that, tick auto-save and edits sync through `songs.json` in your repo.
- **Songs in set: All** plays every song in the chosen category. YouTube links are found just in time, two songs ahead.

## Default hook, scrubbing, ads
- **Default hook** (player) and **reset** (library) now try to read YouTube's Most replayed graph for the song and set both IN and OUT. YouTube blocks pages from reading it directly, so this goes through free public CORS proxies and may fail; then the saved default is used. For reliable results run `scripts/fetch_hooks.py`.
- **Scrub:** drag anywhere on the waveform to move through the song. Drag the green IN / OUT lines to change the hook (saved).
- The default GitHub repo is `user84003/Songs.Party` (change it in Song library).
- **Ads:** if the next song starts with a YouTube ad, the current song keeps playing until the real song is playing, then they crossfade (up to 45 seconds). Ads are shown by YouTube per browser: signed-in YouTube Premium accounts and ad-blocking extensions explain why one browser shows ads and another doesn't.

## Faster transitions
The next song is cued on the idle deck while the current one plays, so it starts instantly at the crossfade. YouTube ads are not skipped or blocked by this app; sign in to YouTube Premium in your browser to get no ads, or use audio you have the rights to play.

## Phone layout
Below 700px wide the player switches to a phone layout: compact top bar, title and scrubbable waveform, a one-line 'next song' strip, a collapsible Categories panel, a 2-by-2 grid of actions, and large Skip / Play full buttons pinned to the bottom. The first song now starts inside your tap (phones block audio that starts after a wait); if the phone still blocks it, a 'Tap to play' button appears. Some iPhones also block the second YouTube player, so Chrome on Android works best for crossfades.

## Background and phones
- While a set plays the app asks the phone to keep the screen on (Wake Lock, needs https or localhost), shows the song on the lock screen / notification (Media Session) with play, pause and next, and resumes playback when you come back to the tab.
- The current set and position are remembered every few seconds. If the phone closes the page, open the app again and tap **Resume last set** (valid for 6 hours).
- Limit: YouTube's embedded player is paused by phone browsers when the screen locks or you switch apps. Keeping the screen on is the workaround. Playing in the background needs a different audio source (audio files you may play, via an audio element).
