import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up canvas
fig, ax = plt.subplots(figsize=(16, 8))
ax.axis('off')
ax.set_xlim(-1, 14)
ax.set_ylim(0, 6)

# Function to draw a labeled box
def draw_box(x, y, text, color):
    box = patches.FancyBboxPatch((x, y), 2.8, 0.9,
                                 boxstyle="round,pad=0.05",
                                 edgecolor='black', facecolor=color,
                                 linewidth=2)
    ax.add_patch(box)
    ax.text(x + 1.4, y + 0.45, text,
            ha='center', va='center',
            fontsize=10, fontweight='bold', wrap=True)

# Function to draw arrows
def draw_arrow(x1, y1, x2, y2, text=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.2, text, fontsize=9, ha='center')

# Draw components
draw_box(0, 4, "Event Source\n(API Gateway/EventBridge)", '#c6e2ff')
draw_box(3, 4, "AWS Lambda\n(Function Runtime)", '#add8e6')
draw_box(6, 4, "CloudWatch\n(Metrics)", '#90ee90')
draw_box(6, 2.5, "Feature\nEngineering", '#dcdcff')
draw_box(9, 4, "Lambda Layer\n(AI Model)", '#ffffcc')
draw_box(9, 2.5, "AI Model\n(Isolation Forest)", '#fdfd96')
draw_box(12, 2.5, "S3\n(Model Storage)", '#d3d3d3')
draw_box(9, 1.0, "SNS\n(Alerting System)", '#f08080')

# Draw arrows
draw_arrow(2.8, 4.45, 3, 4.45, "Triggers")
draw_arrow(5.8, 4.45, 6, 4.45, "Sends Metrics")
draw_arrow(6 + 1.4, 4.0, 6 + 1.4, 3.3, "→")     # CW to Feature Eng
draw_arrow(6.8, 2.95, 9, 2.95, "→")             # Feature Eng → AI Model
draw_arrow(10.4, 4.0, 10.4, 2.8, "→")           # Lambda Layer → AI Model
draw_arrow(12, 2.95, 11, 2.95, "Model Load")    # S3 → AI Model
draw_arrow(10.4, 2.5, 10.4, 1.7, "If Anomaly")  # AI Model → SNS

# Save and show
plt.tight_layout()
plt.savefig("Corrected_Serverless_Architecture_Diagram.png", dpi=300, bbox_inches='tight')
plt.show()
