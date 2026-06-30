# Keyframe 完整案例 + Beat 精简 SPATIAL ANCHOR 写法

第一次写 Keyframe、或拿不准某个字段怎么填时，对照这个端到端案例。

## 案例来源

*Divorced Now, a Lycan Princess* SC15 · Julian 豪宅客厅。

**场景信息（来自 Spatial Bible）**

- 场景：Julian 的豪宅客厅，夜晚，壁炉点亮
- 角色 A（Amber）：白人女性，棕色波浪长发，金色晚礼服，蓝宝石头冠（初次与 Julian 对峙时未戴头冠）
- 角色 B（Julian）：拉丁裔男性，深色卷发，黑色西装黑色衬衫领口微开，凌乱发型，血丝眼（对峙前情绪激动）
- 核心家具：中央茶几（FRN-02）、右侧大型书桌（FRN-01）、后方壁炉（FRN-04）
- 光源：壁炉（暖琥珀色，轻微闪烁）+ 吊灯（柔和金色）

## 完整 Keyframe Prompt（可作参照标准）

```
Hyper-realistic cinematic vertical (9:16) still frame.
A grand mansion living room — high ceilings, dark wood paneling, Persian rugs,
low fireplace glow from the back wall.

CAMERA: Side angle, capturing both characters at full body height, facing
  each other across the center of the room. Eye level. CAM-D position:
  front-left corner, diagonal view across the room.

LEFT FIGURE — 【a White woman with brown wavy hair — gold evening gown,
  no tiara, bare shoulders】:
  Standing facing screen-right toward Julian. Posture tense but composed.
  Arms slightly away from body, hands open at her sides. Firelight catching
  her bare shoulders from behind.

RIGHT FIGURE — 【a Hispanic man with dark wavy black hair — black suit,
  black shirt open at collar, slightly disheveled】:
  Standing facing screen-left toward Amber. Posture tight, jaw set.
  One hand loosely at his side, the other slightly raised as if mid-gesture.
  Bloodshot eyes, shadows under them.

FOREGROUND: Low rectangular coffee table (FRN-02) in the foreground center,
  dark wood surface, empty. Polished marble floor catches the firelight.

BACKGROUND: Back wall with active fireplace (FRN-04) slightly screen-left of
  center — low amber flame, subtle flicker. Large mahogany writing desk
  (FRN-01) background screen-right. Tall double doors (DOOR-01) background
  screen-left, closed. Two household servants barely visible in deep
  background, one near each side wall.

LIGHT: Primary — fireplace (FRN-04), warm amber, directional from screen-back-left,
  flickers subtly. Catches Amber's bare shoulders and the left side of
  Julian's face. Secondary — overhead chandelier, soft warm gold, even fill,
  casts brass highlights on desk edges and polished floor.

MOOD: Charged standoff in an opulent room — the space between them is dense
  with unspoken history.

STYLE: Photoreal, cinematic, 4K, vertical 9:16 frame.
  No text, no subtitles, no watermarks. Shallow depth of field,
  both characters sharp, background slightly soft.

NEGATIVE: No text. No extra characters in foreground. No subtitles.
  No watermarks. Do NOT alter costume colors — gold gown stays gold,
  black suit stays black. Do NOT show any jewelry on Amber (no tiara,
  no necklace, no earrings, no bracelet at scene start).
  Do NOT show DOOR-01 as open. Fireplace flame must be LOW and warm,
  not roaring.
```

## 三个关键决策讲解

**为什么用 CAM-D（侧面交叉）而不是 CAM-A（建立宽景）**
侧面机位能让两个角色都以正面/四分之三面朝镜头，方便后续确认面孔一致性；宽景机位拍出的是背面或极远景，不利于角色识别。

**为什么写 "servants barely visible in deep background"**
Spatial Bible 记录了两个仆人在背景区域。不写的话 AI 可能随机添加或完全省略，导致后续 Beat 背景突然出现不明人物。在 Keyframe 里预置他们，锁定空间配置。

**NEGATIVE 里为什么锁 "no jewelry on Amber"**
SC15 剧情是 Amber 逐件脱下首饰，开场时戴着全套，但 Keyframe 要建立的是**场景初始状态**。如果 AI 从资产图里自动给她戴上头冠，后续脱首饰的戏剧节奏会被破坏。凡是剧情中会发生变化的元素，开场状态都要在 NEGATIVE 里钉死。

---

## Beat 提示词里的精简 SPATIAL ANCHOR 写法

Keyframe 生成并质检通过后，后续每条 Beat 的 `[SPATIAL ANCHOR]` 用这个简写模式——图片锁住不变的空间，文字只追踪变化：

```
[SPATIAL ANCHOR — {场景名称} · SC{编号}]
Ground truth from attached reference frame (<scene-ref>):
All furniture positions, landmark IDs, and room proportions match
the reference image. Do not deviate from room geometry in any shot.

LIGHT SOURCES (unchanged from reference):
  {LGT-01}: {光源描述，直接从 Spatial Bible 复制}
  {LGT-02}: {光源描述}

CHARACTER POSITIONS AT START OF THIS BEAT:
  {角色A}: {本 Beat 开始时位置，与 Keyframe 相同则写 "same as reference"}
  {角色B}: {本 Beat 开始时位置}

SCENE UPDATE FROM BEAT {N-1}:
  {如有变化追加更新；无变化则省略此段}
```

**注意**：即使有了图片，LIGHT SOURCES 仍然必须用文字描述。AI 无法从图片准确判断光源动态（壁炉闪烁、日光变化），必须文字补充。
