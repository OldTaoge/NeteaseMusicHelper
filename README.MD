# 网易云音乐助手

# 功能

- 云音乐日推保存
- 歌单下载(自动转码|音乐信息写入|封面)
- 自定义保存格式
- Docker运行 [DockerHub](https://hub.docker.com/repository/docker/oldtaoge/netease_music_helper)

# 依赖

- [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)

# 配置

#### 所有配置均在`data.json`中

1. 配置`API`:位置`api.prefix`
   
2. 配置登录信息: 支持以下登录方式

    - cookies
        1. 提取`MUSIC_U`和`NMTID`
        2. 写入配置文件`user.loginCookies.MUSIC_U`和`user.loginCookies.NMTID`或设置环境变量`NEM_MUSIC_U`和`NEM_NMTID`
    - password
        1. 计算出密码的md5
        2. 填入配置文件`user.loginInfo.phone`或者`user.loginInfo.email`和`user.loginInfo.md5_pass`
3. 配置任务: 写在`NEM_Autorun.Autorun`
## 命名模板

### 通用占位符

	`%seg`: 目录分隔符,用于建立多层文件夹
	`%trackName`: 音乐名(不带后缀名)
	`%artistName`: 艺术家名
	`%suffix`: 后缀名(带`.`)
	`%playlistName`: 歌单名

### 下载命名模板

- `config.nameTemplate.favouriteMusic`
  下载`我喜欢的音乐`时的命名格式
	  举个例子:```Fav%seg%trackName - %artistName%suffix```

- `config.nameTemplate.radar`

    下载`私人雷达`时命名格式

      举个例子:```Radar%seg%playlistName%seg%trackName - %artistName%suffix```

- `config.nameTemplate.playList`

    下载`普通歌单`时的命名格式

    举个例子:```%playlistName%seg%trackName - %artistName%suffix```

- `config.nameTemplate.recommend`
  
    下载`日推`时的命名格式
    
	举个例子:```Recommend%seg%playlistName%seg%trackName - %artistName%suffix```
	
- `config.nameTemplate.convertedPath`

    **仅适用以下通配符**

    - `%seg`: 目录分隔符,用于建立多层文件夹
    - `%sourcePath`: 转码前保存的目录和文件名

    `Cov%seg%sourcePath`

### 日推|雷达保存歌单命名模板

- `config.dailyNameTemplate.recommend`

    日推命名歌单规则,通配符同`time.strftime`

- `config.dailyNameTemplate.radar`

    私人雷达命名歌单规则,通配符同`time.strftime`

### 下载位置

- 见`config.download.path`