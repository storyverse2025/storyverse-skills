# 短剧 Shots Prompt 制作手册

> 本手册面向负责 AI 短剧分镜生成的抽卡师，涵盖提示词写作、机位建立、表演描述、音频处理等核心方法论。

---

## 第一章 基础认知

### 什么是 Shots Prompt

Shots Prompt 是一条 15 秒以内的 AI 生成视频片段对应的提示词，每条对应剧本中的一个 **Beat（节拍）**。每条 Beat 有明确的戏剧目的、情绪弧线和镜头方案。

### 提示词的两种类型

根据是否有站位参考图，提示词分为两种模式：


|                | 无站位图模式                       | 有站位图模式                         |
| -------------- | ---------------------------------- | ------------------------------------ |
| **适用场景**   | 新场景首次制作                     | 已有站位图的延续场景                 |
| **空间描述**   | 必须用文字详细描述所有位置关系     | 图片承载空间信息，文字聚焦表演和机位 |
| **提示词长度** | 较长                               | 可适当精简                           |
| **参考图附件** | 可附前一条 Beat 的尾帧作 scene-ref | 附专门生成的站位图                   |

**原则：只要有站位图，就用。没有时，前一条 Beat 的尾帧也可以作为 scene-ref。**

---

## 第二章 提示词标准结构

每条 shots prompt 按以下区块顺序组织：

```
[REFERENCE]        角色资产图 + 站位参考图
[SPATIAL ANCHOR]   空间锚点与位置关系
[GOAL]             这条 Beat 的核心戏剧目的（1-3句）
[CHARACTER STATES] 每个角色在这条 Beat 里的情绪状态
[SHOT PLAN]        分镜方案（含时间戳、机位、动作）
[DIALOGUE]         台词（仅限实际开口说的话，V.O.不在此处）
[EXPORT]           输出格式与音频说明
[NEGATIVE]         明确禁止生成的内容
```

### 无站位图时的 SPATIAL ANCHOR 写法

需要详细描述每个角色的位置和朝向：

```
[SPATIAL ANCHOR]
Julian: screen-left, facing screen-right toward Amber.
Amber: screen-right, facing screen-left toward Julian.
Archway exit behind Amber at screen-right.
Grand palace ballroom floor. Chandelier warmth.
Height differential: both at floor level.
```

### 有站位图时的 SPATIAL ANCHOR 写法

图片承载空间信息，文字只补充关键变化：

```
[SPATIAL ANCHOR]
Reference: attached scene-ref (staging image).
All character positions match this image.
Key change this beat: Amber steps back from Julian
toward screen-right during Shot B.
```

---

## 第三章 角色锚定

### 核心原则：外貌描述代替人名

AI 工具不认识角色名字，只认识服装和外貌特征。

```
❌ "Julian faces Amber and speaks."
✓ "【a Hispanic man in black tuxedo — dark wavy hair】
   faces 【a White woman in gold dress — sapphire tiara】
   and speaks."
```

### 角色区分区块（多人场景必写）

```
CRITICAL CHARACTER DISTINCTION:
<char-A> = 外貌特征。站位。这条 Beat 的核心行为。
<char-B> = 外貌特征。站位。这条 Beat 的核心行为。
Do NOT conflate any of these.
```

### 服装状态追踪

角色在剧情中的服装/造型变化必须同步更新资产描述：

- 戴上王冠前：`a White woman in gold dress`（无冠）
- 戴上王冠后：`a White woman in gold dress — sapphire tiara`（有冠）

**一旦状态改变，后续所有 Beat 使用新描述。**

---

## 第四章 站位图的生成与使用

### 什么时候需要生成新站位图

- 新场景开始时
- 角色空间关系发生较大变化时（如从台阶对峙变为地面平层对峙）
- 新角色加入，且站位需要重新确认时

### 站位图生成提示词要素

```
Hyper-realistic cinematic vertical (9:16) still frame.
[场景描述]

CAMERA: Side angle, capturing both characters at full
  body height, facing each other. Eye level.

LEFT FIGURE — 【角色A外貌描述】:
  Standing facing screen-right. [姿态描述]

RIGHT FIGURE — 【角色B外貌描述】:
  Standing facing screen-left. [姿态描述]

BACKGROUND: [背景描述]

NEGATIVE: No text. No extra characters.
  Do NOT alter costume colors.
```

### 使用站位图的注意事项

