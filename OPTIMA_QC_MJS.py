import numpy as np
import os
import pandas as pd

datafolder = os.path.expanduser('~/VossLabMount/Projects/Optima/PreprocData')
os.chdir(datafolder)

QC_summary = pd.DataFrame(columns = ['Subject','MPRAGE','Rest','FieldMap','SNR',
                                             'Relative Motion Mean','Relative Motion Median',
                                             'Relative Motion SD','Relative Motion Variance',
                                             'Relative Motion Max',
                                             'Absolute Motion Mean','Absolute Motion Median',
                                             'Absolute Motion SD','Absolute Motion Variance',
                                             'Absolute Motion Max',
                                             'FD Mean','FD Median',
                                             'FD SD','FD Variance',
                                             'FD Min','FD Max',
                                             ])

s = open(os.path.join(datafolder, 'fast_crossx_trim.txt'),'r')
subjects = []
for line in s.readlines():
    subjects.append(line.replace('\n','').split(' '))

s.close()

for sub in subjects:
    

    sub = ''.join(sub)
    subtime = "sub" + sub
    print subtime
    subdir = os.path.join(datafolder, subtime, 'rsOut')
    print subdir
    if not os.path.exists(os.path.join(subdir,'func')):
        print subtime,"does not exist!"
        continue
    if os.path.isfile(os.path.join(subdir,'anat/T1_MNI.nii.gz')):
        MPRAGE=1
        print "MPRAGE = ",MPRAGE
    else:
        MPRAGE=0
        print "MPRAGE = ",MPRAGE
    if os.path.isfile(os.path.join(subdir,'func/RestingStateRaw.nii.gz')):
        REST=1
        print "REST = ",REST
    else:
        REST=0
        print "REST = ",REST
    if os.path.isfile(os.path.join(subdir,'fieldMap/fieldMapMag.nii.gz')):
        FieldMap=1
        print "FieldMap = ",FieldMap
    else:
        FieldMap=0
        print "FieldMap = ",FieldMap
    for line in open(os.path.join(subdir,'func/SNRcalc.txt')):
        columns = line.split(" ")
        SNR=columns[2]
        print "SNR = ",SNR # indexing starts at zeroos.system("awk '{print $3}' os.path.join(subdir,'func/SNRcalc.txt')")
    rel_mot=np.loadtxt(os.path.join(subdir,'func/mcImg_rel.rms'))
    rel_mot_mean = np.mean(rel_mot, dtype=np.float32)
    print "Relative Motion Mean = ",rel_mot_mean
    rel_mot_median = np.median(rel_mot)
    print "Relative Motion Median = ",rel_mot_median
    rel_mot_sd = np.std(rel_mot, dtype=np.float32)
    print "Relative Motion SD = ",rel_mot_sd
    rel_mot_var = np.var(rel_mot, dtype=np.float32)
    print "Relative Motion Variance = ",rel_mot_var
    rel_mot_max = np.amax(rel_mot)
    print "Relative Motion Max = ",rel_mot_max
    abs_mot=np.loadtxt(os.path.join(subdir,'func/mcImg_abs.rms'))
    abs_mot_mean = np.mean(abs_mot, dtype=np.float32)
    print "Absolute Motion Mean = ",abs_mot_mean
    abs_mot_median = np.median(abs_mot)
    print "Absolute Motion Median = ",abs_mot_median
    abs_mot_sd = np.std(abs_mot, dtype=np.float32)
    print "Absolute Motion SD = ",abs_mot_sd
    abs_mot_var = np.var(abs_mot, dtype=np.float32)
    print "Absolute Motion Variance = ",abs_mot_var
    abs_mot_max = np.amax(abs_mot)
    print "Absolute Motion Max = ",abs_mot_max
    if os.path.isfile(os.path.join(subdir,'func/nuisancereg_classic_aroma.feat/stats/fd.txt')):
        fd=np.loadtxt(os.path.join(subdir,'func/nuisancereg_classic_aroma.feat/stats/fd.txt'))
        fd_mean = np.mean(fd, dtype=np.float32)
        print "FD Mean = ",fd_mean
        fd_median = np.median(fd)
        print "FD Median = ",fd_median
        fd_sd = np.std(fd, dtype=np.float32)
        print "FD SD = ",fd_sd
        fd_var = np.var(fd, dtype=np.float32)
        print "FD Variance = ",fd_var
        fd_min = np.amin(fd)
        print "FD Min = ",fd_min
        fd_max = np.amax(fd)
        print "FD Max = ",fd_max
    else:
        print "fd.txt file not found"
        fd_mean = np.nan
        print "FD Mean = ",fd_mean
        fd_median = np.nan
        print "FD Median = ",fd_median
        fd_sd = np.nan
        print "FD SD = ",fd_sd
        fd_var = np.nan
        print "FD Variance = ",fd_var
        fd_min = np.nan
        print "FD Min = ",fd_min
        fd_max = np.nan
        print "FD Max = ",fd_max
    summary_row=pd.Series([sub,MPRAGE,REST,FieldMap,SNR,rel_mot_mean,rel_mot_median,rel_mot_sd,rel_mot_var,rel_mot_max,
                      abs_mot_mean,abs_mot_median,abs_mot_sd,abs_mot_var,abs_mot_max,
                      fd_mean,fd_median,fd_sd,fd_var,fd_min,fd_max],['Subject','MPRAGE','Rest','FieldMap','SNR',
                      'Relative Motion Mean','Relative Motion Median',
                      'Relative Motion SD','Relative Motion Variance',
                      'Relative Motion Max',
                      'Absolute Motion Mean','Absolute Motion Median',
                      'Absolute Motion SD','Absolute Motion Variance',
                      'Absolute Motion Max',
                      'FD Mean','FD Median',
                      'FD SD','FD Variance',
                      'FD Min','FD Max',
                      ])
    print summary_row
    QC_summary=QC_summary.append([summary_row], ignore_index=True)

QC_summary.to_csv(os.path.join(datafolder, 'MR_quality_logs/Optima_QC_data.csv'), index = False)
