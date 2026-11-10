#!/usr/bin/env python3
"""Generate the README's SVG panels in light (assets/) and dark (assets/dark/) themes.

The palette and visual language match the portfolio: pure black, rose accent,
gray tag chips, file-tab section labels and coloured status dots.

Edit the DATA section, then run:  python3 scripts/build_assets.py
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W = 900
FONT = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CH = 0.6  # approx monospace glyph width as a fraction of font-size

# Portfolio palette (Tailwind): black, gray-100/400/600, rose-500, amber-500, emerald-500.
# Light mode uses the darker 600/700 shades so text keeps its contrast on white.
THEMES = {
    "dark": dict(fg="#f3f4f6", muted="#9ca3af", line="#4b5563", panel="#000000",
                 accent="#f43f5e", amber="#f59e0b", green="#10b981"),
    "light": dict(fg="#111827", muted="#4b5563", line="#d1d5db", panel="#ffffff",
                  accent="#e11d48", amber="#b45309", green="#047857"),
}

# ----------------------------------------------------------------- DATA
NAME = "PAUL KAIZIREGE VEDASTO"
ROLE = "FULL-STACK DEVELOPER · INFORMATION SECURITY GRADUATE"
WHERE = "Dar-es-Salaam, Tanzania"
TAGLINE = "Tech Guy. Software Builder. Currently Freelancing."

ABOUT = [  # rendered as about.ts
    ("role", "Full-Stack Developer · InfoSec Graduate"),
    ("education", ["Bachelor's, Information Security — Unique Academy (2026)",
                   "Full-Stack Web Development — Microverse (2023)",
                   "Diploma, Electronics & Telecom — DIT (2020)"]),
    ("recent", "Operations Lead — Mtabe Innovations / Kinara Technologies"),
    ("focus", ["Secure web apps", "PII protection", "AI integration"]),
    ("mentored", "10+ developers at Microverse"),
    ("interests", ["Movies", "Tech News", "Football", "Comics", "Anime"]),
]

# status: research | in dev | live | None (shows the year instead)
PROJECTS = [
    ("pii-encryption-framework", "research", "2026",
     "Information Security capstone — keeps users' personal data (PII) unreadable even if the database is breached, using end-to-end AES-256-GCM encryption.",
     ["Python", "Django", "Cryptography", "Security", "Research"]),
    ("srms-shuleis", "in dev", "2025",
     "Multi-tenant SaaS for managing student records across schools — multiple schools manage their student data in isolated tenants from a single deployment.",
     ["Django", "Next.js", "Multi-tenant"]),
    ("portfolio-v3.0", "live", "2026",
     "Minimal developer portfolio built with Astro and TailwindCSS. Features a VS Code-inspired tab interface, animated terminal, and dark/light mode toggle.",
     ["Astro", "TypeScript", "TailwindCSS"]),
    ("mtabe-platform", None, "2024",
     "Cross-team web & mobile learning platform with analytics and real-time engagement dashboards.",
     ["Django", "Flutter", "REST API", "Next.js"]),
    ("buzz-teenz-voting", None, "2024",
     "Content delivery and real-time voting with Supabase authentication.",
     ["Next.js", "Supabase", "Strapi", "Vercel"]),
]

TIMELINE = [  # (year, label)
    (2016, "DIT diploma"), (2017, "IT support"), (2020, "Diploma done"),
    (2022, "Microverse"), (2023, "Freelance + BSc"), (2024, "Ops Lead"),
    (2026, "BSc InfoSec"),
]

EXPERIENCE = [
    ("Operations Lead", "Mtabe Innovations / Kinara Technologies", "2024 – 2025",
     "Led AI feature development; turned operational data into platform improvements."),
    ("Full-Stack Developer (Contract)", "Freelance · Remote", "2023 – 2024",
     "Built React, Next.js, Strapi and Supabase apps for 2 clients."),
    ("Mentor (Volunteer)", "Microverse · Remote", "2022 – 2023",
     "Mentored 10+ students; ran weekly pair-programming sessions."),
    ("IT Support Technician", "Computer Center Tanzania Ltd", "2017 – 2019",
     "Supported 250+ users a month across 10+ client offices."),
]

STACK = [  # the first group is highlighted in the accent colour
    ("security", ["Ethical Hacking", "Network Security", "AES-256-GCM", "PII Protection", "Secure Auth"]),
    ("languages", ["JavaScript", "TypeScript", "Python", "Ruby", "SQL", "C/C++", "HTML", "CSS"]),
    ("frameworks", ["React", "Next.js", "Astro", "Django", "Ruby on Rails", "Flutter", "Redux", "TailwindCSS"]),
    ("data", ["PostgreSQL", "Supabase", "Strapi"]),
    ("tools", ["Git", "Docker", "Jest", "RSpec", "VS Code"]),
    ("deploy", ["Vercel", "Netlify", "Render", "Heroku"]),
]

CONNECT = [  # (icon label, value)
    ("github", "github.com/kaizipaul"),
    ("linkedin", "linkedin.com/in/kaizipaul"),
    ("email", "paulkaizirege@gmail.com"),
]

SECTIONS = {  # file: (LABEL, tab name)
    "s01": ("ABOUT", "about.ts"),
    "s02": ("SECURITY", "threat-model.md"),
    "s03": ("PINNED", "projects.md"),
    "s04": ("TELEMETRY", "github.stats"),
    "s05": ("EXPERIENCE", "experience.md"),
    "s06": ("SKILLS", "skills.json"),
}

# ----------------------------------------------------------------- HELPERS
def t(x, y, s, size=14, fill="fg", weight="400", anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{{{fill}}}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def tw(s, size):
    return len(s) * size * CH


def wrap(s, size, width):
    limit = int(width / (size * CH))
    lines, cur = [], ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return lines + [cur] if cur else lines


def box(x, y, w, h, rx=8, stroke="line", fill="panel", extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{{{fill}}}" stroke="{{{stroke}}}" {extra}/>')


def doc_icon(x, y, color="accent"):
    """Small file glyph, like the portfolio's tab and project icons."""
    return (f'<path d="M{x} {y} h7 l4 4 v10 h-11 z M{x + 7} {y} v4 h4" fill="none" '
            f'stroke="{{{color}}}" stroke-width="1.2" stroke-linejoin="round"/>')


