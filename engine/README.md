# lc_video — LeetCode 题解动画生成器

把一份「大神题解」变成 1–3 分钟的讲解视频：

```
① 开场（题号/题名/作者/一句话/复杂度）
① 题意
② 大神原文的核心思路（引用原文 + 2–3 条解释）
③ 逐步动画：真正执行大神的代码，逐行高亮 + 数据结构可视化 + 变量面板 + 自动字幕
④ 小结 & 易错点
```

引擎会**真正运行**配置里的代码（`sys.settrace` 逐行追踪），每一步的数组、指针、哈希表、栈、链表、树、网格都是从真实变量画出来的，所以动画不会和代码对不上。每道题只需要写一个配置文件。

## 依赖

Python ≥ 3.10、`pip install pillow pygments`、`ffmpeg`、Noto Sans CJK 字体（`/usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc`；macOS 可 `brew install --cask font-noto-sans-cjk`，然后改 `engine.py` 里的 `FONT_DIR`）。

## 命令

```bash
python make.py configs/ling/0011.py --steps            # 只跑追踪，打印每一步的行号和字幕 + 预估时长（秒级，先用它检查）
python make.py configs/ling/0011.py --preview 20,40,-3 # 把第 20/40/倒数第 3 个关键帧存成 PNG 到 ./preview/
python make.py configs/ling/0011.py out.mp4            # 渲染（1080p/25fps，约 0.7× 实时）
python batch.py                                        # 批量渲染所有配置到 out/，已存在则跳过
python hot100.py render DEST --jobs 5 --budget 110 [--part 0/2] [--newer EPOCH]
                                                       # 直接渲染到归档目录；--part 把任务分给多个并行进程；--newer 重渲早于该时间的视频
python sets.py render <Leetcode>/题单动画 --jobs 3 --budget 100 [--part 0/2] [--newer EPOCH]
                                                       # 「更多题单」（面试经典150/热题173/字节30天/List.md）的配置在 configs/ling2、configs/yiduobo2
python sets.py index <Leetcode>/题单动画                 # 重建 00 题单动画索引.md（每个题单一张表，Hot100 题链到 hot100动画）
pip install av                                         # 装了 PyAV 会自动用变帧率编码，只编码变化的帧，快 3–5 倍
```

## 配置文件格式

`configs/<作者>/<4 位题号>.py`，作者目录：`ling`（灵茶山艾府）、`yiduobo`、`concept`（分类概念讲解）。文件里定义一个 `CONFIG` 字典。配置文件里可以直接用 `L([...])`、`Tr([...])`、`list_vals`、`tree_list`、`ListNode`、`TreeNode` 以及颜色名。

```python
CONFIG = dict(
    num=11, title='盛最多水的容器', difficulty='Medium',      # Easy / Medium / Hard
    category='双指针',                 # hot100 分类名（17 个之一），显示为标签
    author='灵茶山艾府',               # 或 'yiduobo' / '概念讲解'
    technique='相向双指针',            # 开场副标题：作者 · technique
    tags=[],                           # 额外标签（可选）

    code='''                           # 作者原版代码（逐字照搬，Python 3 可运行；见下方“代码规则”）
class Solution:
    def maxArea(self, height: List[int]) -> int:
        ...
''',
    call='Solution().maxArea([1,8,6,2,5,4,8,3,7])',   # 驱动表达式；多行时最后一行必须是表达式
    expect=49,                         # 必填：返回值必须等于它，否则直接报错（保证动画正确）
    result_fn=None,                    # 可选：比较前先转换返回值，如 list_vals（链表）/ tree_list（树）
    setup='',                          # 可选：call 之前执行的语句（不追踪）

    views=[...],                       # 可视化视图，从上到下排列（见下）
    watch=['left', 'right', ('ans', 'ans', 'green')],  # 底部变量面板：名字 或 (显示名, 表达式[, 颜色])
    captions={...},                    # 字幕模板（见下），未覆盖的行自动生成字幕
    skip=[],                           # 包含这些子串的代码行（或行号 int）不单独成一步（例如很碎的赋值）
    max_steps=70,                      # 步数上限；超出时保留前面大部分 + 最后 12 步，中间显示“快进”
    cards=dict(...),                   # 文案卡片（见下）
)
```

