# 任务：为「更多题单」（面试经典 150 / 热题 173 / 字节 30 天高频 / List.md）写动画视频配置

你在 `/home/claude/lc_video/`（已经写好的视频引擎）里工作。先完整读一遍 `README.md`（配置格式、视图、字幕、卡片、质量清单），再挑 2 份已完成的 Hot100 配置当范例看（例如 `configs/ling/0011.py`、`configs/yiduobo/0042.py`、`configs/ling/0739.py`、`configs/yiduobo/0236.py`，`configs/` 下共有 216 份可参考）。

## 素材
- `/home/claude/lc_video/extra.json`：本批题目清单，字段 num/title/sets/ling/yiduobo（文件名，null 表示该作者没有题解）
- `/home/claude/data/extra/ling/NNNN.md`：灵茶山艾府题解（含题目描述 callout、多种写法；行首 `> ` 是 callout 前缀，代码要去掉它）
- `/home/claude/data/extra/yiduobo/NNNN.md`：yiduobo 题解（推导文字 + Python 2 风格代码）。注意：127 用的是他「126 单词接龙II & 127 单词接龙」那篇；140 用的是他 139 那篇里给的 140 代码。
- `/home/claude/data/extra/html/NNNN.html`：部分题目的题面（来自“LeetCode 热题 173 道”），灵神没有题解时用它写题意；都没有时按你对这道 LeetCode 题的了解写题意，并用 `expect` 跑通示例来自证。

## 每道题要做的
对分配给你的每个题号，**作者有题解才写**：
- `configs/ling2/NNNN.py`（author='灵茶山艾府'）
- `configs/yiduobo2/NNNN.py`（author='yiduobo'）

`category` 必须从下面 20 个里选一个最贴切的（决定视频放哪个文件夹，两位作者同一题用同一个）：
哈希、双指针、滑动窗口、子串、普通数组、矩阵、链表、二叉树、图论、回溯、二分查找、栈、堆、贪心算法、动态规划、多维动态规划、技巧、数学、字符串、设计
（“子串”指前缀和/子数组类；“技巧”指位运算、摩尔投票等；“设计”指设计数据结构类题。）
`tags` 里放该题所属题单，从 `extra.json` 的 `sets` 字段照抄（如 `['面试经典150', '字节30天']`）。

步骤：读题解 → 选作者的主要写法，代码逐字照搬（只做 README 允许的 Python 3 最小修改，yiduobo 的 `/` 整除一定要改成 `//` 并在 summary 注明）→ 选小示例输入 → 写 views/watch/captions/cards → `python make.py <cfg> --steps` 迭代到：不报错、expect 通过、关键行都有讲“为什么”的字幕、预估时长 60–180 秒 → `python make.py <cfg> --preview a,b` 抽 2 帧用 Read 看图确认布局。
- 两位作者同一题要体现**各自**的思路与原文（quote 必须摘自各自原文）。
- 文案简体中文短句；summary 写复杂度、易错点。

## 规则
- **不要修改** engine.py / views.py / make.py / tracer.py / common.py / batch.py / hot100.py / README.md，也不要碰别人的配置。引擎不够用时用 `custom` / `text` 视图。
- 不要渲染 mp4，只用 `--steps` 和 `--preview`。不要写 /home/claude/lc_video 以外的地方。

## 最终回复
简短列出写好的配置、步数/预估时长、`--steps` 是否全部通过；没写的题说明原因（例如作者没题解、题解不是 Python 等）。
