import os

from classification import angle_duration_velocity, flash_nade_shot_main, all_feature_combine
from classification.hit import hit_main


def main(data: str) -> None:
    os.mkdir('./classification/data_to_combine')

    flash_nade_shot_main.main(data)
    # TODO: simplify the aim to kill codes, currently is not user-friendly, skip the execution here
    angle_duration_velocity.main(data)
    hit_main.main(data)
    all_feature_combine.main(data)


if __name__ == '__main__':
    data_path = r''
    main(data_path)
