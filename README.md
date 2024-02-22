# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama

## İş Problemi:

Gezinomi yaptığı satışların bazı özelliklerini kullanarak seviye tabanlı (level based) yeni satış tanımları oluşturmak ve bu yeni satış tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir. 

Örneğin: Antalya’dan Herşey Dahil bir otele yoğun bir dönemde gitmek isteyen bir müşterinin ortalama ne kadar kazandırabileceği belirlenmek isteniyor. Bu Case'de bu ve bunun gibi pek çok sonucu elde edeceğiz ve birlikte yorumlayacağız.

## Veri Seti Hikayesi

gezinomi_miuul.xlsx veri seti Gezinomi şirketinin yaptığı satışların fiyatlarını ve bu satışlara ait bilgiler içermektedir. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo tekilleştirilmemiştir. Diğer bir ifade ile müşteri birden fazla alışveriş yapmış olabilir.

## Değişkenler

- SaleId: Satış id 
- SaleDate:Satış Tarihi 
- CheckInDate: Müşterinin otele giriş itarihi 
- Price:Satış için ödenen fiyat 
- ConceptName: Otel konsept bilgisi
- SaleCityName: Otelin bulunduğu şehir bilgisi 
- CInDay:Müşterinin otele giriş günü 
- SaleCheckInDayDiff: Check in ile giriş tarihi gün farkı
- Season:Otele giriş tarihindeki sezon bilgisi

## Proje Görevleri

#Görev_1 Aşağıdaki Soruları Yanıtlayınız:

#Soru_1 miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

İlk önce kütüphanelerimizi yükleyelim.
```python:
import pandas as pd  
import seaborn as sns  
import numpy as np
```
``
Ayrıca excel dosyası okutacağımız için openpyxl kütüphanesini de yüklememiz gerekiyor. Eğer Sizde yüklü değilse veya yüklü olup olmadığını bilmiyorsanız;
```python:
pip install openpyxl --upgrade
```

Bu kodu terminale yazarak kütüphaneyi yükleyebilir veya güncelleştirebilirsiniz.

Bu kod ile miuul_gezinomi.xlsx dosyasını gezinomi.py dosyamıza ekliyoruz. Onunla daha çok işimiz var:
```python:
df = pd.read_excel("miuul_gezinomi.xlsx")  
```

Çıktımızı düzgün bir şekilde almak için satır ve sütunlarımızı ayarlayalım.

```python:
# Maksimum satır ve sütun sayısını ayarlamak için gerekli kodlar;  
pd.set_option('display.max_rows', 100)  
pd.set_option('display.max_columns', 20)  
# Görüntüleme genişliğini ayarlamamız için gerekli kodlar;  
pd.set_option('display.width', 1000)
```

İlk çıktımızı almak için df.info()'yu kullanalım.

```python:
df.info()
```

#Soru_2 Kaç unique şehir vardır? Frekansları nedir?

Benzersiz şehirlerin sayısını bulmak için "==Salecityname==" değişkenini incelememiz gerekiyor. 

```python:
df["SaleCityName"].nunique()  
df["SaleCityName"].value_counts()
```

Bu çıktı sayesinde projemizde Antalya , Muğla , Aydın , İzmir , Girne ve Diğer kategorisine ayrılmış 6 adet seyahat rotası olduğunu öğrendik. Bu rotaların frekanslarını da görmekteyiz.

#Soru_3 Kaç unique Concept vardır?

Bunun için aşağıdaki kodu kullanalım:

```python:
df["ConceptName"].nunique()
```

Cevap olarak "3" çıktısını alıyoruz.

#Soru_4 Hangi Concept’den kaçar tane satış gerçekleşmiş?

Bu veriyi incelemek için "value_counts()" metodunu kullanırız.

```python:
df["ConceptName"].value_counts()
```

#Soru_5 Şehirlere göre satışlardan toplam ne kadar kazanılmış? 

Bunun için "sum()" metodunu kullanmamız gerekir.

