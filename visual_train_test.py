import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def visualize_bootstrap_split(bootstrap_csv_path="/data2/project/2025summer/jjh0709/git/GasLeakage-MultiModal-MTF/Datasess/train_test_bootstrap.csv", 
                              gas_csv_path="/data2/project/2025summer/jjh0709/git/GasLeakage-MultiModal-MTF/Datasess/Mixture_MM.csv",
                              mm_gas_csv_path="/data2/project/2025summer/jjh0709/Data/zkwgkjkjn9-2/Gas Sensors Measurements/Gas_Sensors_Measurements.csv"):
    
    bootstrap_data = pd.read_csv(bootstrap_csv_path)
    Gas = pd.read_csv(gas_csv_path)
    
    bootstrap_1 = bootstrap_data[bootstrap_data['dataset'] == 'bootstrap_1'].copy()
    Gas = Gas[Gas['Gas'] == 'Mixture']
    
    sensors = ['MQ2', 'MQ3', 'MQ5', 'MQ6', 'MQ7', 'MQ8', 'MQ135']
    n = len(sensors)
    
    NoGas_starts = [0, 55, 124, 232, 344, 416, 461, 554, 604, 661, 731, 778, 840, 894, 1012, 1131, 1247, 1375, 1557]
    
    train_serials = np.array(list(bootstrap_1[bootstrap_1['train_test'] == 'train']['Serial Number']))
    test_serials = np.array(list(bootstrap_1[bootstrap_1['train_test'] == 'test']['Serial Number']))
    
    train_serials = train_serials[train_serials < len(Gas)]
    test_serials = test_serials[test_serials < len(Gas)]
    
    fig, axes = plt.subplots(n, 1, figsize=(40, 3*n))
    
    if n == 1:
        axes = [axes]
    
    for i, sensor_name in enumerate(sensors):
        x_data = np.arange(len(Gas))
        y_data = Gas[sensor_name].values
        
        axes[i].plot(x_data, y_data, color='gray', alpha=0.7, linewidth=1)
        axes[i].set_title(f'{sensor_name} - Bootstrap_1')
        
        for j in NoGas_starts:
            axes[i].axvline(x=j, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
        
        if len(train_serials) > 0:
            axes[i].scatter(train_serials, Gas.iloc[train_serials][sensor_name], 
                           color='red', s=20, alpha=0.8, zorder=5, label='Train')
        
        if len(test_serials) > 0:
            axes[i].scatter(test_serials, Gas.iloc[test_serials][sensor_name], 
                           color='blue', s=20, alpha=0.8, zorder=5, label='Test')
        
        axes[i].set_xlabel('Serial Number')
        axes[i].set_ylabel(sensor_name)
        axes[i].legend(loc='upper right')
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

visualize_bootstrap_split()