### 可选开关（默认关闭）

- `threads=True`：同时追踪 `call` 里启动的线程（多线程题）；每步带线程名 `S['_thread']`，信号量/锁在快照里显示成 `Semaphore(1)` / `Lock(free)`。
- `trace_limit=N`：只记录前 N 个追踪事件，之后代码照常跑完但不再记录，末尾自动加一步「快进到结束」（`truncated_caption` 可改文字）。用于写死的大循环。
- `snap_maxlen=M`：快照里超过 M 项的列表只保留前 M 项（配合 `trace_limit`，避免每步深拷贝超大数组）。

### 代码规则

- **逐字照搬作者代码**，只做让它在 Python 3 跑起来的最小修改：
  - yiduobo 常见：`/` 用于整数除法 → `//`；`xrange` → `range`；`print x` → `print(x)`；`dict.iteritems()` → `.items()`；`sys.maxint` → `float('inf')`；删掉 `"""type ..."""` 文档字符串（它占行又没信息量）。改了什么要在小结卡片里写一句「原文为 Python 2 写法，…已改为 …」。
  - 灵神常见：一题给多种写法，选**题解里最主要/最推荐**的那种（通常是最后的优化写法或标题点名的写法），其余写法在小结里一句话带过。
  - LeetCode 预置的 `List/Optional/ListNode/TreeNode/Node/defaultdict/Counter/deque/heapq/bisect/cache/inf/accumulate/pairwise/...` 都已注入，无需 import。
- 代码的注释原样保留：引擎会把**行尾注释**拼到该行的自动字幕前面（灵神的注释就是最好的字幕）。
- 代码太长（> ~32 行）时代码面板会自动滚动，可以接受。
- 输入用题目示例或更小的例子：数组长度 ≤ 8～10、网格 ≤ 4×5、树 ≤ 7～9 个节点；回溯/递归题要保证步数不爆（先 `--steps` 看）。

### views（视图）

每个视图是一个 dict，`type` 决定画法，`h` 是相对高度（会按比例缩放填满左侧面板）。表达式都在“当前这一步执行完后”的变量环境里求值（递归时内层变量优先）；表达式也可以是 `lambda S: ...`（`S` 是变量字典，`S.x` 也行）。

