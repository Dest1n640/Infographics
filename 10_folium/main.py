import folium
from folium import FeatureGroup, LayerControl
from branca.element import Template, MacroElement

places_data = [
    {"name": "Красная площадь", "category": "Достопримечательность", "lat": 55.7535, "lon": 37.6210, "likes": 5000},
    {"name": "Парк Зарядье", "category": "Парк", "lat": 55.7512, "lon": 37.6278, "likes": 4200},
    {"name": "Большой театр", "category": "Театр", "lat": 55.7602, "lon": 37.6185, "likes": 3100},
    {"name": "Третьяковская галерея", "category": "Музей", "lat": 55.7414, "lon": 37.6208, "likes": 3800},
    {"name": "Кафе Пушкинъ", "category": "Ресторан", "lat": 55.7630, "lon": 37.6046, "likes": 2100},
    {"name": "Парк Горького", "category": "Парк", "lat": 55.7289, "lon": 37.6025, "likes": 4800},
    {"name": "Храм Христа Спасителя", "category": "Храм", "lat": 55.7446, "lon": 37.6055, "likes": 2900},
    {"name": "ГУМ", "category": "Торговый центр", "lat": 55.7547, "lon": 37.6215, "likes": 3500},
    {"name": "Памятник Пушкину", "category": "Памятник", "lat": 55.7656, "lon": 37.6053, "likes": 1200},
    {"name": "Стадион Лужники", "category": "Стадион", "lat": 55.7157, "lon": 37.5537, "likes": 4500},
    {"name": "Ленинка (РГБ)", "category": "Библиотека", "lat": 55.7516, "lon": 37.6087, "likes": 1800},
    {"name": "Смотровая Воробьевы горы", "category": "Смотровая площадка", "lat": 55.7093, "lon": 37.5422, "likes": 3900},
    {"name": "ВДНХ", "category": "Парк", "lat": 55.8290, "lon": 37.6310, "likes": 4900},
    {"name": "ЦУМ", "category": "Торговый центр", "lat": 55.7608, "lon": 37.6201, "likes": 2500},
    {"name": "Музей Космонавтики", "category": "Музей", "lat": 55.8228, "lon": 37.6397, "likes": 3200},
    {"name": "White Rabbit", "category": "Ресторан", "lat": 55.7479, "lon": 37.5816, "likes": 2700},
    {"name": "Станция Комсомольская", "category": "Метро", "lat": 55.7766, "lon": 37.6560, "likes": 900},
    {"name": "Памятник Петру I", "category": "Памятник", "lat": 55.7383, "lon": 37.6083, "likes": 850},
    {"name": "Собор Василия Блаженного", "category": "Храм", "lat": 55.7525, "lon": 37.6230, "likes": 4700},
    {"name": "Театр Ленком", "category": "Театр", "lat": 55.7667, "lon": 37.6062, "likes": 1500},
    {"name": "Музей Изобразительных Искусств", "category": "Музей", "lat": 55.7473, "lon": 37.6052, "likes": 3400},
    {"name": "Аптекарский огород", "category": "Парк", "lat": 55.7781, "lon": 37.6358, "likes": 2800},
    {"name": "Депо Москва", "category": "Ресторан", "lat": 55.7801, "lon": 37.5925, "likes": 3600},
    {"name": "Стадион Динамо", "category": "Стадион", "lat": 55.7915, "lon": 37.5598, "likes": 2000},
    {"name": "Москва-Сити (Смотровая)", "category": "Смотровая площадка", "lat": 55.7486, "lon": 37.5385, "likes": 4600},
    {"name": "Европейский", "category": "Торговый центр", "lat": 55.7445, "lon": 37.5660, "likes": 2300},
    {"name": "Памятник Юрию Долгорукому", "category": "Памятник", "lat": 55.7621, "lon": 37.6105, "likes": 1100},
    {"name": "Станция Маяковская", "category": "Метро", "lat": 55.7698, "lon": 37.5959, "likes": 1400},
    {"name": "Библиотека Иностранной литературы", "category": "Библиотека", "lat": 55.7476, "lon": 37.6496, "likes": 700},
    {"name": "Театр Современник", "category": "Театр", "lat": 55.7607, "lon": 37.6455, "likes": 1900}
]

