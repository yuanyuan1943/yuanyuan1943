import pandas as pd
import numpy as np

# --------------------------
# 步骤1：定义已知宫颈癌驱动区域（示例坐标，需根据文献或数据库确认）
# 格式：[染色体, 区域起始位置, 区域终止位置, 关键基因]
# --------------------------
cervical_cancer_driver_regions = [
    {"chr": "3", "start": 180000000, "end": 182000000, "gene": "PIK3CA"},  # 3q26.32
    {"chr": "11", "start": 69000000, "end": 69500000, "gene": "CCND1"},   # 11q13.3
    {"chr": "1", "start": 1500000, "end": 1800000, "gene": "CDKN2A/B"},   # 1p36.33
    {"chr": "20", "start": 40000000, "end": 40500000, "gene": "ZNF217"},  # 20q13.2
    {"chr": "4", "start": 87000000, "end": 87500000, "gene": "EPHA5"}     # 4q21.23
    # 可根据需要补充其他驱动区域
]

# --------------------------
# 步骤2：读取输入数据
# --------------------------
# 示例CNV数据（行：样本，列：探针ID）
cnv_raw = pd.read_csv("data/input/copy number (gene-level)/copy number (gene-level) - gistic2/Gistic2_CopyNumber_Gistic2_all_data_by_genes", index_col=0)
# 示例探针注释（包含探针ID及其基因组位置）
probe_annotations = pd.read_csv(
    "probe_annotations.csv", 
    usecols=["probe_id", "chromosome", "start_position", "end_position"]
)
# 确保染色体格式统一（如去除"chr"前缀）
probe_annotations["chromosome"] = probe_annotations["chromosome"].str.replace("chr", "")


# --------------------------
# 步骤3：筛选位于驱动区域内的探针
# --------------------------
def is_in_driver_region(probe_chr, probe_start, driver_regions):
    """判断探针是否位于任一驱动区域内"""
    for region in driver_regions:
        # 染色体匹配，且探针起始位置在驱动区域范围内
        if (probe_chr == region["chr"]) and (region["start"] <= probe_start <= region["end"]):
            return True
    return False

# 对探针注释表添加“是否在驱动区域”标签
probe_annotations["in_driver_region"] = probe_annotations.apply(
    lambda row: is_in_driver_region(
        probe_chr=row["chromosome"],
        probe_start=row["start_position"],
        driver_regions=cervical_cancer_driver_regions
    ), axis=1
)

# 筛选位于驱动区域的探针ID
driver_probes = probe_annotations[probe_annotations["in_driver_region"]]["probe_id"].tolist()
print(f"筛选前CNV探针数量：{cnv_raw.shape[1]}")
print(f"筛选后驱动区域探针数量：{len(driver_probes)}")


# --------------------------
# 步骤4：获取降维后的CNV数据
# --------------------------
cnv_reduced = cnv_raw[driver_probes]  # 仅保留驱动区域内的探针
print(f"降维后CNV数据形状：{cnv_reduced.shape}")  # (样本数, 驱动区域探针数)


# 可选：保存降维后的数据
cnv_reduced.to_csv("data/output/copy-number.csv")