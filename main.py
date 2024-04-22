import pygame as pg
import moderngl as mgl
from draw import *
import sys

class GraphicsEngine:
    def __init__(self, mode, win_size=(1200, 800)):
        pg.init()
        self.WIN_SIZE = win_size
        self.mode = mode
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.mouse.set_visible(True)
        self.ctx = mgl.create_context() 
        self.ctx.enable(mgl.PROGRAM_POINT_SIZE)
        self.scene = Line(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.scene.update()
    
    def render(self):
        self.ctx.clear(color=(0.5, 0.8, 0.8))
        self.scene.render()
        pg.display.flip()
    
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()

if __name__ == '__main__':
    app = GraphicsEngine(mode='C2') # mode='bezier' or mode='C2'
    app.run()