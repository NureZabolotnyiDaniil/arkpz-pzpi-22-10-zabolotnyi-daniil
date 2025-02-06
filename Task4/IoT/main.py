from machine import Pin, PWM, ADC, Timer
import machine
import time
import urequests as requests
import network
import ujson


class IoTLantern:
    def __init__(self, lantern_id: int, api_base: str):
        self.lantern_id = lantern_id
        self.api_base = api_base
        self.api_url = f"{api_base}/iot/{lantern_id}"
        
        self.log = []
        self.max_log_size = 100
        self._add_log("=== ІНІЦІАЛІЗАЦІЯ ПРИСТРОЮ ===")
        self._add_log(f"ID ліхтаря: {lantern_id}")
        self._add_log(f"API endpoint: {self.api_url}")
        
        try:
            self.led = PWM(Pin(18, Pin.OUT), freq=5000)
            self._add_log("PWM LED ініціалізовано")
            
            self.pir = Pin(23, Pin.IN)
            self._add_log("PIR датчик ініціалізовано")
            
            self.voltage_sensor = ADC(Pin(35))
            self.voltage_sensor.atten(ADC.ATTN_11DB)
            self._add_log("Датчик напруги ініціалізовано")
        except Exception as e:
            self._add_log(f"ПОМИЛКА ІНІЦІАЛІЗАЦІЇ: {str(e)}")
            raise
        
        self.settings = {
            'base_brightness': 10,   # у відсотках
            'active_brightness': 100, # у відсотках
            'active_time': 0         # у секундах
        }
        
        self.last_update = time.time()
        self.connection_status = False
        self.wifi = network.WLAN(network.STA_IF)
        
        self._print_logs()
        
        self._hardware_test()
        
        self._connect_wifi_with_retry()
    

    def _add_log(self, message: str):
        """Логування з негайним виводом"""
        timestamp = time.localtime()
        timestamp_str = f"{timestamp[3]:02}:{timestamp[4]:02}:{timestamp[5]:02}"
        log_entry = f"[{timestamp_str}] {message}"
        self.log.append(log_entry)
        print(log_entry)
        if len(self.log) > self.max_log_size:
            self.log.pop(0)
    

    def _print_logs(self):
        """Вивід усіх логів"""
        print("\n=== ПОВНИЙ ЖУРНАЛ ===")
        for entry in self.log:
            print(entry)
        print("====================\n")
    

    def _hardware_test(self):
        """Апаратний тест світлодіода"""
        self._add_log("Запуск апаратного тесту...")
        for duty in [0, 512, 1023]:
            self.led.duty(duty)
            self._add_log(f"Яскравість: {duty}/1023")
            time.sleep(1)
        self.led.duty(0)
    

    def _connect_wifi_with_retry(self, retries=5):
        """Підключення до WiFi з повторними спробами"""
        ssid = 'Wokwi-GUEST'
        password = ''
        
        for attempt in range(retries):
            self._add_log(f"Спроба підключення до WiFi #{attempt+1}")
            try:
                if not self.wifi.isconnected():
                    self.wifi.active(True)
                    self.wifi.disconnect()
                    time.sleep(1)
                    self.wifi.connect(ssid, password)
                    self._add_log("Триває процес підключення...")
                    
                    for _ in range(15):
                        if self.wifi.isconnected():
                            ip = self.wifi.ifconfig()[0]
                            self._add_log(f"Успішне підключення! IP: {ip}")
                            self.fetch_settings()
                            return True
                        time.sleep(1)
                    self._add_log("Таймаут підключення")
                else:
                    self._add_log("Вже підключено до WiFi")
                    self.fetch_settings()
                    return True
            except Exception as e:
                self._add_log(f"Помилка WiFi: {str(e)}")
            
            time.sleep(5)
        
        self._add_log("Критична помилка: Не вдалося підключитися до WiFi")
        return False
    

    def fetch_settings(self):
        """Отримання налаштувань з покращеною діагностикою"""
        try:
            url = f"{self.api_url}/settings"
            self._add_log(f"Запит налаштувань: {url}")
            response = requests.get(
                url,
                headers={
                    "ngrok-skip-browser-warning": "true",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            self._add_log(f"HTTP статус: {response.status_code}")
            
            if response.status_code == 200:
                self.settings = ujson.loads(response.text)
                self.connection_status = True
                self._add_log(f"Отримано налаштування: {self.settings}")
            else:
                self._add_log(f"Помилка: {response.text}")
            
            response.close()
            return True
        except Exception as e:
            self._add_log(f"Помилка запиту: {repr(e)}")
            self.connection_status = False
            return False
    

    def report_motion(self):
        """Відправка події руху на сервер"""
        retries = 3
        for attempt in range(retries):
            try:
                self._add_log("Відправка події руху")
                response = requests.post(
                    f"{self.api_url}/motion",
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                self._add_log(f"Відповідь руху: {response.status_code}")
                response.close()
                return True
            except Exception as e:
                self._add_log(f"Помилка відправки руху: {repr(e)}")
                time.sleep(2)
        self._add_log("Не вдалося відправити подію руху після 3 спроб")
        return False
    

    def _calculate_duty(self, brightness_percent: int) -> int:
        """Конвертація відсотків яскравості у значення duty"""
        return int((brightness_percent / 100) * 1023)
    

    def run(self):
        """Основний цикл з захистом від збоїв"""
        self._add_log("=== ЗАПУСК ОСНОВНОГО ЦИКЛУ ===")
        last_motion = 0
        base_duty = self._calculate_duty(self.settings['base_brightness'])
        active_duty = self._calculate_duty(self.settings['active_brightness'])
        last_pir_state = 0
        
        try:
            while True:
                current_time = time.time()
                
                # Оновлення налаштувань кожні 60 секунд
                if int(current_time) % 60 == 0:
                    self._add_log("Ініціювання оновлення налаштувань...")
                    if self.fetch_settings():
                        base_duty = self._calculate_duty(self.settings['base_brightness'])
                        active_duty = self._calculate_duty(self.settings['active_brightness'])
                
                pir_value = self.pir.value()
                
                if pir_value and last_pir_state == 0:
                    self._add_log("Виявлено рух! Активується...")
                    last_motion = current_time
                    target_duty = active_duty if self.connection_status else base_duty
                    self.led.duty(target_duty)
                    self._add_log(f"Встановлено яскравість: {target_duty}/1023")
                    
                    if self.connection_status:
                        self.report_motion()
                    last_pir_state = 1
                elif not pir_value:
                    last_pir_state = 0
                    timeout = current_time - last_motion
                    adjusted_timeout = max(self.settings.get('active_time', 5), 0)  # Корекція часу
                    
                    if timeout > adjusted_timeout:
                        self.led.duty(base_duty)
                        self._add_log(f"Повернення до базової яскравості: {base_duty}/1023")
                
                time.sleep(0.5)
                
        except Exception as e:
            self._add_log(f"ФАТАЛЬНА ПОМИЛКА: {str(e)}")
            self._emergency_blink()
            machine.reset()
    
    
    def _emergency_blink(self):
        """Аварійна індикація"""
        for _ in range(5):
            self.led.duty(1023)
            time.sleep(0.5)
            self.led.duty(0)
            time.sleep(0.5)


# Запуск пристрою
try:
    lantern = IoTLantern(
        lantern_id=3,
        api_base="http://6511-83-24-98-99.ngrok-free.app"
    )
    lantern.run()
except Exception as e:
    print(f"КРИТИЧНИЙ ЗБІЙ: {str(e)}")
    machine.reset()
