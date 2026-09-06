# Photopea Computer Use 绘画流程

## 操作方式

在 `https://www.photopea.com/` 中使用宿主提供的 computer use。先读取工具文档，确认截图、鼠标按下／移动／抬起、键盘和本地文件对话框的支持情况，再接管用户指定的浏览器或标签页。工具调用签名以宿主文档为准。

画面制作通过原生 UI 交互完成：选择工具、设置参数、绘制笔画轨迹、编辑图层与蒙版，最终导出分层 PSD 和 PNG。本地 Python 工具链协同负责语料整理、学术参考检索与工程规范校验。在无 GUI 交互的分析环境中，亦可独立运行人物观察与学术构图设计流程。

使用现有免费工具、内置笔刷和许可明确的免费资源。额外购买、账户授权和云端发布由用户决定；本地 PSD 是默认工程文件。菜单以下文英文名称辅助定位，执行时以当前界面语言和实际入口为准。

## 1. 建立文档与工作状态

1. 读取 session，确认目标人物、选定艺术家、方向和参考。新作通过 `File > New` 创建指定像素尺寸的 RGB 文档，默认 1600×2000 px；修改任务通过 `File > Open` 打开用户 PSD 或 `photopea.project_path`。
2. 查看当前文档标签、图像尺寸、缩放和图层面板。通过 `Window` 打开需要的 Layers、Brush、Properties、History 面板；保留足够绘画区域。
3. 参考图优先作为独立文档打开。需要临摹定位时，将图像作为独立图层置入，命名 `Reference`、降低不透明度并锁定；最终隐藏或移除。
4. 建立按职责命名的图层或组：`Ground`、`Color Fields`、`Structure`；按需要增加 `Texture`、`Adjustments`、`Study`。像素笔迹、形状、蒙版和调整层分别保留，组数随构图复杂度增减。
5. 在重大结构调整前保存一个本地 PSD 检查点。恢复时同时核对磁盘文件与当前画面，继承已完成内容。

### 鼠标与画布控制

- 每组笔迹前确认活动文档、图层名称、图层类型、选中的是内容还是蒙版缩略图、当前选区、工具、颜色与参数。点选面板完成后再进入画布绘制。
- 笔刷大小使用文档像素；屏幕显示大小同时受缩放影响。缩放、平移、展开侧栏后重新截图定位，以画布内相对位置安排笔迹。
- 自由笔迹采用宿主支持的按下、连续移动、抬起动作。长曲线分成有意义的笔段；需要精确曲率时使用 Pen 路径和节点调整。
- 无压感输入时采用固定尺寸与不透明度，通过宽窄笔段、重复薄涂和蒙版塑造变化；压感选项仅在输入工具支持时启用。
- 快捷键以画布获得焦点为前提；文件操作优先点击菜单。一次完成一类操作后查看结果，菜单、变换框或文件对话框关闭后再继续画笔输入。
- 笔迹没有出现时，先检查选区、锁定、可见性、图层类型及蒙版目标；落笔错误时使用 Undo 或 History 回到该动作之前，再校正状态。

## 2. 选择工具并做局部试样

Photopea 提供完备的像素绘画、贝塞尔矢量路径、混色涂抹、图层蒙版与滤镜系统。通过低不透明度多次薄涂、羽化蒙版与涂抹交界的有机组合，能够高效表现出柔和晕染与水彩层叠的艺术视觉效果。

