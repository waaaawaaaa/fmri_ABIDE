% 加载数据
load('F:\ABIDE_DATA\feature_extra\g_postprocess_results\tz_tc_norm.mat', 'tc');

% 获取要绘制的数据
subject_idx = 423;
data = squeeze(tc(subject_idx, :, 2:8))';

% 设置图像参数
figure('Position', [100 100 800 400]);
colormap(jet);
x = 1:size(data, 2);
y = 1:size(data, 1);

% 绘制图像
subplot(2, 1, 1);
h = imagesc(x, y, data);
set(gca, 'YDir', 'reverse');
ylabel('IC index');
xlabel('Time point');
title(sprintf('IC*time plot for subject %d', subject_idx));
colorbar;

% 绘制脑电图效果
subplot(2, 1, 2);
hold on;
for i = 1:size(data, 1)
    plot(x, data(i, :) + i, 'k', 'LineWidth', 1);
end
ylim([0, size(data, 1)+1]);
xlabel('Time point');
title(sprintf('EEG-like plot for subject %d', subject_idx));
