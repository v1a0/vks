<div align="center">
	<div>
		<img width="200" src=".pic/vks-200.png" alt="VKS logo" style="position: relative; float: left; width: 200px; margin-right: 40px; margin-bottom: 90px; margin-top: 13px; pointer-events: none">
	</div>
<br>

# VKS v 0.2 ![Python:3.7](https://img.shields.io/badge/Python-3.7-yellow) [![stability-unstable](https://img.shields.io/badge/stability-unstable-yellow.svg)](https://github.com/emersion/stability-badges#unstable) [![License:MIT](https://img.shields.io/badge/license-MIT-green)](https://img.shields.io/github/license/V1A0/VkScrapper)
Program for monitor <b>your own</b> online activity on [vk.com]

</div><br>

# About

### Features:
- [x] 📈 Recording online activity
- [x] 🎯 Multiple targets support

### Coming soon
> - [ ] 📊 Live time visualizing data
> - [ ] 🌐 Proxy support
> - [ ] 🕵🏼 Secure mode
> - [ ] 🔀 Random proxy (sslproxies.org)
> - [ ] 🎲 Random headers (773 headers)
> - [ ] 📑 Scrapping profile info
> - [ ] ❌ Get new proxy if previous failed
> - [ ] 👪 Multiple tokens support
> - [ ] 🎱 Predicting activity


# How to run

First of all, set your settings in file `settings.py`:
1. API_TOKEN - Your VK API token
2. TARGETS = list of targets ids

<details><summary>Example sets</summary>

```python
API_TOKEN = '000fuck0vk000i8oppkq22so2c7binpyysm5lpwxl3uliibir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000'

TARGETS = [
    '123456789', '987654321', '121201'
]
```
</details>

And just run your main script `python3.8 main.py`.


# How to get API_TOKEN

Go to
`https://vk.com/editapp?act=create`

Create "Standalone app" and copy apps ID
Replace "__APPs_ID__" in the link below to your app IP
`https://oauth.vk.com/authorize?client_id=___APPs_ID___&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`


<details><summary>[Example]</summary>

`https://oauth.vk.com/authorize?client_id=1234567&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`

</details>
<br>


After you visit this link you'll be automatically redirected to new link
it will be looks like:

`https://oauth.vk.com/blank.html#access_token=___YOUR_API_TOKEN____&expires_in=0&user_id=1&email=durov@t.me`
__YOUR_API_TOKEN__ it is you API_TOKEN


<details><summary>[Example]</summary>

`https://oauth.vk.com/authorize?client_id=000fuck0vk000i8oppkq22so2c7binpyysm5lpwxl3uliibir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000&scope=photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications&response_type=token`

</details>

---
Official instruction:
https://vk.com/dev/access_token



[vk.com]: (https://vk.com/)