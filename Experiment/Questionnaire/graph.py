import json
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

fig, ax = plt.subplots()
ax.set_xlabel('Epoch')
ax.set_xlim(0, 20)
ax.set_ylabel('Loss')
plt.gca().xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
with open(r'C:\Users\init\Downloads\run-.-tag-epoch_val_loss.json') as fp:
    data_array = np.array(json.load(fp))
    epoch = data_array[:, 1].astype(int)
    val_loss = data_array[:, 2]

    ax.plot(epoch, val_loss, color='r', label='validation loss')

with open(r'C:\Users\init\Downloads\run-.-tag-epoch_loss.json') as fp:
    data_array = np.array(json.load(fp))
    epoch = data_array[:, 1].astype(int)
    loss=data_array[:, 2]

    ax.plot(epoch, loss, color = 'g', label = 'training loss')

    ax.legend()
    plt.show()
