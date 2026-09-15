import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
    with open(filepath, 'r') as f:
        content = f.read()

    if 'SPAMMY_LOG_TAGS' in content:
        print(f"Already patched {filepath}")
        return

    insertion = """
# Silence spammy vendor logs
SPAMMY_LOG_TAGS := \\
    Diag_Lib \\
    AGM \\
    AHAL \\
    CamX

ifneq ($(TARGET_BUILD_VARIANT),eng)
PRODUCT_VENDOR_PROPERTIES += \\
    $(foreach tag,$(SPAMMY_LOG_TAGS),log.tag.$(tag)=S)
endif
"""
    
    # Insert before the inherit-product for common.mk or at the end
    target = "# Inherit from the common OEM chipset makefile."
    if target in content:
        content = content.replace(target, insertion + "\n" + target)
    else:
        content += "\n" + insertion
        
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file("device.mk")
