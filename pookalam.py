import turtle
import math

# --- Setup ---
screen = turtle.Screen()
screen.bgcolor("white")
t = turtle.Turtle()
t.hideturtle()
t.pensize(1)
t.color("black")
turtle.tracer(0, 0)

# --- Radii ---
inner = 50      # innermost circle
third = 165     # inner ring (outer radius of the band)
second = 180    # outer ring inner boundary
outer = 300     # outermost circle

# ---------- Helpers ----------
def draw_inward_arc(r_inner, r_outer, angle_start, angle_end, steps=20):
    points = []
    for i in range(steps + 1):
        t_ratio = i / steps
        ang = math.radians(angle_start + (angle_end - angle_start) * t_ratio)
        r = r_inner + (r_outer - r_inner) * math.sin(math.pi * t_ratio)  # bulge inward
        points.append((r * math.cos(ang), r * math.sin(ang)))
    t.penup(); t.goto(points[0]); t.pendown()
    for x, y in points[1:]:
        t.goto(x, y)

def draw_star(center_x, center_y, radius, petals=6):
    angle_step = 360 / petals
    for i in range(petals):
        angle = math.radians(i * angle_step)
        tip_x = center_x + radius * math.cos(angle)
        tip_y = center_y + radius * math.sin(angle)
        left_x = center_x + radius/2 * math.cos(angle - math.radians(angle_step/4))
        left_y = center_y + radius/2 * math.sin(angle - math.radians(angle_step/4))
        right_x = center_x + radius/2 * math.cos(angle + math.radians(angle_step/4))
        right_y = center_y + radius/2 * math.sin(angle + math.radians(angle_step/4))
        color = "yellow" if i % 2 == 0 else "orange"
        t.penup(); t.goto(center_x, center_y); t.pendown()
        t.fillcolor(color); t.begin_fill()
        t.goto(left_x, left_y); t.goto(tip_x, tip_y); t.goto(right_x, right_y); t.goto(center_x, center_y)
        t.end_fill()

def draw_mini_flower(center_x, center_y, radius=20, petals=4):
    angle_step = 360 / petals
    for j in range(petals):
        ang = math.radians(j * angle_step)
        tip_x = center_x + radius * math.cos(ang)
        tip_y = center_x + 0  # placeholder to keep vars aligned in mind

    angle_step = 360 / petals
    for j in range(petals):
        ang = math.radians(j * angle_step)
        tip_x = center_x + radius * math.cos(ang)
        tip_y = center_y + radius * math.sin(ang)
        left_x = center_x + radius/2 * math.cos(ang - math.radians(angle_step/4))
        left_y = center_y + radius/2 * math.sin(ang - math.radians(angle_step/4))
        right_x = center_x + radius/2 * math.cos(ang + math.radians(angle_step/4))
        right_y = center_y + radius/2 * math.sin(ang + math.radians(angle_step/4))

        t.penup(); t.goto(center_x, center_y); t.pendown()
        t.fillcolor("pink"); t.begin_fill()
        t.goto(left_x, left_y); t.goto(tip_x, tip_y); t.goto(right_x, right_y); t.goto(center_x, center_y)
        t.end_fill()

# ---------- Geometry (your original layout) ----------
# Concentric circles (outlines)
for r in [outer, second, third, inner]:
    t.penup(); t.goto(0, -r); t.pendown(); t.circle(r)

# Outer band cross lines
t.penup(); t.goto(second, 0); t.pendown(); t.goto(outer, 0)
t.penup(); t.goto(-second, 0); t.pendown(); t.goto(-outer, 0)
t.penup(); t.goto(0, second); t.pendown(); t.goto(0, outer)
t.penup(); t.goto(0, -second); t.pendown(); t.goto(0, -outer)

# 12 outer radial lines (180 -> 300)
num_outer_lines = 12
angle_step_outer = 360.0 / num_outer_lines
for i in range(num_outer_lines):
    ang = math.radians(i * angle_step_outer)
    x1, y1 = second * math.cos(ang), second * math.sin(ang)
    x2, y2 = outer * math.cos(ang), outer * math.sin(ang)
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

