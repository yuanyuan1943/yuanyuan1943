# Model v1.0.14

## 00-多模态融合.ipynb
使用随机模拟数据作为输入，训练、评估模型

## 01-gene单模态训练.ipynb
加载 gene 和 label 数据, 且使用 gene 替代其他特征(如 cnv)进行训练

### 核心库
- Python 3.10.11

## 02-模态训练(gene+cnv) .ipynb
导入 cnv 数据

## 03-模态训练(gene+cnv+wsi).ipynb
导入 wsi 数据 且迎合 wsi 特征数据尺寸 (len(sample_key_len), len(feature_len)) -> (?, 2048)

## 04-模态训练(gene+cnv+wsi+report).ipynb
导入 report 数据 且迎合 report 特征数据尺寸 (len(sample_key_len), len(feature_len)) -> (?, 768)

## 05-模态训练(模态尺寸统一).ipynb
模态尺寸作为参数导入, 由模型统一尺寸

## 06-dev.ipynb
目前特征不足以支撑模型训练
数据样本失衡可能导致预测倾向样本数量更多的类别

## 07-特征加载器(report).ipynb
加载 report 数据(已经由模型进行训练)

## 08-特征加载器(graphy).ipynb
加载 graphy 数据(已经由模型进行训练)

## 09-特征融合.ipynb
!!! 注意事项 !!!
关注训练过程
关注样本平衡
关注交叉注意力


## 10-单模态实验数据(genev0.0.1).ipynb
手动调参组合, Dropout 0.20070 lr 0.00007305015
```python
# tb004-0120-0927.tar.gz
model = MultiOmicsModel(0.20070).to(device) # 250120-0928
optimizer = optim.Adam(model.parameters(), lr=0.00007305015) # 250120-0928
```
Dropout 越小 曲线越顺滑 毛刺越小
lr 越大 曲线越陡峭

数据结果不稳定，同样参数下结果不同

## 11-缩减模型复杂度.ipynb

模型复杂度

## 12-改变模型输出尺寸绘制ROC.ipynb

将模型输出尺寸从 (batch_size, 2) 改为 (batch_size, 1)
- 修改损失函数 criterion = nn.BCEWithLogitsLoss()
- 修改模型输出层 nn.Linear(2, 1) -> torch.sigmoid(nn.Linear(2, 1))

切换模态组合导出曲线数据

## 13-单模态K折实验数据.ipynb

5折交叉验证模型，并输出指标

```bash
5-3 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000
5-4 0.9697 0.9231 0.9091 0.9091 0.9091 0.9333 0.8424
5-5 0.9822 0.9615 0.9600 1.0000 0.9231 1.0000 0.9258
最终平均结果:
           Auc        Acc        F1-score   Pre        Sn         Sp         Mcc        
Genomic    0.8111     0.7884     0.7861     0.7950     0.7916     0.7802     0.5767   
```