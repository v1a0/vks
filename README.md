<div align="center">
	<div>
		<img width="200" src=".pic/vks-200.png" alt="VKS logo" style="position: relative; float: left; width: 200px; margin-right: 40px; margin-bottom: 90px; margin-top: 13px; pointer-events: none">
	</div>
<br>

# VKS v 0.2.4 ![Python:3.9](https://img.shields.io/badge/Python-3.9-green)  
Program for monitor <b>your own</b> online activity on [vk.com]

</div><br>

# About

### Features:
- [x] 📈 Recording online activity (module.onliner)
- [x] 📑 Particularly profile data scrapping (module.onliner)
- [x] 🎯 Multiple targets support
- [x] 👪 Multiple API tokens support
- [x] 🌐 Proxy support
    - [x] Common proxy settings
    - [x] Personal proxy settings (for different API tokens)
- [x] ⚙️ Custom modules
    - [x] Modules exceptions
    - [x] On/Off modules
    - [x] Any delay for any module
- [x] ~~🔀 Random proxy (sslproxies.org)~~ (Banhammered)

### Coming soon
> - [ ] 📊 Live time visualizing data
> - [ ] 📑 Scrapping profile info
> - [ ] 🎱 Predicting activity



# How to run

First of all, set your settings in file `settings.py`:
1) API_TOKENS = list of your VK API tokens
2) TARGETS_IDS = list of targets ids

Optional
1) PROXY = Custom proxy settings

<details><summary> < Example > </summary>

```python
# Main settings

API_TOKENS = [
    '000fuck0fvk000i8oppkq22so2c7binpysm5lpwxlfoxcbbir7kcr2ir8g0rgbu7lv4mo0000use0tlgrm000',
]

TARGETS_IDS = [
   '123456789', '987654321', '121201',
]



# Optional settings

MODULES = [
    modules.onliner,
    modules.my_module
]

MODULES_EXCEPTS = {
    MODULES[1]: [
        TARGETS_IDS[0], 
        TARGETS_IDS[2]
    ]
}

PROXY = {
    "http": "http://123.45.6.78:4321",
    "https": "https://123.45.6.78:4321",
    "ftp": ""
}

PROXY_FOR_BOT = {
    API_TOKENS[0]: {
        "http": "http://123.45.6.78:4321",
        "https": "https://123.45.6.78:4321",
        "ftp": ""
    }
}

REQ_FREQUENCY = 0.1
```

More details about new settings I'll add soon
</details>

And just run your main script `python3.9 main.py`.


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