```python:
totalsales= df.groupby("SaleCityName")["Price"].sum()  
print(totalsales)
```

#Soru_6 Concept türlerine göre göre ne kadar kazanılmış?

Bir toplama işlemi yapılacağı için yine "sum()" metodunu kullanıyoruz.

```python:
conceptsales= df.groupby("ConceptName")["Price"].sum()  
print(conceptsales)
```

#Soru_7 Şehirlere göre PRICE ortalamaları nedir? 

Şehirlere göre tatil fiyatı ortalamalarını öğrenmek için "agg()" metodunu kullanalım. 
```python:
print(df.groupby("SaleCityName")["Price"].agg("mean")) #tek bir fonksiyon olduğu için köşeli parantez kullanmadık.
```

#Soru_8 Conceptlere göre PRICE ortalamaları nedir? 

Önceki sorudaki "SaleCityName" i "ConceptName" olarak değiştirdiğimizde direkt olarak sorunun cevabını elde ederiz.
```python:
df.groupby("ConceptName")["Price"].agg("mean") 
```

#Soru_9 Şehir-Concept kırılımında PRICE ortalamaları nedir?

Bunun için Şehir ve Concept'i köşeli parantez içine almamız gerekecek.

```python:
df.groupby(["SaleCityName" ,"ConceptName"])["Price"].agg("mean") 
```

#Görev_2 

SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz. 

- SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir. 
- Aralıkları ikna edici şekilde oluşturunuz. Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullanabilirsiniz. 
- Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz.

Çözüm: "SaleCheckInDayDiff" değişkenini kategorik değişkene alma ve aralıklarını belirlemek için aşağıdaki kodu uygulayabiliriz.

```python:
df['EB_Score'] = pd.cut(df['SaleCheckInDayDiff'], bins=[-1, 7, 30, 90, float("inf")], labels=['Last Minuters', 'Potential Planners', 'Planners', 'Early Bookers'])           # float("inf")= Sonsuz float değeri temsil eder.
print(df.head(50))
```

float("inf") yerine şunu da kullanabilirdik. Kodumuz bu şekilde "SaleCheckInDayDiff" değişkenindeki maksimum değeri kontrol eder. Aşağıdaki kullanım kodun okunabilirliği açısından daha iyi bir kullanımdır.
```python:
df["SaleCheckInDayDiff"].max()
```

#Görev_3

- SaleCityName - ConceptName - EB_Score kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz.

```python:
df.groupby(by=["SaleCityName", 'ConceptName', "EB_Score" ]).agg({"Price": ["mean", "count"]})
```

- SaleCityName - ConceptName - Seasons kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz.
```python:
df.groupby(by=["SaleCityName", 'ConceptName', "Seasons" ]).agg({"Price": ["mean", "count"]})
```

- SaleCityName - ConceptName - CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz.

```python:
df.groupby(by=["SaleCityName", 'ConceptName', "CInDay" ]).agg({"Price": ["mean", "count"]})
```

#Görev_4 

SaleCityName - ConceptName - Seasons kırılımının çıktısını PRICE'a göre sıralayınız. Elde ettiğiniz çıktıyı agg_df olarak kaydediniz.

Burada "sort_values()" metodunu kullanmamız gerekiyor.

```python:
agg_df = df.groupby(by=["SaleCityName" , "ConceptName" , "Seasons"]).agg({"Price":"mean"}).sort_values("Price", ascending=False)  
print(agg_df.head())
```

#Görev_5

Indekste yer alan isimleri değişken ismine çeviriniz.

• Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz. 
==İpucu= reset_index()==

```python:
agg_df.reset_index(inplace=True) # Indeksin adlarını değişken isimlerine çevirir.
agg_df.head()
```

#Görev_6 

Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
- Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz. 
- Yeni eklenecek değişkenin adı: sales_level_based 
- Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.

```python:
agg_df["sales_level_based"] = agg_df[["SaleCityName" , "ConceptName" , "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)  
print(agg_df.head())
```

