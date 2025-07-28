

# gene v1.0.4

## 00-WGCNA提取特征.ipynb

https://omicverse.readthedocs.io/en/latest/Tutorials-bulk/t_wgcna/#relating-modules-to-external-information-and-identifying-important-genes

使用 WGGCNA 进行基因表达分析
(当前时间241206)由于版本等原因，这里选择 WGCNA 之前版本测试得出的 valid gene 20115 中的 2 ~ 18 .csv
即在20115个可分析基因中，选择 2 ~ 18 个基因进行 WGCNA 分析，大约 11643 个基因，近似于原数据量的 50% 左右
具体差异可参考 module_matrix 图像

存储对象约 2.6G


## 01-WGCNA读取已分析结果.ipynb
connectivity 含义 ???
提取各个 module 中 connectivity 大于 connectivity_mean 的值


## 02-提取ConnectTop对应样本.ipynb
将 connect top 的样本合并到 wgcna.csv
根据 sample key 提取\生成 对应的拷贝数样本到 copy-number.csv

```python
# all_data 数据
#              TCGA-2W-A8YY-01  TCGA-4J-AA1J-01  TCGA-BI-A0VR-01  \
# Gene Symbol                                                      
# ACAP3                    0.0           -0.009            0.211   
# ACTRT2                   0.0           -0.009            0.211   
# AGRN                     0.0           -0.009            0.211   
# ANKRD65                  0.0           -0.009            0.211   
# ATAD3A                   0.0           -0.009            0.211   
copy_number_file_path = data_input_dir_path / "copy number (gene-level)/copy number (gene-level) - gistic2/Gistic2_CopyNumber_Gistic2_all_data_by_genes"
assert copy_number_file_path.exists()

# all_thresholded 数据
#              TCGA-2W-A8YY-01  TCGA-4J-AA1J-01  TCGA-BI-A0VR-01  \
# Gene Symbol                                                      
# ACAP3                      0                0                1   
# ACTRT2                     0                0                1   
# AGRN                       0                0                1   
# ANKRD65                    0                0                1   
# ATAD3A                     0                0                1  
copy_number_thresholded_file_path = data_input_dir_path / "copy number (gene-level)/copy number (gene-level) - gistic2 thresholded/Gistic2_CopyNumber_Gistic2_all_thresholded.by_genes"
assert copy_number_thresholded_file_path.exists()
```