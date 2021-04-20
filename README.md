# docker-telegrambot-yourls
Docker Telegram Bot for YOURLS URL-Shortening


You need a Telegram Bottoken, available at the [@BotFather](https://t.me/BotFather), the YOURLS Server and API Secretkey


| Variable      | Description                                                                     | Example Value                                  | Optional |
|---------------|---------------------------------------------------------------------------------|------------------------------------------------|----------|
| TELEGRAM_API  | Bottoken from [@BotFather](https://t.me/BotFather)                              | 1628160035:AAFgCrFB4nsF41qfzvZXlndilM5-I7XPEe8 | no       |
| YOURLS_SECRET | Secret Token from YOURLS Installation                                           | 1337asdf                                       | no       |
| YOURLS_DOMAIN | Domain behind YOURLS Installation                                               | tue.sk                                         | no       |
| ADMIN_LIST    | List for authorized Users allowed to use /short.<br/>Requires Telegram User-IDs | 227985688, 886589722                           | yes      |

If the Image is run without ADMIN_LIST all Users are allowed to run the /short command
<br/><br/>
### Run the image without User restriction:
```
docker run -e \
TELEGRAM_API='1628160035:AAFgCrFB4nsF41qfzvZXlndilM5-I7XPEe8' \
YOURLS_SECRET='1337asdf' \
YOURLS_DOMAIN='tue.sk' \
--name telegrambot \
tueska/telegrambot-yourls
```

### Run the image with restriction:
```
docker run -e \
TELEGRAM_API='1628160035:AAFgCrFB4nsF41qfzvZXlndilM5-I7XPEe8' \
YOURLS_SECRET='1337asdf' \
YOURLS_DOMAIN='tue.sk' \
ADMIN_LIST='227985688, 886589722' \
--name telegrambot \
tueska/telegrambot-yourls
```