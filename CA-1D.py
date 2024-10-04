import pygame as pg
import math
pg.init()

class Node:
    ALL_NODES = []
    def __init__(self, pos):
        self.pos = pos
        self.conx = []
        self.on = False
        self.r = 10
        Node.ALL_NODES.append(self)

    def flip(self):
        self.on = not self.on

    def set_state(self, state):
        self.on = state

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

    def draw(self, surface):
        pg.draw.line(surface, (150, 150, 150), self.nodes[0].pos, self.nodes[1].pos, 3)


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def main():
    run = True
    screen = pg.display.set_mode((1000, 750))
    clock = pg.time.Clock()
    fps = 60
    Connection([Node((100, 100)), Node((200, 200))])
    last_clicked = None
    move_node = None
    while run:
        clock.tick(fps)
        screen.fill((255, 255, 255))
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

if __name__ == "__main__":
    main()