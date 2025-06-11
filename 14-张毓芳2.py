import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_error


# 1. 数据获取与预处理
def get_stock_data(ticker, start_date, end_date):
    """
    从Yahoo Finance获取股票数据
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


# 获取苹果公司股票数据
ticker = 'AAPL'
start_date = '2010-01-01'
end_date = '2023-12-31'
stock_data = get_stock_data(ticker, start_date, end_date)

# 检查数据
print("股票数据前5行:")
print(stock_data.head())

# 选择特征 - 使用OHLCV数据
features = ['Open', 'High', 'Low', 'Close', 'Volume']
data = stock_data[features]

# 数据标准化
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)


# 2. 数据降维（PCA）
def apply_pca(data, n_components=None):
    """
    应用PCA降维
    """
    pca = PCA(n_components=n_components)
    pca_data = pca.fit_transform(data)
    return pca, pca_data


# 应用PCA，保留95%的方差
pca, pca_data = apply_pca(scaled_data, 0.95)
print(f"\n保留的PCA组件数量: {pca.n_components_}")
print(f"解释方差比: {pca.explained_variance_ratio_}")

# 可视化解释方差
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Explained Variance')
plt.grid()
plt.show()


# 3. 构建时间序列数据集
def create_dataset(data, time_steps=1):
    """
    创建时间序列数据集
    """
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps), :])
        y.append(data[i + time_steps, 0])  # 预测第一个主成分
    return np.array(X), np.array(y)


# 设置时间步长
TIME_STEPS = 20

# 创建数据集
X, y = create_dataset(pca_data, TIME_STEPS)

# 划分训练集和测试集
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]


# 4. LSTM模型构建
def build_lstm_model(input_shape):
    """
    构建LSTM模型
    """
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


# 构建模型
model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
model.summary()

# 训练模型
early_stop = EarlyStopping(monitor='val_loss', patience=5)
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# 绘制训练历史
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

# 5. 预测与评估
# 在测试集上进行预测
predictions = model.predict(X_test)


# 反标准化预测结果
# 我们需要构建一个与原始PCA数据形状相同的数组来逆变换
def inverse_transform_predictions(predictions, pca_data, X_test):
    """
    将预测结果反转换回原始空间
    """
    # 创建一个与原始PCA数据形状相同的数组
    dummy_array = np.zeros((len(predictions), pca_data.shape[1]))
    dummy_array[:, 0] = predictions.flatten()  # 只替换第一个主成分

    # 逆PCA变换
    inv_pca = pca.inverse_transform(dummy_array)

    # 逆标准化
    inv_scale = scaler.inverse_transform(inv_pca)

    # 获取收盘价（假设Close是第3列，索引为3）
    close_predictions = inv_scale[:, 3]

    # 获取实际值
    actual_values = np.zeros((len(y_test), pca_data.shape[1]))
    actual_values[:, 0] = y_test

    inv_pca_actual = pca.inverse_transform(actual_values)
    inv_scale_actual = scaler.inverse_transform(inv_pca_actual)
    actual_close = inv_scale_actual[:, 3]

    return close_predictions, actual_close


predicted_close, actual_close = inverse_transform_predictions(predictions, pca_data, X_test)

# 计算评估指标
mse = mean_squared_error(actual_close, predicted_close)
mae = mean_absolute_error(actual_close, predicted_close)
rmse = np.sqrt(mse)

print(f"\n评估指标:")
print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

# 可视化预测结果
plt.figure(figsize=(14, 7))
plt.plot(actual_close, label='Actual Close Price', color='blue')
plt.plot(predicted_close, label='Predicted Close Price', color='red', alpha=0.7)
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()