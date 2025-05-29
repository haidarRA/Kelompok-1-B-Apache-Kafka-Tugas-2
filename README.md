# Tugas 2 Apache Kafka Kelompok 1 Kelas B

Anggota Kelompok:
| Nama                     | NRP        |
| ------------------------ | ---------- |
| Muhammad Faqih Husain    | 5027231023 |
| Furqon Aryadana          | 5027231024 |
| Haidar Rafi Aqyla        | 5027231029 |

_________________

## Detail Tugas
Terdapat sebuah sistem Big Data dengan arsitektur seperti gambar di atas. Sistem tersebut berfungsi untuk menyimulasikan pemrosesan data stream menggunakan Kafka dan Apache Spark. Untuk kemudahan pemrosesan, Kafka Consumer tidak wajib menggunakan Spark Streaming. Alur yang diharapkan adalah sebagai berikut.

<ol>
  <li>Terdapat sebuah file dataset yang akan dibaca secara sekuensial oleh Kafka Producer. TIDAK DIPERBOLEHKAN MENGGUNAKAN DATASET YANG SUDAH DIGUNAKAN PADA TUGAS-TUGAS SEBELUMNYA. </li>
  <li>Kafka Producer akan mengirimkan data per baris ke Kafka Server seolah-olah sedang melakukan streaming. Proses ini dapat dilakukan dengan menambahkan jeda/sleep secara random agar data tidak dikirimkan secara langsung.</li>
  <li>Kafka consumer membaca data yang ada di dalam Kafka server dan akan menyimpan data yang diterima dalam bentuk batch. Batch dapat ditentukan berdasarkan: 
Jumlah data yang diterima</li>
Rentang waktu proses (window) Sehingga nanti akan didapatkan beberapa file dataset sesuai dengan batch yang dipilih.
  <li>Spark script bertugas untuk melakukan training model sesuai dengan data yang masuk. Diharapkan ada beberapa model yang dihasilkan sesuai dengan jumlah data yang masuk. Kalian dapat menentukan sendiri berapa jumlah data yang diproses untuk tiap model. Contoh:</li>
    Terdapat 3 model dengan skema sebagai berikut:
    <ol>
    <li>Model 1: Menggunakan data selama 5 menit pertama atau 500.000 data pertama.</li>
    <li>Model 2: Menggunakan data selama 5 menit kedua atau 500.000 data kedua.</li>
    <li>Model 3: Menggunakan data selama 5 menit ketiga atau 500.000 data ketiga.</li>
    </ol>
    Terdapat 3 model dengan skema sebagai berikut:
    <ol>
    <li>Model 1: 1/3 data pertama</li>
    <li>Model 2: 1/3 data pertama + 1/3 data kedua</li>
    <li>Model 3: 1/3 data pertama + 1/3 data kedua + 1/3 data terakhir (semua data)</li>
    </ol>
  <li>Model-model yang dihasilkan akan digunakan di dalam API. Buatlah endpoint sesuai dengan jumlah model yang ada.</li>
  <li>User akan melakukan request ke API. API akan memberikan respon sesuai dengan request user. Misal:</li>
    <ol>
    <li>Apabila user melakukan request rekomendasi, maka input yang diperlukan adalah rating dari user dan response yang diberikan adalah daftar rekomendasi.</li>
    <li>Apabila modelnya adalah kasus clustering, maka response yang diberikan adalah ada di cluster mana data input dari user tersebut.</li>
    <li>Jumlah API yang dibuat minimal sebanyak jumlah anggotanya (apabila ada 3 anggota, maka minimal membuat 3 api endpoint dengan fungsi berbeda)</li>
    </ol>
</ol>

_________________

## Dataset:
Dataset yang dipilih untuk tugas ini adalah dataset "Bitcoin Historical Data" dari link Kaggle berikut.
https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data/data

Dataset ini berisi data Bitcoin dari awal tahun 2012 sampai sekarang dengan kurang lebih **7 juta baris data** dan kolom - kolom berikut.
1. Timestamp: Waktu mulai dari time window (60s window), dalam format Unix time
2. Open: Harga awal saat mulainya time window
3. High: Harga tertinggi dari Bitcoin saat mulainya time window
4. Low: Harga terendah dari Bitcoin saat mulainya time window
5. Close:  Harga akhir saat mulainya time window
6. Volume: Volume dari transaksi Bitcoin saat time window ini

