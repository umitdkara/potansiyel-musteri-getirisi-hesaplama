import pandas as pd
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Soru 1 : miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_excel("miuul_gezinomi.xlsx")
# Maksimum satır ve sütun sayısını ayarlamak için gerekli kodlar;
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)
# Görüntüleme genişliğini ayarlamamız için gerekli kodlar;
pd.set_option('display.width', 1000)
# df.info ile dosyamıza bir göz atalım.
df.info()
df.describe()

# Soru 2:Kaçunique şehir vardır? Frekansları nedir?
df["SaleCityName"].value_counts()

# Soru 3:Kaç unique Concept vardır?

df["ConceptName"].nunique()

# Soru 4:Hangi Concept’ den kaçar tane satış gerçekleşmiş?

df["ConceptName"].value_counts()

# Soru 5:Şehirlere göre satışlardan toplam ne kadar kazanılmış?

toplamsatis= df.groupby("SaleCityName")["Price"].sum()
print(toplamsatis)

# Soru 6:Concept türlerine göre göre ne kadar kazanılmış?

conceptsales= df.groupby("ConceptName")["Price"].sum()
print(conceptsales)

# Soru 7:Şehirlere göre PRICE ortalamaları nedir?

print(df.groupby("SaleCityName")["Price"].agg("mean"))

# Soru 8:Conceptlere göre PRICE ortalamaları nedir?

print(df.groupby("ConceptName")["Price"].agg("mean")) #tek bir fonksiyon olduğu için köşeli parantez kullanmadık.

# Soru9:Şehir-Concept kırılımında PRICE ortalamaları nedir?

df.groupby(["SaleCityName" ,"ConceptName"])["Price"].agg("mean")


#SaleCheckInDayDiffdeğişkenini kategorik bir değişkene çeviriniz.

#SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
# Aralıkları ikna edici şekilde oluşturunuz. Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullanabilirsiniz.
# Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz.


#float("inf")= Sonsuz float değeri temsil eder.
df['EB_Score'] = pd.cut(df['SaleCheckInDayDiff'], bins=[-1, 7, 30, 90, float('inf')], labels=['Last Minuters', 'Potential Planners', 'Planners', 'Early Bookers'])
print(df.head(20))


#Görev_3

#- Şehir- Concept- EB Score, Şehir- Concept- Sezon, Şehir- Concept- CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz


print(df.groupby(by=["SaleCityName", 'ConceptName', "EB_Score"] ).agg({"Price": ["mean", "count"]}))
# SaleCityName - ConceptName - Seasons kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz.


print(df.groupby(by=["SaleCityName", 'ConceptName', "Seasons" ]).agg({"Price": ["mean", "count"]}))

# - SaleCityName - ConceptName - CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz.

df.groupby(by=["SaleCityName", 'ConceptName', "CInDay" ]).agg({"Price": ["mean", "count"]})

#Görev_4

# SaleCityName - ConceptName - Seasons kırılımının çıktısını PRICE'a göre sıralayınız. Elde ettiğiniz çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(by=["SaleCityName" , "ConceptName" , "Seasons"]).agg({"Price":"mean"}).sort_values("Price", ascending=False)
print(agg_df.head())

#Görev_5

# Indekste yer alan isimleri değişken ismine çeviriniz.

# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.

agg_df.reset_index(inplace=True) # Indeksin adlarını değişken isimlerine çevirir.
print(agg_df.head())


#Görev_6

#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
# Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
# Yeni eklenecek değişkenin adı: sales_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.

agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)
print(agg_df.head())

#Görev_7

# Yeni müşterileri (personaları) segmentlere ayırınız.

 # Yeni personaları PRICE’a göre 4 segmente ayırınız.
 # Segmentleri SEGMENTisimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
 # Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).


agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("SEGMENT", observed=False).agg({"Price": ["mean", "max", "sum"]})
print(agg_df.head())


#Görev_8

# GÖREV 8: Oluşan son df'i price değişkenine göre sıralayınız.
# "ANTALYA_HERŞEY DAHIL_HIGH" hangi segmenttedir ve ne kadar ücret beklenmektedir?
#############################################
agg_df.sort_values(by="Price")
print(agg_df[agg_df["sales_level_based"] =="ANTALYA_HERŞEY DAHIL_HIGH"])

# Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
antalya_high_season_all_inclusive = agg_df[(agg_df["SaleCityName"] == "Antalya") & (agg_df["ConceptName"] == "Herşey Dahil") & (agg_df["Seasons"] == "High")]
average_income_antalya_high_season = antalya_high_season_all_inclusive["Price"].mean()
print("Antalya'da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama getirisi: ", average_income_antalya_high_season)

# Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?
girne_low_season_half_board = agg_df[(agg_df["SaleCityName"] == "Girne") & (agg_df["ConceptName"] == "Yarım Pansiyon") & (agg_df["Seasons"] == "Low")]
segment_of_girne_low_season_half_board = girne_low_season_half_board["SEGMENT"].iloc[0] # İlk örnekten segmenti alıyoruz
print("Girne'de yarım pansiyon bir otele düşük sezonda giden bir tatilcinin segmenti: ", segment_of_girne_low_season_half_board)
