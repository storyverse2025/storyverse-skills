---
name: keyframe-prompt
description: >-
  AI 短剧（竖屏 9:16 微短剧）Keyframe / 空间基准帧提示词生成方法论。Keyframe 是一张静止图，把 Spatial Bible 的文字空间信息图像化，锁住"角色站位 + 家具光源位置 + 机位坐标系"三件事，作为整场戏的 scene-ref 反复挂载到每个 Beat，解决 AI 每次独立生成、空间随机漂移的问题。只要任务涉及下列任意一项就用这个 skill，哪怕用户没说"Keyframe"三个字：为某个场景写空间基准帧 / scene-ref / staging image 的提示词；把一段剧本或 Spatial Bible 转成静帧提示词；确认场景初始站位与机位；质检已写好的 Keyframe 提示词；诊断"生成出来角色位置/朝向不对"；或在 Beat 提示词里写引用 scene-ref 的精简版 SPATIAL ANCHOR。配合 Kling、Seedance 等工具使用。它聚焦"建图像锚"这一交付物，是 ai-short-drama-storyboard 全流水线里 Spatial Bible 之后、写 Beat 之前的那一步。
license: 内部方法论，整合自项目 Keyframe 制作方法论文档与实战案例。
---

# Keyframe 提示词制作手册

Keyframe（空间基准帧）是一张**静止图片**，不是视频，没有动作也没有台词。它是 Spatial Bible 的图像化呈现，生成并质检通过后，作为 `scene-ref` 挂载到整场戏每一个 Beat 的 `[REFERENCE]` 区块里反复复用。

## 它解决的核心矛盾

AI 视频工具每次生成都是**独立调用、没有跨 Beat 的上下文记忆**。不做空间锚定的话，同一场景里桌子位置、角色站位、光线方向每次都会随机漂移。方案是两层锚：Spatial Bible 是**文字锚**，Keyframe 是**图像锚**。有了图像锚之后，后续每个 Beat 的 `[SPATIAL ANCHOR]` 可以从"完整描述整个房间"精简为"参照附图，只补本 Beat 的变化"。

它在全流水线里的位置：建完 Spatial Bible 之后、开始写 Beat / Canvas Shot 之前。（整条流水线见 `ai-short-drama-storyboard` skill。）

## 行为准则（最重要，违反它就等于没做对）

用户请求帮忙写 Keyframe 时，**直接先出一版填好的草稿，不要先反问一堆"你需要提供 XXX"。** 把已知信息填进模板，对不确定的字段用 `[请确认: ...]` 就地标注，再让用户补确认。让用户自己对照模板填空 = 没帮上忙。

## 什么时候需要新建一张 Keyframe

下面三种情况，必须在写 Beat 提示词**之前**先做 Keyframe：

| 触发条件 | 说明 |
|---------|------|
| 新场景开始 | 剧情切到新空间——新房间、室外、不同楼层都算 |
| 空间关系大幅变化 | 如角色从台阶上方对峙移到地面平层、从房间转到走廊 |
| 新角色加入场景 | 三角/多角站位要重新确认，原两人站位图失效 |

原则：有现成 Keyframe 就用。没有时，前一条 Beat 的尾帧可临时充当 scene-ref，但专门生成的更稳。

## Keyframe 锁住的三件事

1. **角色站位**——谁站哪、面朝哪个方向、在画面什么位置（screen-left / center / right）
2. **场景空间**——家具、光源、出入口在三维空间里的相对位置
3. **机位基准**——从哪个角度建立空间，决定后续所有 Beat 的机位坐标系

## 制作流程

准备阶段（每个新场景做一次）：

1. **建 Spatial Bible**——填 LANDMARKS（家具/出入口位置）、LIGHT SOURCES（光源方向/色温/动态）、CHARACTER START POSITIONS（初始站位）、CAMERA POSITIONS（4-5 个固定机位）。
2. **写 Keyframe Prompt**——用 Spatial Bible 的信息填 `assets/keyframe-template.txt`。机位默认 **CAM-D（侧面交叉）**，两角色全身入画、正面相对；建立宽景时才用 CAM-A。包含完整 LIGHT / STYLE / NEGATIVE。
3. **生成图片并质检**（六项见下），通过后保存为该场景的 scene-ref 资产。

执行阶段（每个 Beat 重复）：

4. 把基准帧挂到每条 Beat 的 `[REFERENCE]` 末尾：`(image3) <scene-ref> [场景一句话描述]`。
5. `[SPATIAL ANCHOR]` 只补充变化——精简写法见 `references/case-and-anchor.md`。

## 机位默认选 CAM-D 的原因

侧面交叉机位让两个角色都以正面/四分之三面朝镜头，方便后续核对面孔一致性；建立宽景（CAM-A）拍出来常是背面或极远景，不利于角色识别。除非用户明确要宽景，否则默认 CAM-D。

## Keyframe 质检清单（生成后逐条核对）

```
□ 空间三维感成立（近 / 中 / 远景层次可辨认）
□ 特殊空间特征保留（落地窗 / 壁炉 / 天花板高度等）
□ 角色站位符合剧情逻辑（谁在主权区域，谁是来访者）
□ 光线方向与时间段一致（日景 / 夜景 / 壁炉暖光等）
□ 机位与后续 Beat 的机位方案兼容
□ 没有多余元素（多余角色 / 字幕 / 水印 / 门框穿帮）
```

## 模板与案例（动手时调取）

- **填空模板**：`assets/keyframe-template.txt`——`{花括号}` 是待替换内容，`[方括号]` 是说明，输出时删说明只留实际描述。
- **完整实战案例 + 关键决策讲解 + Beat 里的精简 SPATIAL ANCHOR 写法**：`references/case-and-anchor.md`。第一次写、或拿不准某个字段怎么填时，对照这个案例。

## 收信息时的默认值（用户没给就用这些，并标注待确认）

| 必要信息 | 用户没给时怎么办 |
|---------|----------------|
| 场景类型和氛围 | 从剧情上下文推断，草稿里标 `[请确认]` |
| 角色外貌（人种/发型/服装） | 按角色名推断常见设定，标 `[请补充]` |
| 空间地标（家具/光源位置） | 按场景类型给合理默认，标 `[待确认]` |
| 机位偏好 | 默认 CAM-D 侧面交叉，两人全身正对 |

## 常见请求模式与处理方式

- **"帮我写这个场景的 Keyframe" + 附剧本段落** → 从剧本提取角色/场景/情绪，直接出草稿。
- **"我有 Spatial Bible，帮我转成 Keyframe Prompt" + 附文本** → 提取 LANDMARKS / LIGHT SOURCES / CHARACTER START POSITIONS 填模板。
- **"这个 Keyframe 有什么问题？" + 附已写好的提示词** → 对照质检清单逐项核查，给具体修改建议。
- **"生成出来角色位置/朝向不对" + 描述问题** → 通常是 CAMERA 描述不够精确，或 LEFT/RIGHT FIGURE 的 `facing` 方向写反了；给修改方案。
