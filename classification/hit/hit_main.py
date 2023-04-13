from classification.hit import cheater_s1_distance_when_damaging, cheater_s2_ratio_of_hits_when_player_is_moving, \
    cheater_s3_ratio_of_hit_group, cheater_s4_hit_precision, hit_data_combine


def main(data_path):
    cheater_s1_distance_when_damaging.main(data_path)
    cheater_s2_ratio_of_hits_when_player_is_moving.main(data_path)
    cheater_s3_ratio_of_hit_group.main(data_path)
    cheater_s4_hit_precision.main(data_path)
    hit_data_combine.main()
