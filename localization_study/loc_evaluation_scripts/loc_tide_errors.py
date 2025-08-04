import json
import os
import io
import sys
import tempfile
from collections import Counter
from tidecv import TIDE
import tidecv.datasets as datasets


def make_box_poly_from_bbox(bbox):
    x, y, w, h = bbox
    return [[
        x,     y,
        x + w, y,
        x + w, y + h,
        x,     y + h
    ]]

def patch_coco_json(orig_json_path):
    data = json.load(open(orig_json_path))
    for ann in data.get("annotations", []):
        seg = ann.get("segmentation")
        if (
            (not isinstance(seg, list))
            or (not seg)
            or isinstance(seg[0], (int, float))
        ):
            ann["segmentation"] = make_box_poly_from_bbox(ann["bbox"])
    fd, fixed_path = tempfile.mkstemp(
        suffix=".json", prefix="patched_", dir=os.path.dirname(orig_json_path)
    )
    os.close(fd)
    with open(fixed_path, "w") as f:
        json.dump(data, f)
    print(f"Patched JSON written to: {fixed_path}")
    return fixed_path

def run_tide_evaluation(orig_ann, resFile, tag, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Load Data
    fixed_ann = patch_coco_json(orig_ann)
    gt = datasets.COCO(fixed_ann)
    pred = datasets.COCOResult(resFile)

    tide = TIDE()
    res = tide.evaluate(gt, pred, mode=TIDE.BOX, pos_threshold=0.25)

    # Save TIDE Summary (dAP)
    summary = os.path.join(out_dir, f"{tag}_tide_dAP_summary.txt")
    buf = io.StringIO()
    sys.stdout = buf
    tide.summarize()
    sys.stdout = sys.__stdout__

    with open(summary, "w") as f:
        f.write(buf.getvalue())
    print(f"Summary saved to: {summary}")

    # Save Plots
    tide.plot(out_dir)
    print(f"Plots saved to: {out_dir}")

    # Count errors (absolute)
    err_counter = Counter(type(err).__name__ for err in res.errors)

    # Total error count
    total_errors = sum(err_counter.values())

    # Print and save absolute + % breakdown
    counts = os.path.join(out_dir, f"{tag}_error_counts.txt")
    with open(counts, "w") as f:
        f.write(f"Error Type Counts for {tag}\n")
        f.write(f"Total Errors: {total_errors}\n\n")

        print("Error Breakdown (absolute count and percentage):")
        for err_name, count in err_counter.items():
            percent = (count / total_errors) * 100 if total_errors > 0 else 0.0
            print(f"{err_name:20s}: {count:4d} ({percent:.1f}%)")
            f.write(f"{err_name:20s}: {count:4d} ({percent:.1f}%)\n")
            
        print(f"Error counts saved to: {counts}")


if __name__ == "__main__":
   
    # Choose run
    run_number = "01"

    # Define project structure paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    BASE_PATH = project_root
    RESULTS_PATH = os.path.join(project_root, "loc_results")
    os.makedirs(RESULTS_PATH, exist_ok=True)

    dataset_runs = [
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_echinus.json", f"{RESULTS_PATH}/25conf_single_class_DUO_echinus_test_run_{run_number}/predictions.json", "echinus_single_DUO", f"{RESULTS_PATH}/tide_error_evaluation/echinus_single_DUO"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_echinus.json", f"{RESULTS_PATH}/25conf_balanced_echinus_test_run_{run_number}/predictions.json", "echinus_balanced", f"{RESULTS_PATH}/tide_error_evaluation/echinus_balanced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_echinus.json", f"{RESULTS_PATH}/25conf_reduced_0.25_echinus_test_run_{run_number}/predictions.json", "echinus_0.25_reduced", f"{RESULTS_PATH}/tide_error_evaluation/echinus_0.25_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_echinus.json", f"{RESULTS_PATH}/25conf_reduced_0.5_echinus_test_run_{run_number}/predictions.json", "echinus_0.5_reduced", f"{RESULTS_PATH}/tide_error_evaluation/echinus_0.5_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_echinus.json", f"{RESULTS_PATH}/25conf_reduced_0.75_echinus_test_run_{run_number}/predictions.json", "echinus_0.75_reduced", f"{RESULTS_PATH}/tide_error_evaluation/echinus_0.75_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_holothurian.json", f"{RESULTS_PATH}/25conf_single_class_DUO_holothurian_test_run_{run_number}/predictions.json", "holothurian_single_DUO", f"{RESULTS_PATH}/tide_error_evaluation/holothurian_single_DUO"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_holothurian.json", f"{RESULTS_PATH}/25conf_balanced_holothurian_test_run_{run_number}/predictions.json", "holothurian_balanced", f"{RESULTS_PATH}/tide_error_evaluation/holothurian_balanced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_holothurian.json", f"{RESULTS_PATH}/25conf_reduced_0.25_holothurian_test_run_{run_number}/predictions.json", "holothurian_0.25_reduced", f"{RESULTS_PATH}/tide_error_evaluation/holothurian_0.25_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_holothurian.json", f"{RESULTS_PATH}/25conf_reduced_0.5_holothurian_test_run_{run_number}/predictions.json", "holothurian_0.5_reduced", f"{RESULTS_PATH}/tide_error_evaluation/holothurian_0.5_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_holothurian.json", f"{RESULTS_PATH}/25conf_reduced_0.75_holothurian_test_run_{run_number}/predictions.json", "holothurian_0.75_reduced", f"{RESULTS_PATH}/tide_error_evaluation/holothurian_0.75_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_scallop.json", f"{RESULTS_PATH}/25conf_single_class_DUO_scallop_test_run_{run_number}/predictions.json", "scallop_single_DUO", f"{RESULTS_PATH}/tide_error_evaluation/scallop_single_DUO"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_scallop.json", f"{RESULTS_PATH}/25conf_single_class_DUO_limited_scallop_test_run_{run_number}/predictions.json", "scallop_limited", f"{RESULTS_PATH}/tide_error_evaluation/scallop_limited"),
    # no predictions made for 0.25 scallop data, all gt missed (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_scallop.json", f"{RESULTS_PATH}/25conf_reduced_0.25_scallop_test_run_{run_number}/predictions.json", "scallop_0.25_reduced", f"{RESULTS_PATH}/tide_error_evaluation/scallop_0.25_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_scallop.json", f"{RESULTS_PATH}/25conf_reduced_0.5_scallop_test_run_{run_number}/predictions.json", "scallop_0.5_reduced", f"{RESULTS_PATH}/tide_error_evaluation/scallop_0.5_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_scallop.json", f"{RESULTS_PATH}/25conf_reduced_0.75_scallop_test_run_{run_number}/predictions.json", "scallop_0.75_reduced", f"{RESULTS_PATH}/tide_error_evaluation/scallop_0.75_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_starfish.json", f"{RESULTS_PATH}/25conf_single_class_DUO_starfish_test_run_{run_number}/predictions.json", "starfish_single_DUO", f"{RESULTS_PATH}/tide_error_evaluation/starfish_single_DUO"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_starfish.json", f"{RESULTS_PATH}/25conf_balanced_starfish_test_run_{run_number}/predictions.json", "starfish_balanced", f"{RESULTS_PATH}/tide_error_evaluation/starfish_balanced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_starfish.json", f"{RESULTS_PATH}/25conf_reduced_0.25_starfish_test_run_{run_number}/predictions.json", "starfish_0.25_reduced", f"{RESULTS_PATH}/tide_error_evaluation/starfish_0.25_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_starfish.json", f"{RESULTS_PATH}/25conf_reduced_0.5_starfish_test_run_{run_number}/predictions.json", "starfish_0.5_reduced", f"{RESULTS_PATH}/tide_error_evaluation/starfish_0.5_reduced"),
    (f"{BASE_PATH}/loc_evaluation_scripts/ground_truths/ground_truth_test_starfish.json", f"{RESULTS_PATH}/25conf_reduced_0.75_starfish_test_run_{run_number}/predictions.json", "starfish_0.75_reduced", f"{RESULTS_PATH}/tide_error_evaluation/starfish_0.75_reduced"),
    ]


    for orig_ann, resFile, tag, out_dir in dataset_runs:
        print(f"Running: {tag}")
        run_tide_evaluation(orig_ann, resFile, tag, out_dir)
    print("All TIDE evaluations completed.")