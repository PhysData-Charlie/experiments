import json

def extract_keys(list_of_dicts): # made with ChatGPT 4.0
    all_keys = set()
    for dictionary in list_of_dicts:
        all_keys.update(dictionary.keys())
    return list(all_keys)

def metric_mean(df, x_list, y_list):
    mean, counter = 0, 0
    if len(x_list) != 0:
        for x in x_list:
            mean += df[x]
            counter += 1
    if len(y_list) != 0:
        for y in y_list:
            mean -= df[y]
            counter += 1
    mean /= counter
    return mean

def norm_list(df_list, key_list):
    max_vals = {k: 0.0 for k in key_list}
    for k in df_list.keys():
        for q in key_list:
            if max_vals[q] < df_list[k][q]:
                max_vals[q] = df_list[k][q]

    for k in df_list.keys():
        for q in key_list:
            df_list[k][q] = df_list[k][q] / max_vals[q]

    return df_list

def common_sets(l_list):
    s = set(l_list[0]) & set(l_list[1])
    for l in l_list[2:]:
        s_temp = s & set(l)
        s = s_temp

    return s

def sort_by(df1, df2, n, m, thr):
# for i in range(0,2):
    i = 0
    dfi = []
    for j in range(0,m):
        dfi.append({**df1[str(i+1)+'_'+str(j)], **df2[str(i+1)+'_'+str(j)]})
        # get metric means
        dfi[j]['mean'] = (dfi[j]['RMSE'] + dfi[j]['PSNR'] + dfi[j]['SSIM'] + dfi[j]['ERGAS'] + dfi[j]['SCC'] + dfi[j]['RASE'] + dfi[j]['VIF'] + dfi[j]['Fdist1'] + dfi[j]['Fdist2'] + dfi[j]['Fdist3'] + dfi[j]['MutInf']) / 11
        dfi[j]['mean_1'] = (dfi[j]['PSNR'] + dfi[j]['SSIM'] + dfi[j]['SCC'] + dfi[j]['RASE'] + dfi[j]['VIF']) / 5
        dfi[j]['mean_2'] = (dfi[j]['ERGAS'] + dfi[j]['RASE']) / 2
        dfi[j]['mean_3'] = (dfi[j]['mean_1'] - dfi[j]['mean_2']) / 2
        dfi[j]['mean_4'] = (dfi[j]['Fdist1'] + dfi[j]['Fdist2'] + dfi[j]['Fdist3']) / 3
        dfi[j]['mean_5'] = (dfi[j]['mean_4'] - dfi[j]['MutInf']) / 2

    counter, good_counter, best_counter, ok_counter = 0, 0, 0, 0
    good_list, best_list, ok_list = [], [], []

    ##### SORTING BY METRIC COMBINATIONS ######

    print('\n Trying sorting by individual metrics...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        counter += 1
        img_list = []
        dfi_sorted = sorted(dfi, key=lambda w: w[x], reverse=True)
        for j in range(0,n):
            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
            print('Not bad: sorting by {}'.format(x))
            good_counter += 1
            good_list.append({str(x): img_list})
            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                print('Best: sorting by: {}'.format(x))
                best_counter += 1
                best_list.append({str(x): img_list})
            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                print('Good: sorting by: {}'.format(x))
                ok_counter += 1
                ok_list.append({str(x): img_list})
            
    ###

    print('\nTrying sorting by means combination (2)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            if x != y:
                counter += 1
                img_list = []
                for j in range(0,m):
                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y], [])
                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                for j in range(0,n):
                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                    print('Not bad: sorting by {}+{}'.format(x, y))
                    good_counter += 1
                    good_list.append({str(x)+'+'+str(y): img_list})
                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                        print('Best: sorting by: {}+{}'.format(x, y))
                        best_counter += 1
                        best_list.append({str(x)+'+'+str(y): img_list})
                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                        print('Good: sorting by: {}+{}'.format(x, y))
                        ok_counter += 1
                        ok_list.append({str(x)+'+'+str(y): img_list})

    print('\nTrying sorting by means combination (2)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            if x != y:
                counter += 1
                img_list = []
                for j in range(0,m):
                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x], [y])
                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                for j in range(0,n):
                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                    print('Not bad: sorting by {}-{}'.format(x, y))
                    good_counter += 1
                    good_list.append({str(x)+'-'+str(y): img_list})
                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                        print('Best: sorting by: {}-{}'.format(x, y))
                        best_counter += 1
                        best_list.append({str(x)+'-'+str(y): img_list})
                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                        print('Good: sorting by: {}-{}'.format(x, y))
                        ok_counter += 1
                        ok_list.append({str(x)+'-'+str(y): img_list})

    ###

    print('\nTrying sorting by means combination (3)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                if (x != y) & (x != z) & (y != z):
                    counter += 1
                    img_list = []
                    for j in range(0,m):
                        dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y], [z])
                    dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                    for j in range(0,n):
                        img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                    if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                        print('Not bad: sorting by {}+{}-{}'.format(x, y, z))
                        good_counter += 1
                        good_list.append({str(x)+'+'+str(y)+'-'+str(z): img_list})
                        if len(set(good_images[cls_name]) & set(img_list)) == 10:
                            print('Best: sorting by: {}+{}-{}'.format(x, y, z))
                            best_counter += 1
                            best_list.append({str(x)+'+'+str(y)+'-'+str(z): img_list})
                        elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                            print('Good: sorting by: {}+{}-{}'.format(x, y, z))
                            ok_counter += 1
                            ok_list.append({str(x)+'+'+str(y)+'-'+str(z): img_list})

    print('\nTrying sorting by means combination (3)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                if (x != y) & (x != z) & (y != z):
                    counter += 1
                    img_list = []
                    for j in range(0,m):
                        dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z], [y])
                    dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                    for j in range(0,n):
                        img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                    if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                        print('Not bad: sorting by {}-{}+{}'.format(x, y, z))
                        good_counter += 1
                        good_list.append({str(x)+'-'+str(y)+'+'+str(z): img_list})
                        if len(set(good_images[cls_name]) & set(img_list)) == 10:
                            print('Best: sorting by: {}-{}+{}'.format(x, y, z))
                            best_counter += 1
                            best_list.append({str(x)+'-'+str(y)+'+'+str(z): img_list})
                        elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                            print('Good: sorting by: {}-{}+{}'.format(x, y, z))
                            ok_counter += 1
                            ok_list.append({str(x)+'-'+str(y)+'+'+str(z): img_list})

    print('\nTrying sorting by means combination (3)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                if (x != y) & (x != z) & (y != z):
                    counter += 1
                    img_list = []
                    for j in range(0,m):
                        dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z], [])
                    dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                    for j in range(0,n):
                        img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                    if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                        print('Not bad: sorting by {}+{}+{}'.format(x, y, z))
                        good_counter += 1
                        good_list.append({str(x)+'+'+str(y)+'+'+str(z): img_list})
                        if len(set(good_images[cls_name]) & set(img_list)) == 10:
                            print('Best: sorting by: {}+{}+{}'.format(x, y, z))
                            best_counter += 1
                            best_list.append({str(x)+'+'+str(y)+'+'+str(z): img_list})
                        elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                            print('Good: sorting by: {}+{}+{}'.format(x, y, z))
                            ok_counter += 1
                            ok_list.append({str(x)+'+'+str(y)+'+'+str(z): img_list})

    print('\nTrying sorting by means combination (3)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                if (x != y) & (x != z) & (y != z):
                    counter += 1
                    img_list = []
                    for j in range(0,m):
                        dfi[j]['mean_temp'] = metric_mean(dfi[j], [x], [y, z])
                    dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                    for j in range(0,n):
                        img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                    if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                        print('Not bad: sorting by {}-{}-{}'.format(x, y, z))
                        good_counter += 1
                        good_list.append({str(x)+'-'+str(y)+'-'+str(z): img_list})
                        if len(set(good_images[cls_name]) & set(img_list)) == 10:
                            print('Best: sorting by: {}-{}-{}'.format(x, y, z))
                            best_counter += 1
                            best_list.append({str(x)+'-'+str(y)+'-'+str(z): img_list})
                        elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                            print('Good: sorting by: {}-{}-{}'.format(x, y, z))
                            ok_counter += 1
                            ok_list.append({str(x)+'-'+str(y)+'-'+str(z): img_list})

    ###

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q], [])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}+{}+{}+{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}+{}+{}+{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}+{}+{}+{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z], [q])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}+{}+{}-{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}+{}+{}-{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}+{}+{}-{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q], [z])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}+{}-{}+{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}+{}-{}+{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}+{}-{}+{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q): img_list})
    
    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q], [y])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}-{}+{}+{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}-{}+{}+{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}-{}+{}+{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y], [z, q])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}+{}-{}-{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}+{}-{}-{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}+{}-{}-{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z], [y, q])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}-{}+{}-{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}-{}+{}-{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}-{}+{}-{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, q], [y, z])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}-{}-{}+{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}-{}-{}+{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}-{}-{}+{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = metric_mean(dfi[j], [x], [y, z, q])
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}-{}-{}-{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}-{}-{}-{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}-{}-{}-{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q): img_list})

    ###

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q, r], [])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}+{}+{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}+{}+{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}+{}+{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q], [r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}+{}+{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}+{}+{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}+{}+{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, r], [q])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}+{}-{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}+{}-{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}+{}-{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q, r], [z])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}-{}+{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}-{}+{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}-{}+{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q, r], [y])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}+{}+{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}+{}+{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}+{}+{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z], [q, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}+{}-{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}+{}-{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}+{}-{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q], [z, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}-{}+{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}-{}+{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}-{}+{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q], [y, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}+{}+{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}+{}+{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}+{}+{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, r], [z, q])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}-{}-{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}-{}-{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}-{}-{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, r], [y, q])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}+{}-{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}+{}-{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}+{}-{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, q, r], [y, z])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}-{}+{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}-{}+{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}-{}+{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y], [z, q, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}+{}-{}-{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}+{}-{}-{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}+{}-{}-{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z], [y, q, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}+{}-{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}+{}-{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}+{}-{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, q], [y, z, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}-{}+{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}+{}-{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}+{}-{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, r], [y, z, q])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}-{}-{}+{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}-{}-{}+{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}-{}-{}+{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r): img_list})

    print('\nTrying sorting by means combination (5)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        if (x != y) & (x != z) & (x != q) & (x != r) & (y != z) & (y != q) & (y != r) & (z != q) & (z != r) & (q != r):
                            counter += 1
                            img_list = []
                            for j in range(0,m):
                                dfi[j]['mean_temp'] = metric_mean(dfi[j], [x], [y, z, q, r])
                            dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                            for j in range(0,n):
                                img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                            if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                print('Not bad: sorting by {}-{}-{}-{}-{}'.format(x, y, z, q, r))
                                good_counter += 1
                                good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                    print('Best: sorting by: {}-{}-{}-{}-{}'.format(x, y, z, q, r))
                                    best_counter += 1
                                    best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})
                                elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                    print('Good: sorting by: {}-{}-{}-{}-{}'.format(x, y, z, q, r))
                                    ok_counter += 1
                                    ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r): img_list})

    ###

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q, r, t], [])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q, r], [t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q, t], [r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, r, t], [q])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q, r, t], [z])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q, r, t], [y])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}+{}+{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, q], [r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
    
    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, r], [q, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q, r], [z, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q, r], [y, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}+{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'+'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z, t], [q, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q, t], [z, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
    
    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q, t], [y, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}+{}-{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    
    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, z], [q, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, q], [z, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, q], [y, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y, t], [z, q, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z, t], [y, q, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, r, t], [y, z, q])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}-{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}-{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}-{}-{}+{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, y], [z, q, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}+{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}+{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}+{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'+'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, z], [y, q, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}+{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'+'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, q], [y, z, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}-{}+{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'+'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, r], [y, z, q, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}-{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}-{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}-{}-{}+{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'+'+str(r)+'-'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x, t], [y, z, q, r])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}-{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}-{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}-{}-{}-{}+{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'+'+str(t): img_list})

    print('\nTrying sorting by means combination (6)...\n')
    for x in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
        for y in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
            for z in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                for q in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                    for r in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                        for t in ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF', 'Fdist1', 'Fdist2', 'Fdist3', 'MutInf']:
                            if (x != y) & (x != z) & (x != q) & (x != r) & (x != t) & (y != z) & (y != q) & (y != r) & (y != t) & (z != q) & (z != r) & (z != t) & (q != r) & (q != t) & (r != t):
                                counter += 1
                                img_list = []
                                for j in range(0,m):
                                    dfi[j]['mean_temp'] = metric_mean(dfi[j], [x], [y, z, q, r, t])
                                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                                for j in range(0,n):
                                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                                    print('Not bad: sorting by {}-{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                    good_counter += 1
                                    good_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                        print('Best: sorting by: {}-{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        best_counter += 1
                                        best_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})
                                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                        print('Good: sorting by: {}-{}-{}-{}-{}-{}'.format(x, y, z, q, r, t))
                                        ok_counter += 1
                                        ok_list.append({str(x)+'-'+str(y)+'-'+str(z)+'-'+str(q)+'-'+str(r)+'-'+str(t): img_list})

    ##### SORTING BY MEANS COMBINATIONS ######

    print('\nTrying sorting by means...\n')
    for x in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
        counter += 1
        img_list = []
        dfi_sorted = sorted(dfi, key=lambda w: w[x], reverse=True)
        for j in range(0,n):
            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
            print('Not bad: sorting by {}'.format(x))
            good_counter += 1
            good_list.append({str(x): img_list})
            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                print('Best: sorting by: {}'.format(x))
                best_counter += 1
                best_list.append({str(x): img_list})
            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                print('Good: sorting by: {}'.format(x))
                ok_counter += 1
                ok_list.append({str(x): img_list})

    print('\nTrying sorting by means combination (2)...\n')
    for x in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
        for y in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
            if x != y:
                counter += 1
                img_list = []
                for j in range(0,m):
                    dfi[j]['mean_temp'] = (dfi[j][x] + dfi[j][y]) / 2
                dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                for j in range(0,n):
                    img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                    print('Not bad: sorting by {}-{}'.format(x, y))
                    good_counter += 1
                    good_list.append({str(x)+'_'+str(y): img_list})
                    if len(set(good_images[cls_name]) & set(img_list)) == 10:
                        print('Best: sorting by: {}-{}'.format(x, y))
                        best_counter += 1
                        best_list.append({str(x)+'_'+str(y): img_list})
                    elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                        print('Good: sorting by: {}-{}'.format(x, y))
                        ok_counter += 1
                        ok_list.append({str(x)+'_'+str(y): img_list})

    print('\nTrying sorting by means combination (3)...\n')
    for x in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
        for y in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
            for z in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
                if (x != y) & (x != z) & (y != z):
                    counter += 1
                    img_list = []
                    for j in range(0,m):
                        dfi[j]['mean_temp'] = (dfi[j][x] + dfi[j][y] + dfi[j][z]) / 3
                    dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                    for j in range(0,n):
                        img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                    if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                        print('Not bad: sorting by {}-{}-{}'.format(x, y, z))
                        good_counter += 1
                        good_list.append({str(x)+'_'+str(y)+'_'+str(z): img_list})
                        if len(set(good_images[cls_name]) & set(img_list)) == 10:
                            print('Best: sorting by: {}-{}-{}'.format(x, y, z))
                            best_counter += 1
                            best_list.append({str(x)+'_'+str(y)+'_'+str(z): img_list})
                        elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                            print('Good: sorting by: {}-{}-{}'.format(x, y, z))
                            ok_counter += 1
                            ok_list.append({str(x)+'_'+str(y)+'_'+str(z): img_list})

    print('\nTrying sorting by means combination (4)...\n')
    for x in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
        for y in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
            for y in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
                for q in ['mean', 'mean_1', 'mean_2', 'mean_3', 'mean_4', 'mean_5']:
                    if (x != y) & (x != z) & (x != q) & (y != z) & (y != q) & (z != q):
                        counter += 1
                        img_list = []
                        for j in range(0,m):
                            dfi[j]['mean_temp'] = (dfi[j][x] + dfi[j][y] + dfi[j][z] + dfi[j][q]) / 4
                        dfi_sorted = sorted(dfi, key=lambda w: w['mean_temp'], reverse=True)
                        for j in range(0,n):
                            img_list.extend([dfi_sorted[j].get(k) for k in ['target']])
                        if len(set(bad_images[cls_name]) & set(img_list)) == 0:
                            print('Not bad: sorting by {}-{}-{}-{}'.format(x, y, z, q))
                            good_counter += 1
                            good_list.append({str(x)+'_'+str(y)+'_'+str(z)+'_'+str(q): img_list})
                            if len(set(good_images[cls_name]) & set(img_list)) == 10:
                                print('Best: sorting by: {}-{}-{}-{}'.format(x, y, z, q))
                                best_counter += 1
                                best_list.append({str(x)+'_'+str(y)+'_'+str(z)+'_'+str(q): img_list})
                            elif len(set(good_images[cls_name]) & set(img_list)) >= thr:
                                print('Good: sorting by: {}-{}-{}-{}'.format(x, y, z, q))
                                ok_counter += 1
                                ok_list.append({str(x)+'_'+str(y)+'_'+str(z)+'_'+str(q): img_list})
                        
    print('Total cases analyzed: {}'.format(counter))
    print('Not bad cases found: {} ({}%)'.format(good_counter, round(good_counter/counter*100,1)))
    print('Good cases found: {} ({}%)'.format(ok_counter, round(ok_counter/counter*100,1)))
    print('Best cases found: {} ({}%)'.format(best_counter, round(best_counter/counter*100,1)))

    return counter, good_counter, ok_counter, best_counter, extract_keys(good_list), extract_keys(ok_list), extract_keys(best_list)
                

