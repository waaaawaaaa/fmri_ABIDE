% icatb_batch_file_run('Input_spatial_ica.m')

% Enter the values for the variables required for the ICA analysis.
% Variables are on the left and the values are on the right.
% Characters must be enterd in single quotes
%
% After entering the parameters, use icatb_batch_file_run(inputFile); 

% numselectComp=50;%对特征值进行筛选时，最后筛选出来的特征数量

% global TIMECOURSE_POSTPROCESS;
% TIMECOURSE_POSTPROCESS.save_timecourses = 1;
input_data_hd_patterns = {'F:\ABIDE_DATA\raw_data\UCLA_51310\func\rp_arest.txt';
    'F:\ABIDE_DATA\raw_data\UCLA_51311\func\rp_arest.txt';
    'F:\ABIDE_DATA\raw_data\UCLA_51312\func\rp_arest.txt'};

%% Modality. Options are fMRI and EEG
modalityType = 'fMRI';

%% Type of stability analysis
% Options are 1 and 2.
% 1 - Regular Group ICA
% 2 - Group ICA using icasso
% 3 - Group ICA using Minimum spanning tree (MST)
which_analysis = 2;

%% ICASSO options. 单个受试者，按论文意思用不上，注释掉
% This variable will be used only when which_analysis variable is set to 2.
icasso_opts.sel_mode = 'randinit';  % Options are 'randinit', 'bootstrap' and 'both'
icasso_opts.num_ica_runs = 2; % Number of times ICA will be run
% Most stable run estimate is based on these settings. 
icasso_opts.min_cluster_size = 2; % Minimum cluster size
icasso_opts.max_cluster_size =80; % Max cluster size. Max is the no. of components

%% Enter TR in seconds. If TRs vary across subjects, TR must be a row vector of length equal to the number of subjects.
TR = [1,2,3];


%% Group ica type
% Options are spatial or temporal for fMRI modality. By default, spatial
% ica is run if not specified.
group_ica_type = 'spatial';

%% Parallel info
% enter mode serial or parallel. If parallel, enter number of
% sessions/workers to do job in parallel
parallel_info.mode = 'serial';
% parallel_info.mode = 'parallel';
parallel_info.num_workers = 4;

%% Group PCA performance settings. Best setting for each option will be selected based on variable MAX_AVAILABLE_RAM in icatb_defaults.m. 
% If you have selected option 3 (user specified settings) you need to manually set the PCA options. See manual or other
% templates (icatb/icatb_batch_files/Input_data_subjects_1.m) for more information to set PCA options 
%
% Options are:
% 1 - Maximize Performance
% 2 - Less Memory Usage
% 3 - User Specified Settings
perfType = 1;

%% Conserve disk space
% Conserve disk space. Options are:
% 0 - Write all analysis files including intermediate files (PCA, Backreconstruction, scaled component MAT files)
% 1 - Write only necessary files required to resume the analysis. The files written are as follows:
%   a. Data reduction files - Only eigen vectors and eigen values are written in the first data reduction step. PCA components are written at the last reduction stage.
%   b. Back-reconstruction files - Back-reconstruction files are not written to the disk. The information is computed while doing scaling components step
%   c. Scaling components files - Scaling components MAT files are not written when using GIFT or SBM.
%   d. Group stats files - Only mean of all data-sets is written.
% 2 - Write all files till the group stats. Cleanup intermediate files at the end of the group stats (PCA, Back-reconstruct, Scaled component MAT files in GIFT). Analysis cannot be
% resumed if there are any changes to the setup parameters. Utilities that work with PCA and Backreconstruction files like Remove components, Percent Variance, etc won't work with this option .
conserve_disk_space = 0;


%% Design matrix selection
% Design matrix (SPM.mat) is used for sorting the components
% temporally (time courses) during display. Design matrix will not be used during the
% analysis stage except for SEMI-BLIND ICA.
% options are ('no', 'same_sub_same_sess', 'same_sub_diff_sess', 'diff_sub_diff_sess')
% 1. 'no' - means no design matrix.
% 2. 'same_sub_same_sess' - same design over subjects and sessions
% 3. 'same_sub_diff_sess' - same design matrix for subjects but different
% over sessions
% 4. 'diff_sub_diff_sess' - means one design matrix per subject.

keyword_designMatrix = 'no';

