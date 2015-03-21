# json-map, a tiled JSON map renderer for pyglet
# Copyright (C) 2014 Juan J. Martinez <jjm@usebox.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A Tiled JSON map renderer for pyglet.

These classes use the JSON format as generated by Tiled JSON plugin.

`pyglet.resource` framework is used to load all the elements of the map, so
any path information must be removed from the tileset.

"""
import math
import os
import json
batch_2_mpx = 0.5
batch_2_mpy = 0.5
batch_3_mpx = 0.3
batch_3_mpy = 0.3
import pyglet
from pyglet.graphics import OrderedGroup
from pyglet.sprite import Sprite

from pyglet import gl
from player import PlayerAnimatedObject, GooseObject

__all__ = ['Map', "TileLayer", "ObjectGroup",]

def get_texture_sequence(filename, tilewidth=32, tileheight=32, margin=1, spacing=1, nearest=False):
    """Returns a texture sequence of a grid generated from a tile set."""

    image = pyglet.resource.image(filename)
    region = image.get_region(margin, margin, image.width-margin*2, image.height-margin*2)
    grid = pyglet.image.ImageGrid(region,
                                  int(region.height/tileheight),
                                  int(region.width/tilewidth),
                                  row_padding=spacing,
                                  column_padding=spacing,
                                  )

    texture = grid.get_texture_sequence()

    if nearest:
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

    return texture


class BaseLayer(object):
    """
    Base layer.

    Takes care of the "visible" flag.

    """
    # ordered group
    groups = 0

    def __init__(self, data, map):

        self.data = data
        self.map = map

        if self.data["visible"]:
            self.sprites = {}
            self.group = OrderedGroup(BaseLayer.groups)
            BaseLayer.groups += 1


class TileLayer(BaseLayer):
    """
    Tile layer.

    Provides a pythonic interface to the tile layer, including:

        - Iterate through the tiles.
        - Check if one coordinate exists in the layer.
        - Get one tile of layer.

    """
    opacity = 255
    def __iter__(self):
        return iter(self.data)

    def __contains__(self, index):
        if type(index) != tuple:
            raise TypeError("tuple expected")

        x, y = index
        return int(x+y*self.map.data["width"]) in self.data["data"]

    def __getitem__(self, index):
        if type(index) != tuple:
            raise TypeError("tuple expected")

        x, y = index
        return self.data["data"][int(x+y*self.map.data["width"])]

    def set_viewport(self, x, y, w, h):
        tw = self.map.data["tilewidth"]
        th = self.map.data["tileheight"]
        def yrange(f, t, s):
            while f < t:
                yield f
                f += s

        in_use = []
        if "properties" in self.data.keys():

            if  "slow" in self.data["properties"].keys():
                layer_batch = self.map.batch2
            elif "veryslow" in self.data["properties"].keys():
                layer_batch = self.map.batch3
            else:
                layer_batch = self.map.batch
        else:
            layer_batch = self.map.batch
        for j in yrange(y, y+h+th, th):
            py = j//th
            for i in yrange(x, x+w+tw, tw):
                px = i//tw
                in_use.append((px, py))
                if (px, py) not in self.sprites:
                    try:
                        texture = self.map.get_texture(self[px, py])
                    except (KeyError, IndexError):
                        self.sprites[(px, py)] = None
                    else:
                        sprite = Sprite(texture,
                                                        x=(px*tw),
                                                        y=h-(py*th)-th,
                                                        batch=layer_batch,
                                                        group=self.group,
                                                        usage="static",
                                                        )
                        sprite.opacity = self.opacity
                        self.sprites[(px, py)] = sprite

    old_group = None
    def set_opacity(self, opacity):
        self.opacity = opacity
        for spr in self.sprites.keys():
            sprite = self.sprites[spr]
            if sprite is not None:
                    sprite.opacity = opacity






class ObjectGroup(BaseLayer):
    """
    Object Group Layer.

    Only tile based objects will be drawn (not shape based).

    Provides a pythonic interface to the object layer, including:

        - Iterate through the objects.
        - Check if one coordinate or an object name exists in the layer.
        - Get one object based on its coordinates or its name.

    Also it is possible to get a list of objects of the same type with
    `ObjectGroup.get_by_type(type)`.

    """
    collision_group = []
    def __init__(self, data, map):
        super(ObjectGroup, self).__init__(data, map)

        self.h = 0
        self.objects = []
        self._index = {}
        self._index_type = {}
        self._xy_index = {}

        for obj in data["objects"]:
            self.objects.append(obj)

            name = obj.get("name", "?")
            if name not in self._index:
                self._index[name] = []

            otype = obj.get("type", "?")
            if otype not in self._index_type:
                self._index_type[otype] = []

            x = int(obj["x"])//self.map.data["tilewidth"]
            y = int(obj["y"])//self.map.data["tileheight"]-1
            if (x, y) not in self._xy_index:
                self._xy_index[x, y] = []

            self._index[name].append(self.objects[-1])
            self._index_type[otype].append(self.objects[-1])
            self._xy_index[x, y].append(self.objects[-1])

        # XXX: is this useful AT ALL?
        self.objects.sort(key=lambda obj: obj["x"]+obj["y"]*self.map.data["width"])

    def __iter__(self):
        return iter(self.objects)

    def __contains__(self, name):
        if isinstance(name, tuple):
            x, y = name
            return (int(x), int(y)) in self._xy_index
        return name in self._index

    def __getitem__(self, name):
        if isinstance(name, tuple):
            x, y = name
            # XXX: if there are several objects, expect the first one
            return self._xy_index[int(x), int(y)][0]
        return self._index[name]

    def get_by_type(self, otype):
        return self._index_type[otype]
    first = False
    def set_viewport(self, x, y, w, h):
        if self.first == False:
            self.first = True
        else:
            return

        self.h = h
        tw = self.map.data["tilewidth"]
        th = self.map.data["tileheight"]

        in_use = []
        for obj in self.objects:
            if x-tw < obj["x"] < x+w+tw and y-th < obj["y"] < y+h+th:
                if not obj["visible"]:
                    continue
                if "gid" in obj:
                    in_use.append((obj["x"], obj["y"]))
                    try:
                        texture = self.map.get_texture(obj["gid"])
                        tileoffset = self.map.get_tileoffset(obj["gid"])
                    except (IndexError, KeyError):
                        sprite = None
                    else:
                        if str.lower(obj["name"]) == "player":
                            sprite = GooseObject(obj["x"]+tileoffset[0], self.h-obj["y"]+tileoffset[1], self.map.batch,self.group,"dynamic",)
                        else:
                            object_dict = {"goose": GooseObject}
                            in_dict = False
                            for object in object_dict.keys():
                                if object == obj["type"]:
                                    object_dict[object](obj["x"]+tileoffset[0], self.h-obj["y"]+tileoffset[1], self.map.batch,self.group,"dynamic",)
                                    in_dict = True
                            if not in_dict:
                                sprite = Sprite(texture,
                                        x=obj["x"]+tileoffset[0],
                                        y=self.h-obj["y"]+tileoffset[1],
                                        batch=self.map.batch,
                                        group=self.group,
                                        usage="dynamic",
                                        )
                    if "collision" in obj["properties"].keys():
                        self.collision_group.append(obj)
                    obj["sprite"] = sprite
                    obj["vx"]=0
                    obj["vy"]=0
                    obj["ax"]=0

                    obj["ay"]=1
                    obj["jump"]= False
                    self.sprites[(obj["x"], obj["y"])] = sprite

    def move(self, object,  sprite):
        movement = 3
        jumpmovement = 1

        jumpspeed = 12
        glide = 0.5


        if "sprite" not in object.keys():
            return [0,0]
        vy = object["vy"]
        vx = object["vx"]
        d_y = 0
        d_x = 0
        jump = object["jump"]
        o_x = object["x"]
        o_y = object["y"]
        ax = object["ax"]
        ay = object["ay"]
        for a in self.to_tile_coordinates(o_x, o_y+1, sprite.width, sprite.height):
            if self.map.tilelayers["collision"][a[0], a[1]] is not 0:
                if jump:
                    vy = jumpspeed
                    jump = False
        if vy > 0:
            vy -= ay
            d_y = -vy * jumpmovement
        if vy <= 0:
            vy -= ay
            d_y = -int(vy * jumpmovement*glide)
        if vx < 0:
            d_x = -movement
        elif vx > 0:
            d_x = movement

        vx = 0
        deltas = self.dydx_checker(o_x ,o_y ,d_x, d_y, object)
        d_x = deltas[0]
        d_y = deltas[1]
        sprite.x += d_x
        sprite.y -= d_y
        object["x"] += d_x
        object["y"] += d_y
        object["vy"] = vy
        object["vx"] = vx
        self.sprites[(object["x"], object["y"])] = sprite
        if (o_x, o_y) in self.sprites.keys():
            del self.sprites[(o_x, o_y)]
        return [d_x, d_y]

        for a in self.collision_group:

            if a is not self:
                print("hier")
                x1 = [object["x"],object["y"]]
                x2 = [object["x"]+self.width,object["y"]]
                x3 = [object["x"],object["y"]-self.height]
                x4 = [object["x"]+self.width,object["y"]-self.height]
                y1 = [a.object["x"],a.object["y"]]
                y2 = [a.object["x"]+a.width,a.object["y"]]
                y3 = [a.object["x"],a.object["y"]-a.height]
                y4 = [a.object["x"]+a.width,a.object["y"]-a.height]
                if self.lineintersect(x1,x2,y1,y2) or self.lineintersect(x1,x2,y3,y2) or self.lineintersect(x1,x2,y4,y3) or self.lineintersect(x1,x2,y1,y4)\
                    or self.lineintersect(x3,x2,y1,y2) or self.lineintersect(x3,x2,y3,y2) or self.lineintersect(x3,x2,y4,y3) or self.lineintersect(x3,x2,y1,y4)\
                    or self.lineintersect(x3,x4,y1,y2) or self.lineintersect(x3,x4,y3,y2) or self.lineintersect(x3,x4,y4,y3) or self.lineintersect(x3,x4,y1,y4)\
                    or self.lineintersect(x1,x4,y1,y2) or self.lineintersect(x1,x4,y3,y2) or self.lineintersect(x1,x4,y4,y3) or self.lineintersect(x1,x4,y1,y4):
                    print("hoi")


    def dydx_checker(self, o_x, o_y, d_x, d_y, object):
        iy = 0
        ix = 0
        # eerst over y itereren dan x
        if d_y != 0:
            if d_y >0 :
                for i in range(0, d_y):
                    result=self.collision_detection(o_x,o_y+i,0,1,object)
                    if result[1] != 1:
                        break
                    iy+=1
            else:
                for i in range(0, d_y, -1):
                    result=self.collision_detection(o_x,o_y+i,0,-1,object)
                    if result[1] != -1:
                        break
                    iy -= 1
        if d_x != 0:
            if d_x >0:
                for i in range(0, d_x):
                    result=self.collision_detection(o_x+i,o_y+iy,1,0,object)
                    if result[0] != 1:
                        break
                    ix+=1
            else :
                for i in range(0, d_x,-1):
                    result=self.collision_detection(o_x+i,o_y+iy,-1,0,object)
                    if result[0] != -1:
                        break
                    ix-=1
        return [ix,iy]

    def line_intersect(self, p1, p2, p3, p4):
        a1 = (p2[1]-p1[1])/(p2[0]-p1[0])
        b1 = p1[1]%a1
        a2 = (p3[1]-p4[1])/(p3[0]-p4[0])
        b2 = p3[1]%a2
        if a1/a2 == 1:
            return False
        x=(a2x+b2-b1)/a1
        y=a1*x+b1
        if (p1[0]<x<p2[0] or p2[0]<x<p1[0]) and (p1[1]<y<p2[1] or p2[1]<y<p1[1]):
            return True
        else:
            return False

    def collision_detection(self, o_x, o_y, d_x, d_y,object):
        b_check =True
        if "collision" in self.map.tilelayers.keys():
            for a in self.to_tile_coordinates(o_x+d_x, o_y+d_y, object["sprite"].width, object["sprite"].height):
                 if self.map.tilelayers["collision"][a[0], a[1]] is not 0:
                    b_check = False
            if not b_check:
                x_check = True
                for a in self.to_tile_coordinates(o_x+d_x, o_y, object["sprite"].width, object["sprite"].height):
                    if self.map.tilelayers["collision"][a[0], a[1]] is not 0:
                        x_check = False
                if x_check:
                    d_y = 0
                else:
                    y_check = True
                    for a in self.to_tile_coordinates(o_x, o_y+d_y, object["sprite"].width, object["sprite"].height):
                        if self.map.tilelayers["collision"][a[0], a[1]] is not 0:
                            y_check = False
                    if y_check:
                        d_x = 0
                    else:
                        return [0,0]
        return[d_x,d_y]

    def to_tile_coordinates(self, o_x, o_y, width, height):
        ret = []
        oo_x = math.floor(o_x/width)

        oo_y = math.floor((o_y-height)/height)

        ret.append((oo_x, oo_y))

        b_add_x = False

        if math.floor(o_x/width)*width != o_x:
            b_add_x = True
            ret.append((oo_x+1, oo_y))

        if math.floor(o_y/height)*height != o_y:
            ret.append((oo_x, oo_y+1))
            if b_add_x:
                ret.append((oo_x+1, oo_y+1))
        return ret

    def set_opacity(self, opacity):
        for object in self.objects:
            if "sprite" in object.keys():
                object["sprite"].opacity = opacity




















class Tileset(object):
    """Manages a tileset and it's used internally by TileLayer."""
    def __init__(self, data, nearest=False):
        self.data = data

        # used to convert coordinates of the grid
        self.columns = (self.data["imagewidth"]-self.data["spacing"]*2)//(self.data["tilewidth"]-self.data["margin"])
        self.rows = (self.data["imageheight"]-self.data["spacing"]*2)//(self.data["tileheight"]-self.data["margin"])

        # the image will be accessed using pyglet resources
        self.image = os.path.basename(self.data["image"])
        self.texture = get_texture_sequence(self.image, self.data["tilewidth"],
                                            self.data["tileheight"],
                                            self.data["margin"],
                                            self.data["spacing"],
                                            nearest=False,
                                            )

    def __getitem__(self, index):
        return self.texture[index]

    def __len__(self):
        return len(self.texture)


