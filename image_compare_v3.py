from image_similarity_measures.evaluate import evaluation
from PIL import Image
import json
import os
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
from numpy import asarray
import numpy as np

# class_list = ['backpack', 'bike', 'calculator', 'headphones', 'keyboard', 'laptop_computer', 'monitor', 'mouse', 'mug', 'projector']
class_list = ['mug', 'projector']

for cls_name in class_list:

    cls_folder = cls_name+'/'

    os.chdir(cls_folder)
    syn_img = os.listdir()
    syn_img.remove('chosen')
    syn_img.remove('original')
    os.chdir('chosen')
    syn_img.extend(['chosen/'+s for s in os.listdir()])
    os.chdir('..')
    os.chdir('original')
    ori_img = ['original/'+s for s in os.listdir()]
    os.chdir('..')
    os.chdir('..')

    def img_compare(source_path, img1, img2):

        image_1 = Image.open(source_path+img1)
        image_1.resize((256,256)).save(source_path+'temp_1_v3.jpg')
        image_1 = asarray(Image.open(source_path+'temp_1_v3.jpg'))

        image_2 = Image.open(source_path+img2)
        image_2.resize((256,256)).save(source_path+'temp_2_v3.jpg')
        image_2 = asarray(Image.open(source_path+'temp_2_v3.jpg'))

        try:
            res_mse = mse(image_1, image_2)
        except:
            res_mse = np.nan
        try:
            res_rmse = rmse(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_psnr = psnr(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_ssim = ssim(image_1, image_2)[0]
        except:
            res_rmse = np.nan
        try:
            res_uqi = uqi(image_1, image_2)
        except:
            res_rmse = np.nan
        # res_msssim = msssim(image_1, image_2)
        try:
            res_ergas = ergas(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_scc = scc(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_rase = rase(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_sam = sam(image_1, image_2)
        except:
            res_rmse = np.nan
        try:
            res_vif = vifp(image_1, image_2)
        except:
            res_rmse = np.nan

        # res = {'MSE': res_mse, 'RMSE': res_rmse, 'PSNR': res_psnr, 'SSIM': res_ssim,  'UQI': res_uqi, 'MSSSIM': res_msssim, 'ERGAS': res_ergas, 'SCC': res_scc, 'RASE': res_rase, 'SAM': res_sam, 'VIF': res_vif}
        res = {'MSE': res_mse, 'RMSE': res_rmse, 'PSNR': res_psnr, 'SSIM': res_ssim,  'UQI': res_uqi, 'ERGAS': res_ergas, 'SCC': res_scc, 'RASE': res_rase, 'SAM': res_sam, 'VIF': res_vif}

        mean = 0.0
        for i, k in enumerate(res.keys()):
            mean += res[k]
        res['mean'] = mean/float(i)

        res['source'] = img1
        res['target'] = img2

        return res

    results = {}
    print('Results between original and synthetic images...')
    for i, x in enumerate(ori_img):
        res_x = []
        for j, y in enumerate(syn_img):
            # print('Original: {} | Synthetic: {}'.format(x, y))
            res = img_compare(cls_folder, x, y)
            # print(res)
            results[str(i)+'_'+str(j)] = res
            res_x.append(res)

    with open('resultsv3_{}.json'.format(cls_name), 'wt') as f:
        json.dump(results, f)
        f.close()
    print('Results saved as: {}'.format('resultsv3_{}.json'.format(cls_name)))

    print('Calculating metrics between synthetic images...')
    results = {}
    for i, x in enumerate(syn_img):
        for j, y in enumerate(syn_img):
            res_x = []
            if x != y:
                # print('Synthetic_1: {} | Synthetic_2: {}'.format(x, y))
                res = img_compare(cls_folder, x, y)
                # print(res)
                results[str(i)+'_'+str(j)] = res
                res_x.append(res)

    with open('results_interv3_{}.json'.format(cls_name), 'wt') as f:
        json.dump(results, f)
        f.close()
    print('Results saved as: {}'.format('results_interv3_{}.json'.format(cls_name)))
