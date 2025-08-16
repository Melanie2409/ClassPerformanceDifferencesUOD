# Class-Specific Performance Differences in the Detecting Underwater Objects (DUO) Dataset

This is the official repository for my Bachelors Thesis **"A Systematic Analysis of Class-Specific Performance Differences in Underwater Object Detection"**.

## Summary
Underwater Object Detection (UOD) is an important tool in underwater robotics, offering significant contributions to marine ecosystem monitoring and conservation, sustainable oceanic resource management, and efficient aquaculture automation. However, the unique conditions in the underwater environment are challenging: image quality is often degraded by blur, low contrast, and color distortion; target objects are typically small, densely clustered, and visually similar to the background or other species; and, due to the difficulty in obtaining and correctly labeling underwater data, public datasets are limited. Available benchmarks often exhibit strong class imbalance,~\ie~contain far more examples of some classes than others, and show similar disparities in performance across different species. This thesis investigates the reasons behind these performance gaps and seeks to answer the central research question: \textit{What factors influence the under-performance of specific classes in underwater object detection, and to what extent?}

In this thesis, three key aspects are examined to answer this research question, namely the influence of different stages of the detection process, the effect of training data quantity, and the impact of intrinsic object characteristics on class-specific performance gaps. These are systematically addressed using a two-stage experimental framework, decomposing object detection into localization and classification tasks and conducting experiments under controlled data conditions for each task. For the localization task, we use a YOLO11 detector on single-class datasets and employ the TIDE error toolkit to evaluate the distinguishability of every target from the background and the bounding box accuracy. The classification study tests a pre-trained ResNet-18 classifier on object crops to analyze species assignment. 

This thesis focuses on the public  Detecting Underwater Objects (DUO) dataset, which has a proven record of scallop under-performance across several independent studies. Compared to the other species, the scallop class is arguably the most difficult to detect from a human perspective. Our experimental results support this suspected visual difficulty. The performance differences between classes persist even with balanced training data, which is evident in accuracy gaps in both the localization and classification analysis. We identify the foreground-background separation as the most problematic detection step. While more training examples allow for better feature learning, it is not enough to mitigate the challenges posed by small and visually less distinct objects. Moreover, we observe high sensitivity of the minority scallop class to the class distribution and available data of other classes, revealing a precision-recall tradeoff. 

Therefore, we recommend imbalanced datasets when prioritizing precision but balanced distribution for better recall. We encourage the design of class-aware detectors and evaluation protocols in future, and suggest focusing on algorithmic improvements for localization modules in particular. By providing these insights, this thesis contributes to developing more robust and higher-performing detection models, fostering further research and advancements in the application of AI to marine monitoring and conservation.

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
