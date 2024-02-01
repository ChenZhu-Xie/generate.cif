clc;clear;
fid=fopen('CLT_810_SHG.cif','wt');
fprintf(fid,'DS 1 2 40;\n');
fprintf(fid,'9 Cell0;\n');

xx=0;yy=0;width=0;length=0;
fprintf(fid,'9 Cell0;\n');
xx=0;yy=0;width=0;length=0;
%1-1

% fprintf(fid,'L CPG;\n');
% T=3.08;  % 周期 3.08+0.02*i um
% xx=3000:T:23000;  % 区域 长 20 mm
% xx=-xx;  % -23 ~ - 3 mm 的 区域 左下角 x 坐标
% a=size(xx);
% yy=zeros(a)-2750+5500;  % 5.5*i - 2.75 mm 的 区域 左下角 y 坐标
% length=ones(a).*1000;  % 区域 宽 1 mm
% width=ones(a);  % 畴宽 1 um
% textf=[width;length;xx;yy];
% textf=textf.*2000;  % 1mm 对应 2000 个 cif 单位
% textf=floor(textf./2).*2;
% fprintf(fid,'B %ld %ld %ld %ld;\n',textf);

for i=1:1:5
fprintf(fid,'L CPG;\n');
T=3.08+0.02*i;  % 周期 3.08+0.02*i um
xx=3000:T:23000;  % 区域 长 20 mm
xx=-xx;  % -23 ~ - 3 mm 的 区域 左下角 x 坐标
a=size(xx);
yy=zeros(a)-2750+5500*i;  % 5.5*i - 2.75 mm 的 区域 左下角 y 坐标
length=ones(a).*1000;  % 区域 宽 1 mm
width=ones(a);  % 畴宽 1 um
textf=[width;length;xx;yy];
textf=textf.*2000;  % 1mm 对应 2000 个 cif 单位
textf=floor(textf./2).*2;
fprintf(fid,'B %ld %ld %ld %ld;\n',textf);

end

for i=1:1:5
fprintf(fid,'L CPG;\n');
T=3.08+0.02*i;
xx=3000:T:23000;
a=size(xx);
yy=zeros(a)-2750+5500*i;
length=ones(a).*1000;
width=ones(a);
textf=[width;length;xx;yy];
textf=textf.*2000;
textf=floor(textf./2).*2;
fprintf(fid,'B %ld %ld %ld %ld;\n',textf);

end

for i=1:1:5
fprintf(fid,'L CPG;\n');
T=3.12;
xx=10000:T:20000;
xx=[-xx,xx];
a=size(xx);
yy=zeros(a)+2750-5500*i;
length=ones(a).*200*i;
width=ones(a);
textf=[width;length;xx;yy];
textf=textf.*2000;
textf=floor(textf./2).*2;
fprintf(fid,'B %ld %ld %ld %ld;\n',textf);

end


fprintf(fid,'DF;\n');
fprintf(fid,'E\n');
fclose(fid);