% specify location of design matrix here if you have selected 'same_sub_same_sess' or
% 'same_sub_diff_sess' option for keyword_designMatrix variable
% OnedesignMat = 'C:\MATLAB6p5p2\work\Example Subjects\Visuomotor_data\SPM.mat';

%% Specify BIDS info. Data file patterns is read from the bids structure and input_data_file_patterns variable is skipped
% bids_info.root_dir = root_dir;
% bids_info.subjects =;
% bids_info.sessions =; 
% bids_info.task =; 


%% There are three ways to enter the subject data
% options are 1, 2, 3 or 4
dataSelectionMethod = 4;


%% Method 1

% If you have all subjects in one directory and their sessions in a separate folder or in the subject folder then specify 
% root directory, filePattern, flag and file numbers to include.
% Options for flag are: data_in_subject_folder, data_in_subject_subfolder
%
% 1. data_in_subject_subfolder - Data is selected from the subject sub
% folders. Number of sessions is equal to the number of sub-folders
% containing the specified file pattern.
%
% 2. data_in_subject_folder - Data is selected from the subject
% folders. Number of sessions is 1 and number of subjects is equal to the number of subject folders
% containing the specified file pattern.

% You can provide the file numbers ([1:220]) to include as a vector. If you want to
% select all the files then leave empty.

% Note: Make sure the sessions are the same over subjects.

sourceDir_filePattern_flagLocation = {'F:\ABIDE_DATA1\processed_data', '*.nii'};

% Specify design matrix filter pattern here if you have selected
% 'diff_sub_diff_sess' option for keyword_designMatrix variable for Method 1. It looks
% for the design matrix in the respective subject folder or session folders.
% spmDesignFilter = 'SPM*.mat';    

%%%%%%%%%%%%%%%%%%%%%%%%% end for Method 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Method 4
% Input data file pattern for data-sets must be in a cell array. The no. of rows of cell array correspond to no. of subjects
% and columns correspond to sessions. In the below example, there are 3
% subjects and 1 session. If you have multiple sessions, please see
% Input_data_subjects_2.m file.
% input_data_file_patterns = {'C:\MATLAB6p5p2\work\Example Subjects\Visuomotor_data\sub01_vis\ns*.img';
%     'C:\MATLAB6p5p2\work\Example Subjects\Visuomotor_data\sub02_vis\ns*.img';
%     'C:\MATLAB6p5p2\work\Example Subjects\Visuomotor_data\sub03_vis\ns*.img'};
% file_root = 'F:/ABIDE_DATA1/raw_data';
% smooth_filename = find_smooth_filename(file_root);
% input_data_file_patterns = smooth_filename;
input_data_file_patterns = {'F:\ABIDE_DATA\raw_data\UCLA_51310\func\sw*.nii';
    'F:\ABIDE_DATA\raw_data\UCLA_51311\func\sw*.nii';
    'F:\ABIDE_DATA\raw_data\UCLA_51312\func\sw*.nii'};

% Input for design matrices will be used only if you have a design matrix
% for each subject i.e., if you have selected 'diff_sub_diff_sess' for
% variable keyword_designMatrix.
% input_design_matrices = {};

% Enter no. of dummy scans to exclude from the group ICA analysis. If you have no dummy scans leave it as 0.
dummy_scans = 0;

%%%%%%%% End for Method 4 %%%%%%%%%%%%

%% Enter directory to put results of analysis
outputDir = 'F:\preprocess\feature_extra';

%% Enter Name (Prefix) Of Output Files
prefix = 'g';

%% Enter location (full file path) of the image file to use as mask
% or use Default mask which is []
maskFile = [];

%% Group PCA Type. Used for analysis on multiple subjects and sessions when 2 data reduction steps are used.
% Options are 'subject specific' and 'grand mean'. 
%   a. Subject specific - Individual PCA is done on each data-set before group
%   PCA is done.
%   b. Grand Mean - PCA is done on the mean over all data-sets. Each data-set is
%   projected on to the eigen space of the mean before doing group PCA.
%
% NOTE: Grand mean implemented is from FSL Melodic. Make sure that there are
% equal no. of timepoints between data-sets.
%
group_pca_type = 'subject specific';

%% Back reconstruction type. Options are 1 and 2
% 1 - Regular
% 2 - Spatial-temporal Regression 
% 3 - GICA3
% 4 - GICA
% 5 - GIG-ICA
backReconType = 4;