def chip(x, y, label, size=12, active=False):
    w = tw(label, size) + 18
    c = "accent" if active else "line"
    return w, (box(x, y, w, 24, rx=3, stroke=c) + t(x + w / 2, y + 16.5, label, size,
                                                    "accent" if active else "muted", anchor="middle"))


def chips(x, y, labels, max_x, size=12, active=False, gap=7):
    out, x0 = [], x
    for lb in labels:
        w = tw(lb, size) + 18
        if x + w > max_x:
            x, y = x0, y + 32
        _, s = chip(x, y, lb, size, active)
        out.append(s)
        x += w + gap
    return "".join(out), y + 24


STATUS = {"research": "accent", "in dev": "amber", "live": "green"}


def status_tag(right, y, status):
    """Right-aligned status label with a drawn icon (font glyphs like ◐ render inconsistently)."""
    c = STATUS[status]
    cx, cy = right - tw(status, 12) - 10, y - 4
    if status == "research":
        icon = f'<rect x="{cx - 3.5:.1f}" y="{cy - 3.5:.1f}" width="7" height="7" fill="{{{c}}}" transform="rotate(45 {cx:.1f} {cy:.1f})"/>'
    elif status == "in dev":
        icon = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="none" stroke="{{{c}}}" stroke-width="1.4"/>'
                f'<path d="M{cx:.1f} {cy - 4.5:.1f} a4.5 4.5 0 0 0 0 9 z" fill="{{{c}}}"/>')
    else:
        icon = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{{{c}}}"/>'
    return icon + t(right, y, status, 12, c, anchor="end")


def svg(h, body, alt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" '
            f'viewBox="0 0 {W} {h:.0f}" role="img" aria-label="{escape(alt)}" '
            f'font-family="{FONT}"><title>{escape(alt)}</title>{body}</svg>')


BLINK = '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>'

