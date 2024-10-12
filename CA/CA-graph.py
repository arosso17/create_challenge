import pygame as pg
import math
pg.init()

font = pg.font.Font('freesansbold.ttf', 32)

class Node:
    ALL_NODES = []
    I = 0
    def __init__(self, pos):
        self.pos = pos
        self.conx = []
        self.on = False
        self.r = 10
        self.i = Node.I
        Node.I += 1
        Node.ALL_NODES.append(self)

    def to_string(self, v=False):
        return self.i

    def flip(self):
        self.on = not self.on

    def draw(self, surface):
        if self.on:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        pg.draw.circle(surface, color, self.pos, self.r)
        pg.draw.circle(surface, (150, 150, 150), self.pos, self.r + 2, 3)


class Connection:
    ALL_CONX = []
    def __init__(self, nodes):
        self.nodes = nodes
        for n in self.nodes:
            n.conx.append(self)
        Connection.ALL_CONX.append(self)

    def to_string(self):
        return f"({self.nodes[0].to_string(), self.nodes[1].to_string()})"

    def draw(self, surface):
        pg.draw.line(surface, (150, 150, 150), self.nodes[0].pos, self.nodes[1].pos, 3)


def clamp(x, l, u):
    return max(l, min(u, x))

def step(nodes, rule):
    board = []
    for i, node in enumerate(nodes):
        board.append(apply_rule(node, rule))
    for i, node in enumerate(nodes):
        node.on = board[i]

def apply_rule(node, rule):
    cons = []
    for con in node.conx:
        if con.nodes[0] == node:
            cons.append(1 if con.nodes[1].on else 0)
        else:
            cons.append(1 if con.nodes[0].on else 0)
    if node.on:
        return rule[0] <= sum(cons) <= rule[1]
    else:
        return rule[2] <= sum(cons) <= rule[3]

def generate_circle(n):
    points = []
    center = (500, 375)
    radius = 350
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append(Node((x, y)))
    for i in range(len(points)):
        Connection([points[i-1], points[i]]).to_string()
    return points

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def change_rule(rule):
    return font.render('Rule: ' + str(rule), True, (0, 0, 0))

def save_state():
    return [node.on for node in Node.ALL_NODES]

def load_state(saved_state):
    for i, n in enumerate(Node.ALL_NODES):
        n.on = saved_state[i]

def main(rule, n):
    run = True
    text = change_rule(rule)
    screen = pg.display.set_mode((1000, 750))
    clock = pg.time.Clock()
    fps = 60
    generate_circle(n)
    last_clicked = None
    move_node = None
    nodes_save = save_state()
    while run:
        clock.tick(fps)
        screen.fill((255, 255, 255))
        screen.blit(text, (text.get_rect().width/2, 750 - text.get_rect().height))
        if move_node is not None:
            move_node.pos = pg.mouse.get_pos()[:]
        for con in Connection.ALL_CONX:
            con.draw(screen)
        for node in Node.ALL_NODES:
            node.draw(screen)
        if last_clicked is not None:
            pg.draw.circle(screen, (50, 250, 50), last_clicked.pos, last_clicked.r)
        if move_node is not None:
            pg.draw.circle(screen, (50, 50, 250), move_node.pos, move_node.r + 2, 3)
        pg.display.flip()
        keys = pg.key.get_pressed()

        if keys[pg.K_RETURN]:
            fps = 3
            step(Node.ALL_NODES, rule)
        else:
            fps = 60

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONUP:
                move_node = None
                if keys[pg.K_LCTRL]:
                    mouse_pos = pg.mouse.get_pos()
                    place = True
                    for n in Node.ALL_NODES:
                        if distance(n.pos, mouse_pos) < 2 * n.r:
                            place = False
                    if place:
                        Node(mouse_pos)
                elif keys[pg.K_LSHIFT]:
                    mouse_pos = pg.mouse.get_pos()
                    for n in Node.ALL_NODES:
                        if distance(n.pos, mouse_pos) < n.r:
                            if last_clicked is not None and n != last_clicked:
                                Connection([last_clicked, n])
                                last_clicked = None
                            else:
                                last_clicked = n
                            break
                else:
                    mouse_pos = pg.mouse.get_pos()
                    for n in Node.ALL_NODES:
                        if distance(n.pos, mouse_pos) < n.r:
                            n.flip()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if keys[pg.K_TAB]:
                    mouse_pos = pg.mouse.get_pos()
                    for n in Node.ALL_NODES:
                        if distance(n.pos, mouse_pos) < n.r:
                            move_node = n

            elif event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    last_clicked = None
                if event.key == pg.K_SPACE:
                    step(Node.ALL_NODES, rule)
                if keys[pg.K_r]:
                    if event.key == 8:
                        rule = rule[:-1]
                        if rule == '':
                            rule = '0'
                        text = change_rule(rule)
                    if 58 > event.key > 47:
                        rule += str(event.key - 48)
                        rule = str(clamp(int(rule), 0, 255))
                        text = change_rule(rule)
                if event.key == pg.K_s:
                    nodes_save = save_state()
                if event.key == pg.K_l:
                    load_state(nodes_save)

if __name__ == "__main__":
    rule = (0, 1, 1, 2)
    n = 20
    main(rule, n)