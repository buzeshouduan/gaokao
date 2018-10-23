import pandas as pd
wy_list=pd.read_excel("wy_list.xlsx")
bf=pd.read_excel("20181023bf.xlsx")
print(wy_list.head(),bf.head())

bf_no=[]
for i in range(len(bf['主要变更对象'])):
    if ',' in bf['主要变更对象'][i]:
        a=bf['主要变更对象'][i].split(",")
        for j in wy_list['list'].tolist():
            if j in a:
                bf_no.append(bf['变更编号'][i])


b=pd.DataFrame(bf_no)
b.to_excel("result.xlsx")