Burada "upper()" metodu ile bütün harfleri büyütme işlemini uyguladık. Ayrıca lambda ile kullan-at bir değişken oluşturduk. Bu değişkenimizin amacı sadece kelimeler arasına _ koymak. axis=1 ifadesi "Bu değişikliği sütunlarda yap." anlamına gelmektedir. Eğer axis=0 olsaydı, bu değişikliği satırlarda uygulayacaktı ve kodumuz hata verecekti.

#Görev_7

Yeni müşterileri (personaları) segmentlere ayırınız. 

 - Yeni personaları PRICE’a göre 4 segmente ayırınız.
 - Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz. 
 - Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

```python:
agg_df["SEGMENT"] = pd.qcut(agg_df[["Price"]] , 4 , labels=["D","C","B","A"])  
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})  
print(agg_df.head())
```

Koddaki `4`, `pd.qcut()` fonksiyonunun bölme işlemi için kaç segmente ayıracağını belirtir. **`pd.qcut()` fonksiyonu, verilen sütunu belirtilen sayıda eşit genişlikte segmentlere böler.**

Örneğin, `pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])` ifadesindeki `4`, `Price` sütununu dört eşit genişlikte segmente böleceğini belirtir. Yani, bu ifade dört farklı kategori oluşturur.

#Görev_8 

Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.

-  Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?

Burada ilk önce Antalya'da Herşey Dahil tatilini Yaz aylarında(Yüksek Sezon) yapan müşterileri bir değişken içine almamız gerekir. Hep birlikte aşağıdaki kodu inceleyelim.
```python:
antalya_high_season_all_inclusive = agg_df[(agg_df["SaleCityName"] == "Antalya") & (agg_df["ConceptName"] == "Herşey Dahil") & (agg_df["Seasons"] == "High")]  
average_income_antalya_high_season = antalya_high_season_all_inclusive["Price"].mean()  
print("Antalya'da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama getirisi: ", average_income_antalya_high_season)  
```
"antalya_high_season_all_inclusive" isimli değişkene yukarıda bahsettiğim ayrıştırıcı özelliklerimizi girdik  daha sonra "average_income_antalya_high_season" isimli değişkende de bu değişkenimizdeki bütün müşterilerin "Price" ortalamalarını aldık.

- Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?

Bunun için oluşturduğumuz "SEGMENT" 'ten yararlanacağız.

```python:
girne_low_season_half_board = agg_df[(agg_df["SaleCityName"] == "Girne") & (agg_df["ConceptName"] == "Yarım Pansiyon") & (agg_df["Seasons"] == "Low")]  
segment_of_girne_low_season_half_board = girne_low_season_half_board["SEGMENT"].iloc[0] # İlk örnekten segmenti alıyoruz  
print("Girne'de yarım pansiyon bir otele düşük sezonda giden bir tatilcinin segmenti: ", segment_of_girne_low_season_half_board)  
```

Bu örnekte "Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama" konusunu inceledik ve elimizdeki veri setini inceleyip ondan anlamlı veriler çıkardık. Bu veriler sayesinde yeni müşterilerin tatil için ortalama ne kadar para harcayacağını tahmin ettik. Örneğin, "Antalya'da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir müşterinin ortalama getirisi  64.92 olarak tahmin edildi. Ayrıca, müşterilerin rezervasyonlarını ne kadar önceden yaptıklarını da kategorize ettik ve bu kategorilere göre segmentler oluşturduk.

Şu anda yaptığımız analizler sadece ortalama fiyatları içeriyor, ancak gelecekte müşteri segmentlerinin davranışlarını daha ayrıntılı olarak inceleyebilir ve tahmin modelleri oluşturabiliriz.

Bu analizler, firmaların pazarlama stratejilerini optimize etmesine ve farklı müşteri segmentlerine daha iyi hizmet etmesine yardımcı olabilir.

**Veri Bilimi yolculuğumda bizlere bu case'i sunan Miuul ekibine teşekkürü bir borç bilirim.**

