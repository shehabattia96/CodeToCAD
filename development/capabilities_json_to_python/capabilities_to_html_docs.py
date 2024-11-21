"""
A script to generate the HTML docs from capabilities.json + jinja2 templates.
"""

import os
import json
from datetime import datetime
from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)
from development.capabilities_json_to_python.template_utils import get_jinja_environment
from development.capabilities_json_to_python.paths import (
    capabilities_to_python_documentation_html,
)
from development.get_provider_supported_decorators import (
    get_provider_supported_decorators,
)

HTML_DOCS_PROVIDERS = ["Blender", "Fusion360", "Onshape"]

def _get_provider_supports():
    supported_providers = {}

    for provider_name in HTML_DOCS_PROVIDERS:
        supported_providers[provider_name] = get_provider_supported_decorators(
            provider_name
        )

    return supported_providers

def generate_html_for_epoch(epoch, capabilities_data, output_path):
    template = get_jinja_environment().get_template(
        capabilities_to_python_documentation_html
    )
    output_from_parsed_template = template.render(
        capabilities_loader=CapabilitiesLoader(capabilities_data),
        supported_providers=_get_provider_supports(),
        epochs=get_all_epochs()  # Pass the list of epochs to the template
    )
    with open(output_path, "w") as fh:
        fh.write(output_from_parsed_template)

def get_all_epochs():
    return sorted(os.listdir("docs/capabilities/"))

if __name__ == "__main__":
    epochs = get_all_epochs()
    latest_epoch = epochs[-1] if epochs else None

    for epoch in epochs:
        with open(f"docs/capabilities/{epoch}/capabilities.json") as f:
            capabilities_data = json.load(f)
        
        output_path = f"docs/release/{epoch}/docs.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        generate_html_for_epoch(epoch, capabilities_data, output_path)

    # Generate the latest release version
    if latest_epoch:
        with open(f"docs/capabilities/{latest_epoch}/capabilities.json") as f:
            capabilities_data = json.load(f)
        generate_html_for_epoch(latest_epoch, capabilities_data, "docs/release/docs.html")

    # Generate the development version
    with open("codetocad/capabilities.json") as f:
        capabilities_data = json.load(f)
    generate_html_for_epoch("develop", capabilities_data, "docs/develop/docs.html")

    print("HTML documentation generation complete.")