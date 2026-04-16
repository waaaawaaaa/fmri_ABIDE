% parameters_file='E:\ABIDE_DATA1\acquisition_information.xlsx';
% nii_file = 'E:\abide\raw_data\NYU_50967\func\rest.nii';

function [TR,slice_order,n_slices] = read_parameters(nii_file)
% 计算得到.nii影像的层数，TR,扫描顺序
%%对数据集的介绍以及采集参数   重点关注fMRI的采集参数
% TR；  TA=TR-TR/n_slices；slice_order=[1:2:n_slice,2:2:n_slice];
% CALTECH     N=38   
%         SMRI：TR=1590ms,TE=2.73ms,Voxel size:1.0×1.0×1.0mm,分辨率：176*256*256
%         fMRI：TR=2000ms，TE=30ms，扫描顺序：Interleaved，Voxel size: 3.5×3.5×3.5mm ,n_slices=34;矩阵大小：64*64*34*150
% CMU     N=27   
%         SMRI：TR=1870ms,TE=2.48ms,Voxel size:1.0×1.0×1.0mm,分辨率：169*215*200
%         fMRI：TR=2000ms，TE=30ms，扫描顺序：Interleaved，Voxel size: 3.5×3.5×3.5mm ,n_slices=28;矩阵大小：64*64*34*150
% KKI        
%         fMRI：TR=2500ms，TE=30ms，扫描顺序：ascend，n_slices=47, 矩阵大小：96*96*47*156
% MAXMUN       
%         fMRI：TR=3000ms，扫描顺序：Interleaved，n_slices=28
% NYU       
%         fMRI：TR=2000ms，扫描顺序：Interleaved，n_slices=33
% OLIN       
%         fMRI：TR=1500ms，扫描顺序：Interleaved，n_slices=29
% OHSU       
%         fMRI：TR=2500ms，扫描顺序：Interleaved，n_slices=36
% SDSU       
%         fMRI：TR=2000ms，扫描顺序：Interleaved，n_slices=42
% SBL       
%         fMRI：TR=2200ms，扫描顺序：descend，n_slices=38
% Stanford       
%         fMRI：TR=2000ms，扫描顺序：unknow(记作Interleaved)，n_slices=29
% Trinity       
%         fMRI：TR=2000ms，扫描顺序：ascend，n_slices=38
% UCLA       
%         fMRI：TR=3000ms，扫描顺序：Interleaved，n_slices=34
% Leven      
%         fMRI：TR=shortest(记作2000ms)，扫描顺序：ascend，n_slices=32
% Pitt       
%         fMRI：TR=1500ms，扫描顺序：Interleaved，n_slices=29
% USM      
%         fMRI：TR=2000ms，扫描顺序：Interleaved，n_slices=40
% yale       
%         fMRI：TR=2000ms，扫描顺序：Interleaved，n_slices=34
% UM       
%         fMRI：TR=2000ms，扫描顺序：unknow，n_slices=40

    sites={'Caltech','CMU','KKI','MaxMun','NYU','Olin','OHSU','SDSU','SBL','Stanford','Trinity','UCLA','Leuven','Pitt','USM','Yale','UM'};
    TR_all = {2,2,2.5,3,2,1.5,2.5,2,2.2,2,2,3,2,1.5,2,2,2};
    slice_order_all = {'Interleaved','Interleaved','ASCEND','Interleaved','Interleaved','Interleaved','Interleaved','Interleaved','DESCEND','unknow','ASCEND','Interleaved','ASCEND','Interleaved','Interleaved','Interleaved','unknow'};
    n_slice_all = [34,28,47,28,33,29,36,42,38,29,38,34,32,29,40,34,40];
    %%
    % TR；  TA=TR-TR/n_slice；slice_order=[1:2:n_slice,2:2:n_slice];
    % file_name = 'E:\abide\raw_data\NYU_50967\func\rest.nii';
    % nii_info = niftiinfo(file_name);
    % n_slice = nii_info.ImageSize(3);
    %% 没跑通
    % sites = xlsread(parameters_file,'sheet1','A');
    % TR_all = xlsread(parameters_file,'sheet1','B');
    % slice_order_all = xlsread(parameters_file,'sheet1','C');
    % n_slices_all = xlsread(parameters_file,'sheet1','D');
    %%
    parts = strsplit(nii_file, '\');
    site = strsplit(parts{4}, '_');
    site_index= find(strcmp(sites,site{1}));
    TR = TR_all{site_index};
    slice_order_name = slice_order_all{site_index};
    n_slices = n_slice_all(site_index);
        %存在极个别参数与官网上不一致的情况，按实际参数操作
    file_func=fullfile(nii_file,'func/rest.nii');
    info = niftiinfo(file_func);
    n_slices_real = info.ImageSize(3);
    if n_slices_real ~= n_slices
        n_slices=n_slices_real;
        disp(['slice不匹配:' file_func]);
    end
    if isequal(slice_order_name,'ASCEND')
        slice_order=[1:1:n_slices];
    elseif isequal(slice_order_name,'DESCEND')
        slice_order=[n_slices:-1:1];
    else
        slice_order=[1:2:n_slices,2:2:n_slices];
    end
    