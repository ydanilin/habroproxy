import requests

proxies = {
  'http': 'localhost:8080',
  'https': 'localhost:8080',
}

# r = requests.get('http://www.rgbagira.ru/', proxies=proxies)
# r = requests.get('http://www.rgbagira.ru/', proxies=proxies, data='huj-huj-huj!!!')
r = requests.get('https://habr.com/', proxies=proxies, verify='/tp/docs/G/Pitonizm/habroproxy/cert')
print(r.text)
