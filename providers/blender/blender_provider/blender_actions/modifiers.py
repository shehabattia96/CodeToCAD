from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.enums.axis import Axis
from providers.blender.blender_provider.blender_actions.objects import get_object
from providers.blender.blender_provider.blender_definitions import (
    BlenderBooleanTypes,
    BlenderLength,
    BlenderModifiers,
    BlenderTypes,
)


def clear_modifiers(
    object_name: str,
):
    blender_object = get_object(object_name)

    blender_object.modifiers.clear()


def apply_modifier(entity_name: str, modifier: BlenderModifiers, **kwargs):
    blender_object = get_object(entity_name)

    # references https://docs.blender.org/api/current/bpy.types.BooleanModifier.html?highlight=boolean#bpy.types.BooleanModifier and https://docs.blender.org/api/current/bpy.types.ObjectModifiers.html#bpy.types.ObjectModifiers and https://docs.blender.org/api/current/bpy.types.Modifier.html#bpy.types.Modifier
    blenderModifier = blender_object.modifiers.new(
        type=modifier.name, name=modifier.name
    )

    # blenderModifier.show_viewport = False

    # Apply every parameter passed in for modifier:
    for key, value in kwargs.items():
        setattr(blenderModifier, key, value)


def apply_decimate_modifier(entity_name: str, amount: int):
    apply_modifier(
        entity_name,
        BlenderModifiers.DECIMATE,
        decimate_type="UNSUBDIV",
        iterations=amount,
    )


def apply_bevel_modifier(
    entity_name: str,
    radius: Dimension,
    vertex_group_name=None,
    use_edges=True,
    use_width=False,
    chamfer=False,
    **kwargs,
):
    apply_modifier(
        entity_name,
        BlenderModifiers.BEVEL,
        affect="EDGES" if use_edges else "VERTICES",
        offset_type="WIDTH" if use_width else "OFFSET",
        width=radius.value,
        segments=1 if chamfer else 24,
        limit_method="VGROUP" if vertex_group_name else "ANGLE",
        vertex_group=vertex_group_name or "",
        **kwargs,
    )


def apply_linear_pattern(
    entity_name: str, instance_count, direction: Axis, offset: float, **kwargs
):
    offset_array = [0.0, 0.0, 0.0]

    offset_array[direction.value] = offset

    apply_modifier(
        entity_name,
        BlenderModifiers.ARRAY,
        use_relative_offset=False,
        count=instance_count,
        use_constant_offset=True,
        constant_offset_displace=offset_array,
        **kwargs,
    )


def apply_circular_pattern(
    entity_name: str, instance_count, around_object_name, **kwargs
):
    blender_object = get_object(around_object_name)

    apply_modifier(
        entity_name,
        BlenderModifiers.ARRAY,
        count=instance_count,
        use_relative_offset=False,
        use_object_offset=True,
        offset_object=blender_object,
        **kwargs,
    )


def apply_solidify_modifier(entity_name: str, thickness: Dimension, **kwargs):
    apply_modifier(
        entity_name,
        BlenderModifiers.SOLIDIFY,
        thickness=BlenderLength.convert_dimension_to_blender_unit(thickness).value,
        offset=0,
        **kwargs,
    )


def apply_curve_modifier(entity_name: str, curve_object_name: str, **kwargs):
    curveObject = get_object(curve_object_name)

    apply_modifier(
        entity_name,
        BlenderModifiers.CURVE,
        object=curveObject,
        **kwargs,
    )


def apply_boolean_modifier(
    mesh_object_name: str,
    blender_boolean_type: BlenderBooleanTypes,
    with_mesh_object_name: str,
    **kwargs,
):
    blender_object = get_object(mesh_object_name)
    blender_boolean_object = get_object(with_mesh_object_name)

    assert isinstance(
        blender_object.data, BlenderTypes.MESH.value
    ), f"Object {mesh_object_name} is not an Object. Cannot use the Boolean modifier with {type(blender_object.data)} type."
    assert isinstance(
        blender_boolean_object.data, BlenderTypes.MESH.value
    ), f"Object {with_mesh_object_name} is not an Object. Cannot use the Boolean modifier with {type(blender_boolean_object.data)} type."

    apply_modifier(
        mesh_object_name,
        BlenderModifiers.BOOLEAN,
        operation=blender_boolean_type.name,
        object=blender_boolean_object,
        use_self=True,
        use_hole_tolerant=True,
        # "solver= "EXACT",
        # "double_threshold= 1e-6,
        **kwargs,
    )


def apply_mirror_modifier(
    entity_name: str, mirror_across_entity_name: str, axis: Axis, **kwargs
):
    axis_list = [False, False, False]
    axis_list[axis.value] = True

    blender_mirror_across_object = get_object(mirror_across_entity_name)

    apply_modifier(
        entity_name,
        BlenderModifiers.MIRROR,
        mirror_object=blender_mirror_across_object,
        use_axis=axis_list,
        use_mirror_merge=False,
        **kwargs,
    )


def apply_screw_modifier(
    entity_name: str,
    angle: Angle,
    axis: Axis,
    screw_pitch: Dimension = Dimension(0),
    iterations=1,
    entity_name_to_determine_axis=None,
    resolution=16,
    **kwargs,
):
    # https://docs.blender.org/api/current/bpy.types.ScrewModifier.html
    properties = {
        "axis": axis.name,
        "angle": angle.value,
        "screw_offset": BlenderLength.convert_dimension_to_blender_unit(
            screw_pitch
        ).value,
        "steps": resolution,
        "render_steps": resolution,
        "use_merge_vertices": True,
        "iterations": iterations,
    }

    if entity_name_to_determine_axis:
        blender_mirror_across_object = get_object(entity_name_to_determine_axis)

        properties["object"] = blender_mirror_across_object

    apply_modifier(entity_name, BlenderModifiers.SCREW, **properties, **kwargs)
