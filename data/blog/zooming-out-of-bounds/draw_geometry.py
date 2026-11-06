"""Draw the blog figure as editable SVG. No dependencies or image generation.

Run from any directory with Python 3. The PNG used for social previews is a
render of geometry.svg: rsvg-convert geometry.svg -o geometry-social.png
"""

from html import escape
from math import exp, sin
from pathlib import Path


HERE = Path(__file__).resolve().parent
BLUE = "#375E86"
TEAL = "#35837B"
RED = "#C0392B"
GREY = "#9AACB6"
PALE = "#DEE5E9"
INK = "#323C40"


def text(x, y, content, cls="label", **attrs):
    attributes = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" class="{cls}" {attributes}>{escape(content)}</text>'


def path(d, colour=GREY, width=1.5, **attrs):
    attributes = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" {attributes}/>'


def circle(x, y, r=4, colour=BLUE, fill="white", **attrs):
    attributes = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{colour}" stroke-width="1.6" fill="{fill}" {attributes}/>'


def agent(x, y, scale=1):
    # The same articulated segments and round joints as the RL walkers.
    return f'''<g transform="translate({x} {y}) scale({scale})">
      <path d="M-34 25H34L44 31H-44Z" fill="#EEF1F3"/>
      <path d="M-19-2L7-6" stroke="{INK}" stroke-width="9"/>
      <path d="M-17 0L-23 13L-30 25M5-4L15 9L25 25" stroke="{BLUE}" stroke-width="5" fill="none"/>
      <path d="M-12 0L-7 13L-9 25M7-4L3 10L8 25" stroke="{TEAL}" stroke-width="4" fill="none"/>
      {circle(16, -15, 8, BLUE, BLUE)}
      {''.join(circle(a, b, 3.3) for a, b in [(-17, 0), (-23, 13), (-30, 25), (5, -4), (15, 9), (25, 25)])}
      {''.join(circle(a, b, 2.7, TEAL) for a, b in [(-12, 0), (-7, 13), (-9, 25), (7, -4), (3, 10), (8, 25)])}
    </g>'''


def local_world(mobile=False):
    out = [text(0, 28, "1  Bounded spacetime", "heading"),
           text(0, 59, "Low-dimensional bounded negative experiences", "subheading"),
           '<ellipse cx="225" cy="237" rx="205" ry="134" fill="#F7F9FA"/>',
           '<g clip-path="url(#pocket-clip)">']
    # Curved coordinate lines remain within the finite domain.
    for y in [138, 177, 215, 253, 291, 329]:
        out.append(path(f"M20 {y}Q225 {y+45} 430 {y}", PALE))
    for x in [65, 120, 175, 230, 285, 340, 395]:
        out.append(path(f"M{x} 96Q{x-55} 237 {x} 378", PALE))
    out.append('</g>')
    out.append('<ellipse cx="225" cy="237" rx="205" ry="134" fill="none" stroke="#375E86" stroke-width="2.5"/>')
    out += [agent(133, 208, 0.85), agent(248, 267, 0.9), agent(313, 177, 0.7)]
    out += [circle(56, 237, 5, BLUE, BLUE),
            path("M62 237L94 221M62 237L209 278M62 237L281 187", GREY, 1.6, stroke_dasharray="3 5"),
            text(143, 141, "Bounded refinement", "small"),
            path("M152 220Q183 202 230 201T413 202", TEAL, 2.5),
            path("M272 277Q317 261 331 229T413 202", TEAL, 2.5),
            path("M328 186Q365 178 413 202", TEAL, 2.5),
            circle(230, 201, 4, TEAL, TEAL),
            '<rect x="414" y="187" width="13" height="30" rx="2" fill="white" stroke="#375E86" stroke-width="2"/>',
            path("M427 202H464", TEAL, 2.7, marker_end="url(#teal-arrow)"),
            text(451, 169, "Filter", "small", text_anchor="middle"),
            path("M443 176L423 187", GREY),
            text(0, 410, "Local beginning", "small"),
            path("M64 388L56 333V246", GREY)]
    for d, opacity in [("M140 240Q157 285 181 309", 1),
                       ("M181 309Q195 333 218 319", .78),
                       ("M218 319Q236 302 253 315", .58),
                       ("M253 315Q270 327 288 318", .35),
                       ("M288 318Q305 314 324 318", .14)]:
        out.append(path(d, RED, 2.5, opacity=opacity, stroke_dasharray="5 4"))
    out += [text(228, 410, "Negative intensity fades", "small"),
            path("M327 387L324 331", GREY),
            path("M145 444H345", BLUE, 1.8, marker_end="url(#blue-arrow)"),
            text(245, 472, "Local time", "small", text_anchor="middle")]
    return "\n".join(out)


