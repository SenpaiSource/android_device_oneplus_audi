import os
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
    with open(filepath, 'r') as f:
        content = f.read()

    if 'config_defaultPinnerServiceFiles' in content:
        print(f"Already patched {filepath}")
        return

    insertion = """
    <!-- Array of files to pin to the memory via PinnerService -->
    <string-array translatable="false" name="config_defaultPinnerServiceFiles">
        <item>"/vendor/lib64/libsdmextension.so"</item>
        <item>"/vendor/lib64/libllvm-qgl.so"</item>
    </string-array>
"""
    
    # Insert before </resources>
    if '</resources>' in content:
        content = content.replace('</resources>', insertion + '</resources>')
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Failed to find </resources> in {filepath}")

patch_file("overlay/OPlusFrameworksResTarget/res/values/config.xml")
