本程序通过powershell调用yt-dlp.exe运行。需要下载独立的yt-dlp.exe，放在和YtDlpGuiPy.exe同一个文件夹下，才能使用。
如果您的IP地址被标记，您需要在浏览器中登录YouTube，安装Cookies Export浏览器扩展程序，复制YouTube的Cookies，将其转换为Netscape格式，然后粘贴到cookies.txt文件中。若无需Cookies，请从参数中移除--cookies “./cookies.txt”。
您可能需要安装Node.js以访问所有视频格式。
考虑到VPN节点与YouTube平台的负载情况，本程序设计为每次仅允许下载一个视频，禁止同时执行多个下载任务。
本程序可以自由灵活设定yt-dlp参数，自由设置分辨率，视频封装格式等。只需要在参数设置栏修改参数即可。
请谨慎删除ffmpeg文件夹。务必在yt-dlp.exe同一个目录下创建ffmpeg文件夹，里面放入ffmpeg三件套。

This program runs by invoking yt-dlp.exe via PowerShell. You must download the standalone yt-dlp.exe and place it in the same folder as YtDlpGuiPy.exe for it to function.
If your IP address is flagged, you need to log into YouTube in your browser, install the Cookies Export browser extension, copy YouTube's cookies, convert them to Netscape format, and then paste them into cookies.txt. If you don't need cookies, remove --cookies “./cookies.txt” from the parameters.
You may need to install Node.js to access all video formats.
Considering the load on VPN nodes and the YouTube platform, I designed the program to allow only one video download at a time, prohibiting multiple simultaneous download tasks.
This program allows flexible configuration of yt-dlp parameters, enabling customization of resolution, video container format, and more. Simply modify the parameters in the settings panel.
Please exercise caution when deleting the ffmpeg folder. Ensure that the ffmpeg folder is created in the same directory as yt-dlp.exe and contains the three essential ffmpeg components.