def project(u, v, w):
    return (36 + u * 54 + v * 28 + w * 17,
            312 - u * 19 + v * 24 - w * 69)


def polyline(points, **kw):
    return path("M" + "L".join(f"{x},{y}" for x, y in points), **kw)


def containing_geometry(mobile=False):
    out = [text(0, 28, "2  Encompassing space", "heading"),
           text(0, 59, "Dot products are all you need", "subheading"),
           '<g transform="translate(0 30)">',
           '<g mask="url(#outer-lattice-mask)">']
    # Three families of projected coordinates, with their own interaction scale.
    for w in range(3):
        for v in range(3):
            out.append(polyline([project(u, v, w) for u in range(7)], colour=PALE))
        for u in range(7):
            out.append(polyline([project(u, v, w) for v in range(3)], colour=PALE))
    for u in [0, 2, 4, 6]:
        for v in [0, 2]:
            out.append(polyline([project(u, v, w) for w in range(3)], colour=GREY))
    for u in range(7):
        for v in range(3):
            for w in range(3):
                out.append(circle(*project(u, v, w), r=3.5, colour=GREY, fill="#EEF1F3"))
    out.append('</g>')
    cx, cy = project(2, 1, 1)
    out += [f'<ellipse cx="{cx}" cy="{cy}" rx="47" ry="30" fill="#EEF1F3" stroke="{BLUE}" stroke-width="2.5"/>',
            path(f"M{cx-41} {cy}Q{cx} {cy+12} {cx+41} {cy}", GREY),
            path(f"M{cx-14} {cy-27}Q{cx-28} {cy} {cx-14} {cy+27}", GREY),
            path(f"M{cx+13} {cy-27}Q{cx-1} {cy} {cx+13} {cy+27}", GREY),
            circle(cx-23, cy+3, 3, BLUE, BLUE),
            path(f"M{cx-15} {cy+10}q12 12 24 4", RED, 1.6, stroke_dasharray="3 3"),
            circle(cx+41, cy-8, 4, TEAL, "white"),
            text(10, 115, "Our finite universe", "small"),
            path(f"M130 124L{cx-22} {cy-32}", BLUE, 1.5, stroke_dasharray="4 4")]
    traces = [[(cx+45, cy-8), project(3, 1, 1), project(3, 1, 2), project(4, 1, 2), project(6, 1, 2)],
              [(cx+45, cy-8), project(3, 2, 1), project(4, 2, 1), project(5, 2, 2), project(6, 2, 2)]]
    for pts in traces:
        out.append(polyline(pts, colour=TEAL, width=2.8))
        out += [circle(x, y, 4.5, TEAL, TEAL) for x, y in pts[1:]]
        x, y = pts[-1]
        out.append(path(f"M{x} {y}l42 -15", TEAL, 2.4, stroke_dasharray="4 5", marker_end="url(#teal-arrow)"))
    out += [text(280, 48, "Activations propagate", "small"),
            text(0, 429, "Far richer unrestricted positive experience", "subheading"),
            text(0, 459, "Different coordinates and interaction scales", "small"),
            '</g>']
    return "\n".join(out)


def decay_curve(x, y, length, height, vertical=False):
    out = []
    for segment in range(5):
        points = []
        for i in range(segment * 16, (segment+1) * 16+1):
            t = i/80
            offset = height*exp(-3.8*t)*sin(8*3.14159265*t)
            points.append((x+offset, y+length*t) if vertical else (x+length*t, y+offset))
        out.append(polyline(points, colour=RED, width=2.6, opacity=1-segment*.19, stroke_dasharray="5 4"))
    return "\n".join(out)


def filter_box(x, y):
    return f'''<rect x="{x}" y="{y}" width="76" height="64" rx="3" fill="white" stroke="{BLUE}" stroke-width="2"/>
    {path(f'M{x+19} {y+14}V{y+50}M{x+38} {y+14}V{y+50}M{x+57} {y+14}V{y+50}', PALE, 2)}
    {circle(x+19, y+24, 4, BLUE, BLUE)}{circle(x+38, y+39, 4, BLUE, BLUE)}{circle(x+57, y+27, 4, TEAL, TEAL)}'''


