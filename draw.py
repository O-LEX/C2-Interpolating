import numpy as np
import pygame as pg
import moderngl as mgl

class Line:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.points = []
        self.vertex_data = []
        self.shader_program = self.get_shader_program('default')
    
    def lerp(self, a, b, t):
        return (a[0] * (1 - t) + b[0] * t, a[1] * (1 - t) + b[1] * t)

    def bezier2d(self, points):
        ret = []
        i = 0
        while i < len(points) - 2:
            p0 = points[i]
            p1 = points[i + 1]
            p2 = points[i + 2]
            for t in np.arange(0, 1, 0.01):
                p01 = self.lerp(p0, p1, t)
                p12 = self.lerp(p1, p2, t)
                p = self.lerp(p01, p12, t)
                ret.append(p)
            i += 2
        while i < len(points):
            ret.append(points[i])
            i += 1
        return ret
    
    def update_points(self):
        if len(self.points) < 3:
            self.vertex_data = self.points
            self.vbo = self.get_vbo()
            self.vao = self.get_vao()
            self.render()
            return
        self.vertex_data = self.bezier2d(self.points)
        self.vbo = self.get_vbo()
        self.vao = self.get_vao()
        self.render()

    def update(self):
        x, y = pg.mouse.get_pos()
        x /= self.app.WIN_SIZE[0] / 2
        y /= self.app.WIN_SIZE[1] / 2
        y = 2 - y
        x -= 1
        y -= 1
        self.points.append((x, y))
        self.update_points()

    def render(self):
        if not self.vertex_data:
            return
        self.vao.render(mgl.LINE_STRIP)
    
    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program,
                                    [(self.vbo, '2f', 'in_position')])
        return vao

    def get_vertex_data(self):
        vertex_data = np.array(self.vertex_data, dtype='f4')
        return vertex_data
    
    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert', 'r') as f:
            vert_shader = f.read()
        with open(f'shaders/{shader_name}.frag', 'r') as f:
            frag_shader = f.read()
        
        program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        return program