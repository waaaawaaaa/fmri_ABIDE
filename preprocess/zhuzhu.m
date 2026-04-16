
matlabbatch = prep('F:\ABIDE_DATA\raw_data\Caltech_51456');
spm_jobman('run',matlabbatch);

function matlabbatch = prep(file_name)
    [TR,slice_order,n_slices] = read_parameters(file_name);
    file_anat=fullfile(file_name,'anat/mprage.nii');
    fileListWithDir = icatb_rename_4d_file(fullfile(file_name,'func/rest.nii'));
    file_func=cellstr(fileListWithDir(11:end,:));
    TA=TR-TR/n_slices;
    refslice=ceil(n_slices/2);%时间层校正到中间切片
    %-----------------------------------------------------------------------
    % Job saved on 03-Dec-2023 21:48:26 by cfg_util (rev $Rev: 7345 $)
    % spm SPM - SPM12 (7771)
    % cfg_basicio BasicIO - Unknown
    %-----------------------------------------------------------------------
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'raw';
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{file_anat}};
    %%
    matlabbatch{2}.spm.temporal.st.scans = {
                                            {
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,11'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,12'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,13'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,14'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,15'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,16'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,17'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,18'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,19'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,20'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,21'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,22'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,23'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,24'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,25'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,26'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,27'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,28'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,29'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,30'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,31'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,32'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,33'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,34'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,35'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,36'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,37'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,38'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,39'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,40'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,41'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,42'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,43'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,44'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,45'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,46'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,47'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,48'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,49'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,50'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,51'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,52'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,53'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,54'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,55'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,56'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,57'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,58'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,59'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,60'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,61'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,62'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,63'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,64'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,65'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,66'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,67'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,68'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,69'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,70'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,71'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,72'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,73'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,74'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,75'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,76'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,77'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,78'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,79'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,80'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,81'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,82'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,83'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,84'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,85'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,86'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,87'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,88'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,89'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,90'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,91'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,92'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,93'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,94'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,95'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,96'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,97'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,98'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,99'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,100'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,101'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,102'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,103'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,104'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,105'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,106'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,107'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,108'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,109'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,110'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,111'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,112'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,113'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,114'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,115'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,116'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,117'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,118'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,119'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,120'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,121'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,122'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,123'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,124'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,125'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,126'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,127'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,128'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,129'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,130'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,131'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,132'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,133'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,134'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,135'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,136'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,137'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,138'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,139'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,140'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,141'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,142'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,143'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,144'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,145'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,146'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,147'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,148'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,149'
                                            'F:\ABIDE_DATA\raw_data\Caltech_51456\func\rest.nii,150'
                                            }
                                            }';
    %%
    matlabbatch{2}.spm.temporal.st.nslices = n_slices;
    matlabbatch{2}.spm.temporal.st.tr = TR;
    matlabbatch{2}.spm.temporal.st.ta = TA;
    matlabbatch{2}.spm.temporal.st.so = slice_order;
    matlabbatch{2}.spm.temporal.st.refslice = refslice;
    matlabbatch{2}.spm.temporal.st.prefix = 'a';
    matlabbatch{3}.spm.spatial.realign.estwrite.data{1}(1) = cfg_dep('Slice Timing: Slice Timing Corr. Images (Sess 1)', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.quality = 0.9;
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.sep = 4;
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.fwhm = 5;
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.rtm = 1;
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.interp = 2;
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.wrap = [0 0 0];
    matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.weight = '';
    matlabbatch{3}.spm.spatial.realign.estwrite.roptions.which = [2 1];
    matlabbatch{3}.spm.spatial.realign.estwrite.roptions.interp = 4;
    matlabbatch{3}.spm.spatial.realign.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{3}.spm.spatial.realign.estwrite.roptions.mask = 1;
    matlabbatch{3}.spm.spatial.realign.estwrite.roptions.prefix = 'r';
    matlabbatch{4}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('Realign: Estimate & Reslice: Mean Image', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rmean'));
    matlabbatch{4}.spm.spatial.coreg.estimate.source(1) = cfg_dep('Named File Selector: raw(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
    matlabbatch{4}.spm.spatial.coreg.estimate.other = {''};
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{4}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    matlabbatch{5}.spm.spatial.preproc.channel.vols(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{5}.spm.spatial.preproc.channel.biasreg = 0.001;
    matlabbatch{5}.spm.spatial.preproc.channel.biasfwhm = 60;
    matlabbatch{5}.spm.spatial.preproc.channel.write = [0 1];
    matlabbatch{5}.spm.spatial.preproc.tissue(1).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,1'};
    matlabbatch{5}.spm.spatial.preproc.tissue(1).ngaus = 1;
    matlabbatch{5}.spm.spatial.preproc.tissue(1).native = [1 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(1).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(2).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,2'};
    matlabbatch{5}.spm.spatial.preproc.tissue(2).ngaus = 1;
    matlabbatch{5}.spm.spatial.preproc.tissue(2).native = [1 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(2).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(3).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,3'};
    matlabbatch{5}.spm.spatial.preproc.tissue(3).ngaus = 2;
    matlabbatch{5}.spm.spatial.preproc.tissue(3).native = [1 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(3).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(4).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,4'};
    matlabbatch{5}.spm.spatial.preproc.tissue(4).ngaus = 3;
    matlabbatch{5}.spm.spatial.preproc.tissue(4).native = [1 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(4).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(5).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,5'};
    matlabbatch{5}.spm.spatial.preproc.tissue(5).ngaus = 4;
    matlabbatch{5}.spm.spatial.preproc.tissue(5).native = [1 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(5).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(6).tpm = {'D:\download\R2022a\toolbox\spm12\tpm\TPM.nii,6'};
    matlabbatch{5}.spm.spatial.preproc.tissue(6).ngaus = 2;
    matlabbatch{5}.spm.spatial.preproc.tissue(6).native = [0 0];
    matlabbatch{5}.spm.spatial.preproc.tissue(6).warped = [0 0];
    matlabbatch{5}.spm.spatial.preproc.warp.mrf = 1;
    matlabbatch{5}.spm.spatial.preproc.warp.cleanup = 1;
    matlabbatch{5}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
    matlabbatch{5}.spm.spatial.preproc.warp.affreg = 'mni';
    matlabbatch{5}.spm.spatial.preproc.warp.fwhm = 0;
    matlabbatch{5}.spm.spatial.preproc.warp.samp = 3;
    matlabbatch{5}.spm.spatial.preproc.warp.write = [0 1];
    matlabbatch{5}.spm.spatial.preproc.warp.vox = NaN;
    matlabbatch{5}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                                  NaN NaN NaN];
    matlabbatch{6}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
    matlabbatch{6}.spm.spatial.normalise.write.subj.resample(1) = cfg_dep('Realign: Estimate & Reslice: Resliced Images (Sess 1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','sess', '()',{1}, '.','rfiles'));
    matlabbatch{6}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                              78 76 85];
    matlabbatch{6}.spm.spatial.normalise.write.woptions.vox = [3 3 3];
    matlabbatch{6}.spm.spatial.normalise.write.woptions.interp = 4;
    matlabbatch{6}.spm.spatial.normalise.write.woptions.prefix = 'w';
    matlabbatch{7}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
    matlabbatch{7}.spm.spatial.normalise.write.subj.resample(1) = cfg_dep('Segment: Bias Corrected (1)', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','channel', '()',{1}, '.','biascorr', '()',{':'}));
    matlabbatch{7}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                              78 76 85];
    matlabbatch{7}.spm.spatial.normalise.write.woptions.vox = [1 1 1];
    matlabbatch{7}.spm.spatial.normalise.write.woptions.interp = 4;
    matlabbatch{7}.spm.spatial.normalise.write.woptions.prefix = 'w';
    matlabbatch{8}.spm.spatial.smooth.data(1) = cfg_dep('Normalise: Write: Normalised Images (Subj 1)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
    matlabbatch{8}.spm.spatial.smooth.fwhm = [8 8 8];
    matlabbatch{8}.spm.spatial.smooth.dtype = 0;
    matlabbatch{8}.spm.spatial.smooth.im = 0;
    matlabbatch{8}.spm.spatial.smooth.prefix = 's';
end