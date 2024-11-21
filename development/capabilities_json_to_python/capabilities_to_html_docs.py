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
    
    # print(output_from_parsed_template);
    
    # Ensure the output directory exists before writing the file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding='utf-8') as fh:
        fh.write(output_from_parsed_template)

def get_all_epochs():
    return sorted(os.listdir("docs/capabilities/"))

if __name__ == "__main__":
    epochs = get_all_epochs()
    latest_epoch = epochs[-1] if epochs else None

    for epoch in epochs:
        with open(f"docs/capabilities/{epoch}") as f:
            capabilities_data = json.load(f)
        
        output_path = f"docs/{epoch}"
        generate_html_for_epoch(epoch, f"docs/capabilities/{epoch}", output_path)

    # Generate the latest release version
    if latest_epoch:
        with open(f"docs/capabilities/{latest_epoch}") as f:
            capabilities_data = json.load(f)
        generate_html_for_epoch(latest_epoch, f"docs/capabilities/{latest_epoch}", "docs/release/docs.html")

    # Generate the development version
    with open("codetocad/capabilities.json") as f:
        capabilities_data = json.load(f)
        
    capabilities_data_path = "codetocad/capabilities.json"
    generate_html_for_epoch("develop", "codetocad/capabilities.json", "docs/develop/docs.html")

    print("HTML documentation generation complete.")