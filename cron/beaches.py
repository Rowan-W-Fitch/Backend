from .webscrape import create_beach_api, update_beach_api
from apis.models import Beach
import requests
from rest_framework.response import Response

beaches = {
    "Imperial Beach Pier": ["https://www.surfline.com/surf-report/imperial-pier-northside/5842041f4e65fad6a7708847", 3, 33.1422015, -118.0627561],
    "Ocean Beach Pier": ["https://www.surfline.com/surf-report/ocean-beach-pier-/59aedf63b5e8310014bbe375", 0, 32.7443973, -117.2615996],
    "Ocean Beach Jetty": ["https://www.surfline.com/surf-report/ocean-beach/5842041f4e65fad6a770883f", 3, 32.7471113, -117.2636047],
    "Mission Beach": ["https://www.surfline.com/surf-report/mission-beach/5842041f4e65fad6a7708842", 3, 32.7879624, -117.2918774],
    "Pacific Beach Pier": ["https://www.surfline.com/surf-report/pacific-beach/5842041f4e65fad6a7708841", 3, 32.7962674, -117.2590454],
    "Windansea": ["https://www.surfline.com/surf-report/windansea/5842041f4e65fad6a770883c", 3, 32.8311579, -117.2899036],
    "Scripps Pier": ["https://www.surfline.com/surf-report/scripps-pier-northside/5d703b2ae4a3a8000133196a", 3, 32.8662843, -117.2568256],
    "Del Mar Beach": ["https://www.surfline.com/surf-report/del-mar/5d7687fdb4c559000112e666", 3, 32.9595213, -117.2685396],
    "Del Mar Rivermouth": ["https://www.surfline.com/surf-report/del-mar-rivermouth/5842041f4e65fad6a77088b0", 3, 32.9712155, -117.2673769],
    "Seaside Reef": ["https://www.surfline.com/surf-report/seaside-reef/5842041f4e65fad6a77088b3", 3, 33.0007203, -117.2784916],
    "Cardiff Reef": ["https://www.surfline.com/surf-report/cardiff-reef-south/584204214e65fad6a7709d19", 3, 33.0062688, -117.2971396],
    "Swamis": ["https://www.surfline.com/surf-report/swami-s/5842041f4e65fad6a77088b4", 3, 33.0356447, -117.2954494],
    "Tamarack": ["https://www.surfline.com/surf-report/tamarack/5842041f4e65fad6a7708837", 3, 33.1439698,-117.3482225],
    "Carlsbad State Beach": ["https://www.surfline.com/surf-report/carlsbad-state-beach-north/5d4dc10680c2430001b119fb", 3, 33.1504987,-117.3524959],
    "Blacks": ["https://www.surfline.com/surf-report/blacks/5842041f4e65fad6a770883b", 3, 32.8907, -117.2535],
    "Oceanside Pier": ["https://www.surfline.com/surf-report/oceanside-pier-northside/5842041f4e65fad6a7708835", 3, 33.1934, -117.3860],
    "Lowers": ["https://www.surfline.com/surf-report/lower-trestles/5842041f4e65fad6a770888a", 2, 33.3853, -117.5939],
    "Uppers": ["https://www.surfline.com/surf-report/upper-trestles/5842041f4e65fad6a7708887", 2, 33.3853155, -117.5975894],
    "T Street": ["https://www.surfline.com/surf-report/t-street/5842041f4e65fad6a7708830", 3, 33.4163673, -117.6264938],
    "San Clemente Pier": ["https://www.surfline.com/surf-report/san-clemente-pier-northside/5cc8b55739a02e0001ac69f8", 3, 33.4190257, -117.6233728],
    "Doheny": ["https://www.surfline.com/surf-report/doheny-state-beach/5842041f4e65fad6a77088d7", 0, 33.4610133, -117.686342],
    "Salt Creek": ["https://www.surfline.com/surf-report/salt-creek-overview/584204204e65fad6a770938b", 3, 33.4760643, -117.7250302],
    "The Wedge": ["https://www.surfline.com/surf-report/the-wedge/5842041f4e65fad6a770882b", 0, 33.5928523, -117.8897922],
    "Newport Jetties": ["https://www.surfline.com/surf-report/newport-jetties/5842041f4e65fad6a77088f6", 0, 33.620926, -117.9442217],
    "56th St": ["https://www.surfline.com/surf-report/56th-street-close-up/5a26e1ba9caa98001b09d0e7", 2, 33.6229, -117.9467],
    "Huntington State Beach": ["https://www.surfline.com/surf-report/huntington-state-beach/584204204e65fad6a770998c", 3, 33.6380444, -117.9758009],
    "Huntington Beach Pier": ["https://www.surfline.com/surf-report/hb-pier-northside/5842041f4e65fad6a7708827", 2, 33.654907, -118.004375],
    "HB 17th St": ["https://www.surfline.com/surf-report/17th-st-/5842041f4e65fad6a77088eb", 3, 33.664079, -118.0150748],
    "Goldenwest": ["https://www.surfline.com/surf-report/goldenwest/5842041f4e65fad6a77088ea", 3, 33.668239, -118.0203707],
    "Bolsa Chica": ["https://www.surfline.com/surf-report/bolsa-chica-state-beach-n-/58bdee240cec4200133464f1", 3, 33.6972793, -118.0683508],
    "Lunada Bay": ["https://www.surfline.com/surf-report/lunada-bay/5842041f4e65fad6a770892c", 0, 33.771444, -118.4244907],
    "Haggertys": ["https://www.surfline.com/surf-report/haggerty-s/5842041f4e65fad6a7708920", 0, 33.777012, -118.4274737],
    "Hermosa Beach Pier": ["https://www.surfline.com/surf-report/hermosa-pier-southside/5b17293b9f631f001a010d54", 3, 33.8612058, -118.4077313],
    "Hermosa Beach": ["https://www.surfline.com/surf-report/hermosa-beach/5842041f4e65fad6a7708904", 3, 33.8646935, -118.4149244],
    "Manhattan Beach Pier": ["https://www.surfline.com/surf-report/manhattan-pier-northside/5acd24954031e5001a13854a", 3, 33.8894932, -118.4186522],
    "El Porto": ["https://www.surfline.com/surf-report/el-porto/5842041f4e65fad6a7708906", 3, 33.9038, -118.4192],
    "Topanga": ["https://www.surfline.com/surf-report/topanga-beach/5842041f4e65fad6a770881e", 2, 34.0385874, -118.5910254],
    "Malibu": ["https://www.surfline.com/surf-report/malibu-second-to-third-point/5842041f4e65fad6a7708817", 2, 34.0363, -118.6779],
    "Point Dume": ["https://www.surfline.com/surf-report/point-dume/5842041f4e65fad6a7708936", 2, 34.001201, -118.8086307],
    "Zuma": ["https://www.surfline.com/surf-report/zuma-beach-north/5b156d394a274e001a11fb62", 2, 34.0218023, -118.8486992],
    "Leo Carillo": ["https://www.surfline.com/surf-report/leo-carrillo/5842041f4e65fad6a770893f", 2, 34.0440831, -118.947005],
    "County Line": ["https://www.surfline.com/surf-report/county-line/5842041f4e65fad6a7708813", 2, 34.0514, -118.9600],
    "Ventura Harbor": ["https://www.surfline.com/surf-report/ventura-harbor/5842041f4e65fad6a7708811", 3, 34.245624, -119.263642],
    "Ventura Point": ["https://www.surfline.com/surf-report/ventura-point/584204204e65fad6a77096b1", 3, 34.2743, -119.2992],
    "Faria": ["https://www.surfline.com/surf-report/pitas-point/5842041f4e65fad6a7708957", 3, 34.324963, -119.395704],
    "Rincon": ["https://www.surfline.com/surf-report/rincon/5842041f4e65fad6a7708814", 3, 34.3741622, -119.4767872],
    "Pismo Beach Pier": ["https://www.surfline.com/surf-report/pismo-beach-pier/5842041f4e65fad6a77089ac", 3, 35.138287, -120.644732],
    "Morro Bay": ["https://www.surfline.com/surf-report/morro-bay/5842041f4e65fad6a770880a", 0, 35.3694, -120.8677],
    "Cayucos Pier": ["https://www.surfline.com/surf-report/cayucos-pier/5842041f4e65fad6a77089a2", 3, 35.4493, -120.9064],
    "Pleasure Point": ["https://www.surfline.com/surf-report/pleasure-point/5842041f4e65fad6a7708807", 2, 36.9635, -121.9649],
    "Steamer Lane": ["https://www.surfline.com/surf-report/steamer-lane/5842041f4e65fad6a7708805", 2, 36.9517, -122.0261],
    "Waddell Creek": ["https://www.surfline.com/surf-report/waddell-creek/5842041f4e65fad6a7708980", 3, 37.0963, -122.2782],
    "Ocean Beach": ["https://www.surfline.com/surf-report/north-ocean-beach/5d9b68deab58860001c7359e", 3, 37.7594, -122.5107],
    "Dead Mans": ["https://www.surfline.com/surf-report/fort-point/5842041f4e65fad6a770897a", 0, 37.8106, -122.4771]
}


def create(request):
    for name in beaches.keys():
        print(name)
        create_beach_api(name, beaches[name][0], beaches[name][1], beaches[name][2], beaches[name][3])
    return Response({
    "good": "yes"
    })


# def update():
#     for name in beaches.keys():
#         beach = Beach.objects.get(name = name)
#         print(beach.name)
#         res = update_beach_api(beach.id, beach.surfline_url, beach.name, beach.latitude, beach.longitude, beach.beach_dir)
#         print(res)
#
#
# update()
