% 2023/12/03 zhumengying
% 整理gift跑出来的结果，fnc和tc

% 设置文件夹路径
folder_path = 'F:\ABIDE_DATA\feature_extra\g_postprocess_results';

% 获取文件夹中的.mat文件列表
file_list = dir(fullfile(folder_path, '^g_*.mat'));
num_subjects = length(file_list);

% 初始化存储上三角元素的矩阵
fnc = zeros(num_subjects, 1225);
% 初始化存储timecourses的矩阵
tc_1 = zeros(num_subjects, 300, 50); % 假设最大的timepoint是300

% 逐个读取.mat文件
for i = 1:num_subjects
    file_name = fullfile(folder_path, file_list(i).name);
    fnc_corrs = load(file_name, 'fnc_corrs');
    timecourses = load(file_name, 'timecourses');
    
    % 获取上三角元素
    fnc(i, :) = fnc_corrs.fnc_corrs(triu(true(50), 1));
    tc_1(i, 1:size(timecourses.timecourses, 1), :) = timecourses.timecourses;

end

% 保存整理后的数据到tz_sfc.mat文件
save('F:\ABIDE_DATA\feature_extra\g_postprocess_results\tz_sfc.mat', 'fnc');

% 截取合适的timepoints
tc = tc_1(:, 1:170, :);
% 保存整理后的数据到tz_tc_norm.mat文件
save('F:\ABIDE_DATA\feature_extra\g_postprocess_results\tz_tc_norm.mat', 'tc');