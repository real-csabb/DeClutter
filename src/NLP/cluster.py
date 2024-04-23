import math
import numpy as np
#from embed import embed
from sklearn.cluster import k_means
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import LeaveOneOut
from scipy.stats import loguniform


# Performs LDA clustering with random hyperparameter search
# Inspiration from https://towardsdatascience.com/practical-guide-to-topic-modeling-with-lda-05cd6b027bdf
def random_search(ocr_dict):
    max_num_clusters = len(ocr_dict)
    doc_topic_prior_space = [.001, 1]
    topic_word_prior_space = [.001, 1]
    learning_decay_space = [0.5, 1]
    learning_offset_space = [1, 1000]
    batch_size_space = [1, 128]

    num_iters = 2

    # Extract and tokenize words from text
    vectorizer = CountVectorizer(stop_words='english')
    document_term_matrix = vectorizer.fit_transform(ocr_dict.values())
    feature_names = vectorizer.get_feature_names_out()

    loo = LeaveOneOut()
    num_splits = loo.get_n_splits(document_term_matrix)

    best_score = None
    params = None

    for i in range(num_iters):
        # Randomly select params
        n_components = np.random.randint(1, max_num_clusters + 1)
        doc_topic_prior = loguniform.rvs(*doc_topic_prior_space)
        topic_word_prior = loguniform.rvs(*topic_word_prior_space)
        learning_decay = loguniform.rvs(*learning_decay_space)
        learning_offset = loguniform.rvs(*learning_offset_space)
        batch_size = int(loguniform.rvs(*batch_size_space))

        # Run LDA
        lda = LatentDirichletAllocation(n_components=n_components,
                                        doc_topic_prior=doc_topic_prior,
                                        topic_word_prior=topic_word_prior,
                                        learning_decay=learning_decay,
                                        learning_offset=learning_offset,
                                        batch_size=batch_size)

        total_score = 0

        for train_indices, test_index in loo.split(document_term_matrix):
            # Split data into train and test components
            train_set = document_term_matrix[train_indices]
            test_set = document_term_matrix[test_index]

            lda.fit(train_set)
            total_score += lda.score(test_set)

        print(f'n_components={lda.n_components}\n \
                doc_topic_prior={doc_topic_prior}\n \
                topic_word_prior={topic_word_prior}\n \
                learning_decay={learning_decay}\n \
                learning_offset={learning_offset}\n \
                batch_size={batch_size}\n \
                Avg: {total_score / num_splits}\n')

        if (best_score is None) or (total_score / num_splits > best_score):
            best_score = total_score / num_splits
            params = (n_components, doc_topic_prior, topic_word_prior, learning_decay, learning_offset, batch_size)

    print(best_score)
    return params


# Performs Latent Dirichlet Allocation on a set of texts
# Returns a document term matrix, list of feature names, and the LDA components (see scikit learn docs for
# more info)
def cluster_lda(ocr_dict):
    # Extract and tokenize words from text
    vectorizer = CountVectorizer(stop_words='english')
    document_term_matrix = vectorizer.fit_transform(ocr_dict.values())
    feature_names = vectorizer.get_feature_names_out()
   # vocab = vectorizer.vocabulary_
   #print(vectorizer.vocabulary_)
    #print(feature_names)
    #print(document_term_matrix)

    # Run LDA
    n, doc_topic_prior, topic_word_prior, learning_decay, learning_offset, batch_size = random_search(ocr_dict)
    lda = LatentDirichletAllocation(n_components=n,
                                    doc_topic_prior=doc_topic_prior,
                                    topic_word_prior=topic_word_prior,
                                    learning_decay=learning_decay,
                                    learning_offset=learning_offset,
                                    batch_size=batch_size)
    lda.fit(document_term_matrix)

    return document_term_matrix, feature_names, lda.components_

    # for topic_index, component in enumerate(lda.components_):
    #     word_indexes = component.argsort()[::-1][:10]
    #     topic_words[topic_index] = [feature_names[i] for i in word_indexes]


def cluster_k_means(keywords, num_clusters):
    _, labels, _ = k_means(np.array(embed(keywords)), num_clusters)
    print(labels)


# # Toy implementation of clustering
# def cluster(keywords, cluster_size):
#     labels = [i // cluster_size for i in range(len(keywords))]
#
#     return math.ceil(len(keywords) / cluster_size), labels
