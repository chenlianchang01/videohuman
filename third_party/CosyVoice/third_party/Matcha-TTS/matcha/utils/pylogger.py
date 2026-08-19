import logging

# [vh2 补丁] lightning 为训练专用依赖,推理场景缺失时用恒等装饰器兜底
try:
    from lightning.pytorch.utilities import rank_zero_only
except ModuleNotFoundError:
    def rank_zero_only(fn):
        return fn


def get_pylogger(name: str = __name__) -> logging.Logger:
    """Initializes a multi-GPU-friendly python command line logger.

    :param name: The name of the logger, defaults to ``__name__``.

    :return: A logger object.
    """
    logger = logging.getLogger(name)

    # this ensures all logging levels get marked with the rank zero decorator
    # otherwise logs would get multiplied for each GPU process in multi-GPU setup
    logging_levels = ("debug", "info", "warning", "error", "exception", "fatal", "critical")
    for level in logging_levels:
        setattr(logger, level, rank_zero_only(getattr(logger, level)))

    return logger
