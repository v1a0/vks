<div align="center">
	<div>
		<img width="200" src=".pic/vks-200.png" alt="VKS logo" style="position: relative; float: left; width: 200px; margin-right: 40px; margin-bottom: 90px; margin-top: 13px; pointer-events: none">
	</div>
<br>

# VKS v 0.2.2 ![Python:3.9](https://img.shields.io/badge/Python-3.9-yellow) 
Program for monitor <b>your own</b> online activity on [vk.com]

</div><br>

# About

### Features:
- [x] 📈 Recording online activity
- [x] 🎯 Multiple targets support
- [x] 🌐 Proxy support

### Coming soon
> - [ ] 📊 Live time visualizing data
> - [ ] 📑 Scrapping profile info
> - [ ] 👪 Multiple tokens support
> - [ ] 🎱 Predicting activity
> - [x] ~~🔀 Random proxy (sslproxies.org)~~ (Banhammered)



# How to run

First of all, set your settings in file `settings.py`:
1. API_TOKEN = Your VK API token
2. TARGETS = list of targets ids

Optional
1. PROXY = Custom proxy settings

<details><summary>Example sets</summary>

```pythons
API_TOKEN = '000fuck0fvk000i8oppkq22so2c7binpysm5lpwxl3uliibir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000'

TARGETS = [
    '123456789', '987654321', '121201'
]

# Optional
PROXY = {
    "http": "http://123.45.6.78:4321",
    "https": "https://123.45.6.78:4321",
    "ftp": ""
}
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