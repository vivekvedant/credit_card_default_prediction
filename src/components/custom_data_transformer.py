
from sklearn.base import BaseEstimator, TransformerMixin
import re
from src.utils import read_yaml
from src.constant.training_pipeline import SCHEMA_FILENAME,ROOT_DIR,ARTIFACT_DIR
import os

class NumericalTransformer(BaseEstimator, TransformerMixin):
        
    def fit(self,X):
        return self
    
    def get_columns_by_pattern(self,pattern,X):
        r = re.compile(pattern)
        return list(filter(r.match, X.columns)) 
     
    def get_delay(self,X,col):
        if X[col].min() < 0:
            delay_values = []
            for value in X[col]:
                if value > 0:
                    delay_values.append(0)
                else:
                    delay_values.append(1)
            X["{}_dealy".format(col)] = delay_values
        else:
            X["{}_dealy".format(col)] = -1
        return X[col]
        
    def get_delay_sum(self,X):
        X['pay_delay_sum'] = X[self.get_columns_by_pattern("PAY_[0-9]_dealy",X)].sum(axis = 1)
        return X
    
    def get_bill_pay_diff(self,X):
        for inx in range(1,6):
            X[f"bill_pay_diff_{inx}"] = X[f"PAY_AMT{inx}"] - X[f"BILL_AMT{inx}"]
        return X
    
    def get_bill_amount_mean(self,X):
        for name in ["BILL_AMT","PAY_AMT"]:
            X[f"{name}_mean"] = X[self.get_columns_by_pattern(f"{name}[0-9]",X)].mean(axis = 1)
        return X
    
    def transform(self,X,y = None):
        for col in self.get_columns_by_pattern("PAY_[0-9]",X):
            X [col]= self.get_delay(X,col)
        X = self.get_bill_amount_mean(X)
        X = self.get_bill_pay_diff(X)
        X = self.get_delay_sum(X)
        
        return X


class CategoricalTransformer(BaseEstimator,TransformerMixin):
    
    def fit(self,X):
        return self
    
    def transform(self,X):
        categorical_yaml = read_yaml(os.path.join(ROOT_DIR,ARTIFACT_DIR,SCHEMA_FILENAME))['categorical']
        for col in categorical_yaml.keys():
            X[col] = X[col].replace(categorical_yaml[col])

        return X
    