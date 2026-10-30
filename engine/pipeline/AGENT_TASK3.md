# 任务：给「全部题解」写动画视频配置（灵茶山艾府 / yiduobo）

你在 `/home/claude/lc_video/`（已经写好的视频引擎）里工作。

## 开工前（只做一次）
1. 完整读一遍 `README.md`（配置格式、视图、字幕、卡片、质量清单）。
2. 看 2 份已完成的配置当范例：`configs/ling/0011.py`（灵神 · 双指针）和 `configs/yiduobo/0042.py`（yiduobo）。遇到特定数据结构再按需看对应范例：
   - 链表 `configs/ling/0019.py`　树/递归 `configs/ling/0104.py`、`configs/yiduobo2/0112.py`　回溯+调用栈 `configs/ling2/0047.py`
   - 网格 `configs/yiduobo2/0733.py`　DP 表 `configs/ling2/0516.py` 或 `configs/yiduobo2/0516.py`　栈 `configs/ling2/0682.py`
   - 哈希表 `configs/ling2/0567.py`　堆 `configs/ling/0295.py`　字符串 `configs/ling2/0392.py`　设计题 `configs/ling/0146.py`
   - 自定义绘制 `configs/ling2/1422.py`　公式行 `configs/ling2/0977.py`

## 素材
每个分配给你的题号 KEY 有一份简报 `/home/claude/briefs/KEY.md`：题号、难度、**待做**（要写哪位作者的配置、写到哪个文件）、所在刷题路径、灵神题单位置、题目描述、灵神题解（只含 Python 代码）、yiduobo 题解（Python 2 风格代码 + 推导）。

## 每道题要做的
只写简报「待做」里列出的配置：
- `configs/ling_all/KEY.py`（author='灵茶山艾府'）
- `configs/yiduobo_all/KEY.py`（author='yiduobo'）

字段约定：
- `num`：简报里给的值（普通题是整数；`LCR 004`、`LCP 01`、`面试题 17.06` 这类写成字符串）。`title` 用简报标题。
- `category`：简报有「灵神题单位置」就用它的第一段（如 `滑动窗口与双指针`、`动态规划`）；没有就从这 14 个里选最贴切的：滑动窗口与双指针、二分算法、单调栈、网格图、位运算、图论算法、动态规划、常用数据结构、数学算法、贪心与思维、链表、二叉树与回溯、字符串、设计、模拟。两位作者同一题用同一个。
- `tags`：简报「所在刷题路径」里的前两项（没有就 `[]`）；有难度分可以再加 `'难度分 1263'`。
- `technique`：这份题解用的方法，几个字。

步骤：读简报 → 选作者的主要写法（灵神多写法时选题解里主推/最后的优化写法，其余在 summary 一句话带过）→ 代码**逐字照搬**，只做 README 允许的 Python 3 最小修改（yiduobo：整数除法 `/` 一定改成 `//`、`xrange`→`range`、`print x`→`print(x)`、`iteritems`→`items`、`sys.maxint`→`float('inf')`、`cmp` 排序→`functools.cmp_to_key`、删 `:type` docstring；改过就在 summary 写一句「原文为 Python 2 写法，…已改为 …」）→ 选小示例输入（数组 ≤ 10、网格 ≤ 4×5、树 ≤ 9 节点，回溯/递归要控制步数）→ 写 views / watch / captions / cards → 检查。

检查（在你自己的目录里跑，例如 `mkdir -p /tmp/claude-0/$AGENT && cd /tmp/claude-0/$AGENT`）：
- 一律用 **Python 3.12** 跑检查（和 Mac 渲染环境一致）：`PY=/opt/py312/bin/python; [ -x $PY ] || PY=python3`，然后 `$PY /home/claude/lc_video/make.py /home/claude/lc_video/configs/ling_all/KEY.py --steps`：不报错、`expect` 通过、关键行都有讲「为什么」的字幕（比较/移动/更新答案/递归返回）、预估时长 60–180 秒。
- `$PY ... --preview a,b`：每道题至少抽 1 帧（新视图类型或复杂布局抽 2 帧）用 Read 看 PNG，确认视图不重叠不溢出、指针/颜色在表达核心状态。

特殊题型：
- 设计题：多行 `call`，最后一行是表达式（例如把每次操作的返回值收集成列表）。
- 随机题：在 `setup` 里 `import random; random.seed(0)`，`expect` 用固定种子下的真实输出。
- 交互题（如 guess / isBadVersion / MountainArray）：在 `setup` 里定义题目给的 API。
- **作者代码保持原始写法**，不要为了兼容去改写。视频在 Mac 的 **Python 3.12** 上渲染，3.12 能跑的写法都直接用。只有原代码用到 3.12 没有的东西（3.13+ 的新函数）或第三方库（如 `sortedcontainers.SortedList`）时，才在 `setup` 里补一个等价实现，作者代码一字不改，并在 summary 注明。
- 两位作者同一题要体现**各自**的思路与原文（quote 必须摘自各自原文，文案不要雷同）。
- 文案全中文短句；summary 写复杂度、易错点（3–5 行）。

