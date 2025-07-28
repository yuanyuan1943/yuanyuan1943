
from pathlib import Path

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

sample_labels_file_path = pkg_dir_path.parent / 'survival/data/output/sample-labels.csv'
assert sample_labels_file_path.exists()

valid_gene_file_path = data_input_dir_path / 'valid_gene_20115.csv'

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