# Class-Specific Performance Differences in the Detecting Underwater Objects (DUO) Dataset

This is the official repository for my Bachelors Thesis **"A Systematic Analysis of Class-Specific Performance Differences in Underwater Object Detection"**.

## Thesis Summary
Underwater Object Detection (UOD) is an important tool in underwater robotics, offering significant contributions to marine ecosystem monitoring and conservation, sustainable oceanic resource management, and efficient aquaculture automation. However, the unique conditions in the underwater environment are challenging: image quality is often degraded by blur, low contrast, and color distortion; target objects are typically small, densely clustered, and visually similar to the background or other species; and, due to the difficulty in obtaining and correctly labeling underwater data, public datasets are limited. Available benchmarks often exhibit strong class imbalance, i.e. contain far more examples of some classes than others, and show similar disparities in performance across different species. This thesis investigates the reasons behind these performance gaps and seeks to answer the central research question: What factors influence the under-performance of specific classes in underwater object detection, and to what extent?

In this thesis, three key aspects are examined to answer this research question, namely the influence of different stages of the detection process, the effect of training data quantity, and the impact of intrinsic object characteristics on class-specific performance gaps. These are systematically addressed using a two-stage experimental framework, decomposing object detection into localization and classification and conducting experiments under controlled data conditions for each stage. For the localization analysis, we use a YOLO11 detector on single-class datasets and employ the TIDE error toolkit to evaluate the distinguishability of every target from the background and the bounding box accuracy. The classification study tests a pre-trained ResNet-18 classifier on object crops to analyze species assignment. 

This thesis focuses on the public  Detecting Underwater Objects (DUO) dataset, which has a proven record of scallop under-performance across several independent studies. Compared to the other species, the scallop class is arguably the most difficult to detect from a human perspective. Our experimental results support this suspected visual difficulty. The performance differences between classes persist even with balanced training data, which is evident in accuracy gaps in both the localization and classification analysis. We identify the foreground-background separation as the most problematic detection step. While more training examples allow for better feature learning, it is not enough to mitigate the challenges posed by small and visually less distinct objects. Moreover, we observe high sensitivity of the minority scallop class to the class distribution and available data of other classes, revealing a precision-recall tradeoff. 

Therefore, we recommend imbalanced datasets when prioritizing precision but balanced distribution for better recall. We encourage the design of class-aware detectors and evaluation protocols in future, and suggest focusing on algorithmic improvements for localization modules in particular. By providing these insights, this thesis contributes to developing more robust and higher-performing detection models, fostering further research and advancements in the application of AI to marine monitoring and conservation.





## Repository Usage

This repository is organized into two main sections: `localization_study` and `classification_study`.  


### Localization Study
- **Datasets** → our customized data is available under [`localization_study/loc_datasets/`](localization_study/loc_datasets/)  
- **Training & Evaluation** → handled easiest by navigating into [`localization_study/loc_models/`](localization_study/loc_models/) and using [Pixi](https://pixi.sh/) 
  - Use the following commands:  
    - `pixi run run-all-training` → run training for all data subsets  
    - `pixi run run-all-tests` → run testing for all data subsets  
    - `pixi run run-all` → run both training and testing for all data subsets
  - Otherwise the detailed scripts for localization can be found in [`localization_study/loc_models/scripts`](localization_study/loc_models/scripts)
- **Further Evaluation** → scripts for bounding box accuracy and error analysis are in [`localization_study/loc_evaluation_scripts/`](localization_study/loc_evaluation_scripts/)  
- **Results** → experiment outputs and further evaluation reports will be saved in `localization_study/loc_results/`


### Classification Study
- **Datasets** → our customized data is available under [`classification_study/cls_datasets/`](classification_study/cls_datasets/)  
- **Training & Evaluation** → classifiers are stored in [`classification_study/cls_models/`](classification_study/cls_models/)  
  - These can be run directly for different dataset versions and distributions.  
- **Results** → all experimental outputs will be saved in `classification_study/cls_results/`