| type | 用途 | 关键参数 |
|---|---|---|
| `array` / `string` | 一维数组、字符串格子 | `var`、`pointers={'left':'blue','right':'pink'}`（值为整数的变量/表达式画成下标箭头，会平滑移动）、`window=('left','right')`（闭区间高亮框）、`color=lambda S,i,v: 'green' or None`、`dim=lambda S,i,v: bool`、`cell`（格宽上限，默认 84）、`label`、`index=False` 关闭下标 |
| `bars` | 柱状图（高度=数值），适合接雨水、容器、单调栈 | 同 `array`，外加 `vmax` |
| `map` / `set` | 哈希表 / 集合，新增或改动的键黄色描边 | `var`、`fmt=lambda k, v: str`（set 为 `lambda x: str`）、`font` |
| `stack` / `queue` / `heap` | 栈、队列(deque)、堆（数组形式），新入的绿色 | `var`、`fmt=lambda x: str`（如 `lambda i: f'{i}:{T[i]}'`）、`top_color` |
| `grid` / `table` | 二维网格 / DP 表 | `var`、`cursors=[('i','j','yellow','(i,j)')]`、`color=lambda S,i,j,v: ...`、`rows`/`cols`（表头列表或表达式）、`values=False`、`cell` |
| `linked` | 链表（所有能从变量走到的节点，自动布局：输入的第 k 条链在第 k 行，运行中新建的节点在最后一行；支持环、random 指针） | `pointers={'pre':'pink','cur':'blue'}` |
| `tree` | 二叉树（自动找全树；黄圈 = 当前递归路径上的节点） | `var`（可省略）、`pointers`、`color=lambda S, node: ...`、`path=False` 关闭黄圈（迭代写法时用） |
| `calls` | 递归调用栈（函数名 + 参数），递归/回溯题强烈建议加 | `h`、`hide=('preorder',)` 隐藏长参数 |
| `intervals` | 区间列表画在数轴上 | `var`、`out`（结果区间变量）、`pointer`（当前下标变量） |
| `text` | 一行公式/说明，如 `area = (r−l)×min(..) = 18` | `fn=lambda S: '...'`（支持 \`code\` 和 ==强调== 标记）、`size` |
| `custom` | 自由绘制（兜底） | `draw=lambda cv, S, B, box, T: ...`（`cv.rect/line/text/arrow/rich` 等，见 engine.Canvas） |

颜色名：`blue pink green purple cyan yellow orange red`。

回调里 `S['_line']` 是当前高亮的行号，`S['_inner']` 是只含最内层栈帧的局部变量（递归时避免拿到外层的旧值）（可以用来区分“正在跑哪个循环”）。`text` 视图的 `fn` 也可以写成两个参数 `lambda S, B: ...` 拿到执行前的值。

注意：`==强调==` 里面不能再嵌套反引号或 `=`；Noto CJK 缺 ⌊ ⌋ ✗ ⁿ 等少数符号，用 `floor()`、`×`、`^n` 代替。
同一行在 Python 3.12+ 的列表推导式里会触发多次，引擎只保留连续同一行的最后一次。

### captions（字幕）

自动字幕已经不错：`if/while` 会算出条件真假和两边的值（`判断 height[left] < height[right]（1 < 7）→ 成立`），赋值会列出变化的变量（`cnt['a'] = 2`、`st 末尾加入 3`、`cur.next = ListNode(1)`），`return` 会显示返回值，进入递归会提示“进入新的一层”，行尾注释会拼在前面。

需要讲“为什么”的关键行，用模板覆盖：键是**代码行里的子串**（或行号 int），值是 f-string 风格模板，`{...}` 里可以写任意表达式：当前变量直接用名字，执行前的值用 `B.name`，返回值用 `ret`。也可以给一个函数 `lambda S, B, ret: str`。字幕支持 \`code\` 和 ==强调==。

```python
captions={
    'area = (': '当前容器：宽 `{right-left}` × 高 `min({height[left]}, {height[right]})` = =={area}==',
    'ans = max': '`ans = max({B.ans}, {area}) = {ans}`',
    'left += 1': '左边更矮 → 它和右边任何线都组不出更大面积，扔掉：`left` → {left}',
}
```

模板求值出错会自动退回默认字幕，所以不会崩；但要用 `--steps` 看一遍，确认没有退回。

### cards（文案卡片）

全部中文，短句，每行一屏能读完（≤ 45 字）。\`code\` 显示为代码样式，==文字== 显示为强调色。

```python
cards=dict(
    one_liner='每次扔掉较矮的那根线',                  # 开场一句话：这题的“灵魂”
    complexity='时间 `O(n)`，空间 `O(1)`',
    problem=['...题意 1–3 行，含示例输入输出...'],
    quote='...作者原文里最关键的一段（尽量原文照录，≤ 90 字）...',
    quote_src='—— 灵茶山艾府题解',                      # 可选
    idea=['...用自己的话把原文讲透，2–3 行...'],
    result='（可选）结束时的字幕，默认是“运行结束，返回 …”',
    summary=['复杂度…', '易错点…', '同类题/模板…'],     # 3–5 行
    before=[dict(heading='...', lines=[...])],          # 可选：思路卡之前插入的额外卡片
    after=[dict(heading='...', lines=[...])],           # 可选：小结之前插入的额外卡片（如“另一种写法”）
)
```

## 质量检查清单（每个配置都要过）

1. `python make.py CFG --steps` 不报错，`expect` 通过，步数 ≤ max_steps（或快进合理），预估时长 60–180 秒。
2. 关键行都有讲“为什么”的字幕，没有一屏全是“执行 xxx”。
3. `--preview` 抽 2–3 帧看：视图没有重叠/溢出，指针、窗口、颜色表达的是算法的核心状态。
4. 卡片里的引用来自作者原文；作者的独特思路（比如灵神的“枚举右、维护左”，yiduobo 的推导）要体现出来，两位作者同一题的视频不要写成一样的文案。