1. 站位图作为 `scene-ref` 附在 `[REFERENCE]` 区块的最后一张
2. **避免多余参考图**——若参考图中角色姿态与当前 Beat 不符，AI 会被误导
3. 每次空间关系发生变化时，重新生成站位图并更新 scene-ref

---

## 第五章 摄影机位建立

### 核心方法：四要素空间描述法

不要用"主观镜头""正反打"等电影术语，改用空间坐标描述：


| 要素             | 说明               | 示例                                        |
| ---------------- | ------------------ | ------------------------------------------- |
| **摄影机在哪里** | 空间坐标           | 台阶顶部 / 地面层 / 台阶侧面                |
| **朝哪个方向拍** | 方向               | pointing DOWN / looking UP / facing outward |
| **主体面朝哪里** | 面向摄影机 or 背向 | face toward camera                          |
| **背景是什么**   | 验证机位是否正确   | background: lower stairs and hall floor     |

```
❌ "POV shot from Amber's perspective"
✓ "Camera positioned at throne level at the top of the
   staircase, pointing DOWNWARD toward Olivia below.
   Olivia's face is toward the camera.
   Background: lower staircase and hall floor below her.
   The throne is BEHIND the camera — NOT in background."
```

### 正面镜头的机位推导

**场景**：角色 A 在高处，角色 B 在低处仰视 A，想拍 B 的正面。

```
错误：摄影机放在 B 旁边 → B 背对 A（背对镜头）
正确：摄影机放在 A 和 B 之间（比 B 高）→ B 脸朝摄影机
```

```
Camera: positioned on the stairs ABOVE 【char-B】,
  between her and the throne, pointing DOWN at her face.
  Background: lower staircase and hall floor below her.
  Throne is BEHIND the camera — NOT visible in frame.
```

### 常用机位速查


| 拍摄意图         | 摄影机位置       | 拍摄方向              | 背景           |
| ---------------- | ---------------- | --------------------- | -------------- |
| 仰视高位角色正面 | 低位（地面层）   | 向上（pointing UP）   | 天花板/吊灯    |
| 俯视低位角色正面 | 高位（台阶上方） | 向下（pointing DOWN） | 下方地面/人群  |
| 正面对峙（A脸）  | A 身后，B 侧     | 朝 A（facing A）      | A 身后的空间   |
| 台阶场景正面近景 | 台阶侧，朝外朝下 | 朝外朝下              | 大厅地面和人群 |

---

## 第六章 视线方向规范

### 正反打轴线推导

切换正反打时，画面空间翻转：

- Shot A：Amber 看向 screen-left（Julian 在她左边）
- 切到 Julian 反打后，空间翻转
- Julian 应看向 **screen-LEFT**（不是 screen-right）

**口诀：两人视线在同一条轴上，方向相反。**

### 视线方向与摄影机的关系

当角色的视线方向与摄影机方向重合时，**不要强制要求"不看镜头"**，这会导致视线偏移、表情奇怪。

```
✓ "Her gaze directed UPWARD past the camera toward
   Amber's position above — looking at Amber,
   not at the camera lens itself."
```

### 视线方向锁定写法（NEGATIVE）

```
GAZE LOCK — ALL SHOTS:
  【char-A】gaze: UPWARD toward throne throughout.
    Do NOT render her looking sideways or at camera.
  【char-B】gaze: DOWNWARD toward floor base.
    Do NOT render him looking at Olivia or at camera.
```

---

## 第七章 走位描述规范

### 走位描述三要素

每次描述角色移动，必须同时说明：

1. **移动方向**（朝哪里走）
2. **移动中面朝哪里**（是否转身）
3. **停止后面朝哪里**

```
❌ "Amber steps back."
   → AI 解读为：先转身，再向后走（背对对方）

✓ "Amber takes one step AWAY from Julian — toward the
   archway exit behind her, along the confrontation axis.
   Her body does NOT turn. Her face and chest remain
   directed toward Julian throughout the movement."
```

### 常见走位陷阱


| 描述             | AI 的错误解读 | 正确写法                                                  |
| ---------------- | ------------- | --------------------------------------------------------- |
| "steps back"     | 先转身再退    | + "body does NOT turn"                                    |
| "turns to leave" | 背对所有人    | + "face remains toward Julian as she turns"               |
| "steps closer"   | 方向不明确    | + "moves toward screen-left along the confrontation axis" |

---

