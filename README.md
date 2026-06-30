# StoryVerse Skills

<p align="center">
  <a href="#english"><img alt="Read in English" src="https://img.shields.io/badge/Read-English-111111?style=for-the-badge"></a>
  <a href="#中文"><img alt="阅读中文" src="https://img.shields.io/badge/%E9%98%85%E8%AF%BB-%E4%B8%AD%E6%96%87-666666?style=for-the-badge"></a>
</p>

<a id="english"></a>

## English

StoryVerse Skills is a set of `SKILL.md`-based agent skills for Claude, Codex, OpenClaw, Hermes, and other agents that support the Agent Skills / progressive-disclosure pattern. The current skills focus on the most drift-prone prompt-writing steps in an AI vertical short-drama pipeline:

1. Turn a Spatial Bible into a reusable Keyframe / scene-ref staging image.
2. Turn a single Beat into a stable 15-second shots prompt for AI video tools.

This repository only contains agent skill source folders and packaged `.skill` artifacts. It does not include the old `/sv-*` pipeline slash commands, backend API docs, LangSmith prompt archives, or sample project state files.

The `skills/` directories are the portable source format. The `dist/*.skill` files are packaged snapshots for agents that support `.skill` uploads.

### Skills

| Skill | Purpose | Contents |
| --- | --- | --- |
| [`keyframe-prompt`](./skills/keyframe-prompt) | Write Keyframe / scene-ref prompts for new scenes, major staging changes, or new character entrances | `SKILL.md`, a Keyframe fill-in template, a full example, and a concise Beat-level `SPATIAL ANCHOR` pattern |
| [`shots-prompt-writing`](./skills/shots-prompt-writing) | Turn one Beat into a video generation prompt under 15 seconds and quality-check it | Eight-block prompt structure, appearance-based character anchoring, camera-position reasoning, eyeline axis, blocking, physicalized emotion, audio handling, NEGATIVE locks, and troubleshooting |

### Repository Layout

```text
storyverse-skills/
├── README.md
├── LICENSE
├── package_all.sh
├── dist/
│   ├── keyframe-prompt.skill
│   └── shots-prompt-writing.skill
└── skills/
    ├── keyframe-prompt/
    │   ├── SKILL.md
    │   ├── assets/keyframe-template.txt
    │   └── references/case-and-anchor.md
    └── shots-prompt-writing/
        ├── SKILL.md
        └── references/shots-prompt-manual.md
```

`skills/` is the source of truth. `dist/` contains upload-ready `.skill` package snapshots for compatible clients.

### Install

Use the source folders for Codex, OpenClaw, Hermes, and other local agents. Use `dist/*.skill` only when your client supports packaged `.skill` uploads.

#### Claude.ai / Claude App

Download a `.skill` file from `dist/`, then upload it in Claude Settings -> Capabilities -> Skills.

#### Claude Code / Local Skills

Copy or symlink the source folders into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/keyframe-prompt ~/.claude/skills/
cp -R skills/shots-prompt-writing ~/.claude/skills/
```

If your Claude Code setup uses a different skills path, keep the same folder shape: each skill directory must contain its own `SKILL.md`.

#### Codex

Install as user-level skills:

```bash
mkdir -p ~/.agents/skills
cp -R skills/keyframe-prompt ~/.agents/skills/
cp -R skills/shots-prompt-writing ~/.agents/skills/
```

Or install repo-scoped skills inside a project:

```bash
mkdir -p .agents/skills
cp -R /path/to/storyverse-skills/skills/keyframe-prompt .agents/skills/
cp -R /path/to/storyverse-skills/skills/shots-prompt-writing .agents/skills/
```

Codex detects skill changes automatically; restart Codex if the skills do not appear. See the [Codex Agent Skills docs](https://developers.openai.com/codex/skills).

#### OpenClaw

Install into the active workspace:

```bash
openclaw skills install ./skills/keyframe-prompt --as keyframe-prompt
openclaw skills install ./skills/shots-prompt-writing --as shots-prompt-writing
```

Install globally for all local OpenClaw agents:

```bash
openclaw skills install ./skills/keyframe-prompt --as keyframe-prompt --global
openclaw skills install ./skills/shots-prompt-writing --as shots-prompt-writing --global
```

OpenClaw local installs expect `SKILL.md` at the source root. See the [OpenClaw Skills docs](https://docs.openclaw.ai/tools/skills).

#### Hermes

Copy source folders into Hermes' skills directory:

```bash
mkdir -p ~/.hermes/skills/storyverse
cp -R skills/keyframe-prompt ~/.hermes/skills/storyverse/
cp -R skills/shots-prompt-writing ~/.hermes/skills/storyverse/
```

Then start a new session or reset the current one so Hermes refreshes its skills list. Hermes also supports `hermes skills install` for supported sources. See the [Hermes Skills System docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) and [Working with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills).

#### Other agents

Use the same portable layout:

```text
<agent-skills-root>/
└── keyframe-prompt/
    ├── SKILL.md
    ├── assets/
    └── references/
