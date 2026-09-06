# 资源结构、脚本与维护

## 资料范围与来源

版本 2.0.0 保留候选池全部 14 位艺术家的代表性谱系，制作指南与交付约定迁移为 Photopea 分层绘画。`artist-catalog.json` 作为统一的结构化核心资产库，收录工作期／风格方向、默认作品组与备选研究路径。`visual-guides/` 存放按艺术家独立加载的创作指南。衍生展示表格供阅读概览，资料维护在 JSON 与对应卡片中更新。

首批记录整理于 2026-09-06。主要来源：

- [MoMA 官方馆藏数据](https://github.com/MuseumofModernArt/collection)：使用经由官方发布的 Artworks.csv 提取的作品 ID、标题、年代、媒介、尺寸、馆藏页与 ImageURL，仅精简收录创作所需的核心代表作元数据。
- [蓬皮杜艺术家与馆藏记录](https://www.centrepompidou.fr/fr/ressources/personne/cX44X8E)：确立索尼娅·德劳内的作品元数据与创作事实；若直链未开放则保留直链字段为空，确保画作来源严肃准确。
- [提森博物馆的《同时性对比》](https://www.museothyssen.org/coleccion/artistas/delaunay-sonia/contrastes-simultaneos)：收录作品完整信息及确切的展品画作。索尼娅《电棱镜》的补充研究预览参考 Wikimedia 存档，作品核心权威信息以蓬皮杜记录为基准。
- [Hilma af Klint Foundation](https://hilmaafklint.se/selected-works/)：严格按照官方相册标题、HaK 编号及确切图像链接一一对应；缺失组内细分序号时忠实保留原样标注。
- [古根海姆教师资源 PDF](https://www.guggenheim.org/wp-content/uploads/2018/10/guggenheim-education-hilma-af-klint-teacher-resource-unit-10-5.pdf)：考证希尔玛的代表作与创作背景；《十大》第 2、9 幅图像位于 PDF 第 11 页（零基页 10）。
- [赵无极基金会油画档案](https://www.zaowouki.org/fr/artiste/oeuvres/peintures-a-l-huile/)：严格依从画册标题、图注与高清原图进行事实核验；法文馆藏与存放记录如实保留原始档案记载。
- [Helen Frankenthaler Foundation](https://www.frankenthalerfoundation.org/artworks/paintings)：权威提取作品详情与图像资源，准确辨析油彩浸染与后期丙烯技法。
- [Tate 的《十大》第 9 幅资料](https://shop.tate.org.uk/hilma-af-klint-the-ten-largest-group-iv-no.-9-old-age/afklin2311.html)：以官方文创页面作为补充图像索引，如实标注文档规格与排版边缘；微观细节研读结合博物馆权威 PDF 文件开展。

作品身份与来源均完成严格考证。指南中的构图策略、边缘处理与 Photopea 技法属于启发性创作建议；在具体任务执行时，须结合实时加载的原图进行实际审阅，并记录真实的观测时间戳。

## 字段约定

`artists[]` 包含稳定 ID、名字、别名、默认方向、卡片路径和研究来源。`directions[]` 包含 ID、研究分组名、时间范围、作品 ID 与 `reference_set_ready`（指示是否已配置三至五件代表作记录）。跨时期的备选方向可依据选定的主参考进一步聚焦。

`artworks[]` 分别记录：作品身份、来源、媒介尺寸、方向归属、明确的图像地址及其提取依据、图片状态、研究提示。`metadata_checked_at` 与图片下载时间分开，`viewing_status` 默认置为未看。当无可靠直链时设置 `image.url=null`，支持由浏览器访问作品原页面或扩充同方向权威来源。

`collection_url` 专用于作品溯源与引用，`image.url` 专用于下载原始图像资产。任务过程缓存统一存放在 `work/` 目录并与作品 ID 绑定。局部裁切、重着色与拼贴应用需单独登记处理参数与用途说明，遵从各来源的具体许可要求。

## 三个脚本

### select_artist.py

基于 Python 标准库实现。全面支持中英文、主流译名及标识符查询；对未知输入严格校验并抛出异常，完整响应排除条件。默认依托系统随机源在有效艺术家列表中进行等概率抽取。检测到既有会话时自动继承历史选择。若发生逻辑冲突或全量排除，返回非零状态码。

`--redraw` 用于显式重选指令：归档历史抽选、技法试样和工程检查记录，清理旧方向、参考、试样、保存／重开观察及画质检查。人物证据与既有 PSD 路径保留，重新进入视觉审阅流程；绘制时从原工程另存新版本。`--seed` 用于指定可复现创作与脚本测试。

### reference_assets.py

```text
python <skill>/scripts/reference_assets.py validate
python <skill>/scripts/reference_assets.py list --artist 克利
python <skill>/scripts/reference_assets.py table --out outputs/artist-resources.md
python <skill>/scripts/reference_assets.py prepare --session work/portrait/session.json --out work/portrait/references.json
python <skill>/scripts/reference_assets.py prepare --session work/portrait/session.json --direction <id> --works <id1> <id2> <id3> --out work/portrait/references.json --replace
python <skill>/scripts/reference_assets.py fetch --manifest work/portrait/references.json --out-dir work/portrait/references --contact-sheet work/portrait/reference-sheet.png
```

`validate` 全面核验 ID 唯一性、别名映射、指南卡片对应关系、作品归属及 URL 合法性。`prepare` 默认继承匹配的历史清单并保留看图注记；在主动切换方向或调整参考作品时添加 `--replace`。

`fetch` 严格请求资产清单中登记的公开 HTTPS 图像资源。内置网络超时与大小防护，对图像进行完整性解码；命中本地缓存直接复用，指定 `--refresh` 时强制刷新。针对特定机构（如 AIC）请求遵循访问速率规范，采用平稳串行拉取。失败结果逐项反馈并保留已拉取资产。资源落盘仅代表资产就绪，`visually_inspected` 状态须待人工视觉审阅后确立。

联系表（Contact Sheet）按原比例拼排已获取的参考图像并标注作品 ID，专用于构图横向宏观对比；深入的笔触与肌理研读需结合各作品的高分辨率视图开展。

### verify_delivery.py

Pillow 检查 PNG／JPEG 的完整解码、长边像素规格（默认 ≥2000 px）与记录的画布比例；psd-tools 检查 PSD 解码、内容层数量及与导出图一致的像素尺寸。PSD 至少保留两个独立内容层，实际主要形体和蒙版的可编辑性由操作者在 Photopea 中检查。PSD 路径由 `--project` 指定，或读取 `photopea.project_path`；相对路径按命令工作目录解析。长边阈值可用 `--min-long-edge` 调整。

人工记录包括 PSD 下载、实际文件重开、关键层编辑范围、底稿状态、技法试样、三尺度观察和 PNG 终审。字段定义见 [photopea-workflow.md](photopea-workflow.md)。脚本只检查这些记录的存在性，绘画效果和操作真实性依靠实际 UI 观察。

退出码约定：0 表示格式合规且人工记录结构完备；2 表示文件或数据校验异常；3 表示缺少必要的人工复核项，并在终端明确列出缺失字段。脚本专责客观规格审查，审美与操作有效性依从执行者的真实记录。PDF 作为补充交付介质时须单独打开核验。

数据传输统一采用 UTF-8 编码，Windows 终端建议配合 `python -X utf8` 运行。脚本输入输出路径均由调用参数显式指定，确保技能安装目录的无状态纯净性。

## 更新

变更资产库或指南卡片时，同步递增 `metadata.version` 与 `catalog.version` 并记录维护时间。若遇到图像链接变更，优先循着官方藏品页及权威基金会档案溯源更新，客观记录来源变更流转。完成资源扩充后，系统执行 `validate` 指令、自动化测试套件与技能静态校验。

以仓库内的技能目录为维护基准；安装时复制完整的 `photopea-abstract-portrait` 目录，并按宿主约定刷新技能索引。

### 2.0.0 · 2026-09-06

以 Photopea 的笔刷、路径、选区、蒙版、混合模式和智能滤镜重写绘画流程，全面适配 14 位先驱艺术家的技法指南。工程交付升级为本地分层 PSD 与高分辨率 PNG，规范化沉淀局部试样、工程重开验证与多尺度视觉复核记录。