## 第八章 情绪表演描述规范

### 用物理表现替代抽象情绪词

AI 无法渲染"悲伤""愤怒"等抽象词，需要转化为可视化的物理表现：

```
❌ "She looks devastated."
✓ "A fine tremor visible in her hands and shoulders.
   Her voice is steady despite the trembling body.
   Her jaw does not quiver. Her eyes are dry."
```

### 情绪细化对照表


| 情绪                 | 不要写                | 应该写                                                                                                         |
| -------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------- |
| 冷漠讥讽             | "she is contemptuous" | "cold precision with a trace of something that is almost pity — not angry, contemptuous"                      |
| 外表平静内心恐慌     | "she hides her fear"  | "composed surface over fast-moving interior — her eyes carry the weight, and only barely"                     |
| 声音颤抖             | "her voice trembles"  | "the voice breaks once — a single controlled crack, not a flood. It does NOT break again."                    |
| 表演情绪 vs 真实情绪 | "she cries"           | "the tears draw from genuine grief channeled into a false conclusion — she is lying, but the emotion is real" |

### 非说话角色也需要情绪指令

当角色 A 说话时，角色 B 不能是雕像，必须给出当下情绪：

```
【char-B】soft-focus to her left: his posture settled,
  watching Julian — the expression of someone not
  worried about how this goes. NOT blank or frozen.
```

### 表演夸张度控制

剧本里的动作描述需要翻译成 AI 可以执行的适当力度：


| 剧本描述                             | 提示词翻译                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| "slams his hand against her stomach" | "places his hand firmly against her abdomen — decisive, not violent"                            |
| "recoils"                            | "one small involuntary step or lean back — not dramatic stumbling"                              |
| "whirls to face him"                 | "a decisive pivot — not a slow graceful movement. Shot B opens with her already facing Julian." |

---

## 第九章 音频处理规范

### V.O. / 内心独白（三步处理法）

**错误做法**：把 V.O. 放在 `[DIALOGUE]` 区块 → AI 生成角色开口说台词。

**正确做法**：

**第一步**：V.O. 不出现在 `[DIALOGUE]` 区块。

**第二步**：在 `[EXPORT]` 区块的 Audio 部分描述：

```
01.50: NARRATION TRACK ONLY — pre-recorded voice-over,
  completely decoupled from visual performance:
  "If he knows I'm the Princess, he'll never let me go."
  No lip movement. Audio and visual are independent tracks.
```

**第三步**：在 `[NEGATIVE]` 里锁定：

```
V.O. AUDIO LOCK — CRITICAL:
  The narration is PRE-RECORDED VOICE-OVER.
  【角色】lips do NOT move during this audio.
  Do NOT sync any lip movement to the narration.
  Visual (still face) and audio (narration) are
  INDEPENDENT tracks.
```

**额外技巧**：当角色背对镜头时播放 V.O.，嘴巴不可见，天然规避口型同步问题。

### 正反打 O.S. 对话重叠

当摄影机切到听者（说话人出画），说话人的声音作为画外音继续播放：

```
[Shot B — 听者的镜头]
Action: 【char-B】receiving 【char-A】's words.
  【char-A】's voice continues OFF-SCREEN (O.S.)
  during this shot. 【char-B】's mouth is CLOSED.
  He is listening, not speaking.

[NEGATIVE]
O.S. AUDIO LOCK — Shot B:
  【char-B】lips do NOT move.
  Do NOT sync any lip movement to the O.S. audio.
```

### 静默场景的音频设计

```
[EXPORT] Audio:
  Shot A: complete silence — only fabric sounds and
    physical strain. NO voice from Olivia.
  Shot B: only Julian's labored breathing audible.
    The room is otherwise completely silent.
  Do NOT fill silence with ambient music or crowd sounds.
```

### Reference Audio 音色参考

如果工具支持上传参考音频，可以用来锁定角色音色，比文字描述更稳定。

**两种情况的处理方式：**

**情况 A：工具只支持单条 reference audio（全局应用）**
只能锁定一个音色（通常是主角）。直接在 UI 里上传，提示词无需额外标注。

**情况 B：工具支持多条 reference audio（按角色分别绑定）**
需要在 `[REFERENCE]` 区块里明确映射关系：

