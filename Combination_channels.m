 
% folderPath1 = actualFile folder
folderPath1 = 'F:\CT images with 1 channel';
cd(folderPath1); % path of the folder
% WriteDir = WriteFile Folder
WriteDir = 'F:\CT images with 3 new channel';
files1 = dir('**');
files1(1:2) = [];
totalFiles = numel(files1);
for i =1:totalFiles
Fileaddress{i,1}=strcat(folderPath1,'\',files1(i).name);
file{i} = imread(Fileaddress{i,1});
% Edit the file
[row col]=size(file{i});
% Edit the file
inputs(:,:,1)= file{i}(:,:,1);
% BW1 = edge(I,'sobel');
% inputs(:,:,2)= BW1(:,:,1);
BW = ~imbinarize(file{i});
BW1 = edge(BW,'canny');
BW2 = bwareaopen(BW, round(row*col/100));
se1 = strel('line',5,0);
se2 = strel('line',5,90);
composition = imdilate(1,[se1 se2],'full');
dilatedI = imdilate(BW2,composition);
BW3=zeros(row,col);
BW3(dilatedI>0)=BW1(dilatedI>0);
inputs(:,:,2)= BW1(:,:,1);
inputs(:,:,3)= dilatedI(:,:,1);
file{i}=inputs;
cd(WriteDir) % go to dir where you want to save updated files
writeFileName =files1(i).name;
imwrite(file{i},writeFileName)
cd(folderPath1) % return to actualFile folder
end