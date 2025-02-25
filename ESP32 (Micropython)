from machine import Pin, ADC
import time
import network
import dht
import urequests as requests

# Konfigurasi Ubidots
DEVICE_ID = "67b92bec61085d1a4949aabc"
VARIABEL_LABEL1 = "suhu-1"
VARIABEL_LABEL2 = "kelembapan-1"
VARIABEL_LABEL3 = "pir"
VARIABEL_LABEL4 = "led"
VARIABEL_LABEL5 = "ldr"
VARIABEL_LABEL6 = "ldr_threshold"
WIFI_SSID = "lelymalang3"
WIFI_PASSWORD = "ayobelajar"
UBIDOTS_TOKEN = "BBUS-fK8WktodTih888gFKYV7LrE7Lbqibv"

# Koneksi ke sensor
dht_sensor = dht.DHT11(Pin(21))
pir_pin = Pin(19, Pin.IN)
led_pin = Pin(22, Pin.OUT)
ldr_sensor = ADC(Pin(2))
ldr_sensor.width(ADC.WIDTH_10BIT)  # Resolusi 10-bit (0-1023)

# Koneksi ke WiFi
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Menghubungkan ke WiFi...")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

timeout = 10
start_time = time.time()
while not wifi_client.isconnected():
    if time.time() - start_time > timeout:
        print("Gagal terhubung ke WiFi.")
        break
    time.sleep(0.1)
else:
    print("WiFi Tersambung!")
    print(wifi_client.ifconfig())

# Fungsi mengirim data ke Ubidots
def send_to_ubidots(label, value):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {label: {"value": value}}
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Data {label} dikirim ke Ubidots:", response.text)
        response.close()
    except Exception as e:
        print(f"Gagal mengirim data {label}:", e)

# Fungsi mendapatkan nilai dari Ubidots
def get_ubidots_value(label):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}/{label}/lv"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    try:
        response = requests.get(url, headers=headers)
        data = response.text.strip()
        response.close()
        return int(float(data))
    except Exception as e:
        print(f"Gagal mengambil nilai {label}:", e)
        return 0

# Set nilai awal di Ubidots
send_to_ubidots(VARIABEL_LABEL4, 0)  # LED mati
send_to_ubidots(VARIABEL_LABEL6, 1000)  # Threshold awal LDR

# Fungsi membaca data dari DHT11
def read_dht():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except Exception as e:
        print("Gagal membaca DHT11:", e)
        return None, None

# Fungsi membaca PIR
def read_pir():
    return pir_pin.value()

# Fungsi membaca LDR
def read_ldr():
    try:
        value = ldr_sensor.read()
        print(f"LDR Value: {value}")
        return value
    except OSError as e:
        print("Error membaca LDR:", e)
        return -1  # Nilai default jika gagal

# Loop utama
while True:
    suhu, kelembapan = read_dht()
    if suhu is not None and kelembapan is not None:
        print(f"Suhu: {suhu:.1f}°C, Kelembapan: {kelembapan:.1f}%")
        send_to_ubidots(VARIABEL_LABEL1, suhu)
        send_to_ubidots(VARIABEL_LABEL2, kelembapan)

    pir_status = read_pir()
    print("PIR Status:", "Gerakan terdeteksi" if pir_status else "Tidak ada gerakan")
    send_to_ubidots(VARIABEL_LABEL3, pir_status)

    # Membaca nilai LDR
    ldr_value = read_ldr()

    # Mendapatkan threshold LDR dari Ubidots
    ldr_threshold = get_ubidots_value(VARIABEL_LABEL6)
    print(f"Threshold LDR dari Ubidots: {ldr_threshold}")

    # Logika menyalakan LED berdasarkan LDR
    if ldr_value < ldr_threshold:
        led_pin.value(1)
        send_to_ubidots(VARIABEL_LABEL4, 1)  # LED nyala
        print("LED ON (Karena cahaya rendah)")
    else:
        led_pin.value(0)
        send_to_ubidots(VARIABEL_LABEL4, 0)  # LED mati
        print("LED OFF (Cahaya cukup)")

    time.sleep(5)

