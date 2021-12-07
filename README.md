# Detection of FAKEBOB
Source code for the paper "On the Detection of Adaptive Adversarial Attacks in Speaker Verification Systems".

## File structure
- **./demo/**: showing the idea of MEH-FEST detector in jupyter notebook.
- **./detection_results/**: showing the performance of MEH-FEST detection in jupyter notebook.
- **./detection_countermeasure/**: two adaptive attacks or attackers' countermeasures studied and shown in jupyter notebook.
	- **./detection_countermeasure/epsilon_00025**: reducing the perturbation threshold to 0.00025.
	- **./detection_countermeasure/n-th_FAKEBOB**: (n+1)th MEH-FEST detection method against n-th FAKEBOB attacks. 
- **./detection_extend.sh**: shell script to run "**detection_extend.py**".
- **./detection_extend.py**: n-th MEH-FEST detection method.  

## Reproduce our experiment step by step
1. Follow the instructions at [FAKEBOB GitHub Repo](https://github.com/FAKEBOB-adversarial-attack/FAKEBOB) to generate adversarial audios.
2. Install "**librosa**" python module by running 
    - **pip install 'numpy==1.20'    # required by librosa**
    - **pip install librosa**
3. Copy "**detection_extend.sh**" and "**detection_extend.py**" to be under the root directory of FAKEBOB code.
4. Change the directory name for the folder that contains adversarial audios. For example, change "**./adversarial-audio/gmm-SV-targeted/**" to "**./adversarial-audio/gmm-SV-targeted_epsilon_002/**".
5. Create a new folder for logs, such as "**./logs_gmm_epsilon_002**".
6. Update shell script "**detection_extend.sh**" for "**archi**", "**epsilon**", and the range of "**k**" in the loop. 
7. Run "**./detection_extend.sh**". The detection results can be find in log files under the log folder, such as "**./logs_gmm_epsilon_002/detection_gmm_epsilon_002_extend_min_1_results.txt**".

### If you have any questions, please feel free to comment or contact.
