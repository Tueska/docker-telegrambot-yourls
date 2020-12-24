# docker-telegrambot-yourls
Docker Telegram Bot for YOURLS URL-Shortening

<p>
You need a Telegram Bottoken, available at the <a href="https://t.me/BotFather">BotFather</a>, the YOURLS Server and API Secretkey<br/><br/>
Environment Variables are:
<li>TELEGRAM_API - Bottoken</li>
<li>YOURLS_SECRET - Found in Adminpanel under Tools</li>
<li>YOURLS_DOMAIN - Only the domain, without https://</li>
</p>

Run the image:<br/>
<code>docker run -e TELEGRAM_API='your_bottoken' YOURLS_SECRET='yourls_secret_key' YOURLS_DOMAIN='domain' tueska/telegrambot-yourls</code> 
