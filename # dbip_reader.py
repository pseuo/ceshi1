# dbip_reader.py - DB-IP查询模块
import dbip as dbip_reader
import ipaddress

# Initialize DB-IP readers
dbip_country_reader = dbip_reader.Reader('dbip-country-lite.mmdb')
dbip_city_reader = dbip_reader.Reader('dbip-city-lite.mmdb')
dbip_asn_reader = dbip_reader.Reader('dbip-asn-lite.mmdb')

def get_country(d):
    lang = ["zh-CN", "en"]
    for i in lang:
        if i in d['names']:
            return d['names'][i]
    return d['names']['en']

def get_addr(ip, mask):
    network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
    first_ip = network.network_address
    return f"{first_ip}/{mask}"

def de_duplicate(regions):
    regions = filter(bool, regions)
    ret = []
    [ret.append(i) for i in regions if i not in ret]
    return ret

def get_dbip_info(ip: str):
    try:
        ret = {"ip": ip}
        
        # Query DB-IP ASN
        asn_info = dbip_asn_reader.lookup(ip)
        if asn_info:
            as_ = {"number": asn_info.get("asn"), "name": asn_info.get("organization")}
            ret["as"] = as_

        # Query DB-IP City
        city_info = dbip_city_reader.lookup(ip)
        if city_info:
            ret["addr"] = get_addr(ip, city_info.get("prefix_length", 24))
            if "latitude" in city_info and "longitude" in city_info:
                ret["location"] = {
                    "latitude": city_info["latitude"],
                    "longitude": city_info["longitude"]
                }
            if "country" in city_info:
                country_code = city_info["country"]
                country_name = get_country({"names": {"en": country_code}})
                ret["country"] = {"code": country_code, "name": country_name}
            if "region" in city_info:
                regions = [city_info["region"]]
                if "city" in city_info:
                    regions.append(city_info["city"])
                regions = de_duplicate(regions)
                if regions:
                    ret["regions"] = regions

        # Query DB-IP Country
        country_info = dbip_country_reader.lookup(ip)
        if country_info:
            country_code = country_info["country"]
            country_name = get_country({"names": {"en": country_code}})
            ret["registered_country"] = {"code": country_code, "name": country_name}
        
        return ret
    except ValueError as e:
        return {"error": str(e)}