```
[REFERENCE]
Attach:
(image1) <char-amber> a White woman; brown wavy hair...
(image2) <char-julian> a Hispanic man; dark wavy hair...
(audio1) <voice-amber> reference audio for
  【a White woman in gold dress — sapphire tiara】
  American English. Female.
(audio2) <voice-julian> reference audio for
  【a Hispanic man in black tuxedo】
  American English. Male.
```

> ⚠️ **抽卡师检查项**：每次写提示词前，确认以下两点：
>
> 1. 本条 Beat 涉及哪几个角色开口说话？
> 2. 每个说话角色是否已绑定对应的 reference audio？
>
> 如果工具支持多角色音色绑定，未绑定的角色可能回退到默认音色，导致音色不一致。

---

### 口音锁定（防止英音漂移）

AI 在宫廷、王室等正式场景中容易将美式英语漂移为英式英语。每条 shots prompt 的 `[EXPORT]` 区块中必须加入音色规格：

```
[EXPORT]
...
VOICE: All spoken dialogue in American English accent.
  Pronunciation: American, not British.
  Do NOT use British English vowel sounds,
  intonation patterns, or RP (Received Pronunciation).
```

同时在 `[NEGATIVE]` 里加：

```
Do NOT generate British English accent or RP
  (Received Pronunciation) for any character.
  All characters speak American English throughout.
```

**触发英音的常见原因：**


| 触发因素       | 说明                                                       |
| -------------- | ---------------------------------------------------------- |
| 场景联想       | 宫殿、王座、礼服等视觉信号与英式英语强关联                 |
| 用词风格       | "endorsement""bloodline""heir"等词在训练数据中英式语境更多 |
| 跨 Beat 无锁定 | 每条 Beat 独立生成，无音色记忆，自然漂移                   |

**结论**：口音锁定必须写在每一条 shots prompt 里，不能依赖跨 Beat 的持续效果。

---

## 第十章 节拍拆分规范

### 15 秒内容评估


| 内容类型           | 估算时长 |
| ------------------ | -------- |
| 短台词（5词以内）  | 1.5-2s   |
| 中等台词（一句话） | 2.5-4s   |
| 长台词（复合句）   | 5-7s     |
| 简单物理动作       | 1-2s     |
| VFX 动作序列       | 3-5s     |
| 情绪 Hold          | 2-4s     |
| V.O. 独白          | 3-5s     |

每条 Beat 内容总量控制在 **13-14s**，留 1-2s 余量。

### 拆分判断原则

- **VFX 序列**单独或接近单独放一条——需要呼吸空间
- **卡点台词**（炸弹台词/关键反转）放在 Beat 末尾，配合 Hold
- **情绪弧线完整性** > 内容塞入量
- 单条超过 15s 时，找自然的情绪断点拆开

### 卡点设计原则

```
好的卡点特征：
- 台词已落地，但角色还没有回应
- 反应留给下一条 Beat（或下一集）
- 最后一个画面是悬而未决的表情或状态
```

---

## 第十一章 NEGATIVE 区块写作规范

NEGATIVE 是提示词的保险层。**每一个你不希望出现、但 AI 有可能默认生成的内容，都应该在这里明确禁止。**

### 常用锁定类型速查


| 锁定类型 | 示例写法                                                                    |
| -------- | --------------------------------------------------------------------------- |
| 情绪锁定 | `Do NOT render Amber as tearful or trembling.`                              |
| 走位锁定 | `Do NOT render Amber with her back to Julian.`                              |
| 道具锁定 | `No physical document appears. Neither character holds any paper.`          |
| 高度锁定 | `Do NOT flatten any character to the same level as another.`                |
| 音频锁定 | `Do NOT fill the silence with ambient music or crowd sounds.`               |
| 口型锁定 | `Lips do NOT move during the narration track.`                              |
| 视线锁定 | `Do NOT render Olivia looking at Julian during this line.`                  |
| 表情锁定 | `Do NOT render a wide-open screaming mouth. She is choking, not screaming.` |
| 服装锁定 | `TIARA: visible on 【gold dress】in all shots. Do NOT remove it.`           |
| 背景锁定 | `Do NOT show the throne in background of Shot A.`                           |
| 口音锁定 | `Do NOT generate British English accent for any character.`                 |

### 写 NEGATIVE 的思考流程

生成前问自己：

