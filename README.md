# 言之有画 (Verba Picta)

欸？康定斯基为我作画？！

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](canva-abstract-portrait/SKILL.md)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](requirements.txt)
[![Tests](<https://img.shields.io/badge/tests-14%20passed-success.svg>)](tests/test_scripts.py)
[![Computer Use](<https://img.shields.io/badge/interaction-Canva%20Browser%20UI-orange.svg>)](canva-abstract-portrait/references/canva-workflow.md)

---

## 🌟 核心特色与设计亮点

![1788667518532](image/README/1788667518532.png)

**和女朋友的三天微信对话生成，米罗风格**

- 🎨 **原生 Computer Use 实时绘制**：区别于传统扩散模型的扁平位图输出，Agent 通过原生浏览器交互直接操作 Canva 编辑器，完成色域铺陈、连续曲线绘制、透明度叠加与图层分组锁定，产出结构清晰且可二次交互编辑的原生设计工程。
- 🔬 **行为科学证据链**：基于语言互动模式、情境-反应模型、大五人格特质与 COM-B 行为系统，建立严格溯源的共用证据表。事实推断与视觉转译保持单向映射，确保画像具备扎实的行为学支撑。
- 🏛️ **14 位艺术大师学术策展库**：精选康定斯基、毕加索、蒙德里安、马列维奇、克利、米罗、德劳内、罗斯科、波洛克、马丁、克林特、赵无极、弗兰肯塔勒、克莱因等 14 位先驱，涵盖 43 个风格时期。109 件代表作均追溯至 MoMA、蓬皮杜艺术中心、古根海姆博物馆及艺术家官方基金会权威馆藏。

---

## 🔄 全流程架构

```mermaid
flowchart TD
    A[输入人物对话 / 文本语料] --> B[1. 证据提取与多维分析\n- 语言互动 / 情境反应 / 大五 / COM-B\n- 固化证据 ID 与核心观察]
    B --> C[2. 大师抽选与方向锚定\n- 等概率抽选或指定艺术家\n- 加载专属研究指南]
    C --> D[3. 视觉研读与构图提炼\n- 检索与缓存 3~5 幅权威馆藏\n- 生成 2~3 套差异化构图方案]
    D --> E[4. Canva 原生绘制\n- 全局 Computer Use 控制浏览器\n- 搭建色面 / 矢量造型 / 图层分组锁定]
    E --> F[5. 三尺度质量复核\n- 缩略图全局节奏\n- 正常视距主次\n- 局部放大细节接缝]
    F --> G[6. 成果导出与规范校验\n- 导出高分辨率 PNG\n- verify_delivery 自动化校验\n- 交付图片与可编辑链接]
```

---

## 🎨 艺术家谱系与创作方向矩阵

知识库全面覆盖 14 位艺术大师，每位艺术家均配有开箱即用的默认代表作品组与详尽研究指南：

| 艺术家                         | 默认研究方向与时期                      | 代表作品典藏机构            | 艺术语言核心特质                               | 专属指南                                                                       |
| ------------------------------ | --------------------------------------- | --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------ |
| **瓦西里·康定斯基**     | 坎贝尔壁画组：抒情性非具象 (1914)       | MoMA (纽约现代艺术博物馆)   | 方向性大色带、音乐性动态线条、冷暖色团交响     | [指南](canva-abstract-portrait/references/visual-guides/wassily-kandinsky.md)   |
| **巴勃罗·毕加索**       | 身体变形与多视角人物 (1930–1932)       | MoMA                        | 多重视角轮廓交叠、体量变形、黑粗轮廓与肤色对比 | [指南](canva-abstract-portrait/references/visual-guides/pablo-picasso.md)       |
| **皮特·蒙德里安**       | 新造型主义正交平衡 (1920–1929)         | MoMA                        | 纯粹垂直与水平黑线、非对称原色块、积极空间留白 | [指南](canva-abstract-portrait/references/visual-guides/piet-mondrian.md)       |
| **卡济米尔·马列维奇**   | 至上主义悬浮色块 (1915–1917)           | MoMA                        | 白场空间悬浮感、纯粹几何形态、偏心动势平衡     | [指南](canva-abstract-portrait/references/visual-guides/kazimir-malevich.md)    |
| **保罗·克利**           | 面具与线性色面的象征性造型 (1924–1928) | MoMA                        | 面具式几何提炼、诗性细线律动、手工质感温和色层 | [指南](canva-abstract-portrait/references/visual-guides/paul-klee.md)           |
| **胡安·米罗**           | 梦境绘画与开放场 (1923–1926)           | MoMA                        | 极简开放背景、生物形态符号、高纯度色彩点缀     | [指南](canva-abstract-portrait/references/visual-guides/joan-miro.md)           |
| **索尼娅·德劳内**       | 早期同时性：色面对比与节奏 (1913–1915) | 蓬皮杜艺术中心 / 提森博物馆 | 同心环同心圆弧、邻接色对比、舞动色块节奏       | [指南](canva-abstract-portrait/references/visual-guides/sonia-delaunay.md)      |
| **马克·罗斯科**         | 成熟期叠置色域 (1950–1958)             | MoMA                        | 巨幅叠置色块、渗透式晕染软边、深邃情绪场域     | [指南](canva-abstract-portrait/references/visual-guides/mark-rothko.md)         |
| **杰克逊·波洛克**       | 浇洒与全幅网络 (1947–1950)             | MoMA                        | 全局贯通多层滴流线网、疏密梯度、去中心化动势   | [指南](canva-abstract-portrait/references/visual-guides/jackson-pollock.md)     |
| **阿格尼丝·马丁**       | 细网格与微差 (1963–1964)               | MoMA                        | 均质细线网格、呼吸感微温差、极简秩序美学       | [指南](canva-abstract-portrait/references/visual-guides/agnes-martin.md)        |
| **希尔玛·阿芙·克林特** | 《十大》组作有机形与几何关系 (1907)     | 希尔玛基金会 / 泰特美术馆   | 螺旋卵形有机演化、粉彩明丽基调、图腾式象征形态 | [指南](canva-abstract-portrait/references/visual-guides/hilma-af-klint.md)      |
| **赵无极**               | 动势、密度与开放空间 (1961–1969)       | 赵无极基金会                | 狂草笔势聚散、多维灰调冷暖层叠、深邃大气空间   | [指南](canva-abstract-portrait/references/visual-guides/zao-wou-ki.md)          |
| **海伦·弗兰肯塔勒**     | 浸染色域与线性骨架 (1952–1957)         | 弗兰肯塔勒基金会 / MoMA     | 浸润通透色场、底色呼吸通道、轻盈有机轮廓       | [指南](canva-abstract-portrait/references/visual-guides/helen-frankenthaler.md) |
| **弗朗兹·克莱因**       | 黑白结构与笔势 (1950–1955)             | MoMA                        | 磅礴黑白互锁结构、主动负空间造型、刚劲张力笔触 | [指南](canva-abstract-portrait/references/visual-guides/franz-kline.md)         |

完整作品名录与图像链接详见 [docs/artist-resources.md](docs/artist-resources.md)。

---

## 📦 交付成果与规格标准

任务收敛后提供双轨交付成果：

1. **画作文件**：通过 Canva 下载 UI 导出的高分辨率原生图像（PNG 或印刷 PDF，长边默认 $\ge 2000\text{ px}$）
2. **Canva 可编辑链接**：保留既定编辑权限的直接设计链接，确保所有色面、线条与图层均可在浏览器中继续点选与二次调整。
3. **创作与转译报告**：精简阐明所选艺术大师与风格方向、核心参考画作、3~4 项核心行为特征与视觉形态的映射关系，以及具体的技法运用。
4. **过程资产归档**：会话状态完整保存在 `work/portrait/session.json`，成品与检验清单保存在 `outputs/portrait/`。

---

## 🚀 快速上手与运行环境

### 推荐模型 (Recommended Models)

本 Skill 的核心绘制环节依托 Agent 对原生 Canva 画布的细粒度控制。为保障复杂矢量图形绘制、色彩配置与图层编排的精准度，**强烈推荐使用具备前沿视觉操作能力的最新旗舰模型**：

- **OpenAI Astra**：具备卓越的屏幕空间几何理解、多尺度视觉注意力与端到端复杂工具协同调用能力。
- **Fable 5.1**：在细粒度 GUI 元素识别、坐标微调对齐与多步连续鼠标轨迹规划上展现高稳定度表现。
- **推荐原因**：抽象肖像制作涉及在 Canva 编辑器中开展大色域铺陈、连续曲线锚点调节、半透明遮罩叠加、精确色值选取以及多图层分组锁定等高频精细 GUI 交互；最新旗舰模型拥有出色的原生视觉操作精度与空间推理能力，能有效避免定位漂移与交互试错，充分还原现代艺术大师的构图精髓与质感细节。

### 环境要求

- **宿主环境**：具备全局可用 **Computer Use** 控制能力的大模型智能体环境，以及可进行设计编辑的 Canva 登录状态。
- **Python 运行环境**：Python 3.10+。
- **脚本依赖**：仅需安装基础图形处理库 Pillow。

```shell
python -m pip install -r requirements.txt
```

### 技能安装

将 [canva-abstract-portrait/](canva-abstract-portrait/) 文件夹复制至宿主指定的技能目录即可。入口配置为 [canva-abstract-portrait/SKILL.md](canva-abstract-portrait/SKILL.md)，平台元数据描述见 [canva-abstract-portrait/agents/openai.yaml](canva-abstract-portrait/agents/openai.yaml)。

### 调用 Prompt 示例

```text
使用 canva-abstract-portrait。

目标人物：李明（某开源社区技术带头人）
对话或语料：
[附上目标人物近期在架构选型、技术评审中的代表性讨论、日常交流与复盘发言材料...]

指定艺术家或排除名单（可选）：排除 毕加索
颜色、质感或元素偏好（可选）：偏好深蓝与冷灰，需要有强烈的结构感
画幅与用途（可选）：1600x2000 px 纵向海报
肖像显性程度（可选）：隐约人形
已有 Canva 链接（修改任务时提供）：
```

---

## 🛠️ 本地工程脚本与自动化测试

技能配套了纯净轻量的 Python 工具链，全流程无第三方重型依赖：

### 1. 艺术家抽选引擎 (`select_artist.py`)

在候选艺术家池中执行等概率无偏随机抽选，自动处理别名映射与排除项，并支持断点续创：

```shell
# 默认等概率随机抽取
python canva-abstract-portrait/scripts/select_artist.py --session work/portrait/session.json

# 指定艺术家或排除名单
python canva-abstract-portrait/scripts/select_artist.py --session work/portrait/session.json --artist 赵无极
python canva-abstract-portrait/scripts/select_artist.py --session work/portrait/session.json --exclude 毕加索 --exclude 波洛克
```

### 2. 参考资产准备与拉取 (`reference_assets.py`)

生成结构化参考资产清单，拉取权威馆藏原图至本地并生成多图比对联系表：

```shell
# 校验整个资产库的合法性
python canva-abstract-portrait/scripts/reference_assets.py validate

# 准备参考清单并拉取图像缓存
python canva-abstract-portrait/scripts/reference_assets.py prepare --session work/portrait/session.json --out work/portrait/references.json
python canva-abstract-portrait/scripts/reference_assets.py fetch --manifest work/portrait/references.json --out-dir work/portrait/references --contact-sheet work/portrait/reference-sheet.png

# 重新生成 Markdown 索引表格
python canva-abstract-portrait/scripts/reference_assets.py table --out docs/artist-resources.md
```

### 3. 交付质量与结构校验 (`verify_delivery.py`)

在导出图像后自动化执行像素规格、长宽比一致性、设计链接以及人工质检记录的完整性校验：

```shell
python canva-abstract-portrait/scripts/verify_delivery.py --session work/portrait/session.json --image outputs/portrait/portrait.png --out outputs/portrait/delivery-check.json
```

### 4. 运行单元测试套件

```shell
python -m unittest discover -s tests -v
```

---

## 📁 仓库结构

```text
.
├── README.md                                  # 项目概览与使用指南
├── requirements.txt                           # Python 依赖清单
├── assets/                                    # 项目静态资源与赞赏码
│   ├── sponsor-alipay.jpg                     # 支付宝赞赏码
│   └── sponsor-wechat.jpg                     # 微信赞赏码
├── docs/
│   └── artist-resources.md                    # 14 位艺术家作品速查与馆藏索引
├── tests/
│   └── test_scripts.py                        # 脚本行为与工程完整性测试套件
└── canva-abstract-portrait/                   # 完整、可独立分发的 Skill 目录
    ├── SKILL.md                               # 技能主入口与标准工作流定义
    ├── agents/
    │   └── openai.yaml                        # 平台元数据与配置
    ├── references/
    │   ├── artist-catalog.json                # 结构化核心资产库 (14 艺术家 / 109 作品)
    │   ├── portrait-evidence.md               # 四维行为科学证据提取与转译规范
    │   ├── canva-workflow.md                  # 基于 Computer Use 的 Canva 绘制与交互规范
    │   ├── resource-workflow.md               # 资料维护标准与资产管线工作流
    │   ├── evaluation-cases.md                # 行为一致性与验证案例矩阵
    │   └── visual-guides/                     # 14 位艺术大师的独立创作与视觉指南
    │       ├── agnes-martin.md
    │       ├── franz-kline.md
    │       ├── helen-frankenthaler.md
    │       ├── hilma-af-klint.md
    │       ├── jackson-pollock.md
    │       ├── joan-miro.md
    │       ├── kazimir-malevich.md
    │       ├── mark-rothko.md
    │       ├── pablo-picasso.md
    │       ├── paul-klee.md
    │       ├── piet-mondrian.md
    │       ├── sonia-delaunay.md
    │       ├── wassily-kandinsky.md
    │       └── zao-wou-ki.md
    └── scripts/
        ├── select_artist.py                   # 等概率艺术家抽选脚本
        ├── reference_assets.py                # 馆藏资产拉取与缓存处理脚本
        └── verify_delivery.py                 # 交付物自动化规格校验脚本
```

---

## 📖 数据治理与开源许可

- **元数据与图式版权**：作品事实与元数据依托 MoMA 开放数据集与权威博物馆公开展出信息整理。
- **运行无状态原则**：单次任务产生的语料、临时草稿与成果仅留存在工作目录（`work/` 和 `outputs/`），技能核心目录保持无状态与纯净。
- **可复现性保障**：支持通过 `--seed` 参数实现抽选可复现，服务于自动化评测与确定性验证。

---

## ☕ 支持开发 / Sponsor

如果您觉得本 Skill 为您的生活赋予了一点乐趣与灵感，欢迎赞赏支持作者的持续研发与迭代！您的每一份认可都将直接投入到更多现代艺术流派库建设、复杂构图算法优化与前沿交互模型的适配中。

<div align="center">
  <table>
    <tr>
      <td align="center" width="320">
        <img src="assets/sponsor-alipay.jpg" width="260" alt="支付宝赞赏码" />
        <br />
        <b>支付宝赞赏 (Alipay)</b>
      </td>
      <td align="center" width="320">
        <img src="assets/sponsor-wechat.jpg" width="260" alt="微信赞赏码" />
        <br />
        <b>微信赞赏 (WeChat Pay)</b>
      </td>
    </tr>
  </table>
