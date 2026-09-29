import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")

# Load data
df = pd.read_csv("results.csv")

# Compute Accuracy (%)
accuracy = df.groupby(["Model", "PromptFile"])["Evaluation"].apply(
    lambda x: (x == "PASS").mean() * 100
).reset_index()

# 1. Overall Model Comparison Chart
plt.figure(figsize=(10, 6))
chart1 = sns.barplot(
    data=accuracy, 
    x="Model", 
    y="Evaluation", 
    hue="PromptFile", 
    palette="muted"
)
plt.title("OpenMP Concurrency Benchmark: Accuracy by Model & Prompt Strategy")
plt.ylabel("Accuracy (%)")
plt.xlabel("Model")
plt.ylim(0, 100)
for p in chart1.patches:
    if p.get_height() > 0:
        chart1.annotate(f'{p.get_height():.1f}%', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), 
                        textcoords='offset points')
plt.tight_layout()
plt.savefig("benchmark_accuracy.png")
plt.close()

# 2. Accuracy per OpenMP Test Case Chart
test_accuracy = df.groupby(["CodeFile"])["Evaluation"].apply(
    lambda x: (x == "PASS").mean() * 100
).reset_index()

plt.figure(figsize=(10, 5))
chart2 = sns.barplot(
    data=test_accuracy, 
    x="CodeFile", 
    y="Evaluation", 
    palette="crest"
)
plt.title("Test Case Pass Rate Across All Models")
plt.ylabel("Pass Rate (%)")
plt.xlabel("OpenMP C Benchmark File")
plt.xticks(rotation=30, ha="right")
plt.ylim(0, 100)
for p in chart2.patches:
    if p.get_height() > 0:
        chart2.annotate(f'{p.get_height():.1f}%', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), 
                        textcoords='offset points')
plt.tight_layout()
plt.savefig("testcase_pass_rate.png")
plt.close()

print("Charts successfully saved as benchmark_accuracy.png and testcase_pass_rate.png")