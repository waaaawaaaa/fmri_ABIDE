%2023/11/27    zhumengying
function full_filename = find_filename(file_root,file_name_and_type)
%%找到头动校正的文件，用于TC的去噪  file_name='rp_arest'
%%找到SPM后做完平滑的文件，用于ICA的提取 file_name='swrarest.nii'

% file_root = 'F:/ABIDE_DATA1/raw_data'; 

    file_list = dir(file_root); 
    matchingFiles = {};
    
    for i = 3:length(file_list)  %first two files are blank
        file_name = fullfile(file_root,file_list(i).name);
        if ~exist(fullfile(file_name,'func',file_name_and_type), 'file')
            disp('未找到匹配的文件。');
            disp(file_name);
        else
            matchingFiles{i-2} = fullfile(file_name,'func',file_name_and_type);
        end
    end
    full_filename = matchingFiles';
end
