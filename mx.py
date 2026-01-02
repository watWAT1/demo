import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# 读取数据集
df = pd.read_csv('student.csv', encoding='utf-8-sig')

# 查看数据集基本信息
print('数据集基本信息：')
print(df.info())
print('\n数据集前5行：')
print(df.head())

# 准备特征和目标变量
y = df['期末考试分数']
X = df.drop(['学号', '期末考试分数'], axis=1)

# 对分类变量进行独热编码
X = pd.get_dummies(X, columns=['性别', '专业'], drop_first=False)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f'\n训练集大小：{X_train.shape}')
print(f'测试集大小：{X_test.shape}')

# 训练随机森林回归模型（参数调整以减小模型大小）
rf_model = RandomForestRegressor(
    n_estimators=30,  # 减少决策树数量
    max_depth=10,     # 限制树的最大深度
    min_samples_leaf=5,  # 增加叶子节点最小样本数
    random_state=42
)
rf_model.fit(X_train, y_train)

# 在训练集和测试集上进行预测
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)

# 计算评估指标
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f'\n模型评估结果：')
print(f'训练集MSE：{train_mse:.2f}')
print(f'测试集MSE：{test_mse:.2f}')
print(f'训练集R²评分：{train_r2:.2f}')
print(f'测试集R²评分：{test_r2:.2f}')

# 保存模型到文件
with open('student_rf_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

print('\n模型已保存到 student_rf_model.pkl 文件中')
