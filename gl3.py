#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#Ejercicio 1
#26/07/2021

import struct
from collections import namedtuple
from obj import Obj
import random



V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  v0length = length(v0)
  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def barycentric(A, B, C, P):
  
  b = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(b[2]) < 1:
    return -1, -1, -1   

  return (
    1 - (b[0] + b[1]) / b[2], 
    b[1] / b[2], 
    b[0] / b[2]
  )
  
  


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

# Guarda color
def color(r, g, b):
    # Acepta valores de 0 a 1
    return bytes([b, g, r])

# Variables globales

#BLACK = color(0,0,0)
#WHITE = color(1,1,1)


class Renderer(object):
    #Constructor
    def __init__(self, width, height):
        
        self.height = height
        self.width = width
        self.framebuffer = []
        self.clear_color = color(255, 255, 255)
        self.vertex_color = color(0, 0, 0)
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)

    # Crea el viewport
    def glViewport(self, x, y, width, height):
        self.viewportX = int(x)
        self.viewportY = int(y)
        self.viewportWidth = int(width)
        self.viewportHeight = int(height)

    # color fondo
    def glClearColor(self, r, g, b):
        self.clear_color = color(r, g, b)

    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    
    # Color 
    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)

    # Dibujar un punto
    def glPoint(self, x, y, color ): 
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
            self.framebuffer[y][x] = color
        except IndexError:
            print("\nerror\n")

     #punto normalizado
    #Solo en las coordenadas específicas
    #por lo enteros
    def glPoint2(self, x, y, color = None): 
        x = int( (x + 1) * (self.viewportWidth / 2) + self.viewportX )
        y = int( (y + 1) * (self.viewportHeight / 2) + self.viewportY)
        if x < self.viewportX or x >= self.viewportX + self.viewportWidth or y < self.viewportY or y >= self.viewportY + self.viewportHeight:
            return
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.framebuffer[int(x)][int(y)] = color or self.curr_color

#Basado en lo que se realizó en clase
    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1,color)
            return

        # Pendiente
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        m = dy/dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            
            offset += m
            if offset >= limit:
                
                y += 1 if y0 < y1 else -1
                limit += 1

    
    #Se tomo de ejemplo lo realizado en clase
    def glLoadModel(self, filename, translate = V2(0.0,0.0), scale = V2(1.0,1.0)):
        
        model = Obj(filename)

        for face in model.faces:
            
            vertCount = len(face)

            for v in range(vertCount):
                
                index0 = face[v][0] - 1 
                index1 = face[(v + 1) % vertCount][0] - 1

                vert0 = model.vertices[index0]
                vert1 = model.vertices[index1]

                x0 = round(vert0[0] * scale.x + translate.x)
                y0 = round(vert0[1] * scale.y + translate.y)
                x1 = round(vert1[0] * scale.x + translate.x)
                y1 = round(vert1[1] * scale.y + translate.y)

                self.glLine(V2(x0,y0), V2(x1, y1))


    # Creación del Bitmap
    def glFinish(self, filename):
        # archivo BMP 
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # Por cada pixel se tienen 3 Bytes
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[y][x])
                    
    #Retorna el vertex3
    def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
            return V3(round((vertex[0] + translate[0]) * scale[0]),round((vertex[1] + translate[1]) * scale[1]),round((vertex[2] + translate[2]) * scale[2]))
        
    
    
    #Relleno de los polígonos
    def glFill(self, x,y):

        if (x > 360 and y > 330):
            return color(255, 36, 0)
        elif (y > 325):
            return color(251, 163, 26)
        elif (x > 250 and x < 300 and y > 200):
            return color(223, 30, 38)
        elif (y < 170 and x > 200):
            return color(148, 26, 28)
        else:
            return color(255,0,0)

# Dimensiones
width = 800
height = 740

# Instancia del renderer
r = Renderer(width, height)

r.glClear()
r.glLoadModel('./sphere.obj')

r.glFinish("a.bmp")




                    