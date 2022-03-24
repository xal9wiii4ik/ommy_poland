import typing as tp
import numpy as np
import xgboost as xgb


class MasterComplianceAssessment:
    """
    Assessment of the master's compliance with the order
    """
    def __init__(self):
        self.model = xgb.XGBClassifier()
        self.model.load_model('api/utils/search_masters/ommy_decision_engine_skl_002.json')

    def get_masters_probabilities(self, data: tp.List[tp.List[tp.Union[int, float]]]) -> tp.List[float]:
        """
        Get masters probabilities
        Args:
            data: master data include:
                Profile	Distance	Experience	Number of the work spheres	Friends count
                Orders	Reviews	Rate	Suitable master
        Return:
            list with probabilities
        """

        data = np.array(data)  # type: ignore
        prediction_prob = self.model.predict_proba(data)[:, 1]
        return prediction_prob
