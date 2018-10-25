import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']#图中中文乱码
#1、添加SimHei字体（simhei.ttf文件）到/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
#2、删除~/.matplotlib/下的所有缓存文件rm -rf ~/.matplotlib/*.cache，并重命名fontList.json
#3、在你要画图的的python文件中，添加plt.rcParams['font.sans-serif'] = ['SimHei']  # for Chinese characters

ori_data=pd.read_excel("data/高考志愿.xlsx")
city_list=pd.read_excel("data/中国城市等级.xlsx")
ori_data=ori_data[ori_data['2015年平均线']!='无'].reset_index()#要重置索引，不然concat时对不上


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
        city_class_list.append("一线城市")
    elif local_list[i] in new_first_tier:
        city_class_list.append("新一线城市")
    elif local_list[i] in second_tier:
        city_class_list.append("二线城市")
    elif local_list[i] in third_tier:
        city_class_list.append("三线城市")
    elif local_list[i] in fourth_tier:
        city_class_list.append("四线城市")
    elif local_list[i] in fifth_tier:
        city_class_list.append("五线城市")
    else:
        city_class_list.append("其他")

belong_list=[]
for i in range(len(ori_data['隶属'].tolist())):
    if ori_data['隶属'].tolist()[i]=='教育部':
        belong_list.append("是")
    else:
        belong_list.append("否")

belong=pd.get_dummies(pd.Series(belong_list),prefix="yesno教育部")
city_class=pd.get_dummies(pd.Series(city_class_list),prefix="城市")

new_data=pd.concat([ori_data,city_class,belong,kind_data,yn985_data,yn211_data,yn_zizhu_data],axis=1)
new_data=new_data.drop(['大学名称','所在地','隶属','类型','地址','是否为985','是否为211','是否自主招生'],axis=1)


new_data['2015年平均线']=new_data['2015年平均线'].astype(float)#转换object to float
#new_data['city_class_tmp']=pd.Series(city_class_list)
#new_data['belong_list_tmp']=pd.Series(belong_list)
#new_data['tmp985']=pd.Series(ori_data['是否为985'])
#new_data['tmp211']=pd.Series(ori_data['是否为211'])
#new_data['kind_tmp']=pd.Series(ori_data['类型'])
#new_data['zizhu_tmp']=pd.Series(ori_data['是否自主招生'])#

#print(new_data['2015年平均线'].describe())#[397,694]
#print(new_data['院士（位）'].describe())#[0,70]
#print(new_data['重点学科(个)'].describe())#[0,81]
#print(new_data['博士点（个）'].describe())#[0,283]
#print(new_data['硕士点（个）'].describe())#[0,345]

#import seaborn as sns
#fig=plt.subplots(figsize=(20,12))
#
#ax1=plt.subplot2grid((3,3),(0,0),colspan=1)
#new_data['aver_score']=np.ceil(new_data['2015年平均线']/10)*10
#plt.hist(new_data['aver_score'],bins=30)
#ax1.set_title("2015年平均线分布")
#
#ax2=plt.subplot2grid((3,3),(0,1),colspan=2)
#f1=new_data.loc[:,['2015年平均线','city_class_tmp']]
#sns.boxplot(x='city_class_tmp',y='2015年平均线',data=f1,ax=ax2)
#ax2.set_title("城市等级和2015年平均线关系")
#ax2.set_xlabel("城市等级")
#
#ax3=plt.subplot2grid((3,3),(1,0),colspan=1)
#f2=new_data.loc[:,['2015年平均线','belong_list_tmp']]
#sns.boxplot(x='belong_list_tmp',y='2015年平均线',data=f2,ax=ax3)
#ax3.set_title("2015年平均线与是否教育部直属的关系")
#ax3.set_xlabel("是否教育部直属")
#
#ax4=plt.subplot2grid((3,3),(1,1),colspan=1)
#f3=new_data.loc[:,['2015年平均线','tmp985']]
#sns.boxplot(x='tmp985',y='2015年平均线',data=f3,ax=ax4)
#ax4.set_title("2015年平均线与是否是985的关系")
#ax4.set_xlabel("是否985")
#
#ax5=plt.subplot2grid((3,3),(1,2),colspan=1)
#f4=new_data.loc[:,['2015年平均线','tmp211']]
#sns.boxplot(x='tmp211',y='2015年平均线',data=f4,ax=ax5)
#ax5.set_title("2015年平均线与是否是211的关系")
#ax5.set_xlabel("是否211")
#
#ax6=plt.subplot2grid((3,3),(2,0),colspan=2)
#f5=new_data.loc[:,['2015年平均线','kind_tmp']]
#sns.boxplot(x='kind_tmp',y='2015年平均线',data=f5,ax=ax6)
#ax6.set_title("2015年平均线与学校类型的关系")
#ax6.set_xlabel("学校类型")
#
#ax7=plt.subplot2grid((3,3),(2,2),colspan=1)
#f6=new_data.loc[:,['2015年平均线','zizhu_tmp']]
#sns.boxplot(x='zizhu_tmp',y='2015年平均线',data=f6,ax=ax7)
#ax7.set_title("2015年平均线与自主招生的关系")
#ax7.set_xlabel("是否自主招生")
#
#sns.lmplot(x='院士（位）',y='2015年平均线',data=new_data)
#sns.lmplot(x='硕士点（个）',y='2015年平均线',data=new_data)
#sns.lmplot(x='重点学科(个)',y='2015年平均线',data=new_data)
#sns.lmplot(x='博士点（个）',y='2015年平均线',data=new_data)
#
#plt.show()
from sklearn.preprocessing import Imputer
new_data=new_data.astype(float)
imputer=Imputer(strategy="median")
imputer.fit(new_data)
X=imputer.transform(new_data)
new_data_im=pd.DataFrame(X,columns=new_data.columns)


from  sklearn.model_selection import train_test_split
train_set,test_set=train_test_split(new_data_im,test_size=0.3,random_state=22)
print(train_set[0:10],test_set[:10])
train_set_x=train_set.drop(['2015年平均线'],axis=1)
train_set_y=train_set['2015年平均线'].copy()

corr_matrix=new_data_im.corr()
print(corr_matrix['2015年平均线'].sort_values(ascending=False).head(10))


from sklearn.linear_model import LinearRegression
lin_reg=LinearRegression()
lin_reg.fit(train_set_x,train_set_y)

some_x=train_set_x.iloc[:5]
some_y=train_set_y.iloc[:5]
print(lin_reg.predict(some_x))
print(list(some_y))
