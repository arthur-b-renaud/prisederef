import requests

cookies = {
    'hubspotutk': '3d567d174dae6527a714937dedacfc5d',
    '_ga': 'GA1.1.1677902406.1758553647',
    'FPID': 'FPID2.2.GeqFlUrgA0vixEd6wCd9DSAr2a3ywNm6yzvB9t81bTc%3D.1758553647',
    'FPAU': '1.2.1548351640.1758553647',
    'PHPSESSID': 'asl58et2tdjabls9ibuhha3r3rkp8h6n9p4ouaukkd89ak72ve5pdhdea7jqvaujpfkvprtt0f00re88lq6gsas4ggavtkm8evsg39c',
    '_plantrack': '%257B%2522id%2522%253A%25223500%257C62517%2522%252C%2522email%2522%253A%2522arthur.renaud%2540exalt-company.com%2522%252C%2522name%2522%253A%2522Arthur%2520RENAUD%2522%252C%2522companyExternalId%2522%253A%25223500%2522%257D',
    'intercom-device-id-dszr4kgs': 'f7764805-ffad-42d1-bf53-2141becdab7d',
    '__hstc': '58959922.3d567d174dae6527a714937dedacfc5d.1758553646427.1758707398056.1758877548043.3',
    '_ga_9D4BG4TLWK': 'GS2.1.s1758877547$o4$g1$t1758878309$j60$l0$h663262282',
    'intercom-session-dszr4kgs': 'Q2NJSC9rZmx3Um95cHloS2VFNTdqc2RrTmVpTWxDSHBDbko5ZW5FbitIREhjb0VjaTl5M2VpWXJPNWc1SFAvelJZeWxMYUlYU0lvc2o2M2ZPa0ZPdURoTFVubm8yaDgwcVhBbGJmVGNoSzQ9LS1zWHVyNE5oZXErbSsvM0ZvS1gvRDFRPT0=--2d219b5e5f98bf5adf15389df14c0dfe82df4c81',
}

headers = {
    'accept': 'application/vnd.api+json',
    'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://ui.boondmanager.com/candidates?candidateStates=%5B15%2C1%5D&order=asc&perimeterAgencies=%5B%2212%22%5D&perimeterBusinessUnits=%5B%2212%22%5D&saveSearch=true',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-286de6cc63ebc4472d0e64c43256e910-9af4a9c07fb90950-01',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
    'x-csrf-boondmanager': 'PbcKtjgFxtM2HaWBh6tMZq4VPC8oDXyI/cMgMX+hFMw=',
    'x-front-boondmanager': 'ember',
    'x-front-version': '9.0.4.1',
    # 'cookie': 'hubspotutk=3d567d174dae6527a714937dedacfc5d; _ga=GA1.1.1677902406.1758553647; FPID=FPID2.2.GeqFlUrgA0vixEd6wCd9DSAr2a3ywNm6yzvB9t81bTc%3D.1758553647; FPAU=1.2.1548351640.1758553647; PHPSESSID=asl58et2tdjabls9ibuhha3r3rkp8h6n9p4ouaukkd89ak72ve5pdhdea7jqvaujpfkvprtt0f00re88lq6gsas4ggavtkm8evsg39c; _plantrack=%257B%2522id%2522%253A%25223500%257C62517%2522%252C%2522email%2522%253A%2522arthur.renaud%2540exalt-company.com%2522%252C%2522name%2522%253A%2522Arthur%2520RENAUD%2522%252C%2522companyExternalId%2522%253A%25223500%2522%257D; intercom-device-id-dszr4kgs=f7764805-ffad-42d1-bf53-2141becdab7d; __hstc=58959922.3d567d174dae6527a714937dedacfc5d.1758553646427.1758707398056.1758877548043.3; _ga_9D4BG4TLWK=GS2.1.s1758877547$o4$g1$t1758878309$j60$l0$h663262282; intercom-session-dszr4kgs=Q2NJSC9rZmx3Um95cHloS2VFNTdqc2RrTmVpTWxDSHBDbko5ZW5FbitIREhjb0VjaTl5M2VpWXJPNWc1SFAvelJZeWxMYUlYU0lvc2o2M2ZPa0ZPdURoTFVubm8yaDgwcVhBbGJmVGNoSzQ9LS1zWHVyNE5oZXErbSsvM0ZvS1gvRDFRPT0=--2d219b5e5f98bf5adf15389df14c0dfe82df4c81',
}

params = {
    'candidateStates': '15,1',
    'maxResults': '30',
    'order': 'asc',
    'page': '1',
    'perimeterAgencies': '12',
    'perimeterBusinessUnits': '12',
    'saveSearch': 'true',
    'viewMode': 'list',
}

response = requests.get('https://ui.boondmanager.com/api/candidates', params=params, cookies=cookies, headers=headers)
print(response.json())

import json
with open('/tmp/candidates.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)
