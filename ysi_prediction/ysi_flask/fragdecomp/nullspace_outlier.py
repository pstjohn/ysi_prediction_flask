import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class NullspaceClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, tol=1E-8):
        self.tol = tol

    def fit(self, X, y=None):
        self.u, self.s, self.v = np.linalg.svd(X, full_matrices=False)
        self.rank = (self.s > self.tol).sum()

    def predict(self, X):
        return np.abs(self.v[self.rank:] @ np.asarray(X).T).sum(0) > self.tol
