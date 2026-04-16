%2023/11/22    zhumengying
function smooth_filename = find_smooth_filename(file_root)
%%找到SPM后做完平滑的文件，用于ICA的提取

% file_root = 'F:/ABIDE_DATA1/raw_data'; 

    file_list = dir(file_root); 
    matchingFiles = {};
    
    for i = 3:length(file_list)  %first two files are blank
        file_name = fullfile(file_root,file_list(i).name);
        if ~exist(fullfile(file_name,'func/swrarest.nii'), 'file')
            disp('未找到匹配的文件。');
            disp(file_name);
        else
            matchingFiles{i-2} = fullfile(file_name,'func/swrarest.nii');
        end
    end
    smooth_filename = matchingFiles';
end
