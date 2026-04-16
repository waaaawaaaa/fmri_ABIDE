% 2023.11.24 zhumengying
%根据TC，使用Chronux计算频谱
function [sesInfo] = calculate_spectrum(sesInfo, statusHandle)


if ~exist('sesInfo','var')
    %P=icatb_spm_get(1,'*.mat','Select Parameter File');
    [P] = icatb_selectEntry('typeEntity', 'file', 'title', 'Select Parameter File', 'filter', '*param*.mat');
    if isempty(P)
        error('Parameter file is not selected for analysis');
    end
    [pathstr,fileName]=fileparts(P);
    outputDir = pathstr;
    sesInfo.outputDir = outputDir;
    % Make sure parameter file exists
    load(P);
    if(~exist('sesInfo','var'))
        %         infoCell{1} = P;
        %         icatb_error('The selected file does not contain sesInfo variable', infoCell);
        error(['The selected file ', P, ' does not contain the sesInfo variable']);
    end
else
    outputDir = sesInfo.outputDir;
end

if ~exist('statusHandle', 'var')
    statusHandle = [];
end

if sesInfo.isInitialized == 0
    error('Parameter file has not been initialized');
end


icatb_defaults;

time_series_path = fullfile(outputDir, 'g_agg__component_ica_.nii');
time_series_matrix = niftiread(time_series_path);
load(fullfile(outputDir, [sesInfo.ica_mat_file, '.mat']));

% 设置参数
params.tapers = [3 5]; % 多窗参数，[time_bandwidth, number_of_tapers]
params.Fs = 1; % 采样率
params.fpass = [0 0.1]; % 频率范围

% 计算频谱
[spectrum, frequency] = mtspectrumc(time_series_matrix, params);
% 计算低频谱功率
low_freq_power = trapz(frequency, spectrum); % 对频谱进行积分，得到低频谱功率

% 对低频谱功率进行排序并找到前20个
[sorted_power, sorted_index] = sort(low_freq_power, 'descend');
top_IC_indices = sorted_index(1:20);

icasig_select = icasig(top_IC_indices);

% save in matlab format
icaout = [sesInfo.ica_mat_file, '_sel.mat'];

sesInfo.ica_mat_file = icaout;

icaout = fullfile(outputDir, icaout);


[pp, fileName] = fileparts(sesInfo.userInput.param_file);

j = sesInfo.numReductionSteps;
[dewhiteM, whiteM, pcasig] = load_vars(fullfile(outputDir, [sesInfo.data_reduction_mat_file, '1-', num2str(j), '.mat']));

icatb_save(icaout, 'W', 'icasig_select', 'mask_ind', 'skew');
icatb_save(fullfile(outputDir, [fileName, '.mat']), 'sesInfo');