class_list = ['backpack', 'bike', 'calculator', 'headphones', 'keyboard', 'laptop_computer', 'monitor', 'mouse', 'mug', 'projector']
bad_images = {'backpack': ['sample_1 (2).jpg', 'sample_2 (3).jpg', 'sample_3 (1).jpg', 'sample_3 (3).jpg', 'sample_4 (1).jpg', 'sample_5 (1).jpg', 'sample_5.jpg', 'sample_6 (4).jpg', 'sample_6.jpg', 'sample_7 (3).jpg'],
            'bike': ['sample_19.jpg', 'sample_20.jpg', 'sample_21.jpg', 'sample_30.jpg'],
            'calculator': ['sample_3.jpg', 'sample_10.jpg', 'sample_12.jpg', 'sample_14.jpg', 'sample_16.jpg', 'sample_28.jpg'],
            'headphones': ['sample_15.jpg', 'sample_16.jpg', 'sample_21.jpg', 'sample_25.jpg', 'sample_26.jpg'],
            'keyboard': ['sample_0.jpg', 'sample_2 (4).jpg', 'sample_5 (2).jpg', 'sample_7 (2).jpg'],
            'laptop_computer': ['sample_2 (3).jpg', 'sample_3 (3).jpg', 'sample_3.jpg', 'sample_4 (1).jpg', 'sample_4 (2).jpg', 'sample_4 (3).jpg', 'sample_5 (1).jpg', 'sample_5 (2).jpg', 'sample_5 (4).jpg'],
            'monitor': ['sample_0.jpg', 'sample_1 (2).jpg', 'sample_1.jpg', 'sample_2.jpg', 'sample_4 (2).jpg', 'sample_5 (2).jpg', 'sample_5 (3).jpg', 'sample_6 (3).jpg', 'sample_6.jpg'],
            'mouse': ['sample_6 (1).jpg', 'sample_7 (3).jpg'],
            'mug': ['sample_0 (1).jpg', 'sample_1 (2).jpg', 'sample_2 (1).jpg', 'sample_3 (2).jpg', 'sample_3 (4).jpg', 'sample_5 (3).jpg', 'sample_6 (4).jpg'],
            'projector': ['sample_0 (1).jpg', 'sample_0 (5).jpg', 'sample_1 (4).jpg', 'sample_2 (1).jpg', 'sample_2 (2).jpg', 'sample_2 (4).jpg', 'sample_2.jpg', 'sample_3 (2).jpg', 'sample_3 (5).jpg', 'sample_4 (4).jpg', 'sample_4 (6).jpg', 'sample_5 (2).jpg', 'sample_5 (3).jpg', 'sample_6 (2).jpg', 'sample_7 (2).jpg']}
