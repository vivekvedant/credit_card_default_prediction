from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from  sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


model_config = {
    "Knn": KNeighborsClassifier(),
    "logistic_regression":LogisticRegression(n_jobs = -1),
    "decision Tree":DecisionTreeClassifier(),
    "gradientBoosting":GradientBoostingClassifier(),
    "Adaboost":AdaBoostClassifier(),
    "RandomForest":RandomForestClassifier(n_jobs = -1),
    "Xgboost": XGBClassifier(n_jobs  = -1),
    "Lightgboost": LGBMClassifier(n_jobs = -1),
    "catboost": CatBoostClassifier(verbose = 0)
}