%% Data Pre-processing options
% 1 - Remove mean per time point按时间点去除均值
% 2 - Remove mean per voxel按体素去除均值
% 3 - Intensity normalization强度归一化
% 4 - Variance normalization方差归一化
preproc_type = 3;

%% Maximum reduction steps you can select is 2
% You have the option to select one data-reduction or 2 data reduction
% steps when spatial ica is used. For temporal ica, only one data-reduction
% is done.
numReductionSteps = 2;

%% Batch Estimation. If 1 is specified then estimation of 
% the components takes place and the corresponding PC numbers are associated
% Options are 1 or 0
doEstimation = 0; %估计成分数


%% MDL Estimation options. This variable will be used only if doEstimation is set to 1.
% Options are 'mean', 'median' and 'max' for each reduction step. The length of cell is equal to
% the no. of data reductions used.
% estimation_opts.PC1 = 'max';
% estimation_opts.PC2 = 'mean';

%% Number of pc to reduce each subject down to at each reduction step
% The number of independent components the will be extracted is the same as 
% the number of principal components after the final data reduction step.  
numOfPC1 = 100;
numOfPC2 = 80;

%% Scale the Results. Options are 0, 1, 2
% 0 - Don't scale
% 1 - Scale to Percent signal change
% 2 - Scale to Z scores
scaleType = 0;


%% 'Which ICA Algorithm Do You Want To Use';
% see icatb_icaAlgorithm for details or type icatb_icaAlgorithm at the
% command prompt.
% Note: Use only one subject and one session for Semi-blind ICA. Also specify atmost two reference function names

% 1 means infomax, 2 means fastICA, etc.
algoType = 1;

%% Report generator (fmri and smri only)
display_results.formatName = 'html'; 
display_results.slices_in_mm = (-40:4:72);
display_results.convert_to_zscores = 'yes';
display_results.threshold = 1.0;
display_results.image_values = 'positive and negative';
display_results.slice_plane = 'axial';
display_results.anatomical_file = 'D:\download\R2022a\toolbox\icatb\icatb_templates\ch2bet_3x3x3.nii';

% %Network names and components are used in the plots (only fmri). If you are using
% %moo-icar or constrained ica (spatial), you can specify network names and
% %components within each network. Below is an example from neuromark
% %template labels
% display_results.network_summary_opts.comp_network_names = { 'SC', (1:5);                    
%                                     'AU', (6:7);                  
%                                     'SM', (8:16);  
%                                     'VI', (17:25); 
%                                     'CC', (26:42);      
%                                     'DM', (43:49);
%                                     'CB', (50:53)};
% display_results.network_summary_opts.outputDir = fullfile(outputDir, 'network_summary');
% display_results.network_summary_opts.prefix = [prefix, '_network_summary'];
% display_results.network_summary_opts.structFile = display_results.anatomical_file;
% display_results.network_summary_opts.image_values = display_results.image_values;
% display_results.network_summary_opts.threshold = display_results.threshold;
% display_results.network_summary_opts.convert_to_z = display_results.convert_to_zscores;
%   %some more network summary options
%display_results.network_summary_opts.conn_threshold = 0.2;
%display_results.network_summary_opts.fnc_colorbar_label = 'Corr';
% options are 'slices' and 'render'
%display_results.network_summary_opts.display_type = 'slices';
%display_results.network_summary_opts.slice_plane = 'axial';
% colormap of the correlations
%display_results.network_summary_opts.cmap = jet(64);
% CLIM - range of the data values in [min_value, max_value] format
%display_results.network_summary_opts.CLIM=CLIM;


%% ICA Options - Name by value pairs in a cell array. Options will vary depending on the algorithm. See icatb_icaOptions for more details. Some options are shown below.
% Infomax -  {'posact', 'off', 'sphering', 'on', 'bias', 'on', 'extended', 0}
% FastICA - {'approach', 'symm', 'g', 'tanh', 'stabilization', 'on'}

icaOptions = {'posact', 'off', 'sphering', 'on', 'bias', 'on', 'extended', 0};


%% Specify atmost two reference function names if you select Semi-blind ICA algorithm.
% Reference function names can be acessed by loading SPM.mat in MATLAB and accessing 
% structure SPM.xX.name.
% refFunNames = {'Sn(1) right*bf(1)', 'Sn(1) left*bf(1)'};


%% Specify spatial reference files for constrained ICA (spatial) or moo-icar
% refFiles = {which('ref_default_mode.nii'), which('ref_left_visuomotor.nii'), which('ref_right_visuomotor.nii')};