## Struktur Directory
Struktur directory untuk tugas / project ini adalah sebagai berikut.
```
.
├───data
│   ├───btcusd_1-min_data.csv
│   └───batch
│       ├───batch_1.csv
│       ├───batch_2.csv
│       └───batch_3.csv
├───kafka
│   ├───kafka_consumer.py
│   └───kafka_producer.py
├───model
│   ├───model1
│   ├───model2_high
│   ├───model2_low
│   ├───model3
│   ├───model1.py
│   ├───model2.py
│   └───model3.py
└───api.py
```

## Langkah Pengerjaan
1. Jalankan Zookeeper dan Kafka menggunakan command `.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties` dan `.\bin\windows\kafka-server-start.bat .\config\server.properties`.
![image](https://github.com/user-attachments/assets/06755903-2cfb-47ba-9965-ebdd560ed31a)
![image](https://github.com/user-attachments/assets/07ad9e8b-9826-437c-9529-78095b618189)

2. Buat topic Kafka baru bernama **bitcoin-topic** dengan command `.\bin\windows\kafka-topics.bat --create --topic bitcoin-topic --bootstrap-server localhost:9092`
3. Jalankan Kafka consumer (kafka_consumer.py) dan Kafka producer (kafka_producer.py).
![Screenshot 2025-05-28 145451](https://github.com/user-attachments/assets/cf3ea25c-24c7-4334-aca0-727d4f2f36f6)
![Screenshot 2025-05-28 165624](https://github.com/user-attachments/assets/8bd22b23-9f23-46f9-85b5-bff82b86216c)

   Producer akan mengirimkan seluruh data dari dataset ke consumer dengan kecepatan tinggi, kemudian consumer akan mengumpulkan setiap **2330000 baris data** yang diterima menjadi satu batch. Untuk jumlah keseluruhan batch sendiri ada 3 yang artinya kurang lebih **7 juta data** akan diproses nanti 

4. Buat tiga model dari batch csv yang telah dibuat dengan menjalankan program `model1.py`, `model2.py`, dan `model3.py`. Setiap model mempunyai fungsionalitas yang berbeda, yaitu sebagai berikut.
   <br>a. model1: Memprediksi harga close dari Bitcoin berdasarkan input timestamp Unix. Menggunakan Linear Regression (regresi) untuk modelnya.
   <br>b. model2: Memprediksi nilai low dan high dari Bitcoin berdasarkan input harga open dan volume. Untuk model yang dihasilkan ada dua, yaitu model2_high dan model2_low. Menggunakan Random Forest Regressor (regresi) untuk modelnya.
   <br>c. model3: Memprediksi arah tren Bitcoin (up or down) berdasarkan input harga open, close, dan volume. Menggunakan Logistic Regression (klasifikasi) untuk model ini.

   Untuk mapping model dan batch csv adalah sebagai berikut.
   <br>a. model1 --> batch_3.csv (1/3 data terakhir)
   <br>b. model2 --> batch_2.csv (1/3 data kedua)
   <br>c. model3 --> batch_1.csv (1/3 data pertama)
   
5. Jalankan program `api.py` untuk membuat endpoint API untuk ketiga model. Program ini menggunakan Flask agar bisa berjalan. Untuk endpointnya yang ada adalah sebagai berikut.

   a. **/predict/close**

   Endpoint ini menggunakan model 1 berfungsi untuk memprediksi harga close dari Bitcoin. Parameter yang diterima endpoint ini adalah **timestamp**. Hasil dari prediksi model ini adalah harga close Bitcoin dalam USD.
   ![Screenshot 2025-05-29 201325](https://github.com/user-attachments/assets/04b5a415-bebe-4d7f-a348-c1ccb0465a6c)

   b. **/predict/high_low**
   
   Endpoint ini menggunakan model 2 berfungsi untuk memprediksi nilai high dan low dari Bitcoin. Parameter yang diterima endpoint ini adalah **open** dan **volume**.
   ![Screenshot 2025-05-29 201514](https://github.com/user-attachments/assets/dcad9fa3-d0d9-42fd-9912-27524061a1bc)

   c. **/predict/trend**
   
   Endpoint ini menggunakan model 3 berfungsi untuk memprediksi tren Bitcoin (naik atau turun). Parameter yang diterima endpoint ini adalah **open**, **close**, dan **volume**.
   ![Screenshot 2025-05-29 201706](https://github.com/user-attachments/assets/f4472516-f8e1-409f-bb14-110a6ef192aa)
