<p align="center">
    <img src="https://img.shields.io/badge/NeoGram-Telegram_MTProto_Framework-blue?style=for-the-badge" alt="NeoGram Logo">
    <br>
    <b>A High-Performance, Asynchronous Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://codeberg.org/lucifers/NeoGram">Homepage</a>
    •
    <a href="https://codeberg.org/lucifers/NeoGram/docs">Documentation</a>
    •
    <a href="https://codeberg.org/lucifers/NeoGram/releases">Releases</a>
</p>


## 🚀 About NeoGram

**NeoGram** is an evolved, modern, and fully asynchronous Telegram MTProto API framework built with Python. Designed for both developers building powerful bots and users creating custom clients, NeoGram provides a seamless way to interact with Telegram's API.

NeoGram is a **fork of Pyrogram**, focusing on performance,stability, and new features.

```python
from pyrogram import Client, filters

app = Client("my_account")

@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from NeoGram!")

app.run()
```

## ✨ Key Features

  - 🚀 High Performance: Optimized for speed and efficiency, leveraging modern
    asynchronous patterns.
  - 🛠 User-Friendly: An intuitive API that simplifies complex MTProto
    interactions without sacrificing power.
  - 💎 Highly Abstracted: Low-level Telegram complexities are handled internally,
    allowing you to focus on your logic.
  - ⚡ Async-First: Built from the ground up to be fully asynchronous, ensuring
    non-blocking operations.
  - 📝 Type-Hinted: Comprehensive type hinting for a superior development
    experience in VS Code, PyCharm, and other IDEs.
  - 🔌 Powerful Access: Provides deep access to Telegram's core features for both
    Bot API and Userbot implementations.

## 📦 Installation

Install NeoGram via pip:
```
pip install neogram
```

Or:
```
pip install https://codeberg.org/lucifers/NeoGram.git
```

## 📚 Resources

  - Documentation: Visit our Docs
  - Issues & Discussions: Report bugs on Codeberg

## ⚖️ Disclaimer & Credits

NeoGram is a community-driven fork of Pyrogram.

  - We are not affiliated with, endorsed by, or associated with the official
    Pyrogram project or Telegram Messenger.
  - All original rights to the underlying Pyrogram code belong to its original
    authors.
  - This project is developed for research,educational,community, skills improvement, purposes.

Please support the original Pyrogram project if you find this framework useful.