| 目标 | UI 操作与对象 | 观察重点 |
|---|---|---|
| 软笔薄涂 | 新建像素层，选 Brush；顶部设置笔尖、Size、Hardness、Opacity，`Window > Brush` 调整 Spacing | 圆形笔尖可调硬度；以多次薄涂形成浓淡，观察重叠处的色阶 |
| 干刷、颗粒与飞白 | Brush 面板选择图案笔尖，按需要设置 Tip Shape、Tip Dynamics、Scatter | 用实际笔迹检查印章重复、颗粒尺度与笔触方向；图案笔尖放大后会像素化 |
| 精确结构线 | Pen 的 Shape 模式建立填充／描边形状；Free Pen 将拖拽笔迹转为曲线，可调 Tolerance；自由细线用小尺寸 Brush | Shape 新建形状层，Path 编辑路径，Pixels 直接栅格化；按参考决定几何精度与手工起伏 |
| 连续色域 | `Layer > New Fill Layer > Gradient` 建立可调渐变层，双击缩略图编辑；用蒙版限制范围 | 内部色彩推移与外部轮廓分别控制，渐变方向服务于色域而非统一光源 |
| 局部边缘消隐 | `Layer > Raster Mask > Add`，选择蒙版缩略图，用黑／灰软笔隐藏、白笔恢复 | 黑白灰控制显隐；局部画蒙版可保留相邻清晰边缘 |
| 整体蒙版羽化 | 选择蒙版，在 Properties 调 Feather 与 Density | Feather 柔化蒙版边界而保留原像素；整张蒙版的羽化与局部软笔处理作用范围不同 |
| 受控范围内上色 | 在主体上方建像素层，`Layer > Clipping Mask`；或对已有像素层锁定 Transparency | 剪贴蒙版将上层内容限制在下层透明度范围；锁透明度适合直接给已有笔迹改色 |
| 交界揉合 | 在含有相邻颜色的像素层副本上使用 Smudge，从边界向目标方向短距离拖动 | 观察颜色位移与形体变化；跨层颜色先在保留原层的前提下制作局部合并副本 |
| 局部柔化 | 在像素层副本上使用 Blur 工具并调 Strength | 柔化范围随笔迹分布；与 Smudge 的推移颜色效果分别试验 |
| 可回调的色雾 | 目标色层转 Smart Object，`Filter > Blur > Gaussian Blur`；在智能滤镜下调整参数及滤镜蒙版 | 模糊保留在目标色层，结构线独立；需直接绘画时双击智能对象进入源文档，保存后返回 |
| 叠色与明度 | 在 Layers 顶部比较 Normal、Multiply、Screen、Soft Light 及 Opacity | Normal 保留本色，Multiply 常用于加深，Screen 常用于提亮，Soft Light 用于柔和对比；逐项开关比对 |
| 可回调调色 | `Layer > New Adjustment Layer` 添加 Curves、Hue/Saturation 等，再用蒙版或剪贴限定范围 | 整体明度、局部冷暖与饱和度分开调节 |
| 选区约束 | 矩形／椭圆选框、Lasso 或 Polygonal Lasso 定义范围；`Select > Modify > Feather` 羽化，`Edit > Fill` 填色或添加蒙版 | 选区作用于整个文档中的当前编辑目标；完成后 `Select > Deselect`。Quick Mask 用于以笔刷修改选区，结束后切回常规模式 |

图层类型决定操作方式：Brush、Smudge 和 Blur 笔迹作用于像素层或栅格蒙版；填充层通过参数与蒙版编辑；智能对象通过源文档编辑像素并保留智能滤镜。需要栅格化时保留源层副本。

在 `Study` 组或独立试样文档中做一处“相邻色域＋软硬交界＋细线”的组合。选择两至三项参考特征，分别试验需要的路径；记录实际对象、工具、设置、动作、截图与观察。以下参数是 1600×2000 px 画布的起点，随参考与缩放调整：

- 薄涂：圆形 Brush，Size 80–240 px、Hardness 0–30%、Opacity 10–25%；Flow 若当前工具提供，则单独试调并记录。
- 细线：Brush 2–6 px 或等效形状描边，先比较正常视距的粗细与对比；色场作品可省略线性骨架。
- 连续笔迹：Spacing 从 10–25% 试起；颗粒笔适当增加间距和散布，以局部实际笔迹决定密度。
- 柔化：蒙版 Feather 或 Gaussian Blur 从 4–20 px 小幅增加；需要保留的清晰边界通过局部蒙版或独立图层处理。

试样表现与目标一致后扩展到主画面。若当前路径效果不足，先调整局部设置或换用另一种适合的工具；核心质感仍需取舍时，保留当前工程、记录差异并与用户确认方向。

### 自定义笔刷

内置笔刷足够时直接绘制。需要特定干刷或水彩形状时，可通过 `File > Open` 导入许可明确的 `.abr`，在 Brush 面板选取新笔刷并试画；记录来源、许可、文件路径与设置。也可从本次 UI 绘制的笔迹通过 `Edit > Define New > Brush` 定义笔尖。自定义预设可导出 ABR 便于续画，PSD 保留的是已画笔迹和图层结构，笔刷资源单独管理。

## 3. 分层绘画

1. **底色与体量**：用纯色填充层建立 Ground，以少量大笔迹、选区填色或形状确定主要体量与留白。缩小到适合全图的视距，先调整面积、重心与邻接关系。
2. **内部色层**：在主体上方加剪贴像素层薄涂，或添加带蒙版的渐变层。保持若干相近色的变化与少量强调色，逐层比较混合模式和不透明度。
3. **边缘组织**：按参考区分硬边、软边和融入背景的边。硬边由形状或选区保持；软边在蒙版上处理；需要颜色相互拖移的局部使用 Smudge。
4. **笔触与结构**：在独立像素层绘制方向性笔触，在独立形状或线层组织符号。用疏密、宽窄、断续和倾斜形成节奏；曲线细节在较大视距下完成后回到全图复看。
5. **材质与调色**：参考需要时，在局部层用图案笔刷或许可纹理表现材质，结合蒙版与混合模式。暂时隐藏 Texture 检查色层本身，再恢复并判断颗粒尺度。用调整层完成必要的明度与冷暖协调。
6. **阶段保存**：在构图确定、主要色层完成和终稿三个节点保存 PSD。对可见性、蒙版、滤镜或调色做成品修改后更新 PSD，再导出 PNG。

