from time import time

from ocp_vscode import show_all

from bd_extrusions.vslot import VSlotProfile

start = time()
vslot = VSlotProfile.box(1, 1)
print(f"Time: {time() - start}")

show_all()