1. AI 最可能把这个角色渲染成什么样？如果不对，锁定它。
2. 哪个走位动作容易被误解？锁定方向和身体朝向。
3. 有没有不该出现的道具？锁定。
4. 背景应该是什么？不该出现什么？锁定。
5. 有没有 V.O.？锁定口型。
6. 有没有 O.S. 对话？锁定听者口型。
7. 场景是否容易触发英音？锁定口音。
8. 本条 Beat 有哪几个角色开口说话？每个说话角色是否已绑定 reference audio？

---

## 第十二章 道具 vs 台词的区分

当台词中提到某个物品，但该物品不需要在画面中实际出现时，必须明确说明。

**典型案例**：台词说"签离婚协议"，但画面里不应该出现协议。

```
[GOAL] 或 [SPATIAL NOTE] 里说明：
  "The divorce papers are SPOKEN OF ONLY —
   no physical document appears at any point."

[NEGATIVE] 里锁定：
  No physical document appears in any shot.
  Neither character holds, reaches for, or gestures
  toward any paper or document.
```

---

## 第十三章 常见问题与解决方案

### Q1：角色背对说话对象

**原因**：走位描述未锁定身体朝向。

**解决**：

```
加入：Her body does NOT turn away from Julian.
     Her face and chest remain directed toward him
     throughout and after the movement.
NEGATIVE 加：Do NOT render [角色] with her back to [对方].
```

### Q2：视线方向错误（看向错误的角色）

**原因**：正反打轴线推导错误，或未锁定视线方向。

**解决**：

```
在 SHOT PLAN 的 Action 里明确：
  His gaze directed screen-LEFT-upward toward
  [目标角色]'s position.
NEGATIVE 加：
  Do NOT let [角色] look screen-right.
  Do NOT let [角色] look at [错误的角色].
```

### Q3：V.O. 时角色嘴巴在动

**原因**：V.O. 放在了 DIALOGUE 区块。

**解决**：把 V.O. 移出 DIALOGUE，放入 AUDIO 区块，并在 NEGATIVE 加 V.O. AUDIO LOCK。

### Q4：楼梯出现在错误的背景里

**原因**：摄影机位置描述不准确，或参考图与当前 Beat 不符。

**解决**：

```
明确描述背景应该是什么：
  Background: lower staircase and hall floor below her.
  The throne is BEHIND the camera — NOT visible.
NEGATIVE 加：
  Do NOT show the throne/top of stairs in background.
```

### Q5：角色表情过于夸张或空洞

**原因**：情绪描述使用了抽象词汇，没有给具体的物理表现。

**解决**：将抽象情绪翻译成可视化的物理细节，参考第八章情绪细化对照表。

### Q6：非说话角色像雕像

**原因**：提示词只描述了说话角色，没有给非说话角色的当下情绪指令。

**解决**：在每个 Shot 的 Action 描述中，对每个入画的角色都给出情绪/姿态指令，哪怕只是一句话。

### Q7：口音从美音变成英音

**原因**：宫殿场景 + 正式台词触发英式英语联想，且每条 Beat 独立生成无音色记忆。

**解决**：

```
[EXPORT] 里加：
  VOICE: All spoken dialogue in American English accent.
  Do NOT use British English vowel sounds or
  RP (Received Pronunciation).

[NEGATIVE] 里加：
  Do NOT generate British English accent for any character.
```

每一条 shots prompt 都必须单独写，不能省略。

### Q8：多角色场景音色不一致

**原因**：工具支持多条 reference audio 但只上传了一条，其他角色回退到默认音色。

**解决**：

```
确认每个说话角色都已绑定 reference audio。
如果工具支持多角色绑定，在 [REFERENCE] 区块里
为每个说话角色写对应的 audio 映射：

(audio1) <voice-amber> reference audio for
  【a White woman in gold dress — sapphire tiara】
(audio2) <voice-julian> reference audio for
  【a Hispanic man in black tuxedo】
```

---

## 附录：提示词简洁度原则

随着经验积累，可以适当精简提示词：

- **有站位图时**：SPATIAL ANCHOR 可以大幅压缩，图片承载空间信息
- **机位稳定时**：重复使用同一机位名称（如 CAM-AMBER），不需要每次重新描述
- **角色情绪一致时**：CHARACTER STATES 可以只描述变化，不重复稳定的部分
- **但 NEGATIVE 永远不能省**：越复杂的场景，NEGATIVE 越重要

**判断提示词是否足够的标准**：你自己读完，能不能脑补出一个清晰的镜头画面？如果不能，说明某个地方还不够具体。
