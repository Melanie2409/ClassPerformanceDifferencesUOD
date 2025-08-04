import torch
import wandb as wb
import os
import json 
import pandas as pd

from ultralytics import YOLO

from yolo11_object_detection.logging_helpers import on_val_start, on_val_end

if __name__ == "__main__":

    # Define project structure paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    BASE_PATH = os.path.join(project_root, "loc_datasets", "balanced_data")
    CHECKPOINT_PATH = os.path.join(project_root, "loc_checkpoints")
    RESULTS_PATH = os.path.join(project_root, "loc_results")
    os.makedirs(RESULTS_PATH, exist_ok=True)

    # Classes for balanced testing
    CLASS_LIST = ["echinus", "holothurian", "starfish"]  # no Scallop because DUO-Scallop already has balanced amount

    for class_name in CLASS_LIST:
        print(f"Testing on: {class_name}")
        # Define the run parameters (make sure identical to train run)
        run_number = "01"
        run_name = f"25conf_balanced_{class_name}_test_run_{run_number}"    # We test with confidence threshold 0.25
        project_name = "yolo11-test-balanced"

        images_dir = os.path.join(BASE_PATH, class_name, "images")
        labels_dir = os.path.join(BASE_PATH, class_name, "labels")
        yaml_path = os.path.join(BASE_PATH, class_name, f"temp_data_{class_name}.yaml")

        with open(yaml_path, "w") as f:
            f.write(f"""
        train: {os.path.join(images_dir, "train")}
        val: {os.path.join(images_dir, "valid")}
        nc: 1
        names: ["{class_name}"]
        """)        
        
        # Set device
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            print("Using mps as the default device.")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
            print("Using cuda as the default device.")
        else:
            device = torch.device("cpu")
            print("Using cpu as the default device.")

        # Test saved model
        model_path = os.path.join(f"{CHECKPOINT_PATH}/yolo11-train-balanced/balanced_{class_name}_train_run_{run_number}/weights/best.pt")
        model = YOLO(model_path)
        model.add_callback("on_val_start", on_val_start)
        model.add_callback("on_val_end", on_val_end)
        model = model.to(device)

        # Before model training: results are saved per default in "current_directory/project_name/run_name"
        # Set current working directory to the results path
        current_directory = os.chdir(RESULTS_PATH)

        # Test the model
        results_test = model.val(data=yaml_path, 
                                save_json=True,
                                conf=0.25,
                                iou=0.7,
                                device=device,
                                split="test",
                                project=project_name,
                                name=f"{run_name}",
                                save_txt=True,
                                save_conf=True)
        

        # Finish W&B logging
        wb.finish()