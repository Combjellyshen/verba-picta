# 资源结构、脚本与维护

## 资料范围与来源

版本 1.0.0 覆盖原候选池全部 14 位艺术家。`artist-catalog.json` 是唯一结构化资料源，记录工作用的时期／方向、默认作品组和备选研究入口；不是任何画家的作品全集。`visual-guides/` 是按艺术家加载的制作研究卡。生成的表格只用于浏览，修改资料时更新 JSON 与受影响的卡片，不反向手改生成表格。

首批记录整理于 2026-09-06。主要来源：

- [MoMA 官方馆藏数据](https://github.com/MuseumofModernArt/collection)：使用实际取得的 Artworks.csv 中作品 ID、标题、年代、媒介、尺寸、作品页和 ImageURL；元数据 CC0 不等于图像也可无条件复用。没有把整个数据集塞进技能。
- [蓬皮杜艺术家与馆藏记录](https://www.centrepompidou.fr/fr/ressources/personne/cX44X8E)：索尼娅·德劳内的作品事实；图像不能取得时明确留空，不能拿页面横幅代替画作。
- [提森博物馆的《同时性对比》](https://www.museothyssen.org/coleccion/artistas/delaunay-sonia/contrastes-simultaneos)：作品信息及页面中明确标注的完整图像。索尼娅《电棱镜》的补充研究预览来自 Wikimedia，作品身份仍以蓬皮杜记录为准；不把档案站的许可标签自动当作馆方确认。
- [Hilma af Klint Foundation](https://hilmaafklint.se/selected-works/)：按官方相册标题、HaK 编号和图像链接对应。未注明的组内序号不猜。
- [古根海姆教师资源 PDF](https://www.guggenheim.org/wp-content/uploads/2018/10/guggenheim-education-hilma-af-klint-teacher-resource-unit-10-5.pdf)：希尔玛的作品与系列背景；《十大》第 2、9 幅图像在 PDF 第 11 页（零基页 10）。教育资料的图片使用范围见原文件。
- [赵无极基金会油画档案](https://www.zaowouki.org/fr/artiste/oeuvres/peintures-a-l-huile/)：按标题、图注和相邻原图核对；法文标注的馆藏／存放信息按来源保存，不声称做了当前借展位置调查。
- [Helen Frankenthaler Foundation](https://www.frankenthalerfoundation.org/artworks/paintings)：作品详情及明确的作品图像；区分油彩浸染与后期丙烯。
- [Tate 的《十大》第 9 幅资料](https://shop.tate.org.uk/hilma-af-klint-the-ten-largest-group-iv-no.-9-old-age/afklin2311.html)：官方复制品页面作为补充图像来源，标记其预览尺寸及可能的印刷留边；近看可转用博物馆 PDF，不将商品展示图冒充原作细节。

作品身份与来源已根据上述记录整理。资料卡的构图、边缘和 Canva 方法属于创作建议；每次实际使用必须看图确认，不把建库时间写成看图完成时间。

## 字段约定

`artists[]` 包含稳定 ID、名字、别名、默认方向、卡片路径和研究来源。`directions[]` 包含 ID、研究分组名、时间范围、作品 ID 与 `reference_set_ready`。该标志只表示已配三至五条作品记录，不保证网络永远可用，也不表示每幅已经看过。跨时间的备选方向应根据主参考进一步收窄。

`artworks[]` 分别记录：作品身份、来源、媒介尺寸、方向归属、明确的图像地址及其提取依据、图片状态、研究提示。`metadata_checked_at` 与图片下载时间分开，`viewing_status` 默认未看。没有可靠图片地址时 `image.url=null`，由浏览器打开作品页或补充同方向来源；不抓搜索缩略图或猜 URL。

`collection_url` 用于核实与引用；`image.url` 用于获取图片，二者不互换。单次缓存保存于任务 work 目录，始终关联作品 ID。局部裁切／重着色／拼贴的操作和保留用途另外记录。用于参考学习与用于成品拼贴的素材需求不同，实际复制使用时查看来源说明；不预先禁止整个艺术家或自动改变抽选概率。

## 三个脚本

### select_artist.py

使用 Python 标准库。支持中英文、常用译名和 ID；未知名字报错，不静默忽略排除项。默认系统随机源，在有效艺术家列表上等概率选择。已有 session 的选择直接复用，不改时间戳。冲突、全部排除或错误记录返回非零。

`--redraw` 仅供用户明确要求重新选择时使用，保存旧选择历史，归档并清除过期方向／参考／视觉检查，保留人物证据及原设计链接；旧保存与可编辑检查状态失效，须重新观察。执行者需检查既有画作与新选择的关系。`--seed` 是明确的可复现或测试模式。

### reference_assets.py

```text
python <skill>/scripts/reference_assets.py validate
python <skill>/scripts/reference_assets.py list --artist 克利
python <skill>/scripts/reference_assets.py table --out outputs/artist-resources.md
python <skill>/scripts/reference_assets.py prepare --session work/portrait/session.json --out work/portrait/references.json
python <skill>/scripts/reference_assets.py prepare --session work/portrait/session.json --direction <id> --works <id1> <id2> <id3> --out work/portrait/references.json --replace
python <skill>/scripts/reference_assets.py fetch --manifest work/portrait/references.json --out-dir work/portrait/references --contact-sheet work/portrait/reference-sheet.png
```

`validate` 检查 ID、别名冲突、卡片、方向归属、作品数、来源与 URL 结构，不代表在线图像已验证。`prepare` 默认复用匹配的清单，保留看图注记；只有有意更改方向／参考时用 `--replace`。

`fetch` 仅访问记录中明确的公开 HTTPS 图像，不使用 Canva 接口，不读取登录 cookie。设置超时、文件大小限制，逐图下载并解码；缓存匹配时复用，`--refresh` 才重取。AIC 图像按馆方建议串行间隔，其余也串行处理。失败逐项返回，已成功的文件保留。下载后不会把 `visually_inspected` 标为真。

联系表只拼排已下载的参考图，保留原比例，以作品 ID 标注；它是研究辅助，不作为成品，不替代单幅放大观察。默认源图可能仅约 1024 px，下载成功不等于足以研究所有肌理。

### verify_delivery.py

依赖 Pillow。检查实际 PNG／JPEG 可解码、像素长边（默认至少 2000）、与记录画布比例一致、Canva 链接结构及人工观察记录是否齐备。`--min-long-edge` 可按用户用途修改；不能通过把低分辨率截图放大来通过质量检查。

返回 0 表示机械检查通过且人工记录字段齐全；不意味着脚本独立证实了这些记录。返回 2 表示错误，3 表示缺少人工记录；报告明确列出缺项。不自动声称保存、权限、图层可编辑或审美合格。PDF 为额外交付时须另行实际打开观察，本脚本负责清晰图片。

所有 JSON 使用 UTF-8。Windows 终端有非 ASCII 输出问题时用 `python -X utf8`。脚本输出目录由调用者传入；不要把单次人物资料写回技能目录。

## 更新

修改本地 JSON／卡片后提升 metadata.version 与 catalog.version，记录新的核验日期。图像失效时先查原作品页，再查博物馆／基金会／可靠档案；保留来源变化，不用相似图填缺。补作品后重新运行 validate、受影响脚本的实质测试和技能校验。

以仓库内的技能目录为维护源文件，安装副本按需同步。宿主若配置了按需技能索引，安装、更新或移除后运行该环境自己的刷新流程；本技能不依赖特定用户目录或索引脚本路径。

来源名字、版本与更新方式在 SKILL.md 和本文件中保留；不另加无用途的模板、安装包或大量图片副本。
