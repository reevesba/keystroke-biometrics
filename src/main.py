''' Model Keystroke Biometrics Data

Author: Bradley Reeves
Date: May 27, 2021

'''

import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    BaggingClassifier, AdaBoostClassifier,
    RandomForestClassifier, VotingClassifier
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV
)
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import ConvergenceWarning
from warnings import simplefilter
from prettytable import PrettyTable


def main():
    simplefilter('ignore', category=ConvergenceWarning)

    # Output file
    f = open('../out/results.txt', 'w+')

    # Load the dataset
    dataset = pd.read_csv("../dat/keystroke_biometrics.csv")

    # Train/test split
    X, y = dataset.iloc[:, :15], dataset.iloc[:, 15:]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.75, shuffle=True
    )

    ''' Test different classifiers with default parameters.
    '''
    estimators = [
        MultinomialNB(),
        LogisticRegression(),
        KNeighborsClassifier(),
        LinearSVC(),
        DecisionTreeClassifier(),
        BaggingClassifier(DecisionTreeClassifier()),
        AdaBoostClassifier(DecisionTreeClassifier()),
        RandomForestClassifier(),
        VotingClassifier([
            ('mnb', MultinomialNB()), ('lr', LogisticRegression()),
            ('rf', RandomForestClassifier()), ('svm', LinearSVC())
        ]),
        MLPClassifier()
    ]

    table = PrettyTable(['Algorithm', 'Score'])
    for estimator in estimators:
        scores = cross_val_score(estimator, X, y.values.ravel(), cv=5)
        table.add_row([estimator.__class__.__name__, np.mean(scores)])
    f.write('Estimator Summary\n')
    f.write(str(table) + '\n\n')

    '''Grid search best classifiers
    '''
    pipe = Pipeline(steps=[('classifier', RandomForestClassifier())])

    search_space = [{
        'classifier': [RandomForestClassifier()],
        'classifier__n_estimators': [10, 100, 1000],
        'classifier__max_depth': [5, 10, 15],
        'classifier__min_samples_leaf': [1, 2, 5, 10],
        'classifier__max_leaf_nodes': [2, 5, 10]
        }, {
        'classifier': [KNeighborsClassifier()],
        'classifier__n_neighbors': [5, 11, 15],
        'classifier__weights': ['uniform', 'distance'],
        'classifier__metric': ['euclidean', 'manhattan']
    }]

    gs = GridSearchCV(pipe, search_space, cv=5, n_jobs=1, verbose=10)
    results = gs.fit(X_train, y_train.values.ravel())

    f.write('Best Estimator\n')
    f.write(str(results.best_estimator_) + '\n\n')

    f.write('Best Score\n')
    f.write(str(results.best_score_) + '\n\n')

    # Classify test data
    predictions = results.predict(X_test)
    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    f.write('Classification Report\n')
    f.write(str(report) + '\n\n')

    f.write('Confusion Matrix\n')
    f.write(str(matrix))
    f.close()


if __name__ == "__main__":
    main()
