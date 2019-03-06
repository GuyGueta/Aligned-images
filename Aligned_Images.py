####################################################
# FILE: ex6.py
# WRIETER: guy gueta, guy245, 203428222
# EXERCISE: ex6
# DESCRIPTION: a file that contains a number of functions that work on an
# image and makes actions on it , the main function
#  revives an image source load makes corrections on that image and save it
############################################################################

import Aligned_Images_Helper
import math
import sys

DEFAULT_GRADE = 0
DEFAULT_VAL = 0
BLACK_VAL = 0
WHITE_VAL = 255
DEFAULT_VARIANCE = 0
DEFAULT_SUM = 0
RATIO = 8
CORRECTION = -1
RATIO_AVG = 9
DEFAULT_COUNT = 0
DEFAULT_RANK = 0
ARG_NUMBER = 3
ERROR_MSG = "Wrong number of parameters. The correct usage is: ex6.py " \
            "<image_source> <output > <max_diagonal>"


def variance_calculation(blacks, black_sum, whites, whites_sum):
    """this an help function to otsu the functions takes 4 params the
    number of black and whites pixel ,
    and each cooler sum , and returns a number that is a result of a
    mathematical expression cobain these 4"""
    if whites == 0 or black_sum == 0:
        variance = DEFAULT_VARIANCE
    else:
        whites_mean = (whites_sum / whites)
        black_mean = (black_sum / blacks)
        variance = blacks * whites * ((black_mean - whites_mean) ** 2)
    return variance


def otsu(image):
    """ the function takes an image and choose for her what is the best
    threshold number from the range of 256 and returns it by using
    variance_calculation """
    variance = DEFAULT_VAL
    threshold = DEFAULT_VAL
    for i in range(256):
        blacks = DEFAULT_VAL
        whites = DEFAULT_VAL
        black_sum = DEFAULT_VAL
        white_sum = DEFAULT_VAL
        for row in image:
            for pixel in row:
                if pixel < i:
                    blacks += 1
                    black_sum += pixel
                else:
                    whites += 1
                    white_sum += pixel
        new_var = variance_calculation(blacks, black_sum, whites, white_sum)
        if new_var > variance:
            variance = new_var
            threshold = i
    return threshold


def threshold_filter(image):
    """the function takes an image and returns anew image that here pixel
    are or black or white by using otsu """
    threshold = otsu(image)
    new_image = [][:]
    for row in image:
        new_row = [][:]
        for pixel in row:
            if pixel < threshold:
                pixel = BLACK_VAL
                new_row.append(pixel)
            else:
                pixel = WHITE_VAL
                new_row.append(pixel)
        new_image.append(new_row)
    return new_image


def is_valid(i, j, matrix):
    """ this is an help function to cuppule of functions  , its received a
    matrix that represents an image and  raw and col index then checks if the
    index is out of the matrix range and returns True / False  """
    if i < 0 or j < 0:
        return False
    if i >= len(matrix) or j >= len(matrix[0]):
        return False
    return True


def sum_for_pixel(raw, col, image, filter):
    """ this is an help function to apply filter its sum a value for pixel by
    using the image ,and her raw and col index ,than its make the
    mathematical calculation after using is_valid to cheaks if the index
    are inside the image value and returns it """
    filter_mtrx = filter
    top = raw - CORRECTION  # help to check if the index out of range
    left = col - CORRECTION  # help to check if the index out of range
    sum_val = 0
    for i in range(3):
        for j in range(3):
            if is_valid(top + i, left + j, image):
                sum_val += image[top + i][left + j] * filter_mtrx[i][j]
            else:
                sum_val += image[raw][col] * filter_mtrx[i][j]
    return sum_val


def apply_filter(image, filter):
    """ the function recieves an image and a filter and returns a new image
    in the size of the old one  that every pixel in her is the sum that
    we get by using sum_for_pixel for the pixel in the asme index in the
    old image and returns it """
    filter_mtrx = filter
    new_image = []
    for i in range(len(image)):
        new_raw = []
        for j in range(len(image[0])):
            new_pixel = sum_for_pixel(i, j, image, filter_mtrx)
            new_raw.append(new_pixel)
        new_image.append(new_raw)
    return new_image


def help_detect_edges(raw, col, image):
    """ this is an help function to detect_edges the function receives an
    image  her raw and col index and returns a value for a pixel that been
     calculate for every pixel in the image by using is valid function """
    top = raw - CORRECTION  # help to check if the index out of range
    left = col - CORRECTION  # help to check if the index out of range
    sum_val = DEFAULT_VAL
    for i in range(3):
        for j in range(3):
            if is_valid(top + i, left + j, image):
                sum_val += image[top + i][left + j]
            else:
                sum_val += image[raw][col]
    return sum_val


