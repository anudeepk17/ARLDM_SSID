import argparse
import json
import os

import cv2
import h5py
import numpy as np
from PIL import Image
from tqdm import tqdm


def main(args):
    train_data = json.load(open(os.path.join(args.ssid_json_dir, 'SSID_Train.json')))
    val_data = json.load(open(os.path.join(args.ssid_json_dir, 'SSID_Validation.json')))
    test_data = json.load(open(os.path.join(args.ssid_json_dir, 'SSID_Test.json')))

    prefix = ["train", "val", "test"]
    whole_album = {}
    for i, data in enumerate([train_data, val_data, test_data]):
        album_mapping = {}
        for annot_new in data["annotations"]:
            annot = annot_new[0]
            assert len(annot_new) == 1
            if annot['story_id'] not in album_mapping:
                album_mapping[annot['story_id']] = {"youtube_image_id": [annot['youtube_image_id']],
                                                    "storytext": [annot['storytext']],
                                                    "image_order": [annot['image_order']]}
            else:
                album_mapping[annot['story_id']]["youtube_image_id"].append(annot['youtube_image_id'])
                album_mapping[annot['story_id']]["storytext"].append(
                    annot['storytext'])
                album_mapping[annot['story_id']]["image_order"].append(annot['image_order'])
        whole_album[prefix[i]] = album_mapping

    # for p in prefix:
    #     deletables = []
    #     for story_id, story in whole_album[p].items():
    #         if story['image_order'] >= 5:
    #             print("deleting {}".format(story_id))
    #             deletables.append(story_id)
    #             continue
    #         d = [os.path.exists(os.path.join(args.img_dir, "{}.jpg".format(_))) for _ in story["youtube_image_id"]]
    #         if sum(d) < 5:
    #             print("deleting {}".format(story_id))
    #             deletables.append(story_id)
    #         else:
    #             pass
    #     for i in deletables:
    #         del whole_album[p][i]

    
    f = h5py.File(args.save_path, "w")
    for p in prefix:
        group = f.create_group(p)
        story_dict = whole_album[p]
        length = len(story_dict)
        images = list()
        for i in range(5):
            images.append(
                group.create_dataset('image{}'.format(i), (length,), dtype=h5py.vlen_dtype(np.dtype('uint8'))))
        ssid = group.create_dataset('ssid', (length,), dtype=h5py.string_dtype(encoding='utf-8'))
        for i, (story_id, story) in enumerate(tqdm(story_dict.items(), leave=True, desc="saveh5")):
            imgs = [Image.open('{}/{}.jpg'.format(args.img_dir, yt_id)).convert('RGB') for yt_id in
                    story['youtube_image_id']]
            for j, img in enumerate(imgs):
                img = np.array(img).astype(np.uint8)
                img = cv2.imencode('.png', img)[1].tobytes()
                img = np.frombuffer(img, np.uint8)
                images[j][i] = img
            ssid[i] = '|'.join([t.replace('\n', '').replace('\t', '').strip() for t in story['storytext']])
            # txt_dii = [t.replace('\n', '').replace('\t', '').strip() for t in story['dii']]
            # txt_dii = sorted(set(txt_dii), key=txt_dii.index)
            #dii[i] = '|'.join(txt_dii)
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments for vist hdf5 file saving')
    parser.add_argument('--ssid_json_dir', type=str, required=True, help='ssid json file directory')
    parser.add_argument('--img_dir', type=str, required=True, help='json file directory')
    parser.add_argument('--save_path', type=str, required=True, help='path to save hdf5')
    args = parser.parse_args()
    main(args)