```

If the agent supports the Agent Skills standard, point it at the `skills/<name>/` directories or copy those directories into its configured skills root.

### When To Use

Use `keyframe-prompt` when:

- A new scene starts and you need to lock furniture, light sources, character positions, and the camera coordinate system.
- The spatial relationship within a scene changes enough to require a new scene-ref.
- An existing Keyframe result drifts in character orientation, staging, or room proportions.

Use `shots-prompt-writing` when:

- You already have a single Beat and need a prompt for Seedance, Kling, Runway, Veo, or a similar video tool.
- You need to reason through shot / reverse-shot framing, eyeline direction, character blocking, or background camera placement.
- You need to handle V.O., O.S., reference audio, lip sync, accent drift, or NEGATIVE locks.
- You need to diagnose why a generated shot has wrong backs, wrong eyelines, exaggerated acting, incorrect backgrounds, or inconsistent voices.

### Repackage

After changing `skills/`, regenerate `dist/*.skill`:

```bash
./package_all.sh
```

The script expects Anthropic's skill-creator `package_skill.py` at its default path. If your local path is different, override it with:

```bash
PACKAGER_DIR=/path/to/skill-creator ./package_all.sh
```

### Maintenance Notes

- Keep one directory per skill. The directory name should match the `name` field in `SKILL.md` frontmatter.
- Keep templates and long references inside that skill's own `assets/` or `references/` folder.
- After updating source files, rerun `./package_all.sh` and commit the matching `dist/*.skill` files.
- `LICENSE` is still a placeholder. Before public distribution, replace it with a real license and align each `SKILL.md` frontmatter `license` field.

[中文](#中文)

---

<a id="中文"></a>

## 中文

StoryVerse Skills 是一组基于 `SKILL.md` 的 Agent Skills，适用于 Claude、Codex、OpenClaw、Hermes，以及其他支持 Agent Skills / progressive-disclosure 模式的 agent。当前 skills 聚焦 AI 短剧（竖屏 9:16 微短剧）生成流水线里最容易漂移的两个提示词环节：

1. 把 Spatial Bible 落成一张可复用的 Keyframe / scene-ref 空间基准帧。
2. 把单个 Beat 写成 AI 视频工具能稳定生成的 15 秒 shots prompt。

这个仓库只保留 agent skill 源码目录和 `.skill` 打包产物，不包含旧版 `/sv-*` pipeline slash commands、backend API 文档、LangSmith prompt 归档或示例项目状态文件。

`skills/` 目录是可跨 agent 使用的源码格式；`dist/*.skill` 是给支持 `.skill` 上传的客户端使用的打包快照。

### Skills

| Skill | 用途 | 主要内容 |
| --- | --- | --- |
| [`keyframe-prompt`](./skills/keyframe-prompt) | 为新场景、重大站位变化或新角色加入生成 Keyframe / scene-ref 提示词 | `SKILL.md`、Keyframe 填空模板、完整案例和 Beat 内精简 `SPATIAL ANCHOR` 写法 |
| [`shots-prompt-writing`](./skills/shots-prompt-writing) | 把一个 Beat 写成 15 秒以内的视频生成 prompt，并做质量检查 | 八区块结构、角色外貌锚定、机位推导、视线轴线、走位、情绪物理化、音频、NEGATIVE、排障手册 |

### 目录结构

```text
storyverse-skills/
├── README.md
├── LICENSE
├── package_all.sh
├── dist/
│   ├── keyframe-prompt.skill
│   └── shots-prompt-writing.skill
└── skills/
    ├── keyframe-prompt/
    │   ├── SKILL.md
    │   ├── assets/keyframe-template.txt
    │   └── references/case-and-anchor.md
    └── shots-prompt-writing/
        ├── SKILL.md
        └── references/shots-prompt-manual.md
```

`skills/` 是权威源码；`dist/` 是给兼容客户端上传安装的 `.skill` 打包快照。

### 安装

Codex、OpenClaw、Hermes 和其他本地 agent 优先使用 `skills/` 源码目录；只有客户端支持 `.skill` 上传时，才使用 `dist/*.skill`。

#### Claude.ai / Claude App

下载 `dist/` 里的 `.skill` 文件，在 Claude 的 Settings -> Capabilities -> Skills 上传。

#### Claude Code / 本地 Skills

把源码目录复制或链接到 Claude Code 的 skills 目录：

```bash
mkdir -p ~/.claude/skills
cp -R skills/keyframe-prompt ~/.claude/skills/
cp -R skills/shots-prompt-writing ~/.claude/skills/
```

如果你的 Claude Code 配置使用不同 skills 路径，保持同样目录形态即可：每个 skill 目录里必须有自己的 `SKILL.md`。

#### Codex

安装为用户级 skills：

```bash
mkdir -p ~/.agents/skills
cp -R skills/keyframe-prompt ~/.agents/skills/
cp -R skills/shots-prompt-writing ~/.agents/skills/
```

或者安装为某个项目内的 repo-scoped skills：

```bash
mkdir -p .agents/skills
cp -R /path/to/storyverse-skills/skills/keyframe-prompt .agents/skills/
cp -R /path/to/storyverse-skills/skills/shots-prompt-writing .agents/skills/
```

Codex 通常会自动检测 skill 变更；如果没有出现，重启 Codex。参考 [Codex Agent Skills 文档](https://developers.openai.com/codex/skills)。

#### OpenClaw

安装到当前 workspace：

```bash
openclaw skills install ./skills/keyframe-prompt --as keyframe-prompt
openclaw skills install ./skills/shots-prompt-writing --as shots-prompt-writing
```

安装为所有本地 OpenClaw agents 可见的全局 skills：

```bash
openclaw skills install ./skills/keyframe-prompt --as keyframe-prompt --global
openclaw skills install ./skills/shots-prompt-writing --as shots-prompt-writing --global
```

OpenClaw 的本地安装要求源码根目录直接包含 `SKILL.md`。参考 [OpenClaw Skills 文档](https://docs.openclaw.ai/tools/skills)。

#### Hermes

把源码目录复制到 Hermes skills 目录：

```bash
mkdir -p ~/.hermes/skills/storyverse
cp -R skills/keyframe-prompt ~/.hermes/skills/storyverse/
cp -R skills/shots-prompt-writing ~/.hermes/skills/storyverse/
```

然后开启新 session，或 reset 当前 session，让 Hermes 刷新 skills list。Hermes 也支持对兼容来源使用 `hermes skills install`。参考 [Hermes Skills System 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) 和 [Working with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)。

#### 其他 agents

使用同样的可移植目录结构：

```text
<agent-skills-root>/
└── keyframe-prompt/
    ├── SKILL.md
    ├── assets/
    └── references/
```

如果该 agent 支持 Agent Skills 标准，就把它指向 `skills/<name>/` 目录，或者把这些目录复制到它配置的 skills root。

### 什么时候用

使用 `keyframe-prompt`：

- 新场景开始，需要先锁定家具、光源、角色站位和机位坐标系。
- 同一场戏内空间关系大幅变化，需要新的 scene-ref。
- 已有 Keyframe 生成结果不稳定，角色朝向、站位或空间比例漂移。

使用 `shots-prompt-writing`：

- 已经有单个 Beat，需要写成 Seedance、Kling、Runway、Veo 等视频工具可用的 prompt。
- 需要推导正反打、视线方向、角色走位或背景机位。
- 需要处理 V.O.、O.S.、reference audio、口型同步、口音漂移或 NEGATIVE 锁定。
- 需要质检一条 shots prompt 为什么生成结果背对、视线错、表情过度、背景错或音色不一致。

### 重新打包

改动 `skills/` 后重新生成 `dist/*.skill`：

```bash
./package_all.sh
```

脚本默认寻找 Anthropic skill-creator 的 `package_skill.py`。如果你的本地路径不同，用环境变量覆盖：

```bash
PACKAGER_DIR=/path/to/skill-creator ./package_all.sh
```

### 维护说明

- 每个 skill 一个目录，目录名需要和 `SKILL.md` frontmatter 里的 `name` 一致。
- skill 需要的模板和长参考文档放在该 skill 自己的 `assets/` 或 `references/` 下。
- 更新源码后，重新运行 `./package_all.sh` 并提交对应的 `dist/*.skill`。
- 当前 `LICENSE` 仍是占位文件；公开分发前需要替换为正式授权条款，并同步检查各 `SKILL.md` frontmatter 的 `license` 字段。

[English](#english)
