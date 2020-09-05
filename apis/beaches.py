from .webscrape import create_beach_api, update_beach_api
from .models import Beach

beaches = {
    "Blacks": ["https://www.surfline.com/surf-report/blacks/5842041f4e65fad6a770883b", 1, 32.8907, 117.2535],
    "Oceanside Pier": ["https://www.surfline.com/surf-report/oceanside-pier-northside/5842041f4e65fad6a7708835", 1, 33.1934, 117.3860],
    "Lowers": ["https://www.surfline.com/surf-report/lower-trestles/5842041f4e65fad6a770888a", 2, 33.3853, 117.5939],
    "56th St": ["https://www.surfline.com/surf-report/56th-street-close-up/5a26e1ba9caa98001b09d0e7", 2, 33.6229, 117.9467],
    "Huntington Beach Pier": ["https://www.surfline.com/surf-report/hb-pier-northside/5842041f4e65fad6a7708827", 2, 33.654907, -118.004375],
    "El Porto": ["https://www.surfline.com/surf-report/el-porto/5842041f4e65fad6a7708906", 1, 33.9038, 118.4192],
    "Malibu": ["https://www.surfline.com/surf-report/malibu-second-to-third-point/5842041f4e65fad6a7708817", 2, 34.0363, 118.6779],
    "County Line": ["https://www.surfline.com/surf-report/county-line/5842041f4e65fad6a7708813", 2, 34.0514, 118.9600],
    "Ventura Harbor": ["https://www.surfline.com/surf-report/ventura-harbor/5842041f4e65fad6a7708811", 1, 34.245624, -119.263642],
    "Ventura Point": ["https://www.surfline.com/surf-report/ventura-point/584204204e65fad6a77096b1", 1, 34.2743, 119.2992],
    "Faria": ["https://www.surfline.com/surf-report/pitas-point/5842041f4e65fad6a7708957", 1, 34.324963, -119.395704],
    "Rincon": ["https://www.surfline.com/surf-report/rincon/5842041f4e65fad6a7708814", 1, 34.3741622, -119.4767872],
    "Pismo Beach Pier": ["https://www.surfline.com/surf-report/pismo-beach-pier/5842041f4e65fad6a77089ac", 1, 35.138287, -120.644732],
    "Morro Bay": ["https://www.surfline.com/surf-report/morro-bay/5842041f4e65fad6a770880a", 0, 35.3694, 120.8677],
    "Cayucos Pier": ["https://www.surfline.com/surf-report/cayucos-pier/5842041f4e65fad6a77089a2", 1, 35.4493, 120.9064],
    "Pleasure Point": ["https://www.surfline.com/surf-report/pleasure-point/5842041f4e65fad6a7708807", 2, 36.9635, 121.9649],
    "Steamer Lane": ["https://www.surfline.com/surf-report/steamer-lane/5842041f4e65fad6a7708805", 2, 36.9517, 122.0261],
    "Waddell Creek": ["https://www.surfline.com/surf-report/waddell-creek/5842041f4e65fad6a7708980", 1, 37.0963, -122.2782],
    "Ocean Beach": ["https://www.surfline.com/surf-report/north-ocean-beach/5d9b68deab58860001c7359e", 1, 37.7594, 122.5107],
    "Dead Mans": ["https://www.surfline.com/surf-report/fort-point/5842041f4e65fad6a770897a", 0, 37.8106, 122.4771]
}


def create(request):
    for name in beaches.keys():
        print(create_beach_api(name, beaches[name][0], beaches[name][1], beaches[name][2], beaches[name][3]))

def update(request):
    for name in beaches.keys():
        beach = Beach.objects.get(name = name)
        print(update_beach_api(beach.id, beach.surfline_url, beach.name, beach.latitude, beach.longitude, beach.beach_dir))
