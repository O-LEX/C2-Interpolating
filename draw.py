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
        self.shader_program_points = self.get_shader_program('points')

    def render_points(self):
        points = np.array(self.points, dtype='f4')
        vbo = self.ctx.buffer(points)
        vao = self.ctx.vertex_array(self.shader_program_points,
                                    [(vbo, '2f', 'in_position')])
        vao.render(mgl.POINTS)


    def solveCubic(self, p0, p1, p2):
        a = 0
        b = 1
        cubic_func = lambda t : np.dot((p2-p0),(p2-p0))*t**3 + 3*np.dot((p2-p0),(p0-p1))*t**2+\
            np.dot((3*p0-2*p1-p2),(p0-p1))*t - np.dot((p0-p1),(p0-p1))
        for i in range(100):
            c = (a + b) / 2
            if cubic_func(c) < 0:
                a = c
            else:
                b = c
        return a

    def C2(self, points):
        ret = []
        i = 0
        while i < len(points) - 3:
            p0 = np.array(points[i])
            p1 = np.array(points[i + 1])
            p2 = np.array(points[i + 2])
            p3 = np.array(points[i + 3])
            t0 = self.solveCubic(p0, p1, p2)
            t1 = self.solveCubic(p1, p2, p3)
            b0 = (p1-(1-t0)**2*p0-t0**2*p2)/(2*t0*(1-t0))
            b1 = (p2-(1-t1)**2*p1-t1**2*p3)/(2*t1*(1-t1))
            # bezier_curve = lambda t: (1 - t) ** 2 * p0 + 2 * (1 - t) * t * b0 + t ** 2 * p2
            # for t in np.linspace(0, 1, 10):
            #     ret.append(bezier_curve(t))
            ratio0 = np.pi/2 / (1 - t0)
            f0 = lambda theta : (1 - (theta / ratio0 + t0)) ** 2 * p0 + 2 * (theta / ratio0 + t0) * (1 - (theta / ratio0 + t0)) * b0 + (theta / ratio0 + t0) ** 2 * p2
            ratio1 = np.pi/2 / t1
            f1 = lambda theta : (1 - theta / ratio1) ** 2 * p1 + 2 * (theta / ratio1) * (1 - theta / ratio1) * b1 + (theta / ratio1) ** 2 * p3
            spline = lambda theta : (np.cos(theta)**2)*f0(theta) + (np.sin(theta))**2*f1(theta)
            for theta in np.linspace(0, np.pi/2, 10):
                ret.append(spline(theta))
            i += 1
        return ret
    
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
        if len(self.points) < 4:
            self.vertex_data = self.points
            self.vbo = self.get_vbo()
            self.vao = self.get_vao()
            self.render()
            return
        self.vertex_data = self.C2(self.points)
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
        self.render_points()
    
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