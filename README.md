# Class-Specific Performance Differences in the Detecting Underwater Objects (DUO) Dataset

This is the official repository for my Bachelors Thesis **"A Systematic Analysis of Class-Specific Performance Differences in Underwater Object Detection"** and the related paper titled **"Are All Marine Species Created Equal? Performance Disparities in Underwater Object Detection"**. 

## Summary
Underwater object detection is critical for monitoring marine ecosystems but poses unique challenges, including degraded image quality, imbalanced class distribution, and distinct visual characteristics. Not every species is detected equally well, yet underlying causes remain unclear. We address underlying causes of class-specific performance disparities beyond data quantity to gain insights as to how detection of under-performing marine species can systematically be improved. We decompose object detection into localization and classification tasks using the DUO dataset, where the class for scallops consistently under-performs. Localization analysis using YOLO11 and TIDE finds that foreground-background discrimination is the most problematic stage regardless of data quantity. Classification experiments with ResNet-18 reveal persistent precision gaps even with balanced data — indicating intrinsic feature-based challenges beyond data scarcity and inter-class dependencies. Results demonstrate that performance disparities stem from intrinsic visual characteristics rather than data quantity alone. We recommend imbalanced distributions when prioritizing precision, and balanced distributions when prioritizing recall. Improving under-performing classes should focus on algorithmic advances, especially within localization modules. We publicly release our code and datasets.

## Usage
### Localization Experiments
- Our custom datasets for different localization experiments can be downloaded through localization_study/loc_datasets/
- Training and evaluation is run easiest using Pixi in localization_study/loc_models/ with comand run-all-training, run-all-tests and run-all; the detailed scripts for localization are under localization_study/loc_models/
- Scripts for further evaluation regarding bounding box accuracy and error type analysis are in localization_study/scripts/ and loc_evaluation_scripts/
- All experiment outputs and error reports are saved in localization_study/loc_results/

### Classification Experiments
- Our custom datasets for different classification experiments can be downloaded through classification_study/cls_datasets/
- The classifiers are saved in classification_study/cls_models/ and can be run directly for different dataset versions and distributions 
- All experimental results are saved in classification_study/cls_results/
