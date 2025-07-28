
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score, matthews_corrcoef, roc_auc_score, roc_curve

import torch
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # 检查GPU

cur_file_path = Path(__file__).resolve()

pkg_dir_path = cur_file_path.parent
data_dir_path = pkg_dir_path / "data"
data_input_dir_path = data_dir_path / "input"
data_output_dir_path = data_dir_path / "output"

assert cur_file_path.exists()
assert pkg_dir_path.exists()
assert data_dir_path.exists()
assert data_input_dir_path.exists()
assert data_output_dir_path.exists()


sample_labels_file_path = pkg_dir_path.parent / 'survival/data/output/sample-labels-sf.csv'
assert sample_labels_file_path.exists()

gene_file_path = pkg_dir_path.parent / 'gene/data/output/wgcna.csv'
assert gene_file_path.exists()

copy_number_file_path = pkg_dir_path.parent / "gene/data/output/copy-number.csv"
assert copy_number_file_path

save_resnet_feature_dir_path = pkg_dir_path.parent / "graphy/data/output/resnet-features"
save_bert_feature_dir_path = pkg_dir_path.parent / "report/data/output/bert-features"

import pandas as pd
def load_gene_data_by_sample_key(sample_key_list):
    # 导入 gene 数据
    gene_df = pd.read_csv(gene_file_path, index_col=0).T
    gene_key_list = gene_df.index.tolist()
    if len(gene_key_list) < len(sample_key_list):
        not_in_gene_key = []
        for sample_key in sample_key_list:
            if sample_key not in gene_key_list:
                not_in_gene_key.append(sample_key)
        for gene_key in not_in_gene_key:
            new_row = {col:0 for col in gene_df.columns}
            gene_df.loc[gene_key] = new_row
    gene_key_list = gene_df.index.tolist()
    # print(f"gene 样本数量: {len(gene_key_list)}")

    gene_df = gene_df.loc[sample_key_list, :]
    return gene_df


def load_cnv_data_by_sample_key(sample_key_list):
    # 导入 cnv 数据
    cnv_df = pd.read_csv(copy_number_file_path, index_col=0).T

    cnv_key_list = cnv_df.index.tolist()
    if len(cnv_key_list) != len(sample_key_list):
        not_in_cnv_key = []
        for sample_key in sample_key_list:
            if sample_key not in cnv_key_list:
                not_in_cnv_key.append(sample_key)
        for cnv_key in not_in_cnv_key:
            new_row = {col:0 for col in cnv_df.columns}
            cnv_df.loc[cnv_key] = new_row
    cnv_key_list = cnv_df.index.tolist()
    # print(f"cnv 样本数量: {len(cnv_key_list)}")

    cnv_df = cnv_df.loc[sample_key_list, :]
    return cnv_df


def load_wsi_data_by_sample_key(sample_key_list):
    # 导入 wsi 数据

    feature_dict = {}
    # features_array.append([str(sample_key)] + list(feature))

    not_in_wsi_key = []
    for sample_key in sample_key_list:
        feature_file_path = save_resnet_feature_dir_path / f"{sample_key}.npy"
        if not feature_file_path.exists():
            not_in_wsi_key.append(sample_key)
            continue
        feature = np.load(feature_file_path)
        feature_dict[sample_key] = feature
    
    # 获取已找到特征的长度
    feature_len = next(iter(feature_dict.values())).shape[1]
    for sample_key in not_in_wsi_key:
        feature = np.zeros((1, feature_len))
        feature_dict[sample_key] = feature


    return np.array([
        feature_dict[sample_key] for sample_key in sample_key_list
    ]).reshape(-1, feature_len)


def load_report_data_by_sample_key(sample_key_list):
    # 导入 wsi 数据

    feature_dict = {}
    # features_array.append([str(sample_key)] + list(feature))

    not_in_report_key = []
    for sample_key in sample_key_list:
        feature_file_path = save_bert_feature_dir_path / f"{sample_key}.npy"
        if not feature_file_path.exists():
            not_in_report_key.append(sample_key)
            continue
        feature = np.load(feature_file_path)
        feature_dict[sample_key] = feature


    # 获取已找到特征的长度
    feature_len = next(iter(feature_dict.values())).shape[1]
    for sample_key in not_in_report_key:
        feature = np.zeros((1, feature_len))
        feature_dict[sample_key] = feature


    return np.array([
        feature_dict[sample_key] for sample_key in sample_key_list
    ]).reshape(-1, feature_len)


# 定义Dataset对象
class MultiOmicsDataset(Dataset):
    def __init__(self, gene_array, cnv_array, report_array, wsi_array, label_array):
        self.gene_tensor = torch.tensor(gene_array, dtype=torch.float32)
        self.cnv_tensor = torch.tensor(cnv_array, dtype=torch.float32) 
        self.report_tensor = torch.tensor(report_array, dtype=torch.float32)
        self.wsi_tensor = torch.tensor(wsi_array, dtype=torch.float32)
        self.label_tensor = torch.tensor(label_array, dtype=torch.int32)

    def __len__(self):
        return len(self.label_tensor)

    def __getitem__(self, index):
        return {
            "gene_tensor": self.gene_tensor[index],
            "cnv_tensor": self.cnv_tensor[index],
            "report_tensor": self.report_tensor[index],
            "wsi_tensor": self.wsi_tensor[index],
            "label_tensor": self.label_tensor[index]
        }


def get_model_score(outputs, labels, output_len=2):
    """
    # 假设你有一个模型的输出和相应的真实标签
    # outputs 是模型的输出, 经过softmax后变为概率分布
    # labels 是真实的标签
    outputs = torch.tensor([[0.1, 0.9], [0.8, 0.2], [0.3, 0.7], [0.6, 0.4]])
    labels = torch.tensor([1, 0, 1, 0])
    """
    score_dict = {}
    
    # 将输出转换为预测的类别
    _, predicted = torch.max(outputs, 1)
    predicted = predicted.cpu().detach().numpy()
    # score_dict["predicted"] = predicted

    if isinstance(outputs, torch.Tensor):
        outputs = outputs.cpu().detach().numpy()
    if isinstance(labels, torch.Tensor):
        labels = labels.cpu().detach().numpy()

    # score_dict["outputs"] = outputs
    # score_dict["labels"] = labels


    # 计算AUC
    auc = roc_auc_score(labels, outputs[:, -1])
    score_dict["auc"] = auc


    # 计算准确率 
    # 准确性(accuracy)
    accuracy = accuracy_score(labels, predicted)
    score_dict["accuracy"] = accuracy
    # print(f'Accuracy: {accuracy:.2f}')

    _f1_score = f1_score(labels, predicted)
    score_dict["f1_score"] = _f1_score

    # 计算召回率
    recall = recall_score(labels, predicted)
    score_dict["recall"] = recall
    # print(f'Recall: {recall:.2f}')


    # 计算混淆矩阵并获取TN, FP, FN, TP的值
    tn, fp, fn, tp = confusion_matrix(labels, predicted).ravel()

    # 计算特异性
    specificity = tn / (tn + fp)
    score_dict["specificity"] = specificity
    # print(f"Specificity: {specificity:.2f}")  # 输出特异性值


    # 计算精确率
    precision = precision_score(labels, predicted)
    score_dict["precision"] = precision
    # print(f'Precision: {precision:.2f}')


    # 计算马修斯相关系数
    mcc = matthews_corrcoef(labels, predicted)
    score_dict["mcc"] = mcc
    # print(f'Matthews Correlation Coefficient: {mcc:.2f}')

    return score_dict