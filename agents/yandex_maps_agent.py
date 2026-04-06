#!/usr/bin/env python3
"""
🗺️ YandexMaps-Agent
Yandex Maps Integration Specialist

Геокодирование, построение маршрутов, карты на сайте.
Геолокация, поиск объектов, доставка.
"""

import argparse
from pathlib import Path
from typing import Dict


class YandexMapsAgent:
    """
    🗺️ YandexMaps-Agent
    
    Специализация: Yandex Maps API Integration
    Задачи: Геокодирование, маршруты, виджеты карт
    """
    
    NAME = "🗺️ YandexMaps-Agent"
    ROLE = "Yandex Maps Specialist"
    EXPERTISE = ["Yandex Maps API", "Geocoding", "Routing", "Maps Widgets", "Geolocation"]
    
    API_JS_URL = "https://api-maps.yandex.ru/2.1/?apikey={api_key}&lang=ru_RU"
    GEOCODER_URL = "https://geocode-maps.yandex.ru/1.x"
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["yandex-map-widget.html"] = self._generate_map_widget()
        files["geocoder-api.py"] = self._generate_geocoder()
        files["delivery-calculator.js"] = self._generate_delivery_calc()
        files["store-locator.html"] = self._generate_store_locator()
        files["maps-guide.md"] = self._generate_guide()
        
        return files
    
    def _generate_map_widget(self) -> str:
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Карта на сайте</title>
    <script src="https://api-maps.yandex.ru/2.1/?apikey=YOUR_API_KEY&lang=ru_RU" type="text/javascript"></script>
    <style>
        #map {
            width: 100%;
            height: 500px;
        }
        .map-container {
            position: relative;
        }
        .map-controls {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
        .map-controls input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 250px;
        }
        .map-controls button {
            padding: 8px 16px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="map-container">
        <div class="map-controls">
            <input type="text" id="search-input" placeholder="Введите адрес...">
            <button onclick="searchAddress()">Найти</button>
            <button onclick="getUserLocation()">📍 Моё местоположение</button>
        </div>
        <div id="map"></div>
    </div>

    <script>
        let myMap;
        let myPlacemark;
        let route;

        // Инициализация карты
        ymaps.ready(init);

        function init() {
            // Создание карты
            myMap = new ymaps.Map("map", {
                center: [55.76, 37.64], // Москва
                zoom: 10,
                controls: ['zoomControl', 'searchControl', 'typeSelector']
            });

            // Клик по карте - поставить метку
            myMap.events.add('click', function (e) {
                const coords = e.get('coords');
                setPlacemark(coords);
                getAddress(coords);
            });

            // Поиск по Enter
            document.getElementById('search-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') searchAddress();
            });

            // Автопозиционирование
            getUserLocation();
        }

        // Установить метку
        function setPlacemark(coords) {
            if (myPlacemark) {
                myMap.geoObjects.remove(myPlacemark);
            }

            myPlacemark = new ymaps.Placemark(coords, {
                hintContent: 'Выбранное место',
                balloonContent: 'Загрузка адреса...'
            }, {
                preset: 'islands#redDotIcon',
                draggable: true
            });

            myPlacemark.events.add('dragend', function() {
                getAddress(myPlacemark.geometry.getCoordinates());
            });

            myMap.geoObjects.add(myPlacemark);
            myMap.setCenter(coords, 15);
        }

        // Получить адрес по координатам
        function getAddress(coords) {
            ymaps.geocode(coords).then(function(res) {
                const firstGeoObject = res.geoObjects.get(0);
                const address = firstGeoObject.getAddressLine();
                
                myPlacemark.properties.set({
                    balloonContent: address
                });

                console.log('Адрес:', address);
                console.log('Координаты:', coords);
            });
        }

        // Поиск адреса
        function searchAddress() {
            const address = document.getElementById('search-input').value;
            if (!address) return;

            ymaps.geocode(address, {
                results: 1
            }).then(function(res) {
                const firstGeoObject = res.geoObjects.get(0);
                const coords = firstGeoObject.geometry.getCoordinates();
                const boundedBy = firstGeoObject.properties.get('boundedBy');

                setPlacemark(coords);
                myMap.setBounds(boundedBy, {
                    checkZoomRange: true
                });

                myPlacemark.properties.set({
                    balloonContent: firstGeoObject.getAddressLine()
                });
            });
        }

        // Получить местоположение пользователя
        function getUserLocation() {
            if (!navigator.geolocation) {
                alert('Геолокация не поддерживается вашим браузером');
                return;
            }

            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const coords = [position.coords.latitude, position.coords.longitude];
                    setPlacemark(coords);
                    getAddress(coords);
                },
                function(error) {
                    console.error('Ошибка геолокации:', error);
                }
            );
        }

        // Построить маршрут
        function buildRoute(toCoords) {
            if (!myPlacemark) {
                alert('Сначала выберите начальную точку');
                return;
            }

            const fromCoords = myPlacemark.geometry.getCoordinates();

            if (route) {
                myMap.geoObjects.remove(route);
            }

            ymaps.route([fromCoords, toCoords]).then(function(r) {
                route = r;
                myMap.geoObjects.add(route);
                
                // Показать информацию о маршруте
                const distance = route.getHumanLength();
                const duration = route.getHumanTime();
                
                alert(`Расстояние: ${distance}\\nВремя в пути: ${duration}`);
            });
        }

        // Добавить метки магазинов
        function addStoreMarkers(stores) {
            const clusterer = new ymaps.Clusterer({
                preset: 'islands#invertedVioletClusterIcons',
                clusterDisableClickZoom: true
            });

            const geoObjects = stores.map(store => {
                return new ymaps.Placemark([store.lat, store.lng], {
                    balloonContent: `
                        <strong>${store.name}</strong><br>
                        ${store.address}<br>
                        Тел: ${store.phone}<br>
                        <a href="#" onclick="buildRoute([${store.lat}, ${store.lng}]); return false;">Построить маршрут</a>
                    `
                }, {
                    preset: 'islands#blueShoppingIcon'
                });
            });

            clusterer.add(geoObjects);
            myMap.geoObjects.add(clusterer);
        }

        // Пример добавления магазинов
        const stores = [
            { name: 'Магазин №1', lat: 55.76, lng: 37.64, address: 'Москва, ул. Ленина 1', phone: '+7 999 123-45-67' },
            { name: 'Магазин №2', lat: 55.75, lng: 37.62, address: 'Москва, ул. Гагарина 5', phone: '+7 999 765-43-21' }
        ];

        // Добавить магазины через 2 секунды (после загрузки карты)
        setTimeout(() => addStoreMarkers(stores), 2000);
    </script>