good_images = {c: ['chosen/sample_{}.jpg'.format(s) for s in range(0,10)] for c in class_list}

total_c, notbad_c, good_c, best_c, notbad_l, good_l, best_l = 0, [], [], [], [], [], []

for cls_name in class_list:

    filename1 = 'resultsv3_{}.json'.format(cls_name)
    filename2 = 'resultsv2_{}.json'.format(cls_name)

    df1 = json.load(open(filename1))
    df2 = json.load(open(filename2))

    m = len(df1) // 3

    print('\n== Analysis for class: {} ==\n'.format(cls_name))
    df1 = norm_list(df1, ['RMSE', 'PSNR', 'SSIM', 'ERGAS', 'SCC', 'RASE', 'VIF'])
    df2 = norm_list(df2, ['Fdist1', 'Fdist2', 'Fdist3', 'MutInf'])
    t_c, n_c, g_c, b_c, n_l, g_l, b_l = sort_by(df1, df2, 10, m, 3)

    res = {'Not_bad': n_l, 'Good': g_l, 'Best': b_l}

    with open('metricsv5_results_{}.json'.format(cls_name), 'wt') as f:
        json.dump(res, f)
        f.close()

    notbad_l.append(n_l)
    good_l.append(g_l)
    best_l.append(b_l)
    notbad_c.append(n_c)
    good_c.append(g_c)
    best_c.append(b_c)
    total_c += t_c


# print('\n\nMinimum not bad cases: {}'.format(min(notbad_c)))
# print('Minimum good cases: {}'.format(min(good_c)))
# print('Minimum best cases: {}'.format(min(best_c)))

print('\nTotal cases analyzed: ', total_c)
print('\nNot bad cases per class:', [str(x)+'-'+str(y) for x,y in zip(class_list, notbad_c)])
print('Good cases per class:', [str(x)+'-'+str(y) for x,y in zip(class_list, good_c)])
print('Best cases per class:', [str(x)+'-'+str(y) for x,y in zip(class_list, best_c)])

common_notbad = common_sets(notbad_l)
common_good = common_sets(good_l)
common_best = common_sets(best_l)

print('\nCommon not bad cases: {}'.format(len(common_notbad)))
print(common_notbad)
print('\nCommon good cases: {}'.format(len(common_good)))
print(common_good)
print('\nCommon best cases: {}'.format(len(common_best)))
print(common_best)

res = {'Not_bad': list(common_notbad), 'Good': list(common_good), 'Best': list(common_best)}

with open('metricsv5_results.json', 'wt') as f:
    json.dump(res, f)
    f.close()

    