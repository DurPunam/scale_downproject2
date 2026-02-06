from __future__ import annotations

import numpy as np
from sklearn.linear_model import Ridge


class AlignmentModel:
    def __init__(self) -> None:
        self._model = Ridge(alpha=1.0)
        self._fitted = False

    def fit(self, compressed: np.ndarray, original: np.ndarray) -> None:
        self._model.fit(compressed, original)
        self._fitted = True

    def transform(self, compressed: np.ndarray) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Alignment model not trained")
        return self._model.predict(compressed)
