import argparse
import json
import os
from os import listdir
import cv2
import h5py
import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import gridspec
ssid_json_dir='/Users/anudeep/Desktop/Desktop/Fall23/BMI771/ARLDM/SSID/SSID_Annotations/'
save_samples_dir='/Users/anudeep/Desktop/Desktop/Fall23/BMI771/ARLDM/save_samples_cont'
ssid_img_dir='/Users/anudeep/Desktop/Desktop/Fall23/BMI771/ARLDM/SSID/SSID_Images'
save_path_dir='/Users/anudeep/Desktop/Desktop/Fall23/BMI771/ARLDM/finalCont'
task='visualization' #'continuation
test_data = json.load(open(os.path.join(ssid_json_dir, 'SSID_Test.json')))
imgInit=0
album_mapping={}
annot_new=test_data["annotations"]
if task=='visualization':
    for i in range(len(annot_new)):
        annot = annot_new[i][0]
        assert len(annot_new[i]) == 1
        if annot['story_id'] not in album_mapping:
            album_mapping[annot['story_id']] = {"youtube_image_id": [annot['youtube_image_id']],
                                                "storytext": [annot['storytext']],
                                                "predicted_id": ["{0:0=4d}".format(i)]}
        else:
            album_mapping[annot['story_id']]["youtube_image_id"].append(annot['youtube_image_id'])
            album_mapping[annot['story_id']]["storytext"].append(
                annot['storytext'])
            album_mapping[annot['story_id']]["predicted_id"].append("{0:0=4d}".format(i))
    #print(album_mapping)
    for key in album_mapping.keys():
        real_img = [Image.open('{}/{}.jpg'.format(ssid_img_dir, yt_id)).convert('RGB') for yt_id in
                        album_mapping[key]['youtube_image_id']]
        predict_img=[Image.open('{}/{}.png'.format(save_samples_dir, yt_id)).convert('RGB') for yt_id in
                        album_mapping[key]['predicted_id']]
        image=[real_img,predict_img]
        nrow = 2
        ncol = 5
        fig = plt.figure(figsize=(ncol+1, nrow+1)) 
        gs = gridspec.GridSpec(nrow, ncol,
                wspace=0.0, hspace=0.0, 
                top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
                left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
        for i in range(nrow):
            for j in range(ncol):
                ax= plt.subplot(gs[i,j])
                ax.imshow(image[i][j])
                ax.set_xticklabels([])
                ax.set_yticklabels([])
        footnote_text=""""""
        for j in range(len(album_mapping[key]['storytext'])):
            footnote_text=footnote_text+'\n'+str(j+1)+'.'+album_mapping[key]['storytext'][j]
        plt.figtext(0,1,footnote_text, fontsize=10, color='black')
        save_path = os.path.join(save_path_dir, f'figure_{key}.png')  # Change 'path_to_save_directory'
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()  # Close the figure to avoid multiple plots in the same figure
elif task=='continuation':
    j=0
    for i in range(len(annot_new)):
        annot = annot_new[i][0]
        assert len(annot_new[i]) == 1
        if annot['story_id'] not in album_mapping:
            album_mapping[annot['story_id']] = {"youtube_image_id": [annot['youtube_image_id']],
                                                "storytext": [annot['storytext']],
                                                "predicted_id": [annot['youtube_image_id']]}
        else:
            album_mapping[annot['story_id']]["youtube_image_id"].append(annot['youtube_image_id'])
            album_mapping[annot['story_id']]["storytext"].append(
                annot['storytext'])
            album_mapping[annot['story_id']]["predicted_id"].append("{0:0=4d}".format(j))
            j+=1

    for key in album_mapping.keys():
        real_img = [Image.open('{}/{}.jpg'.format(ssid_img_dir, yt_id)).convert('RGB') for yt_id in
                        album_mapping[key]['youtube_image_id']]
        predict_img=[Image.open('{}/{}.jpg'.format(ssid_img_dir, album_mapping[key]['predicted_id'][0])).convert('RGB')] 
        for yt_id in range(1,len(album_mapping[key]['predicted_id'])):
            predict_img.append(Image.open('{}/{}.png'.format(save_samples_dir, album_mapping[key]['predicted_id'][yt_id])).convert('RGB'))
        image=[real_img,predict_img]
        nrow = 2
        ncol = 5
        fig = plt.figure(figsize=(ncol+1, nrow+1)) 
        gs = gridspec.GridSpec(nrow, ncol,
                wspace=0.0, hspace=0.0, 
                top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
                left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
        for i in range(nrow):
            for j in range(ncol):
                ax= plt.subplot(gs[i,j])
                ax.imshow(image[i][j])
                ax.set_xticklabels([])
                ax.set_yticklabels([])
        footnote_text=""""""
        for j in range(len(album_mapping[key]['storytext'])):
            footnote_text=footnote_text+'\n'+str(j+1)+'.'+album_mapping[key]['storytext'][j]
        plt.figtext(0,1,footnote_text, fontsize=10, color='black')
        save_path = os.path.join(save_path_dir, f'figure_{key}.png')  # Change 'path_to_save_directory'
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()  # Close the figure to avoid multiple plots in the same figure

