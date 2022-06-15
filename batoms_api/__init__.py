import pickle
import os


def render(
    atoms,
    batoms_input={},
    render_input={},
    display=False,
    queue=None,
    post_modifications=[],
):
    """
    atoms: an ASE atoms object
    batoms_input: input parameters to create the Batoms object
    render_input: input parameters to create the Render object
    post_modifications: list of commands to be evaluated following the given sequences
    """
    with open(".batoms.inp", "wb") as f:
        pickle.dump([atoms, batoms_input, render_input, post_modifications], f)
    #
    blender_cmd = "blender"
    if "BLENDER_COMMAND" in os.environ.keys():
        blender_cmd = os.environ["BLENDER_COMMAND"]
    root = os.path.normpath(os.path.dirname(__file__))
    script = os.path.join(root, "script-api.py")
    if display:
        cmd = blender_cmd + " -P " + script
    elif queue == "SLURM":
        cmd = "srun -n $SLURM_NTASKS " + blender_cmd + " -b " + " -P " + script
    else:
        cmd = blender_cmd + " -b " + " -P " + script
    errcode = os.system(cmd)
    if errcode != 0:
        raise OSError("Command " + cmd + " failed with error code %d" % errcode)
