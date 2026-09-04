# Baixing-Hans-skills

Claude Code 技能(Skills)合集,存放可复用的个人技能包。

## 技能列表

| 技能 | 说明 |
| --- | --- |
| [soft-moat-infographic](skills/soft-moat-infographic/SKILL.md) | 生成柔和粉彩风格的中文信息图卡片(对比卡片 / 三步论证流程),HTML/CSS 渲染导出图片 |

## 使用方式

**项目级使用**:把 `skills/` 目录放在项目根目录下,Claude Code 会自动发现其中的技能。

**全局使用**:把需要的技能目录复制到 `~/.claude/skills/`:

```bash
# Windows (PowerShell)
Copy-Item -Recurse skills/soft-moat-infographic "$env:USERPROFILE\.claude\skills\"

# macOS / Linux
cp -r skills/soft-moat-infographic ~/.claude/skills/
```

## 目录结构

```
skills/
└── soft-moat-infographic/
    ├── SKILL.md            # 技能定义(入口)
    ├── agents/             # agent 配置
    ├── assets/             # 示例数据
    ├── references/         # 风格指南等参考资料
    └── scripts/            # 渲染脚本
```

## 新增技能

每个技能一个目录,放在 `skills/` 下,必须包含 `SKILL.md`(带 name / description frontmatter)。可以用 Claude Code 的 `skill-creator` 技能辅助生成。
