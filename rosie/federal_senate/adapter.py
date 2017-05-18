import os

import numpy as np
import pandas as pd
from serenata_toolbox.federal_senate.federal_senate_dataset import FederalSenateDataset
from serenata_toolbox.datasets import fetch

COLUMNS = {
    'net_value': 'total_net_value',
    'recipient_id': 'cnpj_cpf',
    'recipient': 'supplier',
}

class Adapter:
    def __init__(self, path):
        self.path = path

    @property
    def dataset(self):
        path = self.update_datasets()
        self._dataset = pd.read_csv(path, dtype={'cnpj_cpf': np.str}, encoding = "utf-8")
        self.prepare_dataset()

        return self._dataset

    def prepare_dataset(self):
        self.prepare_cpnj_cpf()
        self.rename_columns()

    def prepare_cpnj_cpf(self):
        self._dataset = self._dataset[self._dataset['cnpj_cpf'].notnull()]
        self._dataset['document_type'] = 'simple_receipt'

    def rename_columns(self):
        columns = {v: k for k, v in COLUMNS.items()}
        self._dataset.rename(columns=columns, inplace=True)

    def update_datasets(self):
        os.makedirs(self.path, exist_ok=True)
        federal_senate = FederalSenateDataset(self.path)
        federal_senate.fetch()
        federal_senate.translate()
        federal_senate_reimbursements_path = federal_senate.clean()

        return federal_senate_reimbursements_path

