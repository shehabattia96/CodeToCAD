from providers.blender.blender_provider.blender_actions.context import (
    get_context_view_3d,
    update_view_layer,
)
from providers.blender.blender_provider.blender_actions.objects import get_object
from providers.blender.blender_provider.blender_definitions import BlenderTypes
import bpy


def convert_object_using_ops(existing_object_name: str, convert_to_type: BlenderTypes):
    existing_object = get_object(existing_object_name)
    with get_context_view_3d(
        active_object=existing_object, selected_objects=[existing_object]
    ):
        existing_object.select_set(True)
        bpy.context.view_layer.objects.active = existing_object
        update_view_layer()

        bpy.ops.object.convert(target=convert_to_type.name)
