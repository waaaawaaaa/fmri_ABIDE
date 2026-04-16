% zhumengying
% 2023-10-8
%把从官网上下载的数据整理一下，便于后面预处理
clc;clear;close all;

source_folder = 'F:/ABIDE_DATA/www.nitrc.org/ir/';
target_folder = 'F:/ABIDE_DATA/raw_data';

if ~exist(target_folder, 'dir')
    mkdir(target_folder);
end

file_list = dir(source_folder);
parfor i = 3:length(file_list)  %first two files are blank
    target_id_path = fullfile(target_folder,file_list(i).name);
    source_id_path = fullfile(source_folder,file_list(i).name);

    if ~exist(fullfile(target_id_path, 'func', 'rest.nii'), 'file')
    
        if ~exist(target_id_path, 'dir')
            mkdir(target_id_path);
        end
    
        %结构像
        if ~exist(fullfile(target_id_path, 'anat', 'mprage.nii'), 'file')
            if ~exist(fullfile(source_id_path, 'anat'), 'dir')
                source_anat_path = fullfile(source_id_path, 'hires/NIfTI/hires.nii.gz');
                target_anat_path = fullfile(target_id_path, 'anat');
                gunzip(source_anat_path, target_anat_path);
                movefile(fullfile(target_anat_path,'hires.nii'),fullfile(target_anat_path,'mprage.nii'))
            else
                source_anat_path = fullfile(source_id_path, 'anat/NIfTI/mprage.nii.gz');
                target_anat_path = fullfile(target_id_path, 'anat');
                gunzip(source_anat_path, target_anat_path);
            end
        end
        % target_anat_path = fullfile(target_id_path, 'anat');
        % gunzip(source_anat_path, target_anat_path);
        
        %功能像
        rest_list = dir(fullfile(source_id_path, '*rest*'));
        rest_name =  rest_list.name;
        source_func_path = fullfile(source_id_path, rest_name, 'NIfTI/rest.nii.gz');
        % if length(rest_list)>1
        %     source_func_path = fullfile(source_id_path, rest_1, 'NIfTI/rest.nii.gz');
        % else
        %     source_func_path = fullfile(source_id_path, 'rest/NIfTI/rest.nii.gz');
        % end
        target_func_path = fullfile(target_id_path, 'func');
        gunzip(source_func_path, target_func_path);
        
        disp(['finshed:' file_list(i).name]);
    end

end