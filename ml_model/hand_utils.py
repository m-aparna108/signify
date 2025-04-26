import copy

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []

    for lm in landmarks.landmark:
        x = min(int(lm.x * image_width), image_width - 1)
        y = min(int(lm.y * image_height), image_height - 1)
        landmark_point.append([x, y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = temp_landmark_list[0]
    for index in range(len(temp_landmark_list)):
        temp_landmark_list[index][0] -= base_x
        temp_landmark_list[index][1] -= base_y

    # Flatten
    temp_landmark_list = [coord for point in temp_landmark_list for coord in point]

    # Normalize
    max_value = max(list(map(abs, temp_landmark_list)))
    if max_value != 0:
        temp_landmark_list = list(map(lambda x: x / max_value, temp_landmark_list))

    return temp_landmark_list
