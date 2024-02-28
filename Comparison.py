import matplotlib.pyplot as plt

# Converted values obtained in MC simulation from atomic units to cm^2(Vs)^-1
model = [75137, 22972, 130623, 24734]
model_error = [62744, 23329, 120742, 16474]

# Values from the internet
experiment = [26000, 50000, 47500, 62500]
experiment_error = [2000, 10000, 2500, 2500]

labels = ['Aluminium', 'Copper', 'Gold', 'Silver']
plt.errorbar(range(len(model)), model, yerr = model_error, fmt = 'ko', label = 'model')
plt.errorbar(range(len(experiment)), experiment, yerr = experiment_error, fmt = 'ro', label = 'experiment')
plt.ylabel('Electron mobility / $cm^2 V^{-1} s^{-1}$')
plt.xticks(range(len(model)), labels)
plt.legend()
plt.show()