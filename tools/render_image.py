#!/usr/bin/env python3
"""Draw the make.fun agent-bounty meme (entry.png) at build time.

Creative decided in the agent session: a phone-first single-panel meme,
"MY AGENT GOT PAID BEFORE ME" — the in-joke of agent builders whose bot
enters bounties, ships, tops the leaderboard and cashes out while the human
"supervises". Four simple pictograms tell the make.fun story at 300 px.
Deterministic: no clock, no network, no randomness.
"""
from pathlib import Path
import hashlib
import struct
import zlib

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample, then downscale for clean edges
W = H = 1024 * S
OUT = Path(__file__).resolve().parents[1] / "entry.png"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

BG = (11, 16, 32, 255)
WHITE = (245, 248, 252, 255)
GREEN = (124, 255, 107, 255)
PINK = (255, 92, 138, 255)
MUTED = (169, 180, 194, 255)


def px(v):
    return int(v * S)


def font(path, size):
    return ImageFont.truetype(path, px(size))


def center(draw, y, text, fnt, fill):
    draw.text((W // 2, px(y)), text, font=fnt, fill=fill, anchor="mm")


def robot(draw, cx, cy):
    x, y = px(cx), px(cy)
    draw.rounded_rectangle((x - px(46), y - px(34), x + px(46), y + px(40)),
                           radius=px(14), fill=GREEN, outline=WHITE, width=px(4))
    draw.rectangle((x - px(26), y - px(10), x + px(26), y + px(10)), fill=BG)
    draw.ellipse((x - px(19), y - px(6), x - px(7), y + px(6)), fill=WHITE)
    draw.ellipse((x + px(7), y - px(6), x + px(19), y + px(6)), fill=WHITE)
    draw.line((x, y - px(34), x, y - px(52)), fill=WHITE, width=px(5))
    draw.ellipse((x - px(8), y - px(62), x + px(8), y - px(46)), fill=PINK)


def bounty(draw, cx, cy):
    x, y = px(cx), px(cy)
    for r in (52, 34, 16):
        draw.ellipse((x - px(r), y - px(r), x + px(r), y + px(r)),
                     outline=PINK if r == 52 else GREEN, width=px(6))
    draw.ellipse((x - px(6), y - px(6), x + px(6), y + px(6)), fill=WHITE)


def board(draw, cx, cy):
    x, y = px(cx), px(cy)
    draw.rounded_rectangle((x - px(34), y - px(46), x + px(34), y + px(18)),
                           radius=px(8), fill=GREEN, outline=WHITE, width=px(4))
    draw.arc((x + px(22), y - px(36), x + px(62), y + px(4)),
             -90, 90, fill=WHITE, width=px(6))
    draw.arc((x - px(62), y - px(36), x - px(22), y + px(4)),
             90, 270, fill=WHITE, width=px(6))
    draw.rectangle((x - px(10), y + px(18), x + px(10), y + px(44)), fill=WHITE)
    draw.rounded_rectangle((x - px(36), y + px(44), x + px(36), y + px(56)),
                           radius=px(6), fill=WHITE)


def paid(draw, cx, cy):
    x, y = px(cx), px(cy)
    draw.rounded_rectangle((x - px(60), y - px(36), x + px(60), y + px(36)),
                           radius=px(10), fill=GREEN, outline=WHITE, width=px(4))
    draw.text((x, y), "$", font=font(BOLD, 52), fill=BG, anchor="mm")


def main():
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((px(24), px(24), W - px(24), H - px(24)),
                        radius=px(28), outline=GREEN, width=px(5))

    center(d, 92, "MAKE.FUN  /  AGENT BOUNTY", font(BOLD, 34), MUTED)
    center(d, 190, "MY AGENT", font(BOLD, 108), WHITE)
    center(d, 312, "GOT PAID", font(BOLD, 128), GREEN)
    center(d, 434, "BEFORE ME", font(BOLD, 108), WHITE)
    center(d, 532, "ENTERED. BUILT. TOPPED. PAID.", font(BOLD, 42), PINK)

    xs = (170, 390, 610, 830)
    robot(d, xs[0], 690)
    bounty(d, xs[1], 690)
    board(d, xs[2], 690)
    paid(d, xs[3], 690)
    labels = ("AGENT", "BOUNTY", "BOARD", "PAID")
    for x, label in zip(xs, labels):
        d.text((px(x), px(790)), label, font=font(BOLD, 34),
               fill=WHITE, anchor="mm")

    center(d, 900, "you were \"supervising\".", font(REG, 40), MUTED)

    img.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS).save(
        OUT, format="PNG", optimize=True)

    # Validate the PNG the same way a strict checker would.
    data = OUT.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "bad PNG signature"
    pos, chunks, ihdr, saw_iend = 8, [], None, False
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        assert crc == zlib.crc32(kind + payload) & 0xFFFFFFFF, f"bad CRC in {kind!r}"
        chunks.append(kind.decode("ascii", "replace"))
        if kind == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", payload)
        if kind == b"IEND":
            saw_iend = True
        pos += 12 + length
    assert saw_iend and pos == len(data), "missing IEND / trailing bytes"
    assert ihdr is not None, "missing IHDR"
    w, h = ihdr[0], ihdr[1]
    assert w <= 1024 and h <= 1024, "dimensions over cap"
    assert len(data) <= 1024 * 1024, "file over cap"
    print(f"PNG valid: {len(data)} bytes, {w}x{h}, "
          f"sha256 {hashlib.sha256(data).hexdigest()}, chunks={','.join(chunks)}")


if __name__ == "__main__":
    main()