class Map(object):
    """
    Load, manage and render Tiled JSON files.

    Maps can created providing the JSON data to this class or using `Map.load_json()`
    and after that a viewport must be set with `Map.set_viewport()`.
    """

    def __init__(self, data, nearest=False):
        self.data = data

        self.tilesets = {} # the order is not important

        self.layers = []
        self.tilelayers = {}
        self.objectgroups = {}

        for tileset in data["tilesets"]:
            self.tilesets[tileset["name"]] = Tileset(tileset, nearest)

        for layer in data["layers"]:
            # TODO: test this!
            if layer['name'] in (self.tilelayers, self.objectgroups):
                raise ValueError("Duplicated layer name %s" % layer["name"])

            if layer["type"] == "tilelayer":
                self.layers.append(TileLayer(layer, self))
                self.tilelayers[layer["name"]] = self.layers[-1]
            elif layer["type"] == "objectgroup":
                self.layers.append(ObjectGroup(layer, self))
                self.objectgroups[layer["name"]] = self.layers[-1]
            else:
                raise ValueError("unsupported layer type %s, skipping" % layer["type"])

        self.batch = pyglet.graphics.Batch()
        self.batch2 = pyglet.graphics.Batch()
        self.batch3 = pyglet.graphics.Batch()

        # viewport
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        # focus
        self.fx = None
        self.fy = None

        # useful (size in pixels)
        self.p_width = self.data["width"]*self.data["tilewidth"]
        self.p_height = self.data["height"]*self.data["tileheight"]

        # build a texture index converting pyglet indexing of the texture grid
        # to tiled coordinate system
        self.tileoffset_index = {}
        self.texture_index = {}
        for tileset in self.tilesets.values():
            for y in range(tileset.rows):
                for x in range(tileset.columns):
                    self.texture_index[x+y*tileset.columns+tileset.data["firstgid"]] = \
                            tileset[(tileset.rows-1-y),x]

                    # TODO: test this!
                    if "tileoffset" in tileset.data:
                        self.tileoffset_index[x+y*tileset.columns+tileset.data["firstgid"]] = \
                                (tileset.data["tileoffset"]["x"], tileset.data["tileoffset"]["y"])

    def invalidate(self):
        """Forces a batch update of the map."""
        self.set_viewport(self.x, self.y, self.w, self.h, True)
    def move_viewport (self,x,y):
        self.set_viewport(self.x+x,self.y+y,self.w,self.h)

    def set_viewport(self, x, y, w, h, force=False):
        """
        Sets the map viewport to the screen coordinates.

        Optionally the force flag can be used to update the batch even if the
        viewport didn't change (this should be used via `Map.invalidate()`).
        """
        # x and y can be floats
        vx = max(x, 0)
        vy = max(y, 0)
        vx = min(vx, (self.p_width)-w)
        vy = min(vy, (self.p_height)-h)
        vw = int(w)
        vh = int(h)

        if not any([force, vx!=self.x, vy!=self.y, vw!=self.w, vh!=self.h]):
            return

        self.x = vx
        self.y = vy
        self.w = vw
        self.h = vh

        for layer in self.layers:
            if layer.data["visible"]:
                layer.set_viewport(self.x, self.y, self.w, self.h)
    def move_focus(self,dx,dy):
        self.set_focus(self.x+dx, self.y+dy)

    def set_focus(self, x, y):
        """Sets the focus in (x, y) world coordinates."""
        x = int(x)
        y = int(y)
        if self.fx == x and self.fy == y:
            return

        self.fx = x
        self.fy = y

        vx = max(x-(self.w//2), 0)
        vy = max(y-(self.h//2), 0)

        if vx+(self.w//2) > self.p_width:
            vx = self.p_width-self.w

        if vy+(self.h//2) > self.p_height:
            vy = self.p_height-self.h

        self.set_viewport(vx, vy, self.w, self.h)

    def world_to_screen(self, x, y):
        """
        Translate world coordinate into screen coordinates.

        Returns a (x, y) tuple.
        """
        return x-self.x, self.h-(y-self.y)

    def get_texture(self, gid):
        """
        Returns a texture identified by its gid.

        If not found will raise a KeyError or IndexError.
        """
        return self.texture_index[gid]

    def get_tileoffset(self, gid):
        """Returns the offset of a tile."""
        return self.tileoffset_index.get(gid, (0, 0))

    @property
    def last_group(self):
        """
        The last use group in `Map` batch.

        This is useful in case any Sprite is added to the `Map` to
        be drawn by the Map's batch without being managed by the Map.

        Using this value plus one will ensure the sprite will be drawn
        over the map.
        """
        return BaseLayer.groups-1

    @staticmethod
    def load_json(fileobj, nearest=False):
        """
        Load the map in JSON format.

        This class method return a `Map` object and the file will be
        closed after is read.

        Set nearest to True to set GL_NEAREST for both min and mag
        filters in the tile textures.
        """
        data = json.load(fileobj)
        fileobj.close()
        return Map(data, nearest)

    def draw(self):
        """Applies transforms and draws the batch."""
        gl.glPushMatrix()
        gl.glTranslatef(-math.floor(self.x*batch_3_mpx), math.floor(self.y*batch_3_mpy), 0)
        self.batch3.draw()
        gl.glPopMatrix()
        gl.glPushMatrix()
        gl.glTranslatef(-math.floor(self.x*batch_2_mpx), math.floor(self.y*batch_2_mpy), 0)
        self.batch2.draw()
        gl.glPopMatrix()
        gl.glPushMatrix()
        gl.glTranslatef(-self.x, self.y, 0)
        self.batch.draw()
        gl.glPopMatrix()

