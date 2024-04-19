import numpy as np
import glm
import pygame as pg
import moderngl as mgl

class Line:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()

    def render(self):
        self.vao.render(mgl.LINE_LOOP)
        self.vao.render(mgl.POINTS)
    
    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program,
                                    [(self.vbo, '2f', 'in_position')])
        return vao

    def get_vertex_data(self):
        vertex_data = [(0,0),(0.5,0),(0.5,0.5),(0,0.5)]
        vertex_data = np.array(vertex_data, dtype='f4')
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