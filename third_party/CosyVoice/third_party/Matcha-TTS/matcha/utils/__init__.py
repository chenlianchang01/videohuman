# [vh2 补丁] 训练专用的 import(lightning 等重依赖)改为惰性可选,
# 推理只用到 pylogger/audio 等轻量模块,避免为跑推理安装 lightning。
from matcha.utils.pylogger import get_pylogger

try:
    from matcha.utils.instantiators import instantiate_callbacks, instantiate_loggers
    from matcha.utils.logging_utils import log_hyperparameters
    from matcha.utils.rich_utils import enforce_tags, print_config_tree
    from matcha.utils.utils import extras, get_metric_value, task_wrapper
except ModuleNotFoundError:  # 训练依赖(lightning/hydra 等)未安装时静默跳过
    pass
