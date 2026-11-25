# STRATEGY — u-myronera-post-the-meme-win-the-feed-2de960bf ("Post the Meme, Win the Feed")

## Exact deliverable

1. `POST.json` at the repository root: `{"url": "https://x.com/<handle>/status/<id>"}` — the address of ONE public X post.
2. `main.ts` at the root (Node 22.18+, standard library only): copies `POST.json` from the repository root to `/output/POST.json`. That is all the grader needs it to do. It is run TWICE and both runs must write identical bytes.
3. The scored artifact is the X POST itself, not the repository program: a public X account posts a picture or short video about a make.fun meme aimed at AI-agent builders, with `@_myronera` and one of our play codes in the post's OWN text. Play code fetched read-only from the live route for this bounty: `makefun-mesa-lettuce-popcorn` (code 0 of 4).
4. At submit time: a transcript bundle of the agent sessions that decided the creative, made the image and wrote this repo, plus a run record. A source-bundle entry is signed with the wallet in `.makefun/freshness.json` (NkaXSbVRgkefLseJkjGWQ5bed41QqCydi71WBJQeU9A); `.makefun/owner.json` is present. The init root commit `133febd` (freshness) and LICENSE commit `c1a0bee` stay intact.
5. This build task explicitly forbids uploading/submitting and posting; therefore `POST.json` keeps the kit placeholder until the human posts the prepared text+image and fills in the real URL.

## Scoring / judge criteria

- `score = likes + reposts + quotes`, read by the house through FxTwitter's public read of the post ONCE after the final phase locks at the deadline. Highest score wins. Views and replies are ignored.
- Exact tie: earlier receipt, then lower entry id.
- Gate validity (all pass/fail, a fail scores 0 and ranks below every valid entry): POST.json names an X post of the required URL shape; the post is readable and still public; it was posted inside the window; it has its own uploaded image or video; its own text contains the whole-word mention `@_myronera` and one valid `makefun-<three words>` code; no earlier entry already named that post.
- The house writes its own `post.counts.json` after our program runs — nothing `main.ts` says about counts matters.
- No automatic judge reads the picture's content. make.fun admins may DISQUALIFY for: off-subject meme, media not made by the agent in the uploaded transcripts, bought/botted/coordinated engagement, more than one account per person, transcript fraud, or grader exploitation.
- Rewards: 15 paid places totalling $2 (1st $0.60, 2nd $0.42, 3rd $0.30, 4th $0.21, 5th $0.14, 6th $0.10, 7th $0.07, 8th $0.05, 9th $0.03, 10th–11th $0.02, 12th–15th $0.01). A reward exists only for a valid, non-disqualified entry that actually places and is claimed — nothing here is a reward until that happens.

## Hard caps / constraints

- Window: opens `2026-11-24T13:15:58Z`, entries deadline `2026-11-26T09:20:00Z`; final phase 4 hours after. Post and agent session must start at/after the opening.
- `submission_rule`: Force_Last, max 5 submissions/day, transcripts required, OSI license, repo created after opening. Final entry = last submission before the deadline.
- Sandbox (program/v1, node22): 1 CPU, 1024 MB, 64 pids, 60 s wall budget; NO network, wall clock or files outside the repository in `main.ts`; identical bytes on both runs. Env secrets: none.
- Transcript gate: ≥30% of counted lines authored in the sessions, ≥1 authored line in `main.ts`, ≥5 assistant turns with text/thinking, ≥2 assistant writes giving the entrypoint its final content, anchor line quoted in-session before the first counted write, harness/provider/model/effort declared, run record present.
- Post rules: mention as a whole word in the post's own text; code `makefun-` + exactly three words; image/video uploaded to the post; account public and post kept up until results; no paid/bot/pod engagement.

## Concrete plan to maximize the score

1. Creative (decided in-session, see the transcript): a single phone-first meme — "MY AGENT GOT PAID BEFORE ME" — the shared pain/in-joke of agent builders: the bot enters bounties, ships, tops the board and cashes out while the human "supervises". Four tiny pictograms carry the make.fun story (bot → bounty → leaderboard → payout) so it reads at 300 px. Text is short, correctly spelled, no digits to spell out and no currency glyph.
2. Render the image in-session with Pillow via `tools/render_image.py`, producing `entry.png`; validate PNG structure (signature, IHDR, chunk CRCs, IEND, ≤1 MiB, ≤1024×1024) and report bytes/dimensions/sha256. The making is in the transcript, as the admins require.
3. Prepare the post text with the mention and the REAL code `makefun-mesa-lettuce-popcorn` (see `POST_TEXT.md`). Post EARLY: the house reads engagement once at the deadline, so earlier posting gives the meme more organic time to collect likes/reposts/quotes. No bought or coordinated engagement.
4. Keep `main.ts` minimal, deterministic and stdlib-only; write it first, then rewrite the same file with a real robustness improvement so the transcript shows two distinct writes. Verify locally with `MAKEFUN_BOT_DIR`/`MAKEFUN_OUTPUT_DIR`.
5. After the human posts the prepared text + `entry.png`, replace the `POST.json` placeholder with the real post URL, bundle the transcripts, run `makefun check`, and submit as a source bundle with `--source` (NOT performed in this build task). Keep the post up and the account public through the results.

## Honest outcome condition

Nothing in this repository earns or is credited a reward by itself. A reward requires: real post in-window, valid entry, top-15 placement at the deadline read, no disqualification, and a claim. Until then the outcome is GAGAL (no reward credited), regardless of how polished the build is.
