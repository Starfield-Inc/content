counts = Counter(labels)
order = ["question", "statement", "request"]
values = [counts.get(name, 0) for name in order]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(order, values, color="#3b6ea5")
ax.set_ylabel("Sentences")
ax.set_title("Sentence types labelled by the model")
ax.set_yticks(range(0, max(values) + 2))
fig.tight_layout()
fig.savefig("chart.png", dpi=120)
plt.show()
print(dict(counts))
