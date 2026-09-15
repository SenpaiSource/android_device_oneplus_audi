import os
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
    with open(filepath, 'r') as f:
        content = f.read()

    if 'config_highResTaskSnapshotScale' in content:
        print(f"Already patched {filepath}")
        return

    insertion = """
    <!-- The amount to scale fullscreen snapshots for Overview and snapshot starting windows. -->
    <item name="config_highResTaskSnapshotScale" format="float" type="dimen">0.7</item>

    <!-- Bytes that the PinnerService will pin for WebView -->
    <integer name="config_pinnerWebviewPinBytes">20971520</integer>
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
