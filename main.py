from collections import namedtuple
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import math
#zdefiniowanie punktu
Point = namedtuple('Point', ['x', 'y'])
# funkcja określająca orientację trzech punktów 
def orientation(p, q, r):
    temp = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if temp == 0:
        return 0  # 0 gdy punkty są współliniowe
    elif temp>0:
        return 1 # 1 gdy jest skręt w prawo
    else: 
        return 2 # 2 gdy jest skręt w lewo

# funkcja obliczająca kwadrat odległości między dwoma punktami
def distance_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

def convex_hull(points):
    if len(points) == 1:
        return points
    # szukanie punktu z najmniejszym y lub w przypadku remisu z najmniejszą wartością x
    start = min(points, key=lambda p: (p.y, p.x))
    # sortowanie punktów względem kąta punktu startowego i odległości
    sorted_points = sorted(points, key=lambda p: (
        math.atan2(p.y - start.y, p.x - start.x),
        distance_sq(start, p)
    ))
    # budowanie otoczki - korystanie z funkcji sprawdzjącej skręt - jeżeli skręca w lewo jest dodawany do otoczki. 
    hull = []
    for p in sorted_points:
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)

    return hull
# funkcja okreslająca kształt otoczki
def otoczka_typ(hull):
    l = len(set(hull))
    if l == 1:
        return "punkt"
    elif l == 2:
        return "odcinek"
    elif l == 3:
        return "trójkąt"
    elif l == 4:
        return "czworokąt"
    else:
        return "wielokąt"
    # funkcja rysująca otoczkę wypułką
def draw(points, hull, canvas_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    xs, ys = zip(*[(p.x, p.y) for p in points])
    ax.scatter(xs, ys, color='blue', label='Punkty')

    if len(hull) > 1:
        hx, hy = zip(*[(p.x, p.y) for p in hull] + [hull[0]])
        ax.plot(hx, hy, color='red', label='Otoczka wypukła')

    for i, p in enumerate(points):
        ax.annotate(f'P{i+1}', xy=(p.x, p.y), xytext=(5, 5), textcoords='offset points', fontsize=8, clip_on=True)

    ax.axis('equal')
    ax.grid(True)
    ax.set_title("Otoczka wypukła")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)

    fig.subplots_adjust(bottom=0.3)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, canvas_frame)
    toolbar.update()
    toolbar.pack()
    # główna funkcja wywołująca pozostałe funkcję
def main(points, canvas_frame):
    hull = convex_hull(points)
    draw(points, hull, canvas_frame)
    typ = otoczka_typ(hull)
    poj=next(iter(set(hull)))
    result = f"\nOtoczka wypukła to: {typ} "
    if(typ=='punkt'):
        result+= "Wierzchołek otoczki wypukłej: "
        result+=f"({poj.x}, {poj.y})"
    else:
        result+="Wierzchołki otoczki wypukłej: "
        for p in hull:
            result+=f"({p.x}, {p.y}) "
    return result