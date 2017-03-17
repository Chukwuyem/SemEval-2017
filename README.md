**General Overview**
This folder contains the essential scripts used to participate in SemEval-2017 Task 4 English. There were 5 subtasks (A, B, C, D and E). Data was supplied by SemEval for A, B and C (subtasks D and E were tweet quantification tasks based on B and C respectively). Additional data from SentiStrength was used (http://sentistrength.wlv.ac.uk/). The SentiStrength tool was also used.

Subtask A is a message polarity classification task, classifing tweets into postive, neutral or negative labels. The original data is in the following format:
<ID> <LABEL> <TWEET>

Subtask B is a topic-based message polarity classification task, classifying tweets into postive or negative labels based on a given topic. The original data is in the following format:
<ID> <TOPIC> <LABEL> <TWEET>
Subatask D is a tweet quantification task, based on subtask B where for each topic, an estimate of the distribution of tweets across the postive-negative scale is given.

Subtask C is a topic-based message polarity classification task, classifying tweets on a numeric scale, from -2 to +2, where -2 is most negative, +2 is most positive and 0 is neutral. The original data is in the following format:
<ID> <TOPIC> <LABEL> <TWEET>
Subtask E is a tweet quantification task, based on subtask C where for each topic, an estimate of the distribution of tweets across the five-point scale is given.

The system used for all the subtasks used Conditional Random Fields (CRFs), more specifically the CRF++ implementation (https://taku910.github.io/crfpp/). The whole system is described in detail in the paper (made available soon).

This github folder serves as a source of all the necessary scripts as was used in all the subtasks.

There are 2 sub-folders: Data and Experiment.
The Data folder contains the data for each subtask as was supplied by SemEval (this data was download using a twitter script; as a result, a few dozen tweets were not available. However, the format is unchanged). However, this was changed into multiple formats for experiment-sake. Not all the different formats are available. However, the folder also contains all the scripts that were used to make necessary conversions, including converting from one subtask label format to another in order to have additional training data for former subtask.

The Experiment folder contains scripts and data needed to run one sample experiment. (This is explained fully in the paper). However, a short summary: for each subtask the same experiment setup is used to achieve the best lexical features and CRF params. The only differences between subtasks is data used (five-point vs three-point etc) and the nuances that come with that, like number of columns. This is reflected in the almost exact similarities between scripts. The scripts and data in this folder where used specifically for subtask B/D but the other subtasks had identical setups.

**Data Overview**
- Subtask A data: The data files supplied by SemEval for subtask A.
- Subtask BD data: The data files supplied by SemEval for subtask B and D.
- Subtask CE data: The data files supplied by SemEval for subtask C and E.
- SentiStrength data:
- file-convert-neutral2-subtask-B: This is a script used to convert five-point format data to two-point format.
- file-convert-neutral-subtask-B: This is a script used to format neutral tweets from three-point format, i.e. convert three-point to two-point format.
- file-convert-subtask-B: This is a script used to convert three-point format to five-point format (this was used to convert subtask B data to five-point so the system could be trained with five-point).
- subtaskC-convert-subtask-A: This is a script used to convert five-point format to three-point format data.
- taskAdata-convert: This is a script used to convert three-point format to five-point format (this was used to prep subtask A data for use with subtask C).





