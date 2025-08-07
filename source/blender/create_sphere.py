#!/usr/bin/env python3

import dataclasses
import math
import random
import typing

import bmesh
import bpy


NUM_NODES = 75


@dataclasses.dataclass
class Node:
    x: int = 0
    y: int = 0
    z: int = 0
    radius: int = 1
    neighbours: list = dataclasses.field(default_factory=list)
    
    def distance(self, other):
        return math.sqrt(
            math.pow(self.x - other.x, 2) +
            math.pow(self.y - other.y, 2)
            )


def find_neighbours(node, nodes):
    ordered = [_n for _n in nodes if _n != node]
    ordered.sort(key=lambda n: node.distance(n))
    return ordered[0:3]


def calculate_nodes():
    results = []
    for _ in range(NUM_NODES):
        results.append(Node(
            x=random.uniform(-4, 4),
            y=random.uniform(-8, 8),
            z=random.uniform(-4, 4),
            radius=random.uniform(0.2, 0.9),
            neighbours=list(),
            ))
    for node in results:
        node.neighbours = find_neighbours(node, results)
    return results
    

def get_material(name):
    mat = bpy.data.materials.get(name)
    if mat is None: # create material
        mat = bpy.data.materials.new(name=name)
    return mat


def create_cylinder(source_node: Node, target_node: Node):
    # add a curve to link them together
    bpy.ops.curve.primitive_bezier_curve_add()
    obj = bpy.context.object
    obj.data.dimensions = '3D'
    obj.data.fill_mode = 'FULL'
    obj.data.bevel_depth = 0.025
    obj.data.bevel_resolution = 4
    # set first point to centre of sphere1
    obj.data.splines[0].bezier_points[0].co = (source_node.x, source_node.y, source_node.z)
    obj.data.splines[0].bezier_points[0].handle_left_type = 'VECTOR'
    # set second point to centre of sphere2
    obj.data.splines[0].bezier_points[1].co = (target_node.x, target_node.y, target_node.z)
    obj.data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'
    obj.data.materials.append(get_material('Edge'))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')
    return obj


def create_node(name, node: Node):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new(name)
    basic_sphere = bpy.data.objects.new(name, mesh)

    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=4, radius=node.radius)
    bm.to_mesh(mesh)
    bm.free()

    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.shade_smooth()
    mesh.materials.append(get_material('Vertex'))
    bpy.ops.transform.translate(value=(node.x, node.y, node.z))
    bpy.ops.object.select_all(action='DESELECT')
    return basic_sphere


nodes = calculate_nodes()
for i, node in enumerate(nodes):
    create_node(f'node_{i:02d}', node)
    for j, neighbour in enumerate(node.neighbours):
        create_cylinder(node, neighbour)
