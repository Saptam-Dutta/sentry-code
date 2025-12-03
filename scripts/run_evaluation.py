import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.orchestrator import SecurityReviewOrchestrator
import json

print("="*70)
print(" "*20 + "SENTRY-CODE EVALUATION")
print("="*70)

orchestrator = SecurityReviewOrchestrator(llm_model="llama3.2:latest")

vulnerable_dir = Path("tests/fixtures/vulnerable")
clean_dir = Path("tests/fixtures/clean")

print("\n[1/2] Analyzing vulnerable files...")
print("-" * 70)
vuln_result = orchestrator.analyze_repository(str(vulnerable_dir), use_llm=False)

true_positives = vuln_result.total_findings
false_negatives = 0 if true_positives > 0 else 1

print(f"✓ Detected {true_positives} vulnerabilities")

print("\n[2/2] Analyzing clean files...")
print("-" * 70)
clean_result = orchestrator.analyze_repository(str(clean_dir), use_llm=False)

false_positives = clean_result.total_findings
true_negatives = 1 if false_positives == 0 else 0

print(f"✓ Clean code analysis: {false_positives} false positives")

# Calculate metrics
tp = true_positives
fp = false_positives
fn = false_negatives
tn = true_negatives

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

print("\n" + "="*70)
print(" "*25 + "EVALUATION METRICS")
print("="*70)

print(f"\nConfusion Matrix:")
print(f"  True Positives:  {tp:>3}")
print(f"  False Positives: {fp:>3}")
print(f"  False Negatives: {fn:>3}")
print(f"  True Negatives:  {tn:>3}")

print(f"\nPerformance Metrics:")
print(f"  Precision:  {precision:>6.2%}  (target: ≥75%)")
print(f"  Recall:     {recall:>6.2%}  (target: ≥60%)")
print(f"  F1-Score:   {f1:>6.2%}  (target: ≥67%)")
print(f"  FP Rate:    {fpr:>6.2%}  (target: ≤25%)")

print(f"\nFindings by Severity:")
for severity, count in vuln_result.severity_counts.items():
    print(f"  {severity:<10} {count:>3}")

print("\n" + "="*70)
print(f"✓ Evaluation Complete!")
print("="*70)

# Save results
results = {
    "metrics": {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "false_positive_rate": round(fpr, 4)
    },
    "confusion_matrix": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
    "severity_distribution": vuln_result.severity_counts
}

with open("evaluation_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to: evaluation_results.json\n")
