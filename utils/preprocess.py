#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/25 上午10:01
# @Author  : Lan Jiang
# @File    : preprocess.py

import os
import pandas as pd
import argparse
import pickle
import progressbar
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def preprocess_title(title):
    title = title.lower()
    # Remove Punctuation
    title = title.translate(str.maketrans('', '', string.punctuation))
    # Remove whitespaces and tokenize
    tokens_title = title.strip().split()
    # Remove stopwords
    tokens_title = [word for word in tokens_title if not word in stopwords.words()]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemm_text = [lemmatizer.lemmatize(word) for word in tokens_title]
    prepped_title = ' '.join(lemm_text)
    return prepped_title


def build_corpus(data_dir):
    titles = pd.read_csv(os.path.join(data_dir, "train.csv"))['title'].tolist()
    std_titles = []
    p = progressbar.ProgressBar()
    for i in p(range(len(titles))):
        title = titles[i]
        std_titles.append(preprocess_title(title))
    return std_titles


def load_corpus(args):
    aux_file = os.path.join(args.result_dir, "tok_corpus.pickle")
    if not os.path.exists(aux_file):
        print("building corpus matrix from raw data...")
        corpus = build_corpus(args.data_dir)
        if not os.path.exists(args.result_dir):
            os.mkdir(args.result_dir)
        with open(aux_file, "wb") as f:
            pickle.dump(corpus, f)
        print("building corpus over.")
    else:
        print("load weights matrix from cached file: ", aux_file)
        with open(aux_file, "rb") as f:
            corpus = pickle.load(f)
        print("load over.")
    return corpus


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--result_dir", type=str, default="../result/text")
    args = parser.parse_args()

    tok_corpus = load_corpus(args)
    corpus = [' '.join(item) for item in tok_corpus]
    raw_data = pd.read_csv(os.path.join(args.data_dir, "train.csv"))

    raw_data['std_title'] = corpus
    raw_data.to_csv(os.path.join(args.data_dir, "train.csv"), index=False)
    print("Write std file over.")