# ----------------------------------------------------------------- PANELS
def avatar_uri():
    """Embed the avatar as a data URI: GitHub won't load external images inside an SVG."""
    import base64
    return "data:image/jpeg;base64," + base64.b64encode((ROOT / "assets" / "avatar.jpg").read_bytes()).decode()


def header():
    # avatar in an accent frame, like the portfolio's profile card
    body = [box(10, 10, 132, 132, rx=12, stroke="accent", fill="panel", extra='stroke-width="2"'),
            '<clipPath id="av"><rect x="12" y="12" width="128" height="128" rx="10"/></clipPath>',
            f'<image x="12" y="12" width="128" height="128" clip-path="url(#av)" href="{avatar_uri()}"/>',
            t(170, 50, NAME, 30, "fg", "700", extra='letter-spacing="1"'),
            f'<rect x="{170 + tw(NAME, 30) + len(NAME) + 6:.1f}" y="26" width="14" height="28" fill="{{accent}}">{BLINK}</rect>',
            t(170, 80, ROLE, 14, "accent", extra='letter-spacing="0.5"'),
            # map pin
            f'<path d="M176 98 a6 6 0 0 1 12 0 c0 5 -6 11 -6 11 s-6 -6 -6 -11 z" fill="none" stroke="{{muted}}" stroke-width="1.3"/>'
            f'<circle cx="182" cy="98" r="2" fill="none" stroke="{{muted}}" stroke-width="1.2"/>',
            t(198, 108, WHERE, 14, "muted"),
            t(170, 134, TAGLINE, 14, "fg")]
    return svg(152, "".join(body), f"{NAME} — {ROLE.title()} — {WHERE}")


def section(key):
    label, tab = SECTIONS[key]
    star = label == "PINNED"
    x = 12
    body = [t(x, 27, "★" if star else "›", 13, "muted")]
    x += 18
    body.append(t(x, 27, label, 12, "muted", "700", extra='letter-spacing="1.5"'))
    x += tw(label, 12) + len(label) * 1.5 + 8
    body.append(t(x, 27, "—", 12, "muted"))
    x += 18
    body.append(t(x, 27, tab, 12, "accent"))
    x += tw(tab, 12) + 14
    body.append(f'<line x1="{x:.1f}" y1="22.5" x2="{W - 10}" y2="22.5" stroke="{{line}}"/>')
    return svg(40, "".join(body), f"{label} — {tab}")


def about():
    """Editor window with an about.ts tab, like the portfolio's tab bar."""
    lines = [[("const ", "accent"), ("kai", "fg"), (" = {", "muted")]]
    for key, val in ABOUT:
        vals = val if isinstance(val, list) else [val]
        if isinstance(val, list) and len(", ".join(f'"{v}"' for v in vals)) < 60:
            lines.append([("  " + key, "fg"), (": [", "muted")]
                         + sum([[(f'"{v}"', "muted"), (", " if i < len(vals) - 1 else "", "muted")]
                                for i, v in enumerate(vals)], []) + [("],", "muted")])
        elif isinstance(val, list):
            lines.append([("  " + key, "fg"), (": [", "muted")])
            lines += [[(f'    "{v}"', "muted"), (",", "muted")] for v in vals]
            lines.append([("  ],", "muted")])
        else:
            lines.append([("  " + key, "fg"), (": ", "muted"), (f'"{val}"', "muted"), (",", "muted")])
    lines.append([("};", "muted")])
    lines.append([("export default ", "accent"), ("kai", "fg"), (";", "muted")])

    lh, top = 22, 62
    h = top + len(lines) * lh + 16
    tab_w = 110
    body = [box(10, 6, W - 20, h - 12, rx=6),
            f'<line x1="10" y1="40" x2="{W - 10}" y2="40" stroke="{{line}}"/>',
            f'<line x1="{10 + tab_w}" y1="6" x2="{10 + tab_w}" y2="40" stroke="{{line}}"/>',
            f'<line x1="11" y1="39" x2="{10 + tab_w}" y2="39" stroke="{{accent}}" stroke-width="2"/>',
            doc_icon(24, 16, "fg"), t(44, 28, "about.ts", 12, "fg")]
    for i, segs in enumerate(lines):
        y = top + i * lh
        body.append(t(30, y, str(i + 1), 12, "line", anchor="end"))
        x = 50
        for s, c in segs:
            if s:
                body.append(t(x, y, s, 13, c, extra='xml:space="preserve"'))
                x += tw(s, 13)
    alt = "About Paul: " + "; ".join(f"{k}: {v if isinstance(v, str) else ', '.join(v)}" for k, v in ABOUT)
    return svg(h, "".join(body), alt)