柔性色层参考可采用“薄涂像素层＋局部蒙版＋少量交界揉合＋独立细线”；硬边参考可采用“形状／选区填色＋局部剪贴调色＋精确分区”；动作性参考可采用“宽窄笔迹＋图案笔尖＋分组遮挡”。具体组合跟随选中艺术家的资料卡和本次原图。

## 4. 三尺度复核

依次检查缩略图、正常视距与 100% 或更大的细节视距，并记录 `{scale, checked_at, observation, fix, screenshot_path}`。

- 缩略图：主体体量、留白、色彩面积、视觉重心。
- 正常视距：浓淡层次、软硬边关系、笔触节奏与符号数量，对照参考及试样目标。
- 局部：蒙版接缝、选区漏边、重复笔尖痕迹、模糊光晕、线条接续及像素化。

在 Layers 面板分别点选主要色层、结构线及用到的蒙版；切换可见性，检查每层对应内容。记录关键层的类型与可继续修改的方式。修正集中在对应图层，保留已经成立的结构。

## 5. 保存 PSD、重开与导出

1. 隐藏或移除 Reference 和 Study，确认活动文档为终稿。
2. 点击 `File > Save as PSD`，通过下载／保存对话框取得本地文件。核对实际文件名、路径、大小及修改时间，归档为 `outputs/portrait/portrait.psd`；已有同名工程时保留版本或确认覆盖目标。
3. 保留原文档，通过 `File > Open` 重开刚下载的 PSD。核对尺寸、构图、图层名称、蒙版和智能滤镜；分别点选主要层并切换可见性，再恢复终稿状态。恢复后的内容有修改时重新保存，保持交付文件与终稿一致。
4. 从已核对的文档点击 `File > Export As > PNG`，在导出窗口确认像素尺寸及背景透明状态，下载为 `outputs/portrait/portrait.png`。PNG 用于观赏，PSD 用于继续编辑。
5. 打开实际下载的 PNG 检查裁切、颜色、缺失图层及底稿残留，填写 `export_review`，再运行交付校验脚本。

保存依据是实际 PSD 文件及重开观察。Photopea 首页地址只作编辑器入口，本地项目通过 PSD 恢复。交付包括 PNG、分层 PSD、必要的可再分发笔刷资源及简要图层说明。

## 运行记录

`session.json` 沿用 `stage`、`canvas: {width,height}`、人物证据、选择与参考字段，并按完成情况填写：

| 字段 | 内容 |
|---|---|
| `photopea.project_path` | 实际 PSD 路径，推荐绝对路径 |
| `photopea.save_observed_at`、`save_observation` | PSD 下载时间、文件与保存观察 |
| `photopea.reopened_at`、`reopen_observation` | 重开该文件的时间及图层、蒙版和画面观察 |
| `photopea.editable_layers` | 关键层名称、类型、蒙版／滤镜与实际点选观察组成的列表 |
| `photopea.reference_underlay_status` | `removed`、`hidden` 或 `not_used` |
| `technique_study` | `reference`、`targets`、`trials`、`decision`；每次试样记录工具、图层／蒙版对象、参数、动作、截图路径与观察 |
| `quality_checks` | `thumbnail`、`normal`、`detail` 的观察、时间、修正及截图路径 |
| `export_review` | 实际 PNG 的 `viewed_at` 和 `observation` |

可增记 `photopea.ui_state`（活动文档、缩放、图层、工具及参数）和资源清单帮助恢复；继续执行时通过新截图确认状态。未完成的动作保留为待执行阶段。文件校验检查 PSD／PNG 解码、尺寸、图层数量与记录完整性；视觉判断由操作者完成。

## 官方能力依据

以下页面于 2026-09-06 查阅，用于编写流程；实际 UI 验证随执行任务记录。

- [Brush Tools](https://www.photopea.com/learn/brush-tools)：软硬笔尖、间距、动态、散布、压感及 ABR。
- [Basic Tools](https://www.photopea.com/learn/bt-basic) 与 [Advanced Tools](https://www.photopea.com/learn/bt-advanced)：Brush、Pencil、Smudge、Blur、Sharpen、Dodge、Burn 等像素工具。
- [Masks](https://www.photopea.com/learn/masks)：栅格／矢量蒙版、Density 与 Feather。
- [Layers](https://www.photopea.com/learn/layers) 与 [Other Layers](https://www.photopea.com/learn/other-layers)：混合模式、锁定、剪贴蒙版、填充及调整层。
- [Smart Objects](https://www.photopea.com/learn/smart-objects)：源文档编辑与智能滤镜。
- [Adjustments and Filters](https://www.photopea.com/learn/adjustments-filters)：像素滤镜与可回调的智能滤镜蒙版。
- [Creating Shapes](https://www.photopea.com/learn/vg-creating) 与 [Selections](https://www.photopea.com/learn/selections)：Pen、Free Pen、形状模式、选区羽化和 Quick Mask。
- [Opening and Saving](https://www.photopea.com/learn/opening-saving)：本地 PSD 保存、重开及 PNG 导出。
