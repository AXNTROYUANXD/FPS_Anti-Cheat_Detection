from lstm.economy_preprocess import economy_preprocess
from lstm.engagement_preprocess import engagement_preprocess
from lstm.lstm import lstm_test, lstm_train
from lstm.movement_preprocess import movement_preprocess


def main(data: str, mode: str) -> None:
    economy_preprocess(data)
    engagement_preprocess(data)
    movement_preprocess(data)

    if mode == 'train':
        lstm_train(data, r'')
    elif mode == 'test':
        lstm_test(data)
    else:
        raise Exception('Invalid mode.')


if __name__ == '__main__':
    data_path = r''
    main(data_path, '')
