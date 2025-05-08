# 🎵 NCMusicApi
🚀 高性能异步网易云音乐 Python API，基于FastApi & AioHttp 实现

## 🌐 在线Demo
[在线Demo >>> https://ncmapi.rlmk.cc](https://ncmapi.rlmk.cc)

请勿对公开 Demo 地址发起压测谢谢!

## ✨ 特点
- ⚡ **异步高性能** : 基于FastApi & AioHttp 实现
- 📦 **接口丰富** : 预计最终接口**150左右**接近原生网易云
- 🛠️ **简洁部署** : 即开即用，适合本地和服务器部署
- 🎧 **常用支持** : 支持常见音乐信息获取，如歌曲、专辑、歌词、评论等

## 📥 使用
### 1. 克隆项目
```bash
git clone https://github.com/XiaoMaoR/NCMusicApi.git
cd NCMusicApi
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动服务
```bash
# Python
python main.py
# Windows
.\start.bat
# Linux / MacOS
chmod +x start.sh
./start.sh
```

## 🧪 常用接口示例
| 接口功能|请求路径示例|
|------------------|---------------------------------------------------------------|
| 获取歌曲播放地址| `/api/song.url.v1?id=歌曲ID&level=音质`|
| 获取歌曲歌词信息| `/api/song.lyric.v1?id=歌曲ID`|
| 获取登录二维码密钥| `/api/login.qr.key`|
| 获取主页信息| `/api/home.page`|
| 搜索歌曲| `/api/search.main?keywords=搜索内容&type=song`|
| 更多接口| `/api/{Api名称}`|

参考   [在线Demo >>> https://ncmapi.rlmk.cc](https://ncmapi.rlmk.cc)

## 📌 使用注意
- 🚫 **请勿对公开 Demo 地址发起压测谢谢!**
- 📚 本项目仅供学习和技术研究，如有侵权请联系删除
- 🌍 可部署至公网，但建议配合鉴权或请求频率限制使用

## 🛠️ 开发计划（TODO）
- [x] 基础接口支持
- [x] 登录支持
- [x] 智能缓存
- [ ] 完整接口支持
- [ ] 接口结构优化
- [ ] 完整文档

## ❤️ 鸣谢
- 🎧 网易云音乐官方 Web 接口
- 🧠 Binaryify/NeteaseCloudMusicApi 提供的接口文档参考
- 🛠️ 其他开源项目和Python社区库

## 📄 License
[GNU General Public License v3.0](https://github.com/XiaoMaoR/NCMusicApi/blob/main/LICENSE)

## 🌟 支持我
**如果你觉得这个项目对你有帮助，可以点个 ⭐ Star 鼓励一下！**

- 📮 我的邮箱 xm@prx.mom
- 🐧 我的QQ 1072755450