def detect_edges(image):
    """ the function recives an image  and returns a new image after she
    making for each pixel in the old image a mathematical calculation using
    help_detect_edges and and adding the result to the new image exsectly
    in the same index it in the new image at he same  index, then returns
    the new image """
    new_image = []
    for i in range(len(image)):
        new_raw = []
        for j in range(len(image)):
            correction = (help_detect_edges(i, j, image) - image[i][j]) / \
                         RATIO
            new_pixel = image[i][j] - correction
            if new_pixel < 0:
                new_pixel = new_pixel * CORRECTION
            new_raw.append(int(new_pixel))
        new_image.append(new_raw)
    return new_image


def average_sum(raw, col, image):
    """ this is an help function to downsample_by_3 the function receives an
    image  her raw and col index and returns a value for a pixel that been
     calculate for every pixel in the image  by using is vailed function"""
    top = raw - CORRECTION  # help to check if the index out of range
    left = col - CORRECTION  # help to check if the index out of range
    sum_val = DEFAULT_VAL
    for i in range(3):
        for j in range(3):
            if is_valid(top + i, left + j, image):
                sum_val += image[top + i][left + j]
            else:
                sum_val += image[raw][col]
    return int(sum_val / RATIO_AVG)


def downsample_by_3(image):
    """ the function recives an image and returns a new image that her size of
    index are smaller by 3 by using average_sum"""
    new_list = []
    for i in range(1, len(image), 3):
        new_raw = []
        for j in range(1, len(image[0]), 3):
            new_pixel = average_sum(i, j, image)
            new_raw.append(new_pixel)
        new_list.append(new_raw)
    return new_list


def downsample(image, max_diagonal_size):
    """ the function recieves an image and an int / float value that is the
    max size of a diagonal that the user choose and returns a new image
    that her size is so that her diagonal is smaller or eqoule to the size
    the user insert"""
    mtrx = image
    max_diagonal = math.sqrt((len(mtrx) * 2) + len(mtrx[0] * 2))
    while max_diagonal > max_diagonal_size:
        mtrx = downsample_by_3(mtrx)
        max_diagonal = math.sqrt((len(mtrx) * 2) + len(mtrx[0] * 2))
    return mtrx


def dist_calculation(i, j, lst):
    """ the function get a list of pixsel and 2 index that represent the
    pixsel in the list and calculate the dist between those 2 pixel and
    returns it """
    calculation = math.sqrt(
        ((lst[i][0] - lst[j][0]) ** 2) + ((lst[i][1] - lst[j][1]) ** 2))
    return calculation


def rank_for_line(lst):
    """ the function recies an list of pixel and for that list its cheaks
    how many patterns we have on that list ,calculate there distance
    with dist_calculations and  then calculate each patter rank and add it
    to the total rank of the lsr .the functions reterns the sum rank """
    if not lst:
        return DEFAULT_RANK
    new_list = [lst[0]]
    sum_rank = DEFAULT_RANK
    for i in range(1, len(lst)):
        calculation = dist_calculation(i - 1, i, lst)
        if calculation <= 2:
            new_list.append(lst[i])
        else:
            if len(new_list) < 2:
                new_list = [lst[i]]
            else:
                rank = int((dist_calculation(0, len(new_list) - 1, new_list)
                            ** 2))
                new_list = [lst[i]]
                sum_rank += rank
        if i == len(lst) - 1 and len(new_list) >= 2:
            last_rank = int(dist_calculation(0, len(new_list) - 1,
                                             new_list) ** 2)
            sum_rank += last_rank
    return sum_rank


def list_of_whites(pixel_lst, image):
    """ the function returns a list of pixel and the image of the pixsel
    and for each one chaeks if he is white ,if so she add him up to a new
    lst and returns that list """
    lst = pixel_lst
    whites_list = []
    for i in range(len(lst)):
        if image[lst[i][0]][lst[i][1]] == WHITE_VAL:
            whites_list.append(lst[i])
    return whites_list


def get_angle(image):
    """ the function recives an image and by using list_of_whies and
    rank_for_line and return the angle from the range of 180 that got the
    best ranking and returns it """
    length = len(image)
    width = len(image[0])
    distance = int(math.sqrt(length ** 2 + width ** 2))
    max_rank = DEFAULT_RANK
    best_angle = DEFAULT_VAL
    for angle in range(180):
        rank = DEFAULT_RANK
        if 0 < angle < 90:
            for dist in range(distance):
                pixel_lst = ex6_helper.pixels_on_line(image,
                                                      math.radians(angle),
                                                      dist, True)
                rank += rank_for_line(list_of_whites(pixel_lst, image))
                new_pixel_lst = ex6_helper.pixels_on_line(image, math.radians(
                    angle), dist, False)
                rank += rank_for_line(list_of_whites(new_pixel_lst, image))
        else:
            for dist in range(distance):
                pixel_lst = ex6_helper.pixels_on_line(image,
                                                      math.radians(angle),
                                                      dist, True)
                rank += rank_for_line(list_of_whites(pixel_lst, image))
        if rank > max_rank:
            max_rank = rank
            best_angle = angle
    return best_angle