def security():
    steps = [("USER", "submits PII"), ("DJANGO", "app layer"), ("AES-256-GCM", "encrypt fields"),
             ("DATABASE", "ciphertext only")]
    bw, gap, y = 180, 44, 16
    x0 = (W - (4 * bw + 3 * gap)) / 2
    body = []
    for i, (a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        hot = a == "AES-256-GCM"
        body.append(box(x, y, bw, 64, rx=6, stroke="accent" if hot else "line"))
        body.append(t(x + bw / 2, y + 28, a, 14, "accent" if hot else "fg", "700", "middle"))
        body.append(t(x + bw / 2, y + 48, b, 12, "muted", anchor="middle"))
        if i < 3:
            ax = x + bw
            body.append(f'<line x1="{ax + 6:.1f}" y1="{y + 32}" x2="{ax + gap - 8:.1f}" y2="{y + 32}" '
                        f'stroke="{{accent}}" stroke-dasharray="4 3"><animate attributeName="stroke-dashoffset" '
                        f'values="14;0" dur="1s" repeatCount="indefinite"/></line>')
            body.append(f'<path d="M{ax + gap - 10:.1f} {y + 27} L{ax + gap - 4:.1f} {y + 32} '
                        f'L{ax + gap - 10:.1f} {y + 37}" fill="none" stroke="{{accent}}"/>')
    right = x0 + 4 * bw + 3 * gap
    db_x = right - bw / 2
    body.append(f'<line x1="{db_x:.1f}" y1="{y + 64}" x2="{db_x:.1f}" y2="{y + 92}" stroke="{{line}}" stroke-dasharray="3 3"/>')
    body.append(t(right, y + 110, "breach? attacker reads 9f3a…c71e", 12, "muted", anchor="end"))
    body.append(t(x0, y + 110, "// pii-encryption-framework — capstone research", 12, "muted"))
    s, _ = chips(x0, y + 128, ["Ethical Hacking", "Network Security", "Secure Auth", "PII Protection"], right, active=True)
    body.append(s)
    return svg(y + 164, "".join(body), "Security focus: user PII flows through Django, is encrypted with AES-256-GCM, "
               "and only ciphertext is stored, so a database breach exposes nothing readable.")


def projects():
    """Pinned-repo list, styled like the portfolio's projects.md tab."""
    body, y = [], 6
    for name, status, year, desc, tags in PROJECTS:
        lines = wrap(desc, 13, W - 60)
        h = 40 + len(lines) * 20 + 40
        body.append(f'<line x1="14" y1="{y:.1f}" x2="14" y2="{y + h - 8:.1f}" stroke="{{line}}" stroke-width="2"/>')
        body.append(doc_icon(28, y + 6))
        body.append(t(48, y + 18, name, 15, "fg", "600"))
        if status:
            body.append(status_tag(W - 12, y + 18, status))
        else:
            body.append(t(W - 12, y + 18, year, 12, "muted", anchor="end"))
        for j, ln in enumerate(lines):
            body.append(t(28, y + 44 + j * 20, ln, 13, "muted"))
        s, end = chips(28, y + 44 + len(lines) * 20 - 6, tags, W - 12, size=11)
        body.append(s)
        y = end + 22
    return svg(y - 8, "".join(body), f"{len(PROJECTS)} projects: " + ", ".join(p[0] for p in PROJECTS))


def timeline():
    y0, x1, x2 = 58, 90, W - 90
    lo, hi = TIMELINE[0][0], TIMELINE[-1][0]
    pos = lambda yr: x1 + (yr - lo) / (hi - lo) * (x2 - x1)
    body = [f'<line x1="{x1}" y1="{y0}" x2="{x2}" y2="{y0}" stroke="{{line}}" stroke-width="2"/>']
    for i, (yr, label) in enumerate(TIMELINE):
        x = pos(yr)
        up, last = i % 2 == 0, i == len(TIMELINE) - 1
        body.append(f'<circle cx="{x:.1f}" cy="{y0}" r="{6 if last else 4}" fill="{{{"accent" if last else "panel"}}}" '
                    f'stroke="{{{"accent" if last else "muted"}}}" stroke-width="1.5"/>')
        body.append(t(x, y0 + (-14 if up else 24), str(yr), 12, "accent" if last else "muted", anchor="middle"))
        body.append(t(x, y0 + (-30 if up else 40), label, 12, "accent" if last else "fg",
                      "700" if last else "400", "middle"))
    return svg(112, "".join(body), "Timeline: " + "; ".join(f"{y} {l}" for y, l in TIMELINE))


def experience():
    body, y = [], 8
    for i, (role, org, dates, note) in enumerate(EXPERIENCE):
        if i < len(EXPERIENCE) - 1:
            body.append(f'<line x1="22" y1="{y + 24}" x2="22" y2="{y + 82}" stroke="{{line}}"/>')
        body.append(f'<circle cx="22" cy="{y + 17}" r="5" fill="{{{"accent" if i == 0 else "panel"}}}" '
                    f'stroke="{{accent}}" stroke-width="1.5"/>')
        body.append(t(44, y + 22, role, 15, "fg", "600"))
        body.append(t(W - 12, y + 22, dates, 12, "muted", anchor="end"))
        body.append(t(44, y + 43, org, 13, "fg"))
        body.append(t(44, y + 63, note, 13, "muted"))
        y += 82
    return svg(y, "".join(body), "Experience: " + "; ".join(f"{r}, {o}, {d}" for r, o, d, _ in EXPERIENCE))


def stack():
    """skills.json — keys on the left, tag chips on the right."""
    body, y = [t(12, 22, "{", 13, "muted")], 34
    for i, (key, items) in enumerate(STACK):
        body.append(t(28, y + 17, f'"{key}"', 13, "accent" if i == 0 else "fg"))
        body.append(t(28 + tw(f'"{key}"', 13), y + 17, ":", 13, "muted"))
        s, end = chips(170, y, items, W - 12, size=12, active=i == 0)
        body.append(s)
        y = end + 12
    body.append(t(12, y + 12, "}", 13, "muted"))
    return svg(y + 22, "".join(body), "Skills: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in STACK))


def footer():
    """The portfolio's `npx connect` terminal card."""
    h = 108 + len(CONNECT) * 22 + 40
    body = [box(10, 6, W - 20, h - 12, rx=6),
            t(32, 38, "$", 13, "accent"), t(48, 38, "npx connect", 13, "fg"),
            t(32, 62, "✓ Initializing...", 13, "muted"),
            t(32, 82, "Ready to connect.", 13, "muted")]
    y = 108
    for label, val in CONNECT:
        body += [t(32, y, "→", 13, "accent"), t(56, y, label, 13, "fg"), t(160, y, val, 13, "muted")]
        y += 22
    up = "Uptime: 99.9%"
    body += [t(32, y + 14, up, 13, "fg"),
             f'<rect x="{32 + tw(up, 13) + 4:.1f}" y="{y + 1}" width="8" height="16" fill="{{accent}}">{BLINK}</rect>']
    return svg(h, "".join(body), "Connect: " + ", ".join(f"{l} {v}" for l, v in CONNECT))


def main():
    panels = {"header": header(), "whoami": about(), "security": security(), "projects": projects(),
              "timeline": timeline(), "experience": experience(), "stack": stack(), "footer": footer()}
    for key in SECTIONS:
        panels[key] = section(key)
    for theme, colors in THEMES.items():
        out = ROOT / "assets" / ("dark" if theme == "dark" else "")
        out.mkdir(parents=True, exist_ok=True)
        for name, content in panels.items():
            for k, v in colors.items():
                content = content.replace("{" + k + "}", v)
            (out / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(panels)} panels x {len(THEMES)} themes")


if __name__ == "__main__":
    main()