# 5 inner radial lines (50 -> 165), rotated with one at LEFT horizontal
num_inner_lines = 5
angle_step_inner = 360.0 / num_inner_lines
start_angle = 180
inner_line_pts = []  # save to redraw on top later
for i in range(num_inner_lines):
    a = start_angle + i * angle_step_inner
    rad = math.radians(a)
    x1, y1 = inner * math.cos(rad), inner * math.sin(rad)
    x2, y2 = third * math.cos(rad), third * math.sin(rad)
    inner_line_pts.append(((x1, y1), (x2, y2)))
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

# Outer inward-curving arcs & internal dividers
for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    draw_inward_arc(second, outer, a0, a1)

for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    mid = math.radians((a0 + a1) / 2)
    x1, y1 = second * math.cos(mid), second * math.sin(mid)
    x2, y2 = outer * math.cos(mid), outer * math.sin(mid)
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

# Horizontal divisions inside each outer arc
fractions = [1/3, 2/3]
for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    for frac in fractions:
        pts = []
        steps = 20
        for j in range(steps + 1):
            tr = j / steps
            ang = math.radians(a0 + (a1 - a0) * tr)
            r = second + (outer - second) * math.sin(math.pi * tr) * frac
            pts.append((r * math.cos(ang), r * math.sin(ang)))
        t.penup(); t.goto(pts[0]); t.pendown()
        for x, y in pts[1:]:
            t.goto(x, y)
# ===== Robust brown ring fill + petal fills (replace previous brown/petal code) =====

# 1) Fill the exact donut ring between 'second' and 'outer' using polygon points
steps_ring = 360   # resolution (increase to 720 if you still see tiny seams)
pts = []

# outer circle points (0 -> 2*pi)
for k in range(steps_ring + 1):
    theta = 2 * math.pi * k / steps_ring
    pts.append((outer * math.cos(theta), outer * math.sin(theta)))

# inner circle points in reverse (2*pi -> 0) to create a hole
for k in range(steps_ring, -1, -1):
    theta = 2 * math.pi * k / steps_ring
    pts.append((second * math.cos(theta), second * math.sin(theta)))

# do the fill
t.fillcolor("brown")
t.penup(); t.goto(pts[0]); t.pendown()
t.begin_fill()
for x, y in pts[1:]:
    t.goto(x, y)
t.end_fill()

# 2) Draw petal bands on top of the brown background
colors = ["yellow", "orange", "red"]
fractions = [1/3, 2/3, 1.0]   # same math you used to compute horizontal division curves
angle_step_outer = 360.0 / num_outer_lines

for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    prev_frac = 0.0

    for band_idx, frac in enumerate(fractions):
        pts = []
        steps = 120   # high resolution helps avoid seams; increase if needed

        # upper boundary (a0 -> a1)
        for k in range(steps + 1):
            tr = k / steps
            ang = math.radians(a0 + (a1 - a0) * tr)
            r = second + (outer - second) * math.sin(math.pi * tr) * frac
            pts.append((r * math.cos(ang), r * math.sin(ang)))

        # lower boundary reversed (a1 -> a0)
        for k in range(steps, -1, -1):
            tr = k / steps
            ang = math.radians(a0 + (a1 - a0) * tr)
            r = second + (outer - second) * math.sin(math.pi * tr) * prev_frac
            pts.append((r * math.cos(ang), r * math.sin(ang)))

        # fill this band
        t.fillcolor(colors[band_idx])
        t.penup(); t.goto(pts[0]); t.pendown()
        t.begin_fill()
        for x, y in pts[1:]:
            t.goto(x, y)
        t.end_fill()

        prev_frac = frac

# 3) Re-draw outlines (inward arcs, mid radial dividers, and horizontal division curves)
#    to hide any micro-seams and keep your original lines crisp.

t.color("black")
t.pensize(1)

