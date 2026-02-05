本程序通过powershell调用yt-dlp.exe运行。需要下载独立的yt-dlp.exe，放在和YtDlpGuiPy.exe同一个文件夹下，才能使用。
如果您的IP地址被标记，您需要在浏览器中登录YouTube，安装Cookies Export浏览器扩展程序，复制YouTube的Cookies，将其转换为Netscape格式，然后粘贴到cookies.txt文件中。若无需Cookies，请从参数中移除--cookies “./cookies.txt”。
您可能需要安装Node.js以访问所有视频格式。
考虑到VPN节点与YouTube平台的负载情况，本程序设计为每次仅允许下载一个视频，禁止同时执行多个下载任务。
本程序可以自由灵活设定yt-dlp参数，自由设置分辨率，视频封装格式等。只需要在参数设置栏修改参数即可。
