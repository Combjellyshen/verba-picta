# Canva 抽象人物肖像 Skill

根据指定人物的对话或语料整理有依据的人物观察，研究指定或随机选择的艺术家，再通过 **computer use 操作浏览器中的 Canva 编辑器**，创作抽象人物肖像并交付图片及可编辑设计链接。

主要创作在 Canva 中完成，不使用 Canva MCP、Canva 连接器、REST API 或 Apps SDK，也不以代码绘画或外部生成的整张图片导入替代绘制。

## 技能入口

完整、可复制安装的技能目录是 [`canva-abstract-portrait/`](canva-abstract-portrait/)，入口为 [`SKILL.md`](canva-abstract-portrait/SKILL.md)。仓库根目录放置项目说明、依赖和测试。

```text
canva-abstract-portrait/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── artist-catalog.json
│   ├── visual-guides/          # 14 位艺术家的独立研究卡
│   ├── portrait-evidence.md
│   ├── canva-workflow.md
│   ├── resource-workflow.md
│   └── evaluation-cases.md
└── scripts/
    ├── select_artist.py
    ├── reference_assets.py
    └── verify_delivery.py
```

## 创作与证据

创作优先级为整体审美、艺术语言与绘画质感、人物表达、可编辑程度。证据真实性与完成状态必须如实呈现，不参与审美取舍。

- 大五人格、情境—反应、COM-B 和语言互动观察共用证据 ID，区分本人发言、他评、转述、引用、虚构及 AI 内容。
- 人物观察先于艺术研究固定，最多选三至四个有依据的特征或关系进入画面，允许更少；不使用固定人格配色或形状映射。
- 实际观看同一方向三至五幅参考作品，比较构图候选，在 Canva 中完成大形、轮廓、色层与编辑结构。
- 通过缩略图、正常尺寸及局部放大检查，确认保存、实际下载并打开导出文件后交付。

## 艺术家资源

资源覆盖原候选池的 14 位艺术家，包括康定斯基、毕加索、蒙德里安、马列维奇、克利、米罗、索尼娅·德劳内、罗斯科、波洛克、阿格尼丝·马丁、希尔玛·阿芙·克林特、赵无极、弗兰肯塔勒和克莱因。

v1.0.0 收录 **43 个时期或创作方向、109 条作品记录、107 个图像地址**。每位艺术家都有默认参考组和研究卡。部分备选方向需要在实际使用前补足参考；这些是创作研究分组，不是艺术生涯的完整分期或作品全集。

- [可浏览的艺术家与作品表](docs/artist-resources.md)
- [结构化资源库](canva-abstract-portrait/references/artist-catalog.json)
- [来源、状态与维护方法](canva-abstract-portrait/references/resource-workflow.md)

作品事实主要来自 MoMA 官方馆藏数据、博物馆及艺术家基金会。图像地址可能变化，元数据许可与图像使用条件分开记录。仓库保存资料记录和来源链接；运行时按需获取参考图，不内置下载的原作图像。

## 使用

将整个 `canva-abstract-portrait` 文件夹复制到当前宿主支持的技能目录，或让技能安装器从本仓库的该子目录安装。路径以你的宿主配置为准；代码根据自身文件位置读取资源，不依赖开发者机器的绝对路径。

需要：

- 支持读取技能文件和运行本地脚本的代理环境。
- Python 3.10+；图像解码、参考联系表与测试需要 Pillow。
- 全局可用的 computer use 浏览器控制能力，以及能够编辑设计的 Canva 登录状态。

在仓库根目录安装脚本依赖：

```shell
python -m pip install -r requirements.txt
```

调用示例：

```text
使用 canva-abstract-portrait。

目标人物：
对话或语料：
指定艺术家或排除名单（可选）：
颜色、质感或元素偏好（可选）：
画幅与用途（可选）：
肖像显性程度（可选）：
已有 Canva 链接（修改时提供）：
```

## 脚本与验证

从仓库根目录执行：

```shell
python canva-abstract-portrait/scripts/reference_assets.py validate
python -m unittest discover -s tests -v
python canva-abstract-portrait/scripts/select_artist.py --session work/portrait/session.json
python canva-abstract-portrait/scripts/reference_assets.py prepare --session work/portrait/session.json --out work/portrait/references.json
python canva-abstract-portrait/scripts/reference_assets.py fetch --manifest work/portrait/references.json --out-dir work/portrait/references
```

导出图片后检查：

```shell
python canva-abstract-portrait/scripts/verify_delivery.py --session work/portrait/session.json --image outputs/portrait/portrait.png --out outputs/portrait/delivery-check.json
```

`select_artist.py` 按艺术家等概率抽选并复用已有选择；`reference_assets.py` 管理资源、下载和缓存；`verify_delivery.py` 检查图像文件及必要记录，不声称能自动判定审美或证明 Canva 保存、图层可编辑。

初次建库时，默认组 46 张参考图中有 45 张下载并解码成功，一处补充来源返回 HTTP 429；另有两件备用作品尚无图像直链。这些状态记录在资料库中。实际创作时仍需重新访问和看图。

当前验证覆盖资源结构与 14 项脚本行为；没有将实际 Canva 绘画、保存和导出标记为已完成端到端验证。单次人物语料、下载缓存和导出成品放在 `work/`、`outputs/`，默认由 Git 忽略。

## 维护

以本仓库中的技能目录为源文件。修改资料时更新 `artist-catalog.json` 和对应研究卡，然后重新生成浏览表：

```shell
python canva-abstract-portrait/scripts/reference_assets.py table --out docs/artist-resources.md
```

运行相关测试后提交变更。安装到本机的副本按需同步；只有宿主配置了按需技能索引时，才使用该环境自己的刷新流程。