# redraw inward-curving arcs (use your draw_inward_arc so geometry unchanged)
for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    draw_inward_arc(second, outer, a0, a1)

# redraw radial mid-lines inside outer band
for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    mid = math.radians((a0 + a1) / 2)
    x1, y1 = second * math.cos(mid), second * math.sin(mid)
    x2, y2 = outer * math.cos(mid), outer * math.sin(mid)
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

# redraw the horizontal dividing curves you originally computed
for i in range(num_outer_lines):
    a0 = i * angle_step_outer
    a1 = a0 + angle_step_outer
    for frac in [1/3, 2/3]:
        pts = []
        steps = 120
        for j in range(steps + 1):
            tr = j / steps
            ang = math.radians(a0 + (a1 - a0) * tr)
            r = second + (outer - second) * math.sin(math.pi * tr) * frac
            pts.append((r * math.cos(ang), r * math.sin(ang)))
        t.penup(); t.goto(pts[0]); t.pendown()
        for x, y in pts[1:]:
            t.goto(x, y)
# --- Fill the band between 165 and 180 with green ---
steps_ring = 360
pts = []

# outer boundary (r = 180)
for k in range(steps_ring + 1):
    theta = 2 * math.pi * k / steps_ring
    pts.append((second * math.cos(theta), second * math.sin(theta)))

# inner boundary reversed (r = 165)
for k in range(steps_ring, -1, -1):
    theta = 2 * math.pi * k / steps_ring
    pts.append((third * math.cos(theta), third * math.sin(theta)))

# fill
t.fillcolor("white")
t.penup(); t.goto(pts[0]); t.pendown()
t.begin_fill()
for x, y in pts[1:]:
    t.goto(x, y)
t.end_fill()


# ---------- COLORING (no new geometry, no duplicates) ----------
# 1) Fill the inner ring (50 -> 165) as a solid yellow band
t.penup(); t.goto(0, -third); t.pendown()
t.fillcolor("yellow"); t.begin_fill(); t.circle(third); t.end_fill()

# Punch a hole to keep the center open
t.penup(); t.goto(0, -inner); t.pendown()
t.fillcolor("white"); t.begin_fill(); t.circle(inner); t.end_fill()

# Re-outline inner & outer edges of the band for crisp borders
t.color("black"); t.penup(); t.goto(0, -third); t.pendown(); t.circle(third)
t.penup(); t.goto(0, -inner); t.pendown(); t.circle(inner)

# Redraw the 5 inner radial lines ON TOP so partitions remain visible
for (p1, p2) in inner_line_pts:
    t.penup(); t.goto(p1); t.pendown(); t.goto(p2)

# 2) The 5 small circles (WHITE) and 3) mini flowers (PINK)
num_inner_wedges = 5
angle_step_inner = 360 / num_inner_wedges
start_angle = 180
circle_radius = 35
r_mid = (inner + third) / 2

for i in range(num_inner_wedges):
    angle = start_angle + (i + 0.5) * angle_step_inner
    rad = math.radians(angle)
    cx, cy = r_mid * math.cos(rad), r_mid * math.sin(rad)

    # white filled circle
    t.penup(); t.goto(cx, cy - circle_radius); t.pendown()
    t.fillcolor("red"); t.begin_fill(); t.circle(circle_radius); t.end_fill()
    # outline circle (optional, keeps crisp border)
    t.penup(); t.goto(cx, cy - circle_radius); t.pendown(); t.circle(circle_radius)

    # pink 4-petal flower centered in the small circle
    draw_mini_flower(cx, cy, radius=20, petals=4)

# 4) Innermost circle RED + 6-petal flower (yellow/orange)
t.penup(); t.goto(0, -inner); t.pendown()
t.fillcolor("green"); t.begin_fill(); t.circle(inner); t.end_fill()
# re-outline center circle
t.penup(); t.goto(0, -inner); t.pendown(); t.circle(inner)

draw_star(0, 0, 45, petals=6)


# --- Final update ---
turtle.update()
turtle.done()
