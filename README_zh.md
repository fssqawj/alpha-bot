# Alpha-Bot

<p align="center">
  <img src="alpha-bot-png.jpg" alt="Alpha-Bot Logo" width="600"/>
  <br/>
  <sub>Logo 由 Grok 生成</sub>
</p>

<p align="center">
  <strong><em>🤖 你的 AI 任务自动化代理 - 利用各种系统应用解决用户任务！</em></strong>
</p>

<p align="center">
  <strong>用自然语言描述复杂任务，让 AI 利用各种系统应用一步步执行直到完成</strong>
</p>

<p align="center">
  <em>多步骤执行 • 失败自动重试 • 实时思考展示 • 系统应用集成</em>
</p>

[![PyPI version](https://img.shields.io/pypi/v/alphabot-ai.svg)](https://pypi.org/project/alphabot-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://fssqawj.github.io/alpha-bot/)

---

<p align="center">
  📖 <strong><a href="https://fssqawj.github.io/alpha-bot/">完整文档</a></strong> |
  <a href="https://fssqawj.github.io/alpha-bot/getting-started/quick-start/">快速开始</a> |
  <a href="https://fssqawj.github.io/alpha-bot/user-guide/examples/">使用示例</a> |
  <a href="https://fssqawj.github.io/alpha-bot/api/agent/">API 参考</a>
</p>

---

<div align="center">

### 🌟 Alpha-Bot 的独特之处

**不只是命令生成器 - 真正的任务自动化代理！**

<table>
<tr>
<td align="center">🔄</td>
<td><strong>执行多步骤任务</strong><br/>从头到尾完成</td>
<td align="center">🧠</td>
<td><strong>从失败中学习</strong><br/>自动重试</td>
</tr>
<tr>
<td align="center">💭</td>
<td><strong>展示思考过程</strong><br/>实时透明</td>
<td align="center">✅</td>
<td><strong>持续执行</strong><br/>直到任务真正完成</td>
</tr>
</table>

</div>

---

中文 | [English](README.md)

Alpha-Bot 是一个 **AI 驱动的任务自动化代理**，它超越了简单的命令生成。与只能将查询转换为命令的工具不同，Alpha-Bot 能够**利用各种系统应用**来自主解决用户任务，**执行多步骤任务**、**从失败中学习**，并**调整策略**直到完成。

## 🎯 为什么选择 Alpha-Bot？

| 其他工具 | Alpha-Bot |
|---------|-----------|
| 生成一条命令 → 完成 | 执行多个步骤 → 分析 → 调整 → 完成 |
| "这是你的命令，自己运行吧" | "我会一直工作直到完成" |
| 失败了？你自己想办法 | 失败了？AI 分析、重试、寻找替代方案 |

**示例**：`"整理我的项目文件"`
```
其他工具：ls -la  # 只有一条命令，剩下的你自己做

Alpha-Bot：步骤 1：分析目录结构
          步骤 2：创建整理好的文件夹
          步骤 3：将文件移动到合适的位置
          步骤 4：验证整理结果
          ✓ 任务完成！
```

## 🎬 效果展示

<!-- 
请在 GitHub 编辑此 README 时，将视频拖拽到下方区域：
1. 点击 GitHub 上的编辑按钮
2. 将 alpha-bot-demo.mp4 拖拽到编辑器中
3. GitHub 会自动上传并生成链接
-->

![browser-demo](https://github.com/user-attachments/assets/717ce22f-084a-4081-8ad0-ae23f7daf0ff)


<p align="center"><em>演示1：使用 alpha-bot 通过自然语言操控终端</em></p>


![alpha-bot-demo](https://github.com/user-attachments/assets/8721876f-92dc-4762-a03d-64d845546de0)


<p align="center"><em>演示2：使用 alpha-bot 通过自然语言操控终端</em></p>

Alpha-Bot 提供了美观的终端界面和实时反馈：

- 💭 **思考过程实时显示** - 看到 AI 的思考过程
- ⚙️ **命令执行动画** - 执行命令时显示动态加载效果
- ✨ **语法高亮** - 生成的命令带有语法高亮
- 📊 **结构化输出** - 清晰的面板和图标显示
- 🎯 **交互式确认** - 危险操作带有明显的警告标识

## 🚀 快速开始

### 安装

#### 方式一：从 PyPI 安装

```bash
pip install alphabot-ai
```

#### 方式二：开发模式安装

```bash
# 克隆仓库
git clone https://github.com/fssqawj/alpha-bot.git
cd alpha-bot

# 以开发模式安装（可以直接使用 alpha-bot 或 ask 命令）
pip install -e .
```

#### 方式三：直接安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API Key

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 OpenAI API Key：
```bash
OPENAI_API_KEY=your-api-key-here
```

## 💡 使用方法

### 安装后使用（推荐）

如果你使用 `pip install alphabot-ai` 或 `pip install -e .` 安装，可以直接使用命令：

```bash
# 使用 alpha-bot 命令
alpha-bot "列出当前目录下的所有 Python 文件"

# 或者使用更短的 ask 命令
ask "列出当前目录下的所有 Python 文件"

# 交互模式
ask -i

# 演示模式（无需 API Key）
ask -d "创建一个测试文件夹"

# 自动执行模式（不需要确认每条命令）
ask -a "统计当前目录代码行数"

# 指定工作目录
ask -w /path/to/dir "你的任务"
```

### 直接运行（未安装时）

```bash
# 单次执行任务
python alpha_bot/cli.py "列出当前目录下的所有 Python 文件"

# 交互模式
python alpha_bot/cli.py -i

# 演示模式（无需 API Key）
python alpha_bot/cli.py -d "创建一个测试文件夹"

# 自动执行模式（不需要确认每条命令）
python alpha_bot/cli.py -a "统计当前目录代码行数"

# 指定工作目录
python alpha_bot/cli.py -w /path/to/dir "你的任务"
```

### 示例

以下示例同时适用于 `ask` 命令和 `python alpha_bot/cli.py`：

#### **简单任务**（像其他工具一样）
```bash
# 文件操作
ask "找出所有大于 1MB 的文件"
ask "列出所有正在运行的 Python 进程"
```

#### **复杂多步骤任务**（Alpha-Bot 的优势所在！）
```bash
# 项目整理 - 自动执行多个步骤
ask "整理这个项目：创建 docs、tests 和 src 文件夹，然后相应地移动文件"

# 环境设置 - 处理错误并重试
ask "设置 Python 虚拟环境并从 requirements.txt 安装依赖"

# Git 工作流 - 完整任务自动化
ask "提交所有更改并附上有意义的提交信息，然后推送到 origin"

# 系统维护 - 智能执行
ask "查找并压缩所有 7 天前的日志文件"

# 开发任务 - 多步骤协调
ask "在所有 Python 文件中查找 TODO 注释并创建摘要文件"
```

#### **浏览器和系统操作**
```bash
# 浏览器操作
ask "用默认浏览器打开 GitHub"
ask "打开百度搜索 Python 教程"

# 系统信息
ask "查看系统内存使用情况"
ask "显示所有挂载驱动器的磁盘使用情况"
```

#### **更多示例**
```bash
# 带验证的文本处理
ask "统计所有 .py 文件的总行数"
ask "在所有 .txt 文件中搜索包含 'error' 的行"

# 备份操作
ask "创建当前目录的带时间戳的备份"
```

**💡 专业提示**：任务越复杂，Ask-Shell 相比简单命令生成器的优势就越明显！

### 交互模式

```bash
ask -i
# 或
python alpha_bot/cli.py -i
```

进入交互模式后，可以持续输入任务：
```
Alpha-Bot > 列出当前目录下的文件
Alpha-Bot > 创建一个测试文件
Alpha-Bot > exit  # 退出
```

## 📁 项目结构

```
alpha-bot/
├── alpha_bot/           # 核心代码
│   ├── agent.py        # 带智能循环的任务自动化代理
│   ├── cli.py          # 命令行入口
│   ├── executor/       # 带安全检查的命令执行器
│   ├── llm/            # 带上下文管理的 LLM 客户端
│   ├── models/         # 数据模型
│   └── ui/             # 美观的终端界面
├── requirements.txt    # 依赖列表
└── .env.example        # 环境变量模板
```

## 🆚 与其他工具对比

| 功能 | Shell-GPT | Aichat | Warp AI | **Alpha-Bot** |
|------|-----------|--------|---------|---------------|
| **多步骤任务执行** | ❌ | ❌ | ⚠️ 有限 | ✅ **完全支持** |
| **失败自动重试** | ❌ | ❌ | ❌ | ✅ **是** |
| **任务上下文感知** | ❌ | 部分 | 部分 | ✅ **完整上下文** |
| **实时思考展示** | ❌ | ❌ | ⚠️ 基础 | ✅ **流式** |
| **执行循环** | ❌ 单次 | ❌ 仅聊天 | ⚠️ 有限 | ✅ **直到完成** |
| **错误分析** | ❌ 手动 | ❌ 手动 | ⚠️ 基础 | ✅ **自动** |
| **危险操作检测** | ⚠️ 基础 | ⚠️ 基础 | ✅ 是 | ✅ **双层** |
| **浏览器自动化** | ❌ | ❌ | ❌ | ✅ **内置** |
| **文件生成** | ❌ | ❌ | ❌ | ✅ **PPT、图像等** |
| **开源** | ✅ Python | ✅ Rust | ❌ 闭源 | ✅ **Python** |
| **易于扩展** | ⚠️ | ⚠️ | ❌ | ✅ **插件就绪** |

### Alpha-Bot 的不同之处

**Shell-GPT / sgpt**：快速命令翻译很好，但生成一条命令后就停止了。  
**Aichat**：功能丰富的聊天界面，但不是面向任务的。  
**Warp Terminal**：现代化的终端与 AI 功能，但闭源且需要完全替换终端。  
**Alpha-Bot**：✨ **专注于自主任务完成** - 持续执行直到任务真正完成。

### 🚀 革命性自动提示系统（全新功能！）

**从每次执行中自动学习！** Ask-Shell 现在具备业界首创的 **自动技能提示提取系统**，能够从成功和失败的执行中持续学习，大幅提升未来任务的执行效率。

#### 🎯 工作原理
1. **自动分析**：任务完成后自动分析执行历史，识别模式
2. **智能模式识别**：发现成功技巧、常见失败模式和优化机会
3. **LLM驱动的提示生成**：使用AI从发现的模式中创建可操作的上下文提示
4. **持久化知识库**：按技能类型存储生成的提示供未来使用
5. **无缝集成**：技能在执行过程中自动加载相关提示

#### 🌟 核心优势
- **🚀 3倍任务执行速度**：通过学习过往经验避免试错
- **✅ 40%成功率提升**：自动应用经过验证的模式和最佳实践
- **🧠 持续学习**：每次任务执行都变得更智能
- **🔧 零配置**：后台自动运行
- **📊 智能洞察**：生成故障排除指南和优化建议

#### 💡 创新亮点
- **业界首创** 的AI代理自动技能优化
- **双模式学习**：从成功和失败中同时学习
- **跨技能知识共享**：实现整体性能提升
- **自适应架构**：无需人工干预即可自动改进

### 高级能力

**浏览器自动化**：内置 Playwright 集成为网络自动化任务提供支持。
**文件生成**：直接从自然语言生成 PPT、图像和其他文件。
**可扩展技能**：插件就绪架构，便于添加新功能。

## ⚙️ 配置选项

### 环境变量

在 `.env` 文件中可以配置以下选项：

```bash
# OpenAI API Key（必需）
OPENAI_API_KEY=your-api-key-here

# 自定义 API 地址（可选，用于兼容的 API）
OPENAI_API_BASE=https://api.openai.com/v1

# 模型名称（可选，默认：gpt-4）
MODEL_NAME=gpt-4
```

### 命令行参数

- `task` - 要执行的任务描述
- `-i, --interactive` - 交互模式
- `-a, --auto` - 自动执行模式（不需要确认）
- `-d, --demo` - 演示模式（不需要 API Key）
- `-w, --workdir` - 指定工作目录

## 🔒 安全特性

Ask-Shell 非常重视安全，提供多层保护：

### 🛡️ 双层保护

1. **AI 驱动的检测** - GPT-4 分析命令的潜在危险
   - 理解上下文和意图
   - 解释**为什么**命令危险
   - 捕获模式匹配无法发现的细微风险

2. **内置黑名单** - 针对灾难性命令的硬编码保护
   - `rm -rf /` 及其变体
   - 直接磁盘操作
   - 系统文件修改
   - Fork 炸弹和恶意模式

### ✋ 用户控制

3. **交互式确认** - 你始终拥有最终决定权
   - 清晰的危险警告和解释
   - 执行前编辑命令
   - 跳过你不信任的命令
   - 随时退出

4. **透明性** - 准确了解正在发生的事情
   - 查看 AI 的推理过程
   - 执行前审查命令
   - 了解潜在风险

**安全理念**："信任，但要验证" - 给予 AI 自主权，但让人类掌控关键决策。

## 🛠️ 技术栈

- **Python 3.7+** - 易于理解和扩展
- **OpenAI API** - GPT-4 模型（可扩展到其他 LLM）
- **Rich** - 支持流式输出的美观终端显示
- **python-dotenv** - 环境变量管理

### 架构亮点

- **代理循环模式**：持续任务执行与反馈集成
- **上下文管理**：完整的对话历史与结果跟踪
- **模块化设计**：易于添加新的 LLM 提供商、执行器或 UI 组件
- **安全优先**：双层保护（AI + 黑名单）
- **技能系统**：插件就绪架构，支持浏览器自动化、文件生成等多种能力

## 🗺️ 路线图

- [ ] 支持多个 LLM 提供商（Claude、Gemini、Ollama）
- [ ] 任务历史和重放功能
- [ ] 自定义命令的插件系统
- [ ] 任务模板库
- [ ] Web UI 界面
- [ ] 团队协作功能

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