## 引擎的可选开关（默认关闭，只在需要时用）
- `threads=True`：多线程题（如 1114 按序打印、1195 交替打印）。在 `call` 里按 LeetCode 的方式建线程（`threading.Thread(target=..., name='A')`）、全部 start 再 join，最后一行返回输出列表；`setup` 里 `import threading`。引擎会追踪所有线程，字幕/视图里用 `S['_thread']` 显示当前在跑哪个线程；信号量、锁在变量面板里显示成 `Semaphore(1)`、`Lock(free)`。
- `trace_limit=N`：代码里有写死、缩小输入也去不掉的大循环（如固定枚举 512 个状态、固定开 40000 的计数数组）时，只记录前 N 个事件，其余照常执行但不记录，视频末尾自动加一步「后面同理，快进到结束」（可用 `truncated_caption` 改文字）。`expect` 仍必须正确。配合 `snap_maxlen=M`：快照里超长列表只保留前 M 项（视图也只画这 M 项）。

## 灵神原文只有 Go 代码时（简报「待做」里写着「原文为 Go」）
- 把简报里的 Go 代码**逐行等价转写成 Python 3**：函数结构、变量名、循环顺序、注释都保持不变（`for i := 0; i < n; i++` → `for i in range(n)`，切片 → list，map → dict/defaultdict，`math.MaxInt` → `inf`，`sort.Ints(a)` → `a.sort()`，`var dfs func(...)` 闭包 → 嵌套 `def dfs(...)` + `nonlocal`），外层写成 LeetCode Python 的 `class Solution:` + 同名方法。不要加原文没有的优化、不要换算法。
- `technique` 末尾加「（Go 原文转写）」；summary 第一行写「原文为 Go，已按原逻辑逐行转写为 Python」。quote 照抄灵神原文文字。

## 每完成一个配置，立刻同步到 Mac（重要）
额度用完时整个会话会被直接切断，没同步到 Mac 的配置就丢了。所以每个配置（或 skip 文件）**检查通过后马上**同步，不要攒到最后：
1. Bash：`mkdir -p /mnt/user-data/outputs/cfg && cp /home/claude/lc_video/configs/<dir>/KEY.py /mnt/user-data/outputs/cfg/<dir>__KEY.py`（`<dir>` 是 `ling_all` 或 `yiduobo_all`；skip 文件是 `configs/skipped/<dir>/KEY.txt` → `/mnt/user-data/outputs/cfg/skipped__<dir>__KEY.txt`）
2. 调用 `mcp__remote-devices__device_commit_files`（工具还没加载就先用 ToolSearch 加载它）：`stagedPath` = 上面的文件，`devicePath` = `/Users/9s/Documents/LC_Video/engine/configs/<dir>/KEY.py`（skip 文件：`/Users/9s/Documents/LC_Video/engine/configs/skipped/<dir>/KEY.txt`）。可以把同一道题的两个文件放在一次调用里。
3. 同一个配置之后又改了，要再同步一次。工具不可用或报错就跳过这一步，继续干活（编排者最后会统一同步）。

## 什么时候跳过
确实做不了时不要硬写，写一个一行说明到 `configs/skipped/ling_all/KEY.txt` 或 `configs/skipped/yiduobo_all/KEY.txt`，例如：
- `题意不明`：简报没有题面，yiduobo 文章也看不出题意，而你对这道题没有把握（不要编题意）。
- `无代码`：题解里没有可用的 Python 代码。
- `无法演示`：多线程 / 数据库 / Shell 题，或代码依赖无法在小输入上运行的东西。
写了配置就不要再写 skip，反之亦然。

## 规则
- **不要修改** engine.py / views.py / make.py / tracer.py / common.py / batch.py / hot100.py / sets.py / allsets.py / repo.py / README.md，也不要碰别人的配置和简报。引擎不够用时用 `custom` / `text` 视图。
- 不要渲染 mp4，只用 `--steps` 和 `--preview`。只写你的配置文件、skip 文件和你自己的临时目录。
- 效率：每个配置通常 2–4 次 `--steps` 就够，别无限打磨；但「关键行讲为什么」和 `expect` 正确不能省。

## 最终回复（要短）
每个配置一行：`ling_all/KEY.py  OK  步数  预估秒数`；跳过的写 `SKIP yiduobo_all/KEY  原因`。不要贴配置内容。