def new_image_borders(length, width, angle):
    """ the function receives a length and width of an image ,an angle that
     the user choose and returns the the length and width of the new image
     after making a mathematical calculation , the logic of that calculation
     explained in README"""
    new_length = length * math.cos(abs(math.radians(angle))) + width * \
                                         math.sin(abs(math.radians(angle)))
    new_width = width * math.cos(abs(math.radians(angle))) + length * \
                                        math.sin(abs(math.radians(angle)))
    return int(new_length), int(new_width)


def create_black_image(raw, col):
    """ the function receives the an index of raw and col of an image and
    returns an image at that size ,that contains only black pixels """
    black_mtrx = []
    for i in range(raw):
        black_raw = []
        for j in range(col):
            black_raw.append(BLACK_VAL)
        black_mtrx.append(black_raw)
    return black_mtrx


def raw_change(i, j, angle):
    """ the function receives a raw and col index and an angle , and returns
    a new raw index that is a result of the mathematical calculation
    describe below """
    new_raw_index = math.cos(math.radians(angle)) * i - \
                    math.sin(math.radians(angle)) * j
    return new_raw_index


def col_change(i, j, angle):
    """ the function receives a raw and col index and an angle , and returns
        a new col index that is a result of the mathematical calculation
        describe below """
    new_col_index = math.sin(math.radians(angle)) * i + math.cos(
        math.radians(angle)) * j
    return new_col_index


def cheak_if_inside(raw, col, angle, black_image, image):
    """ the function resives a black image and her raw and col index an
    image and an angle . the functions gives for every raw and col index a
    new value by using raw_change and col_change ,after she make the change
    she  cheaks if the indeax is in the range of the col and raw of the
    regular image if so its returns the new raw and col value if not
    returns False ,False """
    mid_lenth_black = int(len(black_image) / 2)
    mid_width_black = int(len(black_image[0]) / 2)
    mid_lenth_image = int(len(image) / 2)
    mid_width_image = int(len(image[0]) / 2)
    new_raw, new_col = raw_change(raw - mid_lenth_black, col -
                                  mid_width_black, angle) + mid_lenth_image, \
                       col_change(raw - mid_lenth_black,
                                  col - mid_width_black,
                                  angle) + mid_width_image
    if int(new_raw) in range(int(len(image))):
        if int(new_col) in range(int(len(image[0]))):
            return int(new_raw), int(new_col)
    return False, False


def rotate(image, angle):
    """ the function receives an image and an angle that the user insert ,
    and returns a new image that is the image that we insert just inserted
    ,just rotated by the angle , the func using cheak_if _inside ,
    new_image borders and create_black_image."""
    mtrx = image
    new_lenth, new_width = new_image_borders(len(mtrx), len(mtrx[0]), angle)
    new_rotate_image = create_black_image(new_lenth, new_width)
    for i in range(len(new_rotate_image)):
        for j in range(len(new_rotate_image[0])):
            new_raw, new_col = cheak_if_inside(i, j, angle, new_rotate_image,
                                               mtrx)
            if new_raw and new_col:
                new_rotate_image[i][j] = image[new_raw][new_col]
    return new_rotate_image


def make_correction(image, max_diagonal):
    """ the function recives a image and a anumber that the user choose to
    represent the max diagonal of the new image he wants , that the
    function returns a new corected image after using the funcs  downsample ,
    thershold_filter, detect_edges , get angle ,rotate """
    new_image = downsample(image, max_diagonal)
    new_image = threshold_filter(new_image)
    new_image = detect_edges(new_image)
    new_image = threshold_filter(new_image)
    angle = get_angle(new_image) * CORRECTION  # we want to corect the angel
    # we get in get angle
    final_image = rotate(image, angle)
    return final_image


def photo_correction(image_source, output_name, max_diagonal):
    """ the func revives an image source load it with ex6_helper.load image
    makes corrections on that image depends on the value of the max
    diagonal the user insert and saves the new image with ex6_helper.save,"""
    image = ex6_helper.load_image(image_source)
    corrected_image = make_correction(image, max_diagonal)
    ex6_helper.save(corrected_image, output_name)


def main():
    """runs the program (photo_correction) after checking input propriety
        (arguments)"""
    if __name__ == '__main__':
        if len(sys.argv) != ARG_NUMBER + 1:
            print(ERROR_MSG)
        else:
            photo_correction(sys.argv[1], sys.argv[2], int(sys.argv[3]))


main()
