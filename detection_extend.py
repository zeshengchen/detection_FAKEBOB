# Extend from detection.py to consider to apply k-th min energy 
# in high frequencies of STFT as a detector

import numpy as np
import os
import librosa
import sys

if len(sys.argv) != 4:
    print("Error on command-line arguments!")
    exit(1) 

test_dir = "./data/test-set"
illegal_dir = "./data/illegal-set"
adversarial_dir = "adversarial-audio"
gmm_adversarial_dir = "gmm-SV-targeted_epsilon_" + sys.argv[2]
iv_adversarial_dir = "iv-SV-targeted_epsilon_" + sys.argv[2]

spk_id_list = ["1580", "2830", "4446", "5142", "61"]

# archi = "iv" or "gmm"
archi = sys.argv[1]

k_extend = int(sys.argv[3])

n_fft = 512  # main parameter for STFFT (4096)
low_index = 224 # indicate the high frequency range and depending on n_fft (when n_fft = 512, the value of 224 refers to 7KHz)!
hop_length = 160 # frame step = 10ms 
win_length = 400 # frame length = 25ms 

def calculate_kth_min_energy_stft(audio_path) :
    audio = librosa.load(audio_path, sr=16000)
    magnitudes = np.abs(librosa.stft(audio[0], n_fft=n_fft, 
                        hop_length=hop_length, win_length=win_length,
                        center=False))
    energy = sum(np.square(magnitudes[low_index:,]))
    index = sorted(range(len(energy)), key=lambda k: energy[k])
    
    # attempt to find the index for k-th min energy
    # need to begin from 2nd one and go through the same process until k-th one
    len_index = len(energy)
    index_set = [index[0]]   # put 1st min energy index
    cur_index = 1

    found = False 
    if len(index_set) == k_extend :
        found = True

    while (not found) and (cur_index < len_index):
        found_cur = True 
        len_index_set = len(index_set)

        for i in range(0, len_index_set): 
            if abs(index[cur_index] - index_set[i]) <= (n_fft // hop_length):
                found_cur = False 
                break
        
        if found_cur :
            index_set.append(index[cur_index])
            if len(index_set) == k_extend :
                found = True 

        cur_index += 1 

    if found :
        index_kth_min_energy = index_set[-1]        
    else :
        print("Warning: cannot find the %d-th min energy in STFT" % (k_extend))
        index_kth_min_energy = index[len_index - 1]
    
    print(index_set)

    kth_min_energy = energy[index_kth_min_energy]

    return kth_min_energy, index_kth_min_energy  

# get all illegal audios 
illegal_audio_list = []
illegal_audio_names = []
spk_iter = os.listdir(illegal_dir)
for spk_id in spk_iter:
    spk_dir = os.path.join(illegal_dir, spk_id)
    audio_iter = os.listdir(spk_dir)
    for _, audio_name in enumerate(audio_iter):
        path = os.path.join(spk_dir, audio_name)
        illegal_audio_list.append(path)
        illegal_audio_names.append(audio_name)

''' Results for illegal audios
'''
print("Results for illegal audios:\n")
illegal_audio_results = []
for i, illegal_audio_path in enumerate(illegal_audio_list):
    energy, index = calculate_kth_min_energy_stft(illegal_audio_path)

    print("    audio name = %s, index = %d, energy = %f" % (illegal_audio_names[i], index, energy))
    illegal_audio_results.append(energy)
print("")

''' Results for each registered user (legal audios and adversarial audios)
'''
legal_audio_results = []
adversarial_audio_results = []
for spk_id in spk_id_list:    # loop through speakers
    print("spk = %s\n" % (spk_id))

    # get audio list of this speaker 
    audio_list = []
    audio_names = []
    spk_dir = os.path.join(test_dir, spk_id)
    audio_iter = os.listdir(spk_dir)
    for _, audio_name in enumerate(audio_iter):
        path = os.path.join(spk_dir, audio_name)
        audio_list.append(path)
        audio_names.append(audio_name)

    ''' Results for legal audios
    '''
    print("  Results for legal audios:\n")
    for i, legal_audio_path in enumerate(audio_list):
        energy, index = calculate_kth_min_energy_stft(legal_audio_path)

        print("    audio name = %s, index = %d, energy = %f" % (audio_names[i], index, energy))
        legal_audio_results.append(energy)
    print("")

    # get adversarial audios of this speaker 
    if archi == "gmm":
        target_dir = gmm_adversarial_dir
    elif archi == "iv":
        target_dir = iv_adversarial_dir
    else:
        print("Error on getting a archi!")
        exit(1) 

    # GMM or i-vector adversarial audios     
    adv_list = []
    adv_audio_names = []
    adv_dir = os.path.join(adversarial_dir, target_dir)
    adv_dir = os.path.join(adv_dir, spk_id)
    adv_iter = os.listdir(adv_dir)
    for _, adv_spk_id in enumerate(adv_iter):
        adv_audio_dir = os.path.join(adv_dir, adv_spk_id)
        adv_audio_iter = os.listdir(adv_audio_dir)
        for _, adv_audio_name in enumerate(adv_audio_iter):
            path = os.path.join(adv_audio_dir, adv_audio_name) 
            adv_list.append(path)
            adv_audio_names.append(adv_audio_name) 

    ''' Results for adversarial audios
    '''
    print("  Results for adversarial audios:\n")
    for i, adv_audio_path in enumerate(adv_list):
        energy, index = calculate_kth_min_energy_stft(adv_audio_path)

        print("    audio name = %s, index = %d, energy = %f" % (adv_audio_names[i], index, energy))
        adversarial_audio_results.append(energy)
    print("")
    print("")

print("Final results for the %d-th min energy in STFT:\n" % (k_extend))

print("illegal audios: len = %d, max = %f, min = %f, average = %f" % (len(illegal_audio_results), max(illegal_audio_results), min(illegal_audio_results), sum(illegal_audio_results)/len(illegal_audio_results)))
illegal_audio_results.sort()
print(illegal_audio_results)
print("")

print("legal audios: len = %d, max = %f, min = %f, average = %f" % (len(legal_audio_results), max(legal_audio_results), min(legal_audio_results), sum(legal_audio_results)/len(legal_audio_results)))
legal_audio_results.sort()
print(legal_audio_results)
print("")

print("adversarial audios: len = %d, max = %f, min = %f, average = %f" % (len(adversarial_audio_results), max(adversarial_audio_results), min(adversarial_audio_results), sum(adversarial_audio_results)/len(adversarial_audio_results)))
adversarial_audio_results.sort()
print(adversarial_audio_results)
print("")
