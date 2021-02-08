import os
import os.path as osp
from pathlib import Path
import yaml
import TDDFA

root_module_path = Path(TDDFA.__path__[0])


def make_abs_path(file, relative_path) -> str:
    """Returns the absolute path constructed from a path relative to a module's
    parent directory.

    Parameters
    ----------
    file : str or pathlib Path
        The module's __file__ attribute, i.e. the path of its file.
    relative_path : str or pathlib Path
        The path relative to the module's parent directory.

    Returns
    -------
    abs_path : str or pathlib Path
        The path converted to absolute.

    """
    parent_dir = osp.dirname(osp.realpath(file))
    return osp.join(parent_dir, relative_path)


def read_config_file(config_file, relative: bool = True) -> dict:
    """Reads a configuration file, making paths relative to the TDDFA module's
    root folder, if requested.

    Parameters
    ----------
    config_file : os.pathlike
        The path of the configuration file.
    relative : bool
        Whether the paths in the configuration file will be made relative to
        the TDDFA module's root directory.

    Returns
    -------
    cfg : dict
        The loaded configuration file

    """
    cfg = yaml.load(open(config_file), Loader=yaml.SafeLoader)

    if relative:
        for key in ['checkpoint_fp', 'bfm_fp']:
            if key in cfg:
                relative_path = Path(cfg[key])
                abs_path = root_module_path / relative_path
                cfg[key] = os.fspath(abs_path)
    return cfg
