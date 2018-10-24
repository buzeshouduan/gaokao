import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']#图中中文乱码
#1、添加SimHei字体（simhei.ttf文件）到/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
#2、删除~/.matplotlib/下的所有缓存文件rm -rf ~/.matplotlib/*.cache，并重命名fontList.json
#3、在你要画图的的python文件中，添加plt.rcParams['font.sans-serif'] = ['SimHei']  # for Chinese characters

ori_data=pd.read_excel("data/高考志愿.xlsx")
city_list=pd.read_excel("data/中国城市等级.xlsx")
ori_data=ori_data[ori_data['2015年平均线']!='无']

#将字符型转换成数值型
kind_data=pd.get_dummies(ori_data['类型'],prefix='类型')
yn985_data=pd.get_dummies(ori_data['是否为985'],prefix='yesno985')
yn211_data=pd.get_dummies(ori_data['是否为211'],prefix='yesno211')
yn_zizhu_data=pd.get_dummies(ori_data['是否自主招生'],prefix='yesno_zizhu')

#所在地变量太多，分为6类
first_tier=city_list['一线城市'][city_list['一线城市'].notnull()].tolist()
for i in range(len(first_tier)):
    if '市' in first_tier[i]:
        first_tier[i]=first_tier[i].split("市")[0]
print(first_tier)

new_first_tier=city_list['新一线城市'][city_list['新一线城市'].notnull()].tolist()
for i in range(len(new_first_tier)):
    if '市' in new_first_tier[i]:
        new_first_tier[i]=new_first_tier[i].split("市")[0]
print(new_first_tier)

second_tier=city_list['二线城市'][city_list['二线城市'].notnull()].tolist()
for i in range(len(second_tier)):
    if '市' in second_tier[i]:
        second_tier[i]=second_tier[i].split("市")[0]

third_tier=city_list['三线城市'][city_list['三线城市'].notnull()].tolist()
for i in range(len(third_tier)):
    if '市' in third_tier[i]:
        third_tier[i]=third_tier[i].split("市")[0]

fourth_tier=city_list['四线城市'][city_list['四线城市'].notnull()].tolist()
for i in range(len(fourth_tier)):
    if '市' in fourth_tier[i]:
        fourth_tier[i]=fourth_tier[i].split("市")[0]

fifth_tier=city_list['五线城市'][city_list['五线城市'].notnull()].tolist()
for i in range(len(fifth_tier)):
    if '市' in fifth_tier[i]:
        fifth_tier[i]=fifth_tier[i].split("市")[0]

local_list=ori_data['所在地'].tolist()
for i in range(len(local_list)):
    if '市' in local_list[i]:
        local_list[i]=local_list[i].split("市")[0]

city_class_list=[]
for i in range(len(local_list)):
    if local_list[i] in first_tier:
        city_class_list.append("A")
    elif local_list[i] in new_first_tier:
        city_class_list.append("B")
    elif local_list[i] in second_tier:
        city_class_list.append("C")
    elif local_list[i] in third_tier:
        city_class_list.append("D")
    elif local_list[i] in fourth_tier:
        city_class_list.append("E")
    elif local_list[i] in fifth_tier:
        city_class_list.append("F")
    else:
        city_class_list.append("Z")

belong_list=[]
for i in range(len(ori_data['隶属'].tolist())):
    if ori_data['隶属'].tolist()[i]=='教育部':
        belong_list.append("是")
    else:
        belong_list.append("否")

belong=pd.get_dummies(pd.Series(belong_list),prefix="yesno教育部")
city_class=pd.get_dummies(pd.Series(city_class_list),prefix="城市")
new_data=pd.concat([ori_data,city_class,belong,kind_data,yn985_data,yn211_data,yn_zizhu_data],axis=1)
new_data=new_data.drop(['所在地','隶属','类型','地址','是否为985','是否为211','是否自主招生'],axis=1)

new_data['2015年平均线']=new_data['2015年平均线'].astype(float)

print(new_data.info())
fig,axarr=plt.subplots(2,2,figsize=(12,8))
new_data['院士（位）'].value_counts().plot.bar(ax=axarr[0][0])
axarr[0][0].set_title("院士数量")
new_data['重点学科(个)'].value_counts().plot.bar(ax=axarr[0][1])
axarr[0][1].set_title("重点学科数量")
new_data['博士点（个）'].value_counts().plot.bar(ax=axarr[1][0])
axarr[1][0].set_title("博士数量")
new_data['2015年平均线'].value_counts().plot.bar(ax=axarr[1][1])
#new_data['硕士点（个）'].value_counts().plot.bar(ax=axarr[1][1])
axarr[1][1].set_title("硕士数量")
#plt.show()

#print(new_data['2015年平均线'].describe())#[397,694]
#print(new_data['院士（位）'].describe())#[0,70]
#print(new_data['重点学科(个)'].describe())#[0,81]
#print(new_data['博士点（个）'].describe())#[0,283]
#print(new_data['硕士点（个）'].describe())#[0,345]


plt.show()




