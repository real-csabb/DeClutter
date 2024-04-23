from perform_ocr import perform_ocr
from cluster import cluster_lda, random_search
from test_database_ops import get_file_paths


def test_cluster_lda():
    ocr_dict = perform_ocr(['test_images/onix.jpeg', 'test_images/gaussian.webp', 'test_images/string_theory.png',
        'test_images/toughie.webp',
        'test_images/Pokemon-Go-Memes-Did-You-Hear-About-The-New-Pokemon-Pikachu.jpg',
        'test_images/dark_brandon.png'])
    print(ocr_dict['test_images/Pokemon-Go-Memes-Did-You-Hear-About-The-New-Pokemon-Pikachu.jpg'])
    cluster_lda(ocr_dict)


def test_cluster_lda_random_search():
    #ocr_dict = perform_ocr(get_file_paths('test_files'))
    ocr_dict = perform_ocr(['test_files/at-the-mountains-of-madness.pdf',
                            'test_files/The_Call_of_Cthulhu_-_Lovecraft.pdf',
                            'test_files/355_Earths-Moon.pdf',
                            'test_files/d24106256.pdf'])
    #print(ocr_dict['test_images/Pokemon-Go-Memes-Did-You-Hear-About-The-New-Pokemon-Pikachu.jpg'])
    print(random_search(ocr_dict))
