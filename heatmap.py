import seaborn as sns
import matplotlib.pyplot as plt

elo = [
    931.1738834547057,
    1030.3222245067302,
    1013.4574401883818,
    1031.6254821138816,
    986.0123056625374,
    1007.4086640737667,
]
arr = [[1 / (10 ** ((elo[a] - elo[b]) / 400) + 1) for b in range(6)] for a in range(6)]
sns.heatmap(
    arr,
    cmap="crest",
    xticklabels=["2", "5", "8", "12", "15", "18"],
    yticklabels=["2", "5", "8", "12", "15", "18"],
    annot=True,
    annot_kws={"size": 16},
)
plt.show()
