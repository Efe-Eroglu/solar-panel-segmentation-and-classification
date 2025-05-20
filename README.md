<div align="center">

# 🌞 Solar Panel Fault Detection & Segmentation ⚡️

</div>


<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8%2B-orange)
![React](https://img.shields.io/badge/React-18.0%2B-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688)

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />

</div>

<hr>

## 📋 İçerik
- [🚀 Proje Hakkında](#-proje-hakkında)
- [🏗 Sistem Mimarisi](#-sistem-mimarisi)
- [📊 Veri Seti](#-veri-seti)
- [🤖 Modeller](#-modeller)
  - [🧩 Segmentasyon Modeli (U-Net)](#-segmentasyon-modeli-u-net)
  - [🔍 Arıza Tespit Modeli (EfficientNet-B0)](#-arıza-tespit-modeli-efficientnet-b0)
- [📝 Kullanım](#-kullanım)
- [🔌 API Referansı](#-api-referansı)
- [👥 Katkıda Bulunma](#-katkıda-bulunma)
- [📜 Lisans](#-lisans)

<hr>

## 🚀 Proje Hakkında

<div align="center">
<img src="https://img.icons8.com/color/96/000000/solar-panel.png" width="120px"/>
</div>

Bu proje, derin öğrenme teknikleri kullanarak güneş panellerindeki arızaları tespit etmek ve segmentasyon yapmak için geliştirilmiş kapsamlı bir çözümdür. Sistem, görüntü işleme ve makine öğrenimi algoritmalarını kullanarak güneş panellerindeki çatlak, sıcak nokta ve diğer arızaları otomatik olarak tespit eder ve görselleştirir.

### 🔍 Temel Özellikler

| 🔎 | Güneş Paneli Segmentasyonu | U-Net mimarisi kullanarak güneş panellerini arka plandan ayırma |
|---|---------------------------|----------------------------------------------------------------|
| ⚠️ | Arıza Tespiti ve Sınıflandırması | EfficientNet-B0 mimarisi kullanarak panel arızalarını tespit etme |
| 🖥️ | Kullanıcı Dostu Arayüz | React ile geliştirilmiş modern web arayüzü |
| 🔄 | Gerçek Zamanlı İşleme | FastAPI ile hızlı ve verimli backend hizmetleri |
| 📊 | Görselleştirme Araçları | Tespit edilen arızaların ve segmentasyonların görsel raporları |

<hr>

## 🏗 Sistem Mimarisi

<div align="center">
<pre>
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  📷 Kullanıcı   │────▶│  ⚙️ Backend     │────▶│  🧠 Derin       │
│  Arayüzü        │     │  Servisleri     │     │  Öğrenme        │
│  (React)        │     │  (FastAPI)      │     │  Modelleri      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                       │                        │
        │                       │                        │
        └───────────────────────┴────────────────────────┘
</pre>
</div>

Proje, modern bir mikro servis mimarisine sahiptir ve üç ana bileşenden oluşur:

1. **🧠 Derin Öğrenme Modelleri**:
   - U-Net tabanlı segmentasyon modeli
   - EfficientNet-B0 tabanlı arıza sınıflandırma modeli

2. **⚙️ Backend Servisleri (FastAPI)**:
   - Model yükleme ve çalıştırma
   - REST API sunumu
   - Görüntü işleme ve ön işleme

3. **🖥️ Frontend Uygulaması (React)**:
   - Kullanıcı arayüzü
   - Görüntü yükleme ve sonuç görselleştirme
   - Gerçek zamanlı analiz

<hr>

## 📊 Veri Seti

Proje, COCO formatında işaretlenmiş güneş paneli görüntülerini içeren özel bir veri seti kullanmaktadır. Veri seti Roboflow platformu üzerinden alınmış ve COCO formatında işaretlenmiştir.

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| 🔢 **Toplam Görüntü** | 1000+ | Güneş paneli görüntüsü |
| 🏷️ **Sınıflar** | 6 | Normal, Çatlak, Sıcak Nokta, Gölgelenme, Fiziksel Hasar, Kar Kaplı |
| 📏 **Çözünürlük** | 224x224 | Eğitim sırasında standardize edilmiş |
| 📊 **Veri Dağılımı** | Train: 70%, Validation: 15%, Test: 15% | Modellerin eğitim ve değerlendirmesi için |

<div align="center">
<pre>
┌─────────────┐    ┌─────────────┐
│             │    │             │
│  Eğitim     │    │  Doğrulama  │
│  Seti       │    │  Seti       │
│  (70%)      │    │  (15%)      │
│             │    │             │
└─────────────┘    └─────────────┘
      ┌─────────────┐
      │             │
      │  Test       │
      │  Seti       │
      │  (15%)      │
      │             │
      └─────────────┘
</pre>
</div>

<hr>

## 🤖 Modeller

### 🧩 Segmentasyon Modeli (U-Net)


U-Net mimarisi, görseldeki her bir pikseli sınıflandırarak semantik segmentasyon gerçekleştiren encoder-decoder yapısında bir derin öğrenme modelidir. Bu projede güneş panellerini arka plandan ayırmak için ResNet50 tabanlı bir U-Net mimarisi kullanılmıştır.

#### Model Mimarisi

```
┌──────────────┐                                  ┌──────────────┐
│ Giriş        │                                  │ Çıkış        │
│ (224x224x3)  │                                  │ (224x224x1)  │
└──────┬───────┘                                  └──────┬───────┘
       │                                                 │
       ▼                                                 ▲
┌──────────────┐                                  ┌──────────────┐
│ ResNet50     │                                  │ Convolution  │
│ Encoder      │                                  │ (1x1, sigmoid)│
└──────┬───────┘                                  └──────┬───────┘
       │                                                 │
       ▼                                                 ▲
┌──────────────────────────────────────┐         ┌──────────────┐
│ Skip Connections                      │         │ Upsampling   │
│ 1. conv1_relu (128x128)              │──┐      │ Block 4      │
│ 2. conv2_block3_out (64x64)          │  │      │ (128x128)    │
│ 3. conv3_block4_out (32x32)          │  │      └──────┬───────┘
│ 4. conv4_block6_out (16x16)          │  │             │
│ 5. conv5_block3_out (8x8)            │  │             ▲
└──────────────────────────────────────┘  │      ┌──────────────┐
       │                                   │      │ Upsampling   │
       ▼                                   │      │ Block 3      │
┌──────────────┐                           │      │ (64x64)      │
│ Bottleneck   │                           │      └──────┬───────┘
│ (8x8)        │                           │             │
└──────┬───────┘                           │             ▲
       │                                   │      ┌──────────────┐
       ▼                                   └─────▶│ Upsampling   │
┌──────────────┐                           │      │ Block 2      │
│ Upsampling   │                           │      │ (32x32)      │
│ Block 1      │                           │      └──────┬───────┘
│ (16x16)      │                           │             │
└──────┬───────┘                           │             ▲
       │                                   └─────▶┌──────────────┐
       └───────────────────────────────────┐      │ Upsampling   │
                                           └─────▶│ Block 1      │
                                                  │ (16x16)      │
                                                  └──────────────┘
```

#### Teknik Özellikler

| Parametre | Değer |
|-----------|-------|
| **📐 Mimari** | ResNet50 encoder tabanlı U-Net |
| **📏 Giriş Boyutu** | 224x224x3 (RGB görüntüler) |
| **📤 Çıkış** | 224x224x1 (İkili segmentasyon maskesi) |
| **⚙️ Omurga** | ResNet50 (önceden eğitilmiş, dondurulmuş) |
| **🔄 Optimizasyon** | Adam optimizer (lr=0.001) |
| **📉 Loss Fonksiyonu** | Binary Crossentropy |
| **📈 Metrikler** | Accuracy, IoU (Intersection over Union) |
| **🔍 Performans** | Accuracy: 73.04%|


### 🔍 Arıza Tespit Modeli (EfficientNet-B0)

Arıza tespit modeli, transfer öğrenme yaklaşımı ile güneş panellerindeki çeşitli arıza türlerini tespit etmek üzere EfficientNet-B0 mimarisi kullanılarak geliştirilmiştir. Bu modern CNN mimarisi, güneş paneli veri setine ince ayar yapılarak optimize edilmiştir.

#### Model Mimarisi

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Giriş        │      │ EfficientNet │      │ Global Avg   │
│ (224x224x3)  │─────▶│ B0 Omurga    │─────▶│ Pooling      │
└──────────────┘      │ (dondurulmuş)│      └──────┬───────┘
                      └──────────────┘             │
                                                   ▼
                                           ┌──────────────┐
                                           │ Dropout      │
                                           │ (0.2)        │
                                           └──────┬───────┘
                                                  │
                                                  ▼
                                           ┌──────────────┐
                                           │ Dense (6)    │
                                           │ Softmax      │
                                           └──────────────┘
```

#### Teknik Özellikler

| Parametre | Değer |
|-----------|-------|
| **📐 Mimari** | Transfer öğrenme ile ince ayar yapılmış EfficientNet-B0 |
| **📏 Giriş Boyutu** | 224x224x3 (RGB görüntüler) |
| **📤 Çıkış** | 6 sınıf olasılık değerleri (Softmax) |
| **🧮 Toplam Parametreler** | 4,057,257 (15.48 MB) |
| **🛠️ Eğitilebilir** | 7,686 (30.02 KB) |
| **🔒 Dondurulmuş** | 4,049,571 (15.45 MB) |
| **🔄 Optimizasyon** | Adam optimizer (lr=0.001) |
| **📉 Loss Fonksiyonu** | Categorical Crossentropy |
| **📈 Doğruluk** | %85.79 (Doğrulama seti) |

#### Eğitim Performansı

<div align="center">
<pre>
Epoch  Accuracy  Loss    Val Accuracy  Val Loss
  1     0.6961   1.5740    0.7438      0.8177
  2     0.7009   0.8629    0.7796      0.6685
  3     0.7471   0.7267    0.7931      0.5975
  4     0.7713   0.6625    0.8154      0.5455
  5     0.7934   0.6019    0.8255      0.5150
  6     0.8084   0.5669    0.8333      0.4890
  7     0.8060   0.5534    0.8490      0.4715
  8     0.8092   0.5302    0.8468      0.4533
  9     0.8244   0.5135    0.8523      0.4446
 10     0.8294   0.4910    0.8579      0.4263
</pre>
</div>

#### Sınıflandırma Performansı (ROC Eğrisi)

<div align="center">

  ![image](https://github.com/user-attachments/assets/fa9d5fdb-e754-4149-b409-9caf02940d8b)

</div>


<div align="center">
<pre>
Sınıf                 AUC
Bird-drop             0.97
Clean                 0.99
Dusty                 0.97
Electrical-damage     0.99
Physical-Damage       0.99
Snow-Covered          1.00
</pre>
</div>

<hr>

### ⚙️ Backend (FastAPI)

Backend servisi, FastAPI kullanılarak geliştirilmiş modern ve yüksek performanslı bir API sunucusudur.

| Bileşen | Açıklama |
|---------|----------|
| **🔄 API Rotaları** | `/api/segmentation` ve `/api/classification` endpoint'leri |
| **📦 Model Kaydı** | Modellerin yüklenmesi ve işlenmesi için `ModelRegistry` sınıfı |
| **🔒 CORS Desteği** | Cross-Origin kaynak paylaşımı için güvenlik yapılandırması |
| **📊 Veri İşleme** | Görüntü ön işleme ve sonuç formatlanması |
| **📁 Statik Sunucu** | Görüntü ve sonuçların statik dosya olarak sunulması |

### 🖥️ Frontend (React + Vite)

Frontend uygulaması, React ve Vite kullanılarak geliştirilmiş, modern ve kullanıcı dostu bir arayüz sunar.

| Bileşen | Açıklama |
|---------|----------|
| **📷 Görüntü Yükleme** | Sürükle-bırak ve dosya seçiciyi kullanabilirsiniz |
| **📊 Sonuç Gösterimi** | Segmentasyon maskeleri ve arıza analizinin görselleştirilmesi |
| **📱 Responsive Tasarım** | Tüm cihazlarda uyumlu kullanıcı deneyimi |
| **🔄 Gerçek Zamanlı** | Anında sonuç gösterimi ve işleme durumu |
| **📦 Bileşen Mimarisi** | Yeniden kullanılabilir ve bakımı kolay React bileşenleri |

<hr>

### 🔧 Gereksinimler

- Python 3.8+
- Node.js 16+
- npm veya yarn
- CUDA 11.2+ (GPU kullanımı için, opsiyonel)

### 🐍 Backend Kurulumu

```bash
# Depoyu klonlayın
git clone https://github.com/Efe-Eroglu/solar-panel-segmentation-and-classification.git
cd solar-panel-segmentation-and-classification

# Sanal ortam oluşturun (isteğe bağlı)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Backend bağımlılıklarını yükleyin
cd Backend
pip install -r requirements.txt

# Uygulamayı çalıştırın
uvicorn app.main:app --reload
```

### ⚛️ Frontend Kurulumu

```bash
# Frontend dizinine geçin
cd ../Frontend

# Bağımlılıkları yükleyin
npm install
# veya
yarn install

# Geliştirme sunucusunu başlatın
npm run dev
# veya
yarn dev
```

<hr>

## 📝 Kullanım

<div align="center">
<img src="https://img.icons8.com/color/96/000000/user-manual.png" width="80px"/>
</div>

### 🔄 Temel İş Akışı

1. **📤 Görüntü Yükleme**: 
   - Web arayüzünden bir güneş paneli görüntüsü yükleyin
   - Sürükle-bırak veya dosya seçiciyi kullanabilirsiniz

2. **⚙️ İşleme**: 
   - "İşle" düğmesine tıklayarak analizi başlatın
   - İşleme durumu gerçek zamanlı olarak gösterilir

3. **📊 Sonuçları Görüntüleme**: 
   - **Segmentasyon Sonuçları**: Panel sınırları renkli maske ile gösterilir
   - **Arıza Tespiti**: Tespit edilen arızalar ve konumları işaretlenir
   - **Arıza Analizi**: Her bir arıza tipi ve güvenilirlik skorları tablo halinde sunulur
   - **Görsel Rapor**: Sonuçları indirebilir veya paylaşabilirsiniz

<hr>



## 🔌 API Referansı

<div align="center">
<img src="https://img.icons8.com/color/96/000000/api-settings.png" width="80px"/>
</div>

### 📌 Segmentasyon Endpointi

```http
POST /api/segment-image
```

#### İstek

| Parametre | Tip | Gereklilik | Açıklama |
|-----------|-----|------------|----------|
| `file` | `file` | Zorunlu | Segmentasyon yapılacak görüntü dosyası (PNG, JPG, JPEG) |

#### Yanıt

```json
{
  "mask_base64": "iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAABKTUlEQVR4nO3d...",
  "description": "Panel üzerindeki hasarlı bölgeleri vurgulayan segmentasyon maskesi."
}
```

Bu endpoint, yüklenen görüntüdeki güneş panellerini segmente eder ve maskeyi base64 formatında döndürür. Döndürülen maske görüntüsü, panellerin konumunu işaretlemek için kullanılabilir.

### 📌 Sınıflandırma Endpointi

```http
POST /api/predict-class
```

#### İstek

| Parametre | Tip | Gereklilik | Açıklama |
|-----------|-----|------------|----------|
| `file` | `file` | Zorunlu | Sınıflandırılacak görüntü dosyası (PNG, JPG, JPEG) |

#### Yanıt

```json
{
  "predicted_class": "electrical-damage",
  "confidence": 0.87,
  "all_probabilities": {
    "normal": 0.03,
    "bird-drop": 0.02,
    "dusty": 0.04,
    "electrical-damage": 0.87,
    "faulty": 0.03,
    "snow-covered": 0.01
  }
}
```

Bu endpoint, yüklenen güneş paneli görüntüsünü sınıflandırarak panel durumunu tespit eder. Yanıt olarak tahmin edilen sınıf, güven skoru ve tüm sınıfların olasılık değerlerini döndürür.

Sınıflandırma kategorileri:
- **normal**: Normal durumdaki panel
- **bird-drop**: Kuş pisliği bulunan panel
- **dusty**: Tozlu panel
- **electrical-damage**: Elektriksel hasarlı panel
- **faulty**: Fiziksel hasarlı panel
- **snow-covered**: Kar kaplı panel

<hr>

## 👥 Katkıda Bulunma

<div align="center">
<img src="https://img.icons8.com/color/96/000000/group-of-projects.png" width="80px"/>
</div>

Bu projeye katkıda bulunmak istiyorsanız, aşağıdaki adımları izleyin:

1. Projeyi forklayın
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### 📝 Katkı Kuralları

- Kodunuzu açıklayıcı yorumlarla belgelendirin
- Yeni özellikler için birim testleri ekleyin
- Stil kılavuzlarına uyun (PEP8 Python için, ESLint React için)
- Commit mesajlarınızı açıklayıcı tutun

<hr>

## 📜 Lisans

<div align="center">
<img src="https://img.icons8.com/color/96/000000/certificate.png" width="80px"/>
</div>

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

<hr>

<div align="center">
<h3>🌞 Güneş paneli arızalarını zamanında tespit ederek enerji verimliliğini artırın ve bakım maliyetini düşürün! ⚡️</h3>
</div>