def reflection(mobile=False):
    out = [text(0, 27, "3  Reflection and embedding", "heading")]
    if mobile:
        out += [text(0, 61, "Contrast with bounded, decaying experiences", "subheading"),
                text(0, 107, "Experience", "small"), circle(59, 141, 6, BLUE, BLUE),
                path("M65 141H237V235", BLUE, 2.5, marker_end="url(#blue-arrow)"),
                path("M59 147V183H89", RED, 2.6, stroke_dasharray="5 4"),
                decay_curve(90, 183, 115, 23),
                text(10, 220, "Negative experience", "small"),
                text(10, 247, "decays here", "small"),
                path("M0 273H174M300 273H500", GREY, 1.5, stroke_dasharray="5 5"),
                filter_box(199, 241), text(303, 262, "Symmetries", "small"),
                path("M237 305V347", TEAL, 2.8, marker_end="url(#teal-arrow)"),
                text(10, 345, "Filtered", "small"), text(10, 371, "activations", "small"),
                polyline([(237,352),(158,392),(237,425),(324,392),(237,352)], colour=TEAL, width=2.5),
                path("M158 392H324M237 352V425", PALE, 1.5)]
        out += [circle(x,y,5,TEAL,TEAL) for x,y in [(237,352),(158,392),(237,425),(324,392)]]
        out += [text(237, 470, "Far richer unrestricted positive experience", "subheading", text_anchor="middle"),
                text(237, 500, "from bounded, decaying experiences", "small", text_anchor="middle")]
    else:
        out += [text(0, 60, "Maximise positive experience through contrast with bounded, decaying experiences.", "subheading"),
                text(12, 110, "Experience", "small"),
                circle(32, 144, 6, BLUE, BLUE),
                path("M38 144H462", BLUE, 2.5, marker_end="url(#blue-arrow)"),
                path("M32 150V213H70", RED, 2.5, stroke_dasharray="5 4"),
                decay_curve(70, 213, 340, 26),
                text(12, 267, "Negative experience decays within spacetime", "small"),
                path("M504 185V277", GREY, 1.6, stroke_dasharray="5 5"),
                filter_box(466, 112), text(504, 100, "Symmetries", "small", text_anchor="middle"),
                path("M542 144H655", TEAL, 2.8, marker_end="url(#teal-arrow)"),
                text(666, 106, "Filtered activations", "small"),
                polyline([(670,144),(755,118),(846,144),(755,185),(670,144)], colour=TEAL, width=2.5),
                path("M670 144H846M755 118V185M846 144L923 121L1005 144L923 185L846 144", PALE, 1.8),
                path("M846 144L923 121L1005 144", TEAL, 2.5, marker_end="url(#teal-arrow)")]
        out += [circle(x,y,5,TEAL,TEAL) for x,y in [(670,144),(755,118),(846,144),(755,185),(923,121)]]
        out += [text(666, 211, "Far richer unrestricted", "subheading"),
                text(666, 238, "positive experience", "subheading"),
                text(666, 267, "from bounded, decaying experiences", "small")]
    return "\n".join(out)


def draw(mobile=False):
    width, height = (540, 1620) if mobile else (1080, 900)
    label_size, small_size = (21, 20) if mobile else (19, 18)
    cx, cy = project(2,1,1)
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="figure-title figure-description">
<title id="figure-title">Bounded spacetime within an encompassing space</title>
<desc id="figure-description">The universe as a construction within an encompassing space. Primitive structures develop and refine experiences in a simpler setting. Their experiences are reflected or embedded through symmetries, providing contrast for far richer unrestricted positive experience while negative experiences remain bounded and decay.</desc>
<style>
text {{ font-family: "Open Sans", "DejaVu Sans", sans-serif; fill: #525C60; }}
.heading {{ font-size: 25px; font-weight: 600; fill: {INK}; }}
.subheading {{ font-size: {label_size}px; }}
.small {{ font-size: {small_size}px; }}
path, polyline {{ stroke-linecap: round; stroke-linejoin: round; }}
</style>
<defs>
  <marker id="teal-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="{TEAL}" stroke-width="1.5"/></marker>
  <marker id="blue-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="{BLUE}" stroke-width="1.5"/></marker>
  <clipPath id="pocket-clip"><ellipse cx="225" cy="237" rx="205" ry="134"/></clipPath>
  <mask id="outer-lattice-mask"><rect width="520" height="480" fill="white"/><ellipse cx="{cx}" cy="{cy}" rx="51" ry="34" fill="black"/></mask>
</defs>
<rect width="{width}" height="{height}" fill="white"/>
''']
    if mobile:
        out += [f'<g transform="translate(20 24)">{local_world(True)}</g>',
                path("M20 524H520", PALE, 1.5),
                f'<g transform="translate(20 554)">{containing_geometry(True)}</g>',
                path("M20 1080H520", PALE, 1.5),
                f'<g transform="translate(20 1100)">{reflection(True)}</g>']
    else:
        out += [f'<g transform="translate(20 30)">{local_world()}</g>',
                path("M520 28V510", PALE, 1.5),
                f'<g transform="translate(550 30)">{containing_geometry()}</g>',
                path("M20 550H1060", PALE, 1.5),
                f'<g transform="translate(20 582)">{reflection()}</g>']
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "geometry.svg").write_text(draw(), encoding="utf-8")
    (HERE / "geometry-mobile.svg").write_text(draw(mobile=True), encoding="utf-8")
