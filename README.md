# StoryVerse Skills

StoryVerse 的公开 [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) 集合。当前聚焦 **AI 短剧（竖屏 9:16 微短剧）生成流水线**中的提示词写作方法论——把"靠人传帮带"的抽卡经验，沉淀成 Claude 能稳定调用的结构化技能。

## 包含的 Skills

| Skill | 解决什么 | 在流水线里的位置 |
|-------|----------|------------------|
| [`keyframe-prompt`](./skills/keyframe-prompt) | 为一个场景生成 **Keyframe / 空间基准帧**（一张静止图），把 Spatial Bible 的文字空间锁成图像锚，作为 `scene-ref` 反复挂到每个 Beat，解决空间随机漂移 | Spatial Bible 之后、写 Beat 之前 |
| [`shots-prompt-writing`](./skills/shots-prompt-writing) | 把**单个 Beat** 写成 AI 能稳定生成的 15 秒视频提示词：八区块结构、机位推导、视线轴线、走位三要素、情绪物理化、音频处理、NEGATIVE 锁定 | 写 Beat 这一步（流水线最后一环） |

> **流水线全貌**：完整方法论（体量测算 → 定集数时长 → 切 Beat → 建 Spatial Bible → 备资产 → 写提示词 → 质检）由上游的 `ai-short-drama-storyboard` skill 承载，本仓库的两个 skill 是其中相邻两步的深挖版。如需把 storyboard 一并纳入本仓库，直接把它的目录放进 `skills/` 即可，结构通用。

## 目录结构

```
storyverse-skills/
├── README.md
├── LICENSE                        # ⚠️ 公开前需确认授权方式（见下）
├── package_all.sh                 # 一键把每个 skill 打包成 .skill
├── skills/                        # 源码（仓库的权威内容）
│   ├── keyframe-prompt/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   └── references/
│   └── shots-prompt-writing/
│       ├── SKILL.md
│       └── references/
└── dist/                          # 打包产物，方便一键安装（可由 package_all.sh 重新生成）
    ├── keyframe-prompt.skill
    └── shots-prompt-writing.skill
```

约定：每个 skill 一个独立文件夹放在 `skills/` 下，文件夹名 = `SKILL.md` frontmatter 里的 `name`。新增 skill 时照此放入并在上表登记即可。

## 安装与使用

**方式一：在 Claude.ai / Claude App 用打包文件（推荐给非技术同事）**
下载 `dist/` 里对应的 `.skill` 文件 → Claude 的 Settings → Capabilities → Skills → 上传。装好后是账号级技能，所有对话自动触发，无需每次往 project 里塞参考文件。

**方式二：在 Claude Code 用源码**
克隆本仓库，把 `skills/<name>/` 指给 Claude Code 的 skills 目录（或按团队约定挂载）。源码是权威版本，`.skill` 只是打包快照。

触发无需记命令——正常描述需求即可，命中 skill 描述里的场景就会自动调用，例如"把这个 Beat 写成 shots prompt""给这场戏建一张 Keyframe""这条提示词帮我质检"。

## 重新打包

改了任意 `skills/<name>/` 后，重新生成 `dist/`：

```bash
./package_all.sh
```

脚本依赖 Anthropic skill-creator 的 `package_skill.py`；若环境不同，按 `package_all.sh` 顶部注释调整路径。

## ⚠️ 公开前注意

两个 skill 的 `SKILL.md` frontmatter 目前标注为「内部方法论」。本仓库要对外公开，请在发布前确认：
1. 这些方法论是否适合公开（是否含未脱敏的项目/角色/剧本细节）；
2. 选定授权方式并补全 `LICENSE`（当前为占位）。
