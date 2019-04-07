#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xxhash
from os import listdir


class TextComparer:
    def __init__(self, shingle_length, path_to_text_storage, threshold):
        self.shingle_length = shingle_length
        self.full_path_and_names = self.__get_path_to_storage_files(path_to_text_storage)
        self.threshold = threshold

    def find_similar_text(self, new_text):
        hashed_new_text = self.__hashing_shingles(self.__split_into_shingles(self.__canonize_text(new_text)))
        too_similar = []
        for file_fullpath, text_name in self.full_path_and_names:
            with open(file_fullpath, 'r') as text:
                hashed_text = self.__hashing_shingles(self.__split_into_shingles(self.__canonize_text(text.read())))
                match_precentage = self.__compare_hashed_text(hashed_new_text, hashed_text)
                if match_precentage > self.threshold:
                    too_similar.append(text_name)
        return too_similar

    def __get_path_to_storage_files(self, path_to_storage):
        file_names = listdir(path_to_storage)
        full_paths = []
        for name in file_names:
            full_paths.append((path_to_storage + '/' + name, name))
        return full_paths

    def __compare_hashed_text(self, hashed_shingles1, hashed_shingles2):
        equ_counter = 0
        for shingle1 in hashed_shingles1:
            if shingle1 in hashed_shingles2:
                equ_counter += 1
        return (equ_counter / float(len(hashed_shingles1))) * 100

    def __canonize_text(self, text):
        stop_characters = ',!/.\'\n\t\"#@$%^&*()[]{}:;<>?'
        return [word for word in [word.strip(stop_characters) for word in text.lower().split()] if word]

    def __split_into_shingles(self, words_array):
        shingles = []
        for ind in range(len(words_array) - self.shingle_length + 1):
            shingles.append(''.join([word for word in words_array[ind:ind + self.shingle_length]]))
        return shingles

    def __hashing_shingles(self, shingles):
        return [xxhash.xxh64_intdigest(shingle) for shingle in shingles]
