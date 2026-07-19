[![skills.sh](https://skills.sh/b/KeVINWKZ/Materials-SKILL)](https://skills.sh/KeVINWKZ/Materials-SKILL)
<div align="center">

<img src="skills/materials-research-guide/assets/materials-research-guide-icon.png" alt="Materials Research Guide" width="176">

# Materials Skills

Evidence-grounded AI skills for materials-science research.

[![skills.sh](https://skills.sh/b/KeVINWKZ/Materials-SKILL)](https://skills.sh/KeVINWKZ/Materials-SKILL)
![License](https://img.shields.io/badge/license-MIT-c7ced8)

</div>

## Available skills

### Materials Research Guide

为任意材料体系生成有文献依据的实验方案、表征矩阵、竞争机理、创新点评估和论文框架。要求核验来源，并明确区分直接证据、外推、工程筛选起点和证据缺口。

- Skill ID：`materials-research-guide`
- Version：`2.1.0`
- Source：[skills/materials-research-guide](skills/materials-research-guide)

v2.1.0 增加学术检索 Skill 联动、无检索工具时的证据降级、紧凑模式轻量审计、无直接文献时的工程起点规则，以及常见材料领域的方法标准入口。

## Install

查看仓库中可安装的 Skill：

```bash
npx skills add KeVINWKZ/Materials-SKILL --list
```

安装 Materials Research Guide：

```bash
npx skills add KeVINWKZ/Materials-SKILL --skill materials-research-guide --agent codex -g -y
```

也可以安装仓库中的全部 Skill：

```bash
npx skills add KeVINWKZ/Materials-SKILL --all
```

安装完成后可这样调用：

```text
使用 $materials-research-guide，为我的材料体系制定有可核验文献依据的研究方案。
```

## Repository structure

```text
Materials-SKILL/
├── skills.sh.json
├── README.md
├── LICENSE.md
└── skills/
    └── materials-research-guide/
        ├── SKILL.md
        ├── agents/
        ├── assets/
        ├── examples/
        ├── references/
        ├── scripts/
        └── skillhub-metadata.json
```

后续新增 Skill 时，在 `skills/<skill-name>/` 下创建新的 Skill 目录，并将其 slug 加入根目录的 `skills.sh.json` 对应分组。

## Development and validation

```bash
python skills/materials-research-guide/scripts/validate_input.py skills/materials-research-guide/examples/sample-input.json
python skills/materials-research-guide/scripts/audit_output.py skills/materials-research-guide/examples/sample-report.md --mode complete --min-sources 3
python skills/materials-research-guide/scripts/package_skill.py skills/materials-research-guide
```

## Safety

Skill 输出是研究设计辅助材料，不能替代实验室 EHS 审批、SDS、设备 SOP、专业监督或真实实验验证。请勿向仓库提交 API Token、私有论文全文、内部数据或个人凭据。

## License

MIT License. See [LICENSE.md](LICENSE.md).