</body>
</html>
'''
    
    def _generate_geocoder(self) -> str:
        return '''#!/usr/bin/env python3
"""
Yandex Geocoder API Client
Геокодирование и обратное геокодирование
"""

import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import os


@dataclass
class GeoPoint:
    """Географическая точка"""
    lat: float
    lng: float
    address: str
    precision: str


class YandexGeocoder:
    """Клиент геокодера Яндекс"""
    
    BASE_URL = "https://geocode-maps.yandex.ru/1.x"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("YANDEX_MAPS_API_KEY")
    
    def geocode(self, address: str, **kwargs) -> List[GeoPoint]:
        """
        Прямое геокодирование: адрес → координаты
        
        Args:
            address: Адрес для поиска
            **kwargs: Дополнительные параметры
            
        Returns:
            Список найденных точек
        """
        params = {
            "apikey": self.api_key,
            "geocode": address,
            "format": "json",
            "results": kwargs.get("limit", 5),
            "lang": kwargs.get("lang", "ru_RU")
        }
        
        # Ограничение по региону
        if "bbox" in kwargs:
            params["bbox"] = kwargs["bbox"]
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        return self._parse_response(data)
    
    def reverse_geocode(self, lat: float, lng: float, **kwargs) -> Optional[GeoPoint]:
        """
        Обратное геокодирование: координаты → адрес
        
        Args:
            lat: Широта
            lng: Долгота
            **kwargs: Дополнительные параметры
            
        Returns:
            Найденный адрес или None
        """
        coords = f"{lng},{lat}"
        
        params = {
            "apikey": self.api_key,
            "geocode": coords,
            "format": "json",
            "results": 1,
            "kind": kwargs.get("kind", "house")  # house, street, metro, district, locality
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        points = self._parse_response(data)
        
        return points[0] if points else None
    
    def _parse_response(self, data: Dict) -> List[GeoPoint]:
        """Разбор ответа API"""
        points = []
        
        try:
            feature_members = data["response"]["GeoObjectCollection"]["featureMember"]
            
            for member in feature_members:
                geo_object = member["GeoObject"]
                
                # Координаты
                pos = geo_object["Point"]["pos"]
                lng, lat = map(float, pos.split())
                
                # Адрес
                address = geo_object["metaDataProperty"]["GeocoderMetaData"]["text"]
                precision = geo_object["metaDataProperty"]["GeocoderMetaData"]["precision"]
                
                points.append(GeoPoint(
                    lat=lat,
                    lng=lng,
                    address=address,
                    precision=precision
                ))
        except (KeyError, IndexError):
            pass
        
        return points
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Вычислить расстояние между точками (формула гаверсинусов)
        
        Args:
            point1: (lat, lng) первая точка
            point2: (lat, lng) вторая точка
            
        Returns:
            Расстояние в километрах
        """
        import math
        
        R = 6371  # Радиус Земли в км
        
        lat1, lng1 = math.radians(point1[0]), math.radians(point1[1])
        lat2, lng2 = math.radians(point2[0]), math.radians(point2[1])
        
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def find_nearest(self, target: Tuple[float, float], points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
        """
        Найти ближайшую точку
        
        Args:
            target: (lat, lng) целевая точка
            points: Список точек [(lat, lng), ...]
            
        Returns:
            (ближайшая_точка, расстояние)
        """
        nearest = None
        min_distance = float('inf')
        
        for point in points:
            dist = self.calculate_distance(target, point)
            if dist < min_distance:
                min_distance = dist
                nearest = point
        
        return nearest, min_distance


# Пример использования
if __name__ == "__main__":
    geocoder = YandexGeocoder()
    
    # Прямое геокодирование
    print("=== Прямое геокодирование ===")
    results = geocoder.geocode("Москва, Красная площадь 1")
    for point in results[:3]:
        print(f"{point.address}")
        print(f"  Координаты: {point.lat}, {point.lng}")
        print(f"  Точность: {point.precision}")
        print()
    
    # Обратное геокодирование
    print("=== Обратное геокодирование ===")
    point = geocoder.reverse_geocode(55.7539, 37.6208)
    if point:
        print(f"Координаты 55.7539, 37.6208:")
        print(f"  Адрес: {point.address}")
'''
    
    def _generate_delivery_calc(self) -> str:
        return '''/**
 * Delivery Calculator using Yandex Maps
 * Калькулятор стоимости доставки
 */

class DeliveryCalculator {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.warehouse = null; // Координаты склада
    this.tariffs = {
      'economy': { basePrice: 300, pricePerKm: 20, minPrice: 300 },
      'standard': { basePrice: 500, pricePerKm: 35, minPrice: 500 },
      'express': { basePrice: 800, pricePerKm: 60, minPrice: 800 }
    };
  }

  // Установить склад
  setWarehouse(address) {
    return this.geocode(address).then(coords => {
      this.warehouse = coords;
      return coords;
    });
  }

  // Геокодирование
  async geocode(address) {
    const url = `https://geocode-maps.yandex.ru/1.x/?apikey=${this.apiKey}&geocode=${encodeURIComponent(address)}&format=json`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    const pos = data.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos;
    const [lng, lat] = pos.split(' ').map(Number);
    
    return { lat, lng };
  }

  // Рассчитать доставку
  async calculate(address, tariff = 'standard') {
    if (!this.warehouse) {
      throw new Error('Сначала установите адрес склада');
    }

    const destCoords = await this.geocode(address);
    const distance = this.calculateDistance(this.warehouse, destCoords);
    
    const tariffInfo = this.tariffs[tariff];
    const price = Math.max(
      tariffInfo.minPrice,
      tariffInfo.basePrice + (distance * tariffInfo.pricePerKm)
    );

    // Время доставки (примерно)
    const duration = this.estimateDuration(distance);

    return {
      distance: Math.round(distance * 10) / 10, // км, округлено
      duration: duration,
      price: Math.round(price),
      tariff: tariff,
      destination: destCoords,
      address: address
    };
  }

  // Расчёт расстояния (формула гаверсинусов)
  calculateDistance(point1, point2) {
    const R = 6371; // Радиус Земли в км
    const dLat = this.toRad(point2.lat - point1.lat);
    const dLon = this.toRad(point2.lng - point1.lng);
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(this.toRad(point1.lat)) * Math.cos(this.toRad(point2.lat)) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    
    return R * c;
  }

  toRad(deg) {
    return deg * (Math.PI / 180);
  }

  // Оценка времени доставки
  estimateDuration(distance) {
    // Средняя скорость 30 км/ч в городе + время на разгрузку
    const hours = distance / 30 + 0.5;
    
    if (hours < 1) return '30-60 минут';
    if (hours < 2) return '1-2 часа';
    if (hours < 4) return '2-4 часа';
    if (hours < 24) return 'в течение дня';
    return '1-2 дня';
  }

  // Получить все тарифы
  async calculateAllTariffs(address) {
    const results = {};
    
    for (const [name, info] of Object.entries(this.tariffs)) {
      try {
        results[name] = await this.calculate(address, name);
      } catch (e) {
        results[name] = { error: e.message };
      }
    }
    
    return results;
  }
}

// Пример использования
// const calculator = new DeliveryCalculator('YOUR_API_KEY');
// calculator.setWarehouse('Москва, ул. Складская 1').then(() => {
//   calculator.calculate('Москва, Красная площадь 1').then(result => {
//     console.log(`Стоимость: ${result.price}₽, Расстояние: ${result.distance}км`);
//   });
// });
'''
    
    def _generate_store_locator(self) -> str:
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Найти магазин</title>
    <script src="https://api-maps.yandex.ru/2.1/?apikey=YOUR_API_KEY&lang=ru_RU"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .search-box { margin-bottom: 20px; }
        .search-box input {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
        }
        .content { display: flex; gap: 20px; }
        .stores-list {
            width: 350px;
            max-height: 600px;
            overflow-y: auto;
        }
        .store-card {
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .store-card:hover {
            border-color: #007bff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .store-card.active {
            border-color: #007bff;
            background: #f0f7ff;
        }
        .store-card h3 { margin: 0 0 8px 0; font-size: 16px; }
        .store-card p { margin: 4px 0; font-size: 14px; color: #666; }
        .store-card .distance { color: #007bff; font-weight: bold; }
        #map { flex: 1; height: 600px; border-radius: 8px; }
        .no-results { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ Найти ближайший магазин</h1>
        
        <div class="search-box">
            <input type="text" id="address-input" placeholder="Введите ваш адрес...">
        </div>
        
        <div class="content">
            <div class="stores-list" id="stores-list">
                <div class="no-results">
                    Введите адрес, чтобы найти ближайшие магазины
                </div>
            </div>
            <div id="map"></div>
        </div>
    </div>

    <script>
        // База магазинов
        const stores = [
            { id: 1, name: 'Магазин на Тверской', address: 'Москва, Тверская ул., 15', phone: '+7 (999) 111-11-11', hours: '9:00-21:00', lat: 55.758, lng: 37.617 },
            { id: 2, name: 'Магазин на Арбате', address: 'Москва, Арбат, 25', phone: '+7 (999) 222-22-22', hours: '10:00-22:00', lat: 55.752, lng: 37.596 },
            { id: 3, name: 'Магазин в Марьино', address: 'Москва, Люблинская ул., 151', phone: '+7 (999) 333-33-33', hours: '9:00-20:00', lat: 55.65, lng: 37.743 },
            { id: 4, name: 'Магазин на МКАД', address: 'Москва, МКАД 65 км', phone: '+7 (999) 444-44-44', hours: 'круглосуточно', lat: 55.85, lng: 37.39 },
            { id: 5, name: 'Магазин в Химках', address: 'Химки, Ленинградское ш., 5', phone: '+7 (999) 555-55-55', hours: '9:00-21:00', lat: 55.89, lng: 37.44 }
        ];

        let myMap;
        let userPlacemark;
        let storePlacemarks = [];

        ymaps.ready(init);

        function init() {
            myMap = new ymaps.Map('map', {
                center: [55.76, 37.64],
                zoom: 10,
                controls: ['zoomControl']
            });

            // Добавить все магазины на карту
            addAllStores();

            // Обработка ввода адреса
            let timeout;
            document.getElementById('address-input').addEventListener('input', function(e) {
                clearTimeout(timeout);
                timeout = setTimeout(() => searchStores(e.target.value), 500);
            });
        }

        function addAllStores() {
            stores.forEach(store => {
                const placemark = new ymaps.Placemark([store.lat, store.lng], {
                    hintContent: store.name,
                    balloonContent: `
                        <strong>${store.name}</strong><br>
                        📍 ${store.address}<br>
                        📞 ${store.phone}<br>
                        🕐 ${store.hours}
                    `
                }, {
                    preset: 'islands#blueShoppingIcon'
                });
                
                myMap.geoObjects.add(placemark);
                storePlacemarks.push({ store, placemark });
            });
        }

        async function searchStores(address) {
            if (!address.trim()) return;

            try {
                // Геокодируем адрес пользователя
                const res = await ymaps.geocode(address, { results: 1 });
                const userCoords = res.geoObjects.get(0).geometry.getCoordinates();

                // Устанавливаем метку пользователя
                if (userPlacemark) {
                    myMap.geoObjects.remove(userPlacemark);
                }

                userPlacemark = new ymaps.Placemark(userCoords, {
                    hintContent: 'Вы здесь',
                    balloonContent: address
                }, {
                    preset: 'islands#redHomeIcon'
                });

                myMap.geoObjects.add(userPlacemark);

                // Сортируем магазины по расстоянию
                const sortedStores = stores.map(store => {
                    const distance = calculateDistance(userCoords, [store.lat, store.lng]);
                    return { ...store, distance };
                }).sort((a, b) => a.distance - b.distance);

                // Обновляем список
                renderStoresList(sortedStores);

                // Центрируем карту
                myMap.setCenter(userCoords, 11);

            } catch (e) {
                console.error('Ошибка поиска:', e);
            }
        }

        function calculateDistance(point1, point2) {
            // Упрощённый расчёт
            const R = 6371;
            const dLat = (point2[0] - point1[0]) * Math.PI / 180;
            const dLon = (point2[1] - point1[1]) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                      Math.cos(point1[0] * Math.PI / 180) * Math.cos(point2[0] * Math.PI / 180) *
                      Math.sin(dLon/2) * Math.sin(dLon/2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        }

        function renderStoresList(stores) {
            const listEl = document.getElementById('stores-list');
            
            if (stores.length === 0) {
                listEl.innerHTML = '<div class="no-results">Магазины не найдены</div>';
                return;
            }

            listEl.innerHTML = stores.map(store => `
                <div class="store-card" onclick="focusStore(${store.id})" data-id="${store.id}">
                    <h3>${store.name}</h3>
                    <p>📍 ${store.address}</p>
                    <p>📞 ${store.phone}</p>
                    <p>🕐 ${store.hours}</p>
                    <p class="distance">${store.distance.toFixed(1)} км</p>
                </div>
            `).join('');
        }

        function focusStore(storeId) {
            const store = stores.find(s => s.id === storeId);
            if (!store) return;

            // Подсветить карточку
            document.querySelectorAll('.store-card').forEach(el => el.classList.remove('active'));
            document.querySelector(`[data-id="${storeId}"]`).classList.add('active');

            // Центрировать карту
            myMap.setCenter([store.lat, store.lng], 15);

            // Открыть балун
            const item = storePlacemarks.find(sp => sp.store.id === storeId);
            if (item) {
                item.placemark.balloon.open();
            }
        }
    </script>
</body>
</html>
'''
    
    def _generate_guide(self) -> str:
        return '''# Руководство по Яндекс Картам API

## Получение API ключа

1. Перейдите на https://developer.tech.yandex.ru
2. Создайте приложение
3. Подключите "JavaScript API и HTTP Геокодер"
4. Скопируйте API ключ

## JavaScript API

### Базовая инициализация

```html
<script src="https://api-maps.yandex.ru/2.1/?apikey=ВАШ_КЛЮЧ&lang=ru_RU"></script>
<script>
  ymaps.ready(function() {
    const map = new ymaps.Map('map', {
      center: [55.76, 37.64], // Москва
      zoom: 10
    });
  });
</script>
```

### Геокодирование

```javascript
// Адрес → координаты
ymaps.geocode('Москва, Красная площадь').then(function(res) {
  const coords = res.geoObjects.get(0).geometry.getCoordinates();
  console.log(coords); // [55.7539, 37.6208]
});

// Координаты → адрес
ymaps.geocode([55.7539, 37.6208], { kind: 'house' }).then(function(res) {
  const address = res.geoObjects.get(0).getAddressLine();
  console.log(address);
});
```

### Маршруты

```javascript
ymaps.route([fromCoords, toCoords]).then(function(route) {
  map.geoObjects.add(route);
  
  const distance = route.getHumanLength(); // "15 км"
  const duration = route.getHumanTime();   // "25 мин"
});
```

## HTTP Геокодер

```bash
# Прямое геокодирование
curl "https://geocode-maps.yandex.ru/1.x/?apikey=КЛЮЧ&geocode=Москва+Красная+площадь&format=json"

# Обратное геокодирование
curl "https://geocode-maps.yandex.ru/1.x/?apikey=КЛЮЧ&geocode=37.6208,55.7539&format=json"
```

## Лимиты API

| Тип | Бесплатно | Платно |
|-----|-----------|--------|
| JavaScript API | 25,000 загрузок/сутки | От 3000₽/мес |
| Геокодер | 1000 запросов/сутки | От 1500₽/мес |

## Полезные ссылки

- Документация: https://yandex.ru/dev/maps/jsapi/doc/2.1/quick-start/index.html
- Примеры: https://yandex.ru/dev/maps/jsbox/2.1/
- Кабинет разработчика: https://developer.tech.yandex.ru
'''


def main():
    parser = argparse.ArgumentParser(description="🗺️ YandexMaps-Agent")
    parser.add_argument("request", nargs="?", help="Задача")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = YandexMapsAgent()
    
    if args.request:
        print(f"🗺️ {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🗺️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\\nAPI: JavaScript API, HTTP Geocoder")
        print(f"\\nВозможности:")
        print(f"  - Интерактивные карты на сайте")
        print(f"  - Геокодирование адресов")
        print(f"  - Построение маршрутов")
        print(f"  - Поиск ближайших объектов")
        print(f"  - Калькулятор доставки")


if __name__ == "__main__":
    main()
