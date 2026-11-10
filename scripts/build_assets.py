#!/usr/bin/env python3
"""Generate the README's SVG panels in light (assets/) and dark (assets/dark/) themes.

Edit the DATA section, then run:  python3 scripts/build_assets.py
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W = 900
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CH = 0.6  # approx monospace glyph width as a fraction of font-size

THEMES = {
    "light": dict(fg="#0d1117", muted="#57606a", line="#d0d7de", soft="#f6f8fa"),
    "dark": dict(fg="#f0f6fc", muted="#8b949e", line="#30363d", soft="#161b22"),
}

# ----------------------------------------------------------------- DATA
NAME = "PAUL KAIZIREGE VEDASTO"
ROLE = "Full-Stack Developer · Information Security Graduate"
WHERE = "Dar-es-Salaam, Tanzania 🇹🇿  ·  he/him  ·  aka Kai"

WHOAMI = [
    ("role", ["Full-Stack Developer · Information Security Graduate"]),
    ("education", ["Bachelor's, Information Security — Unique Academy (2026)",
                   "Full-Stack Web Development — Microverse (2023)",
                   "Diploma, Electronics & Telecom — DIT (2020)"]),
    ("recent", ["Operations Lead — Mtabe Innovations / Kinara Technologies"]),
    ("focus", ["Secure web apps · PII protection · AI integration"]),
    ("mentoring", ["10+ developers mentored at Microverse"]),
    ("interests", ["Movies, Tech News, Football, Comics, Pop Culture, Anime"]),
]

PROJECTS = [
    ("End-to-End Encryption Framework", "Django · SQL · AES-256-GCM", "2026",
     "Keeps users' personal data (PII) unreadable even if the database is breached. Final-year Information Security project."),
    ("Mtabe Web & Mobile Platform", "Django · Flutter · REST API · Next.js", "2024",
     "Cross-team learning platform with analytics and real-time engagement dashboards."),
    ("Buzz Teenz Voting Platform", "Next.js · Supabase · Strapi · Vercel", "2024",
     "Content delivery and real-time voting with Supabase authentication."),
    ("Weather Report App", "React · Redux · REST API · Netlify", "2023",
     "Forecasts from open weather APIs with Redux state management."),
    ("Rent-a-Car Platform", "React · Ruby on Rails · Redux", "2023",
     "Car reservations with auth, booking forms and availability checks."),
]

TIMELINE = [  # (year, label)
    (2016, "DIT diploma"), (2017, "IT support"), (2020, "Diploma done"),
    (2022, "Microverse"), (2023, "Freelance + BSc"), (2024, "Ops Lead"),
    (2026, "BSc InfoSec 🎓"),
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

STACK = [
    ("SECURITY", ["Ethical Hacking", "Network Security", "AES-256-GCM", "PII Protection", "Secure Auth"]),
    ("LANGUAGES", ["JavaScript", "Python", "Ruby", "SQL", "C/C++", "HTML", "CSS"]),
    ("FRAMEWORKS", ["React", "Next.js", "Django", "Ruby on Rails", "Flutter", "Redux", "Tailwind", "Bootstrap"]),
    ("DATA & CMS", ["PostgreSQL", "Supabase", "Strapi"]),
    ("TOOLS", ["Git", "Docker", "Jest", "RSpec", "VS Code"]),
    ("DEPLOY", ["Vercel", "Netlify", "Render", "Heroku"]),
]

STATUS = "open to security engineering & full-stack roles"

SECTIONS = ["whoami", "security focus", "projects", "telemetry", "the route", "stack"]

# ----------------------------------------------------------------- HELPERS
def t(x, y, s, size=14, fill="fg", weight="400", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{{{fill}}}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def wrap(s, size, width):
    limit = int(width / (size * CH))
    lines, cur = [], ""
    for word in s.split():
        if len(cur) + len(word) + (1 if cur else 0) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return lines + [cur] if cur else lines


def svg(h, body, alt):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{escape(alt)}" '
            f'font-family="{FONT}"><title>{escape(alt)}</title>{body}</svg>')


# ----------------------------------------------------------------- PANELS
def header():
    blink = '<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>'
    name_w = len(NAME) * 38 * CH + (len(NAME) - 1) * 2
    x0 = (W - name_w) / 2
    body = [
        t(W / 2, 34, "~/kaizipaul $ cat profile.md", 13, "muted", anchor="middle"),
        f'<text x="{x0}" y="92" font-size="38" font-weight="700" fill="{{fg}}" letter-spacing="2">{NAME}</text>',
        f'<rect x="{x0 + name_w + 8}" y="62" width="18" height="34" fill="{{fg}}">{blink}</rect>',
        t(W / 2, 128, ROLE, 16, anchor="middle"),
        t(W / 2, 154, WHERE, 13, "muted", anchor="middle"),
        f'<line x1="40" y1="180" x2="{W - 40}" y2="180" stroke="{{line}}"/>',
    ]
    return svg(192, "".join(body), f"{NAME} — {ROLE}")


def section(n, label):
    num = f"{n:02d}"
    x = 10 + len(f"{num} — {label}") * 15 * CH + 16
    body = (t(10, 30, num, 15, weight="700") + t(10 + 3 * 15 * CH, 30, f"— {label}", 15, "muted")
            + f'<line x1="{x}" y1="25" x2="{W - 10}" y2="25" stroke="{{line}}"/>')
    return svg(44, body, f"{num} — {label}")


def whoami():
    rows = sum(len(v) for _, v in WHOAMI)
    h = 60 + rows * 26 + 20
    body = [f'<rect x="10" y="6" width="{W - 20}" height="{h - 12}" rx="6" fill="none" stroke="{{line}}"/>',
            f'<line x1="10" y1="40" x2="{W - 10}" y2="40" stroke="{{line}}"/>']
    for i in range(3):
        body.append(f'<circle cx="{30 + i * 16}" cy="23" r="5" fill="none" stroke="{{muted}}"/>')
    body.append(t(W / 2, 28, "kai@dar-es-salaam: ~ — whoami", 12, "muted", anchor="middle"))
    y = 72
    for key, vals in WHOAMI:
        body.append(t(34, y, key, 14, "muted"))
        for v in vals:
            body.append(t(180, y, v, 14))
            y += 26
    return svg(h, "".join(body), "About Paul: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in WHOAMI))


def security():
    steps = [("USER", "submits PII"), ("DJANGO", "app layer"), ("AES-256-GCM", "encrypt fields"),
             ("DATABASE", "ciphertext only")]
    bw, gap, y = 180, 44, 30
    x0 = (W - (4 * bw + 3 * gap)) / 2
    body = []
    for i, (a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        strong = a == "AES-256-GCM"
        body.append(f'<rect x="{x}" y="{y}" width="{bw}" height="64" rx="4" '
                    f'fill="{{{"fg" if strong else "soft"}}}" stroke="{{fg}}"/>')
        body.append(t(x + bw / 2, y + 28, a, 14, "soft" if strong else "fg", "700", "middle"))
        body.append(t(x + bw / 2, y + 48, b, 12, "soft" if strong else "muted", anchor="middle"))
        if i < 3:
            ax = x + bw
            body.append(f'<line x1="{ax + 6}" y1="{y + 32}" x2="{ax + gap - 8}" y2="{y + 32}" stroke="{{fg}}" '
                        f'stroke-dasharray="4 3"><animate attributeName="stroke-dashoffset" values="14;0" '
                        f'dur="1s" repeatCount="indefinite"/></line>')
            body.append(f'<path d="M{ax + gap - 10} {y + 27} L{ax + gap - 4} {y + 32} L{ax + gap - 10} {y + 37}" '
                        f'fill="none" stroke="{{fg}}"/>')
    db_x = x0 + 3 * (bw + gap) + bw / 2
    body.append(f'<line x1="{db_x}" y1="{y + 64}" x2="{db_x}" y2="{y + 100}" stroke="{{muted}}" stroke-dasharray="3 3"/>')
    body.append(t(x0 + 4 * bw + 3 * gap, y + 118, "breach? attacker reads 9f3a…c71e", 12, "muted", anchor="end"))
    body.append(t(x0, y + 118, "// End-to-End Encryption Framework — final-year project", 12, "muted"))
    body.append(t(x0, y + 150, "Ethical hacking · Network security · Secure auth · PII protection", 13))
    return svg(200, "".join(body), "Security focus: user PII flows through Django, is encrypted with AES-256-GCM, "
               "and only ciphertext is stored, so a database breach exposes nothing readable.")


def projects():
    pad, gap = 18, 20
    half = (W - 20 - gap) / 2

    def card(x, y, width, h, proj):
        name, stack, year, desc = proj
        out = [f'<rect x="{x}" y="{y}" width="{width}" height="{h}" rx="6" fill="none" stroke="{{line}}"/>',
               t(x + pad, y + 30, name, 15, weight="700"),
               t(x + width - pad, y + 30, year, 12, "muted", anchor="end"),
               t(x + pad, y + 52, stack, 12, "muted")]
        out += [t(x + pad, y + 80 + j * 19, ln, 13) for j, ln in enumerate(wrap(desc, 13, width - 2 * pad))]
        return out

    height = lambda proj, width: 86 + len(wrap(proj[3], 13, width - 2 * pad)) * 19
    # first project spans the full width, the rest sit two per row
    body, y = card(10, 6, W - 20, height(PROJECTS[0], W - 20), PROJECTS[0]), 6 + height(PROJECTS[0], W - 20) + gap
    rest = PROJECTS[1:]
    for i in range(0, len(rest), 2):
        row = rest[i:i + 2]
        h = max(height(p, half) for p in row)
        for j, proj in enumerate(row):
            body += card(10 + j * (half + gap), y, half, h, proj)
        y += h + gap
    return svg(int(y - gap + 8), "".join(body), f"{len(PROJECTS)} projects: " + ", ".join(p[0] for p in PROJECTS))


def timeline():
    y0, x1, x2 = 70, 90, W - 90
    lo, hi = TIMELINE[0][0], TIMELINE[-1][0]
    pos = lambda yr: x1 + (yr - lo) / (hi - lo) * (x2 - x1)
    body = [f'<line x1="{x1}" y1="{y0}" x2="{x2}" y2="{y0}" stroke="{{fg}}"/>']
    for i, (yr, label) in enumerate(TIMELINE):
        x = pos(yr)
        up = i % 2 == 0
        last = i == len(TIMELINE) - 1
        body.append(f'<circle cx="{x}" cy="{y0}" r="{6 if last else 4}" fill="{{{"fg" if last else "soft"}}}" stroke="{{fg}}"/>')
        body.append(t(x, y0 + (-16 if up else 26), str(yr), 12, "muted", anchor="middle"))
        body.append(t(x, y0 + (-32 if up else 44), label, 12, weight="700" if last else "400", anchor="middle"))
    return svg(130, "".join(body), "Timeline: " + "; ".join(f"{y} {l}" for y, l in TIMELINE))


def experience():
    body, y = [], 10
    for role, org, dates, note in EXPERIENCE:
        body.append(f'<line x1="22" y1="{y}" x2="22" y2="{y + 74}" stroke="{{line}}"/>')
        body.append(f'<circle cx="22" cy="{y + 18}" r="5" fill="{{fg}}"/>')
        body.append(t(44, y + 23, role, 15, weight="700"))
        body.append(t(W - 14, y + 23, dates, 12, "muted", anchor="end"))
        body.append(t(44, y + 44, org, 13, "muted"))
        body.append(t(44, y + 64, note, 13))
        y += 82
    return svg(y + 4, "".join(body), "Experience: " + "; ".join(f"{r}, {o}, {d}" for r, o, d, _ in EXPERIENCE))


def stack():
    body, y = [], 10
    for label, items in STACK:
        body.append(t(10, y + 21, label, 12, "muted", "700"))
        x = 150
        for it in items:
            w = len(it) * 13 * CH + 22
            if x + w > W - 10:
                x, y = 150, y + 38
            strong = label == "SECURITY"
            body.append(f'<rect x="{x}" y="{y + 4}" width="{w}" height="26" rx="13" '
                        f'fill="{"{fg}" if strong else "none"}" stroke="{{fg}}"/>')
            body.append(t(x + w / 2, y + 22, it, 13, "soft" if strong else "fg", anchor="middle"))
            x += w + 8
        y += 44
    return svg(y + 4, "".join(body), "Stack: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in STACK))


def footer():
    pulse = '<animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>'
    body = (f'<line x1="40" y1="8" x2="{W - 40}" y2="8" stroke="{{line}}"/>'
            f'<circle cx="{W / 2 - len("STATUS: " + STATUS) * 13 * CH / 2 - 14}" cy="45" r="5" fill="{{fg}}">{pulse}</circle>'
            + t(W / 2, 50, f"STATUS: {STATUS}", 13, anchor="middle")
            + t(W / 2, 76, "thanks for stopping by · kwaheri 👋", 12, "muted", anchor="middle"))
    return svg(92, body, f"Current status: {STATUS}")


def main():
    panels = {"header": header(), "whoami": whoami(), "security": security(), "projects": projects(),
              "timeline": timeline(), "experience": experience(), "stack": stack(), "footer": footer()}
    for i, label in enumerate(SECTIONS, 1):
        panels[f"s{i:02d}"] = section(i, label)
    for theme, colors in THEMES.items():
        out = ROOT / "assets" / ("dark" if theme == "dark" else "")
        out.mkdir(parents=True, exist_ok=True)
        for name, content in panels.items():
            (out / f"{name}.svg").write_text(_fill(content, colors), encoding="utf-8")
    print(f"wrote {len(panels)} panels x {len(THEMES)} themes")


def _fill(s, colors):
    for k, v in colors.items():
        s = s.replace("{" + k + "}", v)
    return s


if __name__ == "__main__":
    main()