category_styles = {
    "Достопримечательность": {"color": "red", "icon": "star"},
    "Парк": {"color": "green", "icon": "tree"},
    "Театр": {"color": "purple", "icon": "masks-theater"},
    "Музей": {"color": "blue", "icon": "building-columns"},
    "Ресторан": {"color": "orange", "icon": "utensils"},
    "Храм": {"color": "beige", "icon": "church"},
    "Торговый центр": {"color": "cadetblue", "icon": "cart-shopping"},
    "Памятник": {"color": "gray", "icon": "monument"},
    "Стадион": {"color": "lightgreen", "icon": "futbol"},
    "Библиотека": {"color": "darkblue", "icon": "book"},
    "Смотровая площадка": {"color": "lightblue", "icon": "eye"},
    "Метро": {"color": "darkred", "icon": "train-subway"}
}

likes = [place['likes'] for place in places_data]
min_likes, max_likes = min(likes), max(likes)

def get_radius(like_count):
    return (like_count - min_likes) / (max_likes - min_likes) * 250 + 50

m = folium.Map(location=[55.7512, 37.6184], zoom_start=12, tiles=None)

folium.TileLayer('CartoDB positron', name='Светлая карта').add_to(m)
folium.TileLayer('CartoDB dark_matter', name='Темная карта').add_to(m)
folium.TileLayer('OpenStreetMap', name='Стандартная карта (OSM)').add_to(m)

feature_groups = {}
for cat in category_styles.keys():
    fg = FeatureGroup(name=f'<span style="color: {category_styles[cat]["color"]}">{cat}</span>')
    feature_groups[cat] = fg
    m.add_child(fg)

for place in places_data:
    lat, lon = place['lat'], place['lon']
    cat = place['category']
    name = place['name']
    like = place['likes']
    
    style = category_styles[cat]
    
    popup_text = f"<b>{name}</b><br>Категория: {cat}<br>Лайки: 💖 {like}"
    
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip=name,
        icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
    ).add_to(feature_groups[cat])
    
    folium.Circle(
        location=[lat, lon],
        radius=get_radius(like),
        color=style['color'],
        fill=True,
        fill_color=style['color'],
        fill_opacity=0.3,
        weight=1,
        tooltip=f"Зона популярности ({like} лайков)"
    ).add_to(feature_groups[cat])

LayerControl(collapsed=False).add_to(m)

legend_items = ""
for cat, style in category_styles.items():
    color = style['color']
    if color == 'cadetblue': color = '#5F9EA0'
    elif color == 'darkblue': color = '#00008B'
    elif color == 'darkred': color = '#8B0000'
    elif color == 'lightgreen': color = '#90EE90'
    elif color == 'lightblue': color = '#ADD8E6'
    elif color == 'beige': color = '#D1B26F'
    
    legend_items += f'''
        <div style="margin-bottom: 5px;">
            <i class="fa fa-circle fa-1x" style="color:{color}; margin-right:5px;"></i> {cat}
        </div>
    '''

template = f"""
{{% macro html(this, kwargs) %}}
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"/>
</head>
<body>
<div style="
    position: fixed; 
    bottom: 30px; left: 30px; width: 220px; height: auto; 
    background-color: white; border: 2px solid grey; z-index:9999; font-size:12px;
    padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    ">
    <h4 style="margin-top:0px; margin-bottom:10px; text-align:center;">Легенда категорий</h4>
    {legend_items}
    <hr style="margin:5px 0;">
    <div style="font-size: 10px; color: gray;">
        * Круги под маркерами показывают пропорцию лайков
    </div>
</div>
</body>
</html>
{{% endmacro %}}
"""  

macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

m.save('interactive_moscow_map.html')
print("Карта успешно сгенерирована и сохранена в файл 'interactive_moscow_map.html'!")
