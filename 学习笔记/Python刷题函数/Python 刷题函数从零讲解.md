---
title: Python 刷题函数从零讲解
tags: [leetcode, python, 教程]
---

# Python 刷题函数从零讲解

> 素材：**灵茶山艾府**（灵神，endlesscheng，Python 3）和 **yiduobo**（Python 2 风格）两位作者的 LeetCode 题解。
> 方法：用 Python 的 `ast` 模块把所有题解代码解析成语法树，统计每个内置函数、对象方法、标准库函数、装饰器和语法特性出现在多少篇题解里，再按"出现频率 + 重要性"逐个讲解。

## 0. 普查说明

- 题解文件 **6165** 篇（灵神 2540，yiduobo 3625），其中含 Python 代码的 5907 篇；成功解析 **5901** 篇，完全无法用 AST 解析 6 篇（这些改用正则统计）。
- 代码块 7643 个：直接解析 7605，自动修复后解析 15（Python 2 `print` 语句等），失败 5，另有 18 个其实是"输入/输出示例"文本而非代码，已跳过。
- 去重后共 **223** 个不同的函数 / 方法 / 库成员：内置函数 36 个，对象方法 103 个（其中 58 个是 list/str/dict/set/deque/int 等内置类型的方法，其余多为 LeetCode 提供的接口如 `isBadVersion`、`getInteger` 或设计题自定义类），标准库/第三方库成员 84 个。在至少 3 篇题解中出现的有 **127** 个。
- 另统计了 46 种语法特性、11 种运算符、3 种装饰器。完整数据见同目录 `census.md` / `census.json`。

**统计口径**
- "篇"= 出现该函数的题解文件数（同一文件出现多次只算 1 篇）；另外 `census.json` 里还保存了总出现次数 `occ`。
- **别名已合并**：灵神依赖 LeetCode 的自动导入，常写裸名 `heappush(...)`、`accumulate(...)`、`Counter(...)`、`@cache`、`inf`；yiduobo 有时写 `heapq.heappush(...)`。两种写法都归到 `heapq.heappush` 等"模块.函数"名下。被题解自己重新定义过的名字（例如自定义的 `def pow`、变量 `count`）不计入。
- **方法**只统计"对象.方法(...)"形式的调用，排除了 `self.xxx()`、`super().xxx()` 和题解中自定义类里定义过的同名方法（如并查集的 `find`）。
- Python 2 代码先尝试直接解析，失败则自动修复（`print x` → `print(x)`、`except E, e` → `except E as e`、去掉 Markdown 引用符 `> `），再失败则退回正则匹配函数名。

**出现频率 Top 20（函数 / 方法 / 库成员）**

| # | 名称 | 类别 | 灵神（篇） | yiduobo（篇） | 合计（篇） | 合计出现次数 |
|---|---|---|---|---|---|---|
| 1 | `len` | 内置函数 | 1268 | 2104 | 3372 | 7261 |
| 2 | `range` | 内置函数 | 1077 | 1835 | 2912 | 7849 |
| 3 | `.append()` | 方法 | 556 | 1374 | 1930 | 4258 |
| 4 | `max` | 内置函数 | 660 | 743 | 1403 | 3058 |
| 5 | `enumerate` | 内置函数 | 749 | 482 | 1231 | 2021 |
| 6 | `min` | 内置函数 | 483 | 424 | 907 | 1720 |
| 7 | `set` | 内置函数 | 176 | 465 | 641 | 945 |
| 8 | `.add()` | 方法 | 114 | 377 | 491 | 885 |
| 9 | `sum` | 内置函数 | 320 | 163 | 483 | 736 |
| 10 | `sorted` | 内置函数 | 146 | 327 | 473 | 609 |
| 11 | `int` | 内置函数 | 235 | 209 | 444 | 862 |
| 12 | `.get()` | 方法 | 36 | 388 | 424 | 811 |
| 13 | `.pop()` | 方法 | 148 | 257 | 405 | 620 |
| 14 | `.sort()` | 方法 | 242 | 146 | 388 | 546 |
| 15 | `list` | 内置函数 | 235 | 86 | 321 | 477 |
| 16 | `.join()` | 方法 | 116 | 180 | 296 | 387 |
| 17 | `zip` | 内置函数 | 197 | 80 | 277 | 400 |
| 18 | `math.inf` | 标准库 | 272 | 0 | 272 | 746 |
| 19 | `abs` | 内置函数 | 97 | 141 | 238 | 539 |
| 20 | `ord` | 内置函数 | 102 | 124 | 226 | 599 |

**只有一位作者使用的函数（≥ 5 篇）**

- **只有灵神用**（48 个）：`math.inf`(272)、`functools.cache`(223)、`collections.defaultdict`(172)、`bisect.bisect_left`(144)、`.bit_length()`(109)、`map`(104)、`itertools.pairwise`(86)、`itertools.accumulate`(83)、`.bit_count()`(50)、`all`(44)、`pow`(43)、`divmod`(42)、`bisect.bisect_right`(36)、`.count()`(35)、`math.isqrt`(34)、`math.gcd`(33)、`reversed`(26)、`sortedcontainers.SortedList`(26)、`string.ascii_lowercase`(24)、`any`(24)、`itertools.count`(23)、`math.comb`(22)、`functools.reduce`(20)、`.cache_clear()`(19)、`.bisect_left()`(15)、`operator.xor`(13)、`.discard()`(12)、`heapq.heapreplace`(11)、`math.lcm`(10)、`dict`(10)、`next`(9)、`.zfill()`(9)、`object`(8)、`itertools.permutations`(8)、`heapq.heapreplace_max`(8)、`heapq.nlargest`(8)、`heapq.heapify_max`(8)、`numpy.array`(7)、`heapq.heappushpop`(7)、`itertools.groupby`(7)、`operator.or_`(7)、`heapq.heappush_max`(7)、`itertools.combinations`(6)、`.matrix_power()`(6)、`.rstrip()`(6)、`numpy.linalg`(6)、`.bisect_right()`(5)、`.islower()`(5)
- **只有 yiduobo 用**（4 个）：`copy.deepcopy`(7)、`.release()`(6)、`.acquire()`(6)、`threading.Semaphore`(6)

**怎么读这份文档**
- 每个 `###` 是一个函数或特性，Obsidian 右侧大纲可以直接跳转。
- `python` 代码块都是**可以直接运行**的最小例子，注释里写着实际输出（已用 Python 3.13 逐条执行校验；标注 `# py3.14` 的用 3.14 校验）。
- `py` 代码块是从题解中摘出的**片段**，用来展示"刷题中怎么用"，引用格式为"灵神 0347""yiduobo 0030"（题号）。
- 灵神的代码依赖 LeetCode 自动导入，本地运行前请先粘贴第 11 章末尾的 import 模板。

## 1. 内置函数

内置函数不需要 import，随时可用。下面按"出现频率 + 重要程度"排列。

### len
> 频次：灵神 **1268** 篇 · yiduobo **2104** 篇

**作用**：返回容器的元素个数（列表、字符串、字典、集合、元组、deque……）。
**签名**：`len(obj)` · 时间 O(1)（长度是存好的，不会去数）

```python
print(len([3, 1, 4]))      # 3
print(len("hello"))        # 5
print(len({"a": 1, "b": 2}))  # 2
```

**刷题中怎么用**：几乎每题第一行都是 `n = len(nums)`，然后 `range(n)` 枚举下标。双指针初始化 `left, right = 0, len(nums) - 1`（灵神 0011 / yiduobo 0001）。

```py
n = len(nums)
right = len(sorted_list) - 1   # yiduobo 0001
```

### range
> 频次：灵神 **1077** 篇 · yiduobo **1835** 篇

**作用**：生成一段等差整数序列，用来写 `for` 循环。Python 3 的 `range` 是惰性的（不真的建列表），占 O(1) 内存。
**签名**：`range(stop)` / `range(start, stop[, step])` · 左闭右开 `[start, stop)`

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(2, 8, 2)))    # [2, 4, 6]
print(list(range(4, -1, -1)))  # [4, 3, 2, 1, 0]
print(7 in range(0, 10, 7))    # True  ← range 支持 O(1) 的 in 判断
```

**刷题中怎么用**：
- 倒序遍历：`for i in range(n - 1, -1, -1)`（yiduobo 0018、0029 大量使用）；灵神更常写 `for i in reversed(range(n))`。
- 二维 DP 初始化：`f = [[0] * (n + 1) for _ in range(m + 1)]`（灵神 0062）。
- 当"有序数组"用来二分答案：`bisect_left(range(max(nums)), True, key=check)`（灵神 1283），见第 5 章。

> **易错点**
> 右端点取不到：`range(1, n)` 不含 `n`。倒序时终点写 `-1` 才能取到 0。

### enumerate
> 频次：灵神 **749** 篇 · yiduobo **482** 篇

**作用**：遍历时同时拿到"下标 + 元素"。
**签名**：`enumerate(iterable, start=0)`

```python
for i, c in enumerate("abc"):
    print(i, c)              # 0 a | 1 b | 2 c
print(list(enumerate([10, 20], start=1)))  # [(1, 10), (2, 20)]
```

**刷题中怎么用**（灵神 0001 两数之和）：

```py
idx = {}
for j, x in enumerate(nums):
    if target - x in idx:
        return [idx[target - x], j]
    idx[x] = j
```

灵神几乎从不写 `for i in range(len(nums))` 再取 `nums[i]`，而是 `for i, x in enumerate(nums)`，代码更短也更不容易写错下标。

### zip
> 频次：灵神 **197** 篇 · yiduobo **80** 篇

**作用**：把多个序列"按位置拉链"配对，长度取最短者。
**签名**：`zip(*iterables, strict=False)` · 惰性

```python
a, b = [1, 2, 3], "xyz"
print(list(zip(a, b)))           # [(1, 'x'), (2, 'y'), (3, 'z')]
m = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*m)))             # [(1, 4), (2, 5), (3, 6)]  ← 矩阵转置
print(dict(zip("ab", [1, 2])))   # {'a': 1, 'b': 2}
```

**刷题中怎么用**：
- 同时遍历多个数组：`for h, pre, suf in zip(height, pre_max, suf_max)`（灵神 0042 接雨水）。
- 按列遍历字符串数组：`for col in zip(*strs)`（灵神 0014 最长公共前缀）。
- yiduobo 0582：`for x, y in zip(pid, ppid)` 建图。

> **易错点**
> `zip` 只走到最短序列结束，多出来的元素会被静默丢弃；需要补齐用 `itertools.zip_longest`。

### max
> 频次：灵神 **660** 篇 · yiduobo **743** 篇

**作用**：求最大值，可传多个参数，也可传一个可迭代对象。
**签名**：`max(a, b, ...)` / `max(iterable, *, key=None, default=...)` · O(n)

```python
print(max(3, 7, 5))                       # 7
print(max([3, 7, 5]))                     # 7
print(max(["apple", "fig", "banana"], key=len))  # banana
print(max([], default=0))                 # 0
print(max((2, 'b'), (2, 'a')))            # (2, 'b')  ← 元组按字典序比较
```

**刷题中怎么用**：
- 更新答案：`ans = max(ans, right - left + 1)`（滑动窗口模板，灵神 0003）。
- 求哈希表最大值：`max_cnt = max(cnt.values())`（灵神 0347）。
- 空序列兜底：`return max(str_cnt.values(), default=0)`（灵神 1297）；`max((x for x, c in cnt.items() if x == c), default=-1)`（灵神 1394）。

> **易错点**
> `max([])` 直接抛 `ValueError`，可能为空时一定加 `default=`。另外 `max(a, b)` 在热循环里比 `a if a > b else b` 慢不少，灵神在卡常题会手写比较。

### min
> 频次：灵神 **483** 篇 · yiduobo **424** 篇

**作用 / 签名**：与 `max` 完全对称：`min(iterable, *, key=None, default=...)`。

```python
print(min(4, 2, 8))                 # 2
print(min("bca"))                   # a
pts = [(1, 5), (2, 1), (0, 3)]
print(min(pts, key=lambda p: p[1])) # (2, 1)
```

**刷题中怎么用**：最小值初始化成 `inf` 再不断 `ans = min(ans, ...)`（灵神 0016 用 `ans = inf`）；yiduobo 习惯初始化成 `10 ** 9` 之类的大数（yiduobo 2644 `res = 10 ** 9 + 1`）。

### sum
> 频次：灵神 **320** 篇 · yiduobo **163** 篇

**作用**：对可迭代对象求和。
**签名**：`sum(iterable, /, start=0)` · O(n)

```python
print(sum([1, 2, 3]))               # 6
print(sum(x * x for x in range(4))) # 14  ← 生成器表达式，不建中间列表
print(sum([True, False, True]))     # 2   ← bool 是 int 的子类，可直接计数
print(sum([[1], [2, 3]], []))       # [1, 2, 3]  ← start=[] 拼接列表（慢，仅了解）
```

**刷题中怎么用**：
- 计数：`sum(c == '1' for c in s)`，布尔求和是灵神的常用写法。
- 矩阵乘法一行：`sum(x * y for x, y in zip(row, col))`（灵神 0070 矩阵快速幂）。
- yiduobo 0982：`res += sum([cnt_dict.get(y, 0) for y in check_list])`（先建列表再求和，Python 2 时代常见写法）。

### sorted
> 频次：灵神 **146** 篇 · yiduobo **327** 篇

**作用**：返回一个**新的**已排序列表，原对象不变（对比 `list.sort()` 原地排序）。
**签名**：`sorted(iterable, *, key=None, reverse=False)` · O(n log n)，稳定排序

```python
a = [3, 1, 2]
b = sorted(a)
print(a, b)                          # [3, 1, 2] [1, 2, 3]
print(sorted("bca"))                 # ['a', 'b', 'c']
print(''.join(sorted("bca")))        # abc
print(sorted([(1, 'b'), (0, 'z'), (1, 'a')]))  # [(0, 'z'), (1, 'a'), (1, 'b')]
print(sorted([5, 2, 9], reverse=True))         # [9, 5, 2]
print(sorted(["bb", "a", "ccc"], key=len))     # ['a', 'bb', 'ccc']
```

**刷题中怎么用**：
- 字母异位词分组的 key：`sorted_s = ''.join(sorted(s))`（灵神 0049）。
- 按 key 排序后遍历：`for x, c in sorted(events.items())`（灵神 0056 差分写法）。
- 多关键字排序（一个升序一个降序）：`sorted(envelopes, key=lambda d: (d[0], -d[1]))`（yiduobo 0354 / 灵神 0354 用 `.sort`）。
- `sorted(zip(position, speed), reverse=True)`（灵神 0853 车队）。

> **易错点**
> `sorted` 对字典只返回排好序的 **key** 列表；要按 value 排用 `sorted(d.items(), key=lambda kv: kv[1])`。

### int
> 频次：灵神 **235** 篇 · yiduobo **209** 篇

**作用**：转整数。可指定进制解析字符串；对浮点数是**向 0 截断**。
**签名**：`int(x=0)` / `int(s, base=10)`

```python
print(int("42"), int("-7"))   # 42 -7
print(int("1011", 2))         # 11
print(int("ff", 16))          # 255
print(int(3.9), int(-3.9))    # 3 -3   ← 向 0 截断，不是向下取整
print(int(" 12 "))            # 12     ← 允许首尾空白
```

**刷题中怎么用**：
- 二进制串转数：`int(bin(n)[2:].zfill(32)[::-1], 2)`（灵神 0190 颠倒二进制位）。
- 字符转数字：`x = int(b) - 1`（灵神 0036 数独），或用 `ord(c) - ord('0')`。
- yiduobo 0279：`t = int(sqrt(i))` 求整数平方根（有精度风险，灵神改用 `isqrt`）。

> **易错点**
> 负数除法取整：`int(-7 / 2)` 是 `-3`（向 0），而 `-7 // 2` 是 `-4`（向下）。题目要求"向零截断"（如 0029、0150 逆波兰）时要用 `int(a / b)`。

### str
> 频次：灵神 **83** 篇 · yiduobo **116** 篇

**作用**：把对象转成字符串。

```python
print(str(123) + "4")    # 1234
print(len(str(2 ** 10))) # 4    ← 数位个数
print(str([1, 2]))       # [1, 2]
```

**刷题中怎么用**：数位相关题直接 `s = str(n)` 再遍历字符（灵神 1323 `str(num).replace('6', '9', 1)`）；yiduobo 0038 外观数列 `f[index] += str(cnt) + now`。

### list
> 频次：灵神 **235** 篇 · yiduobo **86** 篇

**作用**：把任意可迭代对象变成列表；也常用来**浅拷贝**。

```python
print(list("abc"))             # ['a', 'b', 'c']
print(list(range(3)))          # [0, 1, 2]
a = [1, 2]; b = list(a); b.append(3)
print(a, b)                    # [1, 2] [1, 2, 3]
```

**刷题中怎么用**：
- 把惰性对象落地：`self.s = list(accumulate(nums, initial=0))`（灵神 0303 前缀和）。
- 字符串要修改时先转列表：`t = list(s)`，改完 `''.join(t)`（灵神 0709）。
- `return list(d.values())`（灵神 0049，题目要求返回 list 而不是 dict_values）。

### set
> 频次：灵神 **176** 篇 · yiduobo **465** 篇

**作用**：创建集合（无序、去重、O(1) 查找）。

```python
s = set([3, 1, 3, 2])
print(sorted(s))         # [1, 2, 3]
print(len(set("hello"))) # 4
print(set())             # set()  ← 空集合只能这样写，{} 是空字典
```

**刷题中怎么用**：
- 去重：`nums[:] = sorted(set(nums))`（灵神 0026，附库函数写法）。
- 滑动窗口里维护字符集合：`window = set()` + `window.add / remove`（灵神 0003）。
- yiduobo 偏爱 `xxx_set = set()` + `if x in xxx_set`（yiduobo 0015、0187、0202）。

### dict
> 频次：灵神 **10** 篇 · yiduobo **0** 篇

**作用**：创建字典。字面量 `{}` 更常用，`dict(...)` 适合从键值对序列构造。从 Python 3.7 起字典**保持插入顺序**。

```python
print(dict(zip("abc", [1, 2, 3])))  # {'a': 1, 'b': 2, 'c': 3}
print(dict([(1, 'x'), (2, 'y')]))   # {1: 'x', 2: 'y'}
print(dict(a=1, b=2))               # {'a': 1, 'b': 2}
```

**刷题中怎么用**：`score = dict(zip(ascii_lowercase, score))`（灵神 1255）；`PREVIOUS = dict(pairwise("croakc"[::-1]))`（灵神 1419）；灵神 1782 注释："`dict()` 比 `Counter` 快一点"。

### tuple
> 频次：灵神 **14** 篇 · yiduobo **10** 篇

**作用**：不可变序列。**可哈希**，所以能当字典的 key / 放进集合，而列表不行。

```python
cnt = {}
row = [1, 0, 1]
cnt[tuple(row)] = cnt.get(tuple(row), 0) + 1
print(cnt)                       # {(1, 0, 1): 1}
print(tuple(sorted([3, 1])))     # (1, 3)
```

**刷题中怎么用**：把列表当哈希 key：`cnt[tuple(row)] += 1`（灵神 1072）；`word_set.add(tuple(sorted(char_dict.items())))`（yiduobo 0893）。

### abs
> 频次：灵神 **97** 篇 · yiduobo **141** 篇

```python
print(abs(-5), abs(3.5))    # 5 3.5
print(abs(3 - 7))           # 4
```

**刷题中怎么用**：判断平衡二叉树 `abs(left_h - right_h) > 1`（灵神 0110 / yiduobo 0110 几乎同一行）；最接近目标 `abs(s - target) < abs(ans - target)`（灵神 0016）；曼哈顿距离 `abs(x1 - x2) + abs(y1 - y2)`。

### ord
> 频次：灵神 **102** 篇 · yiduobo **124** 篇

**作用**：字符 → Unicode 码点（整数）。
**签名**：`ord(c)`，`c` 必须是长度为 1 的字符串

```python
print(ord('a'), ord('A'), ord('0'))   # 97 65 48
print(ord('c') - ord('a'))            # 2   ← 字母映射到 0..25
```

**刷题中怎么用**：长度 26 的计数数组：`cnt_s[ord(c) - ord('a')] += 1`（灵神 0242）。yiduobo 常把常数直接写死：`str_list[ord(char) - 97] += 1`（yiduobo 0049）、`48 <= ord(char) <= 57` 判断数字（yiduobo 0065）。

### chr
> 频次：灵神 **9** 篇 · yiduobo **69** 篇

**作用**：码点 → 字符，`ord` 的逆运算。

```python
print(chr(97))                    # a
print(chr(ord('a') + 25))         # z
print(''.join(chr(ord('a') + i) for i in range(5)))  # abcde
```

**刷题中怎么用**：`t[i] = chr(ord('a') + k)`（灵神 0709）；Excel 列名 `res = chr(tmp + 64) + res`（yiduobo 0168）。

### map
> 频次：灵神 **104** 篇 · yiduobo **0** 篇

**作用**：对每个元素应用函数，返回**惰性迭代器**（Python 3）。
**签名**：`map(func, *iterables)`

```python
print(list(map(int, "123")))          # [1, 2, 3]
print(list(map(str, [1, 2])))         # ['1', '2']
print(max(map(len, ["a", "abc"])))    # 3
print(list(map(lambda x, y: x * y, [1, 2], [3, 4])))  # [3, 8]
```

**刷题中怎么用**：
- `max_len = max(map(len, wordDict))`（灵神 0139 单词拆分）。
- `nums = list(map(str, nums))`（灵神 0179 最大数）。
- `a = map(int, version1.split('.'))`（灵神 0165 比较版本号）。

> **note**
> 普查中 yiduobo 从未使用 `map`（0 篇），而是写列表推导式 `[int(x) for x in ...]`。两种都行；`map` 配合内置函数时更快更短。

### filter
> 频次：灵神 **2** 篇 · yiduobo **0** 篇

**作用**：保留使函数返回真值的元素，惰性。

```python
print(list(filter(str.isalnum, "a,b c!")))   # ['a', 'b', 'c']
print(list(filter(None, [0, 1, '', 'x'])))   # [1, 'x']  ← None 表示按真值过滤
```

**刷题中怎么用**：`s = ''.join(filter(str.isalnum, s)).lower()`（灵神 0125 验证回文串）。

### all
> 频次：灵神 **44** 篇 · yiduobo **0** 篇

**作用**：全部为真才返回 True（空序列返回 True），会**短路**。

```python
print(all([1, 2, 3]))                   # True
print(all(x > 0 for x in [1, -1, 2]))   # False
print(all([]))                          # True
```

**刷题中怎么用**：`return all(c == 0 for c in cnt)`（灵神 0242 有效的字母异位词）；`all(c >= 0 for c in cnt.values())`（灵神 0383）；判断子序列的妙招 `it = iter(t); return all(c in it for c in s)`（灵神 0392，见 `iter`）。

### any
> 频次：灵神 **24** 篇 · yiduobo **0** 篇

**作用**：任一为真即返回 True（空序列返回 False），短路。

```python
print(any(x % 2 == 0 for x in [1, 3, 4]))   # True
print(any([]))                              # False
```

**刷题中怎么用**：`first_col_has_zero = any(row[0] == 0 for row in matrix)`（灵神 0073）；网格搜索入口 `return any(dfs(i, j, 0) for i in range(m) for j in range(n))`（灵神 0079 单词搜索，找到就停）。

### pow
> 频次：灵神 **43** 篇 · yiduobo **0** 篇

**作用**：幂运算；三参数版本是**快速幂取模**，O(log e)。
**签名**：`pow(base, exp[, mod])`

```python
print(pow(2, 10))              # 1024
print(pow(2, 10, 1000))        # 24
print(pow(3, -1, 7))           # 5   ← Python 3.8+：模逆元，3*5 % 7 == 1
MOD = 10 ** 9 + 7
print(pow(2, 100, MOD))        # 976371285
```

**刷题中怎么用**：`(pow(2, i, MOD) - pow(2, len(nums) - 1 - i, MOD)) * x`（灵神 0891 子序列宽度之和）；`pow(10, i, k * 9) == 1`（灵神 1015）。求组合数时用 `pow(x, MOD - 2, MOD)` 求逆元（费马小定理）。

> **易错点**
> 灵神有些题自己定义了同名函数 `def pow(a, n)`（灵神 0552 矩阵快速幂），会覆盖内置 `pow`——自己写代码时尽量别重名。

### divmod
> 频次：灵神 **42** 篇 · yiduobo **0** 篇

**作用**：同时求商和余数，`divmod(a, b) == (a // b, a % b)`。

```python
print(divmod(17, 5))        # (3, 2)
print(divmod(-17, 5))       # (-4, 3)  ← 与 // 和 % 一致，向下取整
q, r = divmod(7, 3)
print(q, r)                 # 2 1
```

**刷题中怎么用**：
- 一维下标 → 二维坐标：`r, c = divmod(y - 1, n)`（灵神 0909 蛇梯棋）。
- 分数转小数：`q, r = divmod(numerator, denominator)`（灵神 0166）。
- 平均分配：`avg, rem = divmod(extra_spaces, gaps)`（灵神 0068 文本左右对齐）。

### reversed
> 频次：灵神 **26** 篇 · yiduobo **0** 篇

**作用**：返回反向迭代器，O(1) 创建，不复制数据（对比切片 `a[::-1]` 会复制 O(n)）。

```python
print(list(reversed([1, 2, 3])))          # [3, 2, 1]
print(''.join(reversed("abc")))           # cba
print(list(reversed(range(3))))           # [2, 1, 0]
```

**刷题中怎么用**：`for bucket in reversed(buckets)`（灵神 0347 桶排序）；`return ''.join(reversed(ans))`（灵神 0067）；灵神 0032 注释"`reversed` 是 O(1) 的"。

> **易错点**
> `reversed` 返回的是迭代器，只能遍历一次，也不能下标访问；需要列表时 `list(reversed(a))` 或 `a[::-1]`。

### iter
> 频次：灵神 **4** 篇 · yiduobo **0** 篇

**作用**：从可迭代对象得到迭代器。迭代器"用掉就没了"，这一点可以被巧妙利用。

```python
it = iter("abcde")
print(next(it), next(it))        # a b
print('c' in it, 'a' in it)      # True False  ← in 会消耗迭代器
s, t = "ace", "abcde"
it = iter(t)
print(all(c in it for c in s))   # True  ← 判断 s 是否为 t 的子序列
```

**刷题中怎么用**：灵神 0392 判断子序列：`it = iter(t); return all(c in it for c in s)`，注释"in 会消耗迭代器"。

### next
> 频次：灵神 **9** 篇 · yiduobo **0** 篇

**作用**：取迭代器的下一个元素；可以给默认值避免 `StopIteration`。
**签名**：`next(iterator[, default])`

```python
print(next(x for x in [1, 4, 6] if x % 2 == 0))    # 4  ← 找第一个满足条件的
print(next((x for x in [1, 3] if x % 2 == 0), -1)) # -1
board = [[1, 2], [3, 4]]
print(list(next(zip(*board))))                     # [1, 3]  ← 取第一列
```

**刷题中怎么用**：`return next(p[1] for p in paths if p[1] not in set_a)`（灵神 1436 旅行终点站）；`first_col = list(next(zip(*board)))`（灵神 0782）。

> **note**
> yiduobo 的 `def next(self)`（0173、0251、0281）是**迭代器类设计题**要求实现的方法，不是调用内置 `next`。

### bin
> 频次：灵神 **10** 篇 · yiduobo **11** 篇

**作用**：整数 → 二进制字符串，带 `0b` 前缀。相关的还有 `hex`（`0x`）、`oct`（`0o`）。

```python
print(bin(10))              # 0b1010
print(bin(10)[2:])          # 1010
print(bin(5)[2:].zfill(8))  # 00000101
print(bin(-5))              # -0b101
print(hex(255), oct(8))     # 0xff 0o10
```

**刷题中怎么用**：`all(bin(i)[2:] in s for i in range(1, n + 1))`（灵神 1016）；数位 DP 中 `list(map(int, bin(right)[2:]))`（灵神 0762）；yiduobo 用 `len(bin(x)) - 2` 求二进制长度（yiduobo 2564），等价于更快的 `x.bit_length()`。

### float
> 频次：灵神 **1** 篇 · yiduobo **6** 篇

```python
print(float("3.5") + 1)       # 4.5
print(float("inf") > 10 ** 18)  # True
print(0.1 + 0.2 == 0.3)       # False  ← 浮点误差
```

**刷题中怎么用**：两位作者都**不写** `float('inf')`（普查 0 次）：灵神用 `math.inf`（灵神 **272** 篇 · yiduobo **0** 篇），yiduobo 用 `10 ** 9`、`10 ** 18` 之类的大整数（见第 8 章）。`float` 主要用于真正需要小数的题，如 yiduobo 0480 `res.append(float(-min_heap[0]))`。

### round
> 频次：灵神 **1** 篇 · yiduobo **1** 篇

```python
print(round(2.5), round(3.5))   # 2 4    ← 银行家舍入（四舍六入五成双）
print(round(3.14159, 2))        # 3.14
```

**刷题中怎么用**：灵神 1870 `h100 = round(hour * 100)` 把浮点转整数后全程用整数算，避免精度问题。

> **易错点**
> Python 3 的 `round(2.5) == 2`，Python 2 是 `3.0`（四舍五入，远离 0）。需要"四舍五入"时写 `int(x + 0.5)`（x ≥ 0）。

### print
> 频次：灵神 **9** 篇 · yiduobo **17** 篇

题解里出现的 `print` 基本是**调试残留**或"打表"（灵神 0039 `print(sum(f))  # 37271`）。yiduobo 的 14 处是 Python 2 的 `print x` 语句（见第 10 章）。提交前记得删掉调试输出，大量输出会拖慢运行。

```python
print(1, 2, sep=", ", end="!\n")   # 1, 2!
```

### isinstance
> 频次：灵神 **2** 篇 · yiduobo **0** 篇

```python
print(isinstance(3, int), isinstance([1], (list, tuple)))  # True True
print(isinstance(True, int))   # True  ← bool 是 int 的子类
```

**刷题中怎么用**：处理"嵌套列表/整数混合"输入时判断类型（灵神 3569 `if isinstance(init_val, int):`）。

### object（`dtype=object`）
> 频次：灵神 **8** 篇 · yiduobo **0** 篇

灵神的 `object` 全部出现在 numpy 矩阵快速幂里：`np.array([[1, 1], [1, 0]], dtype=object)`（灵神 0070、0509）——用 Python 大整数做元素，避免 int64 溢出，再配合 `% MOD`。了解即可。

## 2. 列表 / 字符串 / 字典 / 集合 的方法

"方法"就是写成 `对象.名字(...)` 的函数。先记住四种容器的核心复杂度：

| 容器 | 按下标/键访问 | 尾部增删 | 头部/中间增删 | `x in c` |
|---|---|---|---|---|
| `list` | O(1) | O(1) 均摊 | O(n) | O(n) |
| `str`（不可变） | O(1) | 每次都新建 O(n) | O(n) | O(n·m) |
| `dict` | O(1) 均摊 | — | — | O(1) |
| `set` | — | — | — | O(1) |

### 2.1 列表 list

### list.append
> 频次：灵神 **556** 篇 · yiduobo **1374** 篇

**作用**：在末尾追加一个元素，O(1) 均摊。

```python
a = [1, 2]
a.append(3)
print(a)               # [1, 2, 3]
a.append([4, 5])
print(a)               # [1, 2, 3, [4, 5]]  ← 整个列表作为一个元素
```

**刷题中怎么用**：回溯收集答案 `ans.append(path.copy())`（灵神 0039），栈的入栈 `st.append(c)`（灵神 0020），BFS 下一层 `nxt.append(node.left)`。

> **易错点**
> 回溯时 `ans.append(path)` 存的是**引用**，之后 `path` 被修改，答案也跟着变。必须 `path.copy()` 或 `path[:]`（灵神 0040 注释："也可以写 path[:]"）。

### list.pop
> 频次：灵神 **148** 篇 · yiduobo **257** 篇

**作用**：删除并返回指定位置元素，默认最后一个。`pop()` 是 O(1)，`pop(0)` 是 O(n)。

```python
st = [1, 2, 3]
print(st.pop())     # 3
print(st.pop(0))    # 1
print(st)           # [2]
d = {"a": 1}
print(d.pop("a"), d.pop("b", 0))   # 1 0  ← 字典的 pop 可以给默认值
```

**刷题中怎么用**：栈：`elif not st or st.pop() != mp[c]`（灵神 0020 有效的括号，yiduobo 0020 写法几乎一样）；回溯"恢复现场"：`path.pop()`（灵神 0022）。

> **易错点**
> 用列表当队列 `q.pop(0)` 是 O(n)，BFS 会变慢；用 `collections.deque` 的 `popleft()`。yiduobo 0225 用栈实现队列时写 `self.q.append(self.q.pop(0))` 是题意要求。

### list.sort
> 频次：灵神 **242** 篇 · yiduobo **146** 篇

**作用**：**原地**排序，返回 `None`。参数同 `sorted`。稳定排序（Timsort），O(n log n)。

```python
a = [3, 1, 2]
print(a.sort())          # None
print(a)                 # [1, 2, 3]
iv = [[1, 3], [0, 2], [1, 1]]
iv.sort(key=lambda p: p[0])
print(iv)                # [[0, 2], [1, 3], [1, 1]]  ← 稳定：同 key 保持原顺序
words = ["bb", "a", "ccc"]
words.sort(key=len, reverse=True)
print(words)             # ['ccc', 'bb', 'a']
```

**刷题中怎么用**：区间合并 `intervals.sort(key=lambda p: p[0])`（灵神 0056；yiduobo 0252 `intervals.sort(key=lambda d:d[0])`）；自定义比较 `nums.sort(key=cmp_to_key(...))`（灵神 0179，见第 7 章）。普查中 `.sort` 的关键字参数：灵神 `key=` 98 次 / `reverse=` 33 次。

> **易错点**
> `a = a.sort()` 会让 `a` 变成 `None`！要么 `a.sort()`，要么 `a = sorted(a)`。

### list.reverse
> 频次：灵神 **20** 篇 · yiduobo **114** 篇

```python
a = [1, 2, 3]
a.reverse()
print(a)        # [3, 2, 1]
```

**刷题中怎么用**：二叉树锯齿形层序遍历 `level_res.reverse()`（yiduobo 0103）、自底向上层序 `res.reverse()`（yiduobo 0107）；旋转图像 `row.reverse()`（灵神 0048）。yiduobo 用它 114 篇，远多于灵神。

### list.extend
> 频次：灵神 **20** 篇 · yiduobo **47** 篇

**作用**：把另一个可迭代对象的所有元素追加到末尾（等价 `a += b`）。

```python
a = [1]
a.extend([2, 3])
print(a)            # [1, 2, 3]
a.extend("xy")
print(a)            # [1, 2, 3, 'x', 'y']
```

**刷题中怎么用**：N 叉树 BFS `q.extend(node.children)`（灵神 0429）；格雷码 `res.extend([res[pos] + weight for pos in range(len(res) - 1, -1, -1)])`（yiduobo 0089）。

### list.insert
> 频次：灵神 **1** 篇 · yiduobo **0** 篇

```python
a = [1, 3]
a.insert(1, 2)      # 在下标 1 处插入，O(n)
print(a)            # [1, 2, 3]
a.insert(0, 0)
print(a)            # [0, 1, 2, 3]
```

**刷题中怎么用**：很少用（O(n)）。普查里大多数 `.insert` 是字典树 / 设计题里自定义类的方法（如灵神 2932 `t.insert(y)`），已被排除；按身高重建队列（0406）是 `list.insert` 的经典用法。

### list.remove
> 频次：灵神 **16** 篇 · yiduobo **50** 篇

**作用**：删除**第一个**等于 x 的元素，O(n)；找不到抛 `ValueError`。集合的 `set.remove` 是 O(1)。

```python
a = [1, 2, 1]
a.remove(1)
print(a)            # [2, 1]
s = {1, 2}
s.remove(2)
print(s)            # {1}
```

**刷题中怎么用**：滑动窗口收缩 `window.remove(s[left])`（灵神 0003，集合）；`char_set.remove(char)`（yiduobo 0266）。

### list.index
> 频次：灵神 **14** 篇 · yiduobo **2** 篇

```python
a = [9, 4, 7]
print(a.index(7))        # 2
print("hello".index("l"))  # 2
```

**刷题中怎么用**：由前序+中序构造二叉树 `left_size = inorder.index(preorder[0])`（灵神 0105）。O(n)，若要多次查询应预处理成字典 `{x: i for i, x in enumerate(inorder)}`。

### list.count
> 频次：灵神 **35** 篇 · yiduobo **0** 篇

```python
print([1, 0, 1, 1].count(1))   # 3
print("banana".count("an"))     # 2  ← 字符串的 count 统计不重叠子串
```

**刷题中怎么用**：`cnt0 = [s.count('0') for s in strs]`（灵神 0474 一和零）；`return s[:n].count(1)`（灵神 0481）。

### list.copy
> 频次：灵神 **39** 篇 · yiduobo **17** 篇

**作用**：浅拷贝（只复制一层），等价 `a[:]`、`list(a)`。字典、集合也有 `.copy()`。

```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a)          # [[1, 9], [2]]  ← 内层仍共享
```

**刷题中怎么用**：`ans.append(path.copy())`（灵神 0039/0040）；`tmp_pos_dict = pos_dict.copy()`（yiduobo 0691）。需要完整复制嵌套结构用 `copy.deepcopy`（yiduobo 3320）。

### list.clear
> 频次：灵神 **14** 篇 · yiduobo **1** 篇

```python
a = [1, 2]
a.clear()
print(a)       # []
```

**刷题中怎么用**：复用缓冲区 / 每轮清空临时集合。

### 2.2 字符串 str

字符串**不可变**：所有方法都返回新字符串，原串不变。

### str.join
> 频次：灵神 **116** 篇 · yiduobo **180** 篇

**作用**：用分隔符把字符串序列拼起来，O(总长度)。
**签名**：`sep.join(iterable_of_str)`

```python
print("".join(["a", "b", "c"]))      # abc
print("-".join("abc"))               # a-b-c
print(" ".join(map(str, [1, 2])))    # 1 2
```

**刷题中怎么用**：回溯生成字符串 `ans.append(''.join(path))`（灵神 0017）；Manacher 预处理 `t = "#".join("^" + s + "$")`（灵神 0005）/ `s = '!' + '#'.join(list(s)) + '@'`（yiduobo 0005）。

> **易错点**
> 循环里 `s += c` 拼字符串最坏 O(n²)；先放进列表最后 `''.join` 是 O(n)。`join` 的元素必须都是字符串，数字要先 `map(str, ...)`。

### str.split
> 频次：灵神 **17** 篇 · yiduobo **68** 篇

**作用**：按分隔符切成列表。不传参数时按**任意空白**切且自动丢弃空串。

```python
print("a b  c".split())        # ['a', 'b', 'c']
print("a b  c".split(" "))     # ['a', 'b', '', 'c']
print("/a//b/".split("/"))     # ['', 'a', '', 'b', '']
print("1.2.3".split(".", 1))   # ['1', '2.3']
```

**刷题中怎么用**：简化路径 `for s in path.split('/')`（灵神 0071，空串和 `.` 跳过）；`word_list = s.split()`（yiduobo 0151 反转单词）。

### str.strip / lstrip / rstrip
> 频次：`rstrip` 灵神 **6** 篇 · yiduobo **0** 篇；`lstrip` 灵神 **2** 篇 · yiduobo **0** 篇

**作用**：去掉两端（或左/右）指定字符集合中的字符，默认去空白。

```python
print("  hi  ".strip() + "|")    # hi|
print("xxhixx".rstrip("x"))      # xxhi
print("0012".lstrip("0"))        # 12
```

**刷题中怎么用**：最后一个单词的长度 `s = s.rstrip()`（灵神 0058）；`s = s.rstrip('R')`（灵神 2211，去掉后缀向右的车）。

### str.replace
> 频次：灵神 **8** 篇 · yiduobo **8** 篇

```python
print("a-b-c".replace("-", ""))        # abc
print("9669".replace("6", "9", 1))     # 9969  ← 第三个参数限制替换次数
```

**刷题中怎么用**：`str(num).replace('6', '9', 1)`（灵神 1323）；`start.replace('X', '') != target.replace('X', '')`（灵神 0777）；`S = S.replace('-', '')`（yiduobo 0482）。

### str.find / rfind
> 频次：`find` 灵神 **6** 篇 · yiduobo **12** 篇；`rfind` 灵神 **4** 篇 · yiduobo **1** 篇

**作用**：返回子串第一次（`rfind` 最后一次）出现的下标，找不到返回 **-1**（`index` 则抛异常）。

```python
s = "hello world"
print(s.find("o"), s.rfind("o"))   # 4 7
print(s.find("z"))                 # -1
print(s.find("o", 5))              # 7  ← 可指定起点
```

**刷题中怎么用**：`return len(s) - 1 - s.rfind(' ')`（灵神 0058）；`pos = s.find(char, left, right)`（yiduobo 0003，在窗口内找重复字符）。

### str.startswith / endswith
> 频次：灵神 **3** 篇 · yiduobo **1** 篇

```python
print("leetcode".startswith("leet"))       # True
print("leetcode".startswith("code", 4))    # True  ← 从下标 4 开始判断，无需切片
print("a.py".endswith((".py", ".txt")))    # True  ← 可传元组
```

**刷题中怎么用**：灵神 0833 `if s.startswith(src, i):`，注释"判断 s[i:] 的前缀是否为 src，这样写无需切片"。

### str.lower / upper 及 isXXX 判断
> 频次：`lower` 灵神 **9** 篇 · yiduobo **1** 篇；`isdigit` 灵神 **9** 篇 · yiduobo **4** 篇；`isalpha` 灵神 **4** 篇 · yiduobo **0** 篇；`islower` 灵神 **5** 篇 · yiduobo **0** 篇；`isupper` 灵神 **4** 篇 · yiduobo **0** 篇

```python
print("AbC".lower(), "AbC".upper())        # abc ABC
print("7".isdigit(), "a".isalpha())        # True True
print("a1".isalnum(), "abc".islower())     # True True
print("-1".isdigit())                      # False  ← 负号不算数字
```

**刷题中怎么用**：表达式求值 `elif c.isdigit():`（灵神 0394；yiduobo 0224、0227 `elif char.isdigit():`）；验证回文串 `s[i].lower() == s[j].lower()`（灵神 0125）。

### str.zfill
> 频次：灵神 **9** 篇 · yiduobo **0** 篇

**作用**：左侧补 0 到指定长度。

```python
print("101".zfill(8))       # 00000101
print(bin(5)[2:].zfill(4))  # 0101
```

**刷题中怎么用**：数位 DP 让上下界等长 `low_s = list(map(int, bin(left)[2:].zfill(n)))`（灵神 0762）。

### 2.3 字典 dict

### dict.get
> 频次：灵神 **36** 篇 · yiduobo **388** 篇

**作用**：取值，key 不存在时返回默认值（默认 `None`），不会抛 `KeyError`，也不会插入 key。

```python
d = {"a": 1}
print(d.get("a"), d.get("b"), d.get("b", 0))  # 1 None 0
cnt = {}
for w in ["x", "y", "x"]:
    cnt[w] = cnt.get(w, 0) + 1
print(cnt)        # {'x': 2, 'y': 1}
```

**刷题中怎么用**：这是 **yiduobo 的标志性写法**（388 篇 vs 灵神 36 篇）：`word_dict[word] = word_dict.get(word, 0) + 1`（yiduobo 0030）。灵神则用 `defaultdict(int)` / `Counter`，直接 `cnt[x] += 1`。

### dict.setdefault
> 频次：两位作者均未使用（普查 0 次），但很常见，值得认识

**作用**：key 不存在时插入默认值并返回它；存在则直接返回已有值。

```python
g = {}
for u, v in [(1, 2), (1, 3)]:
    g.setdefault(u, []).append(v)
print(g)         # {1: [2, 3]}
```

替代品：`defaultdict(list)`，见第 3 章。

### dict.items / keys / values
> 频次：`items` 灵神 **79** 篇 · yiduobo **70** 篇；`values` 灵神 **89** 篇 · yiduobo **97** 篇；`keys` 灵神 **3** 篇 · yiduobo **31** 篇

**作用**：返回字典的"视图"（随字典变化而变化），可直接遍历；`keys()` 和 `items()` 视图还支持集合运算。

```python
d = {"a": 3, "b": 1}
for k, v in d.items():
    print(k, v)                  # a 3 | b 1
print(max(d.values()))           # 3
print(sorted(d, key=d.get))      # ['b', 'a']  ← 按 value 排序 key
print(d.keys() & {"a", "z"})     # {'a'}  ← keys 视图支持 & | -
```

**刷题中怎么用**：
- `for x, c in cnt.items():`（灵神 0347）；`max_cnt = max(cnt.values())`（灵神 0347）。
- `return list(d.values())`（灵神 0049）；yiduobo 0049 直接 `return res_dict.values()`——Python 2 中 `values()` 返回列表，Python 3 返回视图，LeetCode 也能接受但最好转 list。
- `for alpha in pre_set & suf_cnt.keys():`（灵神 1930，集合与 keys 视图求交）。
- 按 key 排序输出：`[x[1] for x in sorted(res.items(), key=lambda d:d[0])]`（yiduobo 0314）。

> **易错点**
> 遍历字典时不能增删 key（`RuntimeError: dictionary changed size during iteration`），需要时遍历 `list(d.items())`。

### dict.update
> 频次：灵神 **4** 篇 · yiduobo **8** 篇

```python
d = {"a": 1}
d.update({"b": 2}, c=3)
print(d)               # {'a': 1, 'b': 2, 'c': 3}
s = {1}
s.update([2, 3])
print(s)               # {1, 2, 3}
```

**说明**：普查里不少 `.update` 是线段树/树状数组类的自定义方法（如灵神 0307 `self.update(i, x)`，已排除 `self.`）。`Counter.update` 是"累加计数"，见第 3 章。

### dict.popitem
> 频次：灵神 **3** 篇 · yiduobo **0** 篇

**作用**：删除并返回**最后插入**的 `(key, value)`（LIFO）。`OrderedDict.popitem(last=False)` 可以删最早的。

```python
d = {"a": 1, "b": 2}
print(d.popitem())     # ('b', 2)
```

**刷题中怎么用**：LRU 缓存 `self.cache.popitem()`（灵神 0146，OrderedDict 写法，见第 3 章）。

### 2.4 集合 set

### set.add
> 频次：灵神 **114** 篇 · yiduobo **377** 篇

```python
s = set()
s.add(3); s.add(3); s.add(1)
print(sorted(s), len(s))    # [1, 3] 2
```

**刷题中怎么用**：`vis.add(x)` 标记访问（BFS/DFS 去重）；yiduobo 用得极多（377 篇），如 `double_set.add(...)`（yiduobo 0015）。`SortedList.add` 见第 5 章。

### set.discard
> 频次：灵神 **12** 篇 · yiduobo **0** 篇

**作用**：删除元素，不存在也**不报错**（`remove` 会抛 `KeyError`）。

```python
s = {1, 2}
s.discard(5)
s.discard(1)
print(s)       # {2}
```

**刷题中怎么用**：`set_b.discard(a)  # a 一定不是答案`（灵神 1436）；`dry_day.discard(d)`（灵神 1488，SortedList 同名方法）。

### LeetCode 提供的接口方法（不是 Python 内置）

普查里还有一批方法只出现在特定题目里，例如 `isInteger() / getInteger() / getList()`（嵌套列表 0341、0339 的 `NestedInteger` 接口）、`isBadVersion`、`read4`、`guess`、`knows`、交互题 `moveRight() / isDoorOpen() / closeDoor()`、`ArrayReader.length()` 等。它们由题目定义，看题面说明即可，不需要记。

### 集合运算 & | - ^
> 普查：`&` / `|` 运算符包含位运算与集合运算，见第 8 章

```python
a, b = {1, 2, 3}, {2, 3, 4}
print(a & b, a | b)        # {2, 3} {1, 2, 3, 4}
print(a - b, a ^ b)        # {1} {1, 4}
print({1, 2} <= a)         # True  ← 子集判断
print(a.isdisjoint({9}))   # True
```

**刷题中怎么用**：`pre_set & suf_cnt.keys()`（灵神 1930）。方法版 `a.union(b)`、`a.intersection(b)` 可接受任意可迭代对象。

## 3. collections：计数、默认值字典、双端队列

LeetCode 已经自动 `from collections import *`，所以灵神直接写 `Counter(...)`、`defaultdict(int)`、`deque()`。自己本地运行时要先 `from collections import Counter, defaultdict, deque`。

### Counter
> 频次：灵神 **139** 篇 · yiduobo **30** 篇

**作用**：计数用的字典子类。访问不存在的 key 返回 **0**（但不会插入）。
**签名**：`Counter(iterable_or_mapping)` · 构造 O(n)

```python
from collections import Counter
cnt = Counter("abracadabra")
print(cnt["a"], cnt["z"])          # 5 0
print(cnt.most_common(2))          # [('a', 5), ('b', 2)]
cnt["z"] += 1                      # 可以像 defaultdict(int) 一样直接 +=
print(cnt["z"])                    # 1
print(Counter("aab") == Counter("aba"))   # True  ← 判断字母异位词
```

**刷题中怎么用**：
- 词频：`target_cnt = Counter(words)`（灵神 0030）；`cnt_s = Counter()` 空计数器配合滑动窗口（灵神 0076）。
- 统计列表/元组：`Counter(tuple(sorted(e)) for e in edges)`（灵神 1782）。
- 计数的计数：`Counter(cs.values()) == Counter(ct.values())`（灵神 1657）。

### Counter.most_common / total / 运算
> 频次：`most_common` 灵神 **2** 篇 · yiduobo **0** 篇；`total` 灵神 **2** 篇 · yiduobo **0** 篇

```python
from collections import Counter
a, b = Counter("aabc"), Counter("abd")
print(a.most_common(1))          # [('a', 2)]
print((a & b).total())           # 2  ← 交集取 min，total() 求和（3.10+）
print(a + b)                     # Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
print(a - b)                     # Counter({'a': 1, 'c': 1})  ← 减法会丢掉 ≤0 的项
print(sorted(a.elements()))      # ['a', 'a', 'b', 'c']
```

**刷题中怎么用**：
- 猜数字游戏：`b = (Counter(secret) & Counter(guess)).total() - a`（灵神 0299），`&` 取每个字符的较小次数。
- `mode, total = Counter(nums).most_common(1)[0]`（灵神 2780 求众数）。
- `a = Counter(s).most_common()  # 按出现次数从大到小排序`（灵神 0767 重构字符串）。
- `Counter(6 - x for x in nums1) + Counter(x - 1 for x in nums2)`（灵神 1775，两个 Counter 相加）。

> **易错点**
> `Counter` 里计数可能变成 0 或负数但 key 还在：`len(cnt)` 不等于"出现过的不同元素数"。滑动窗口要在计数归 0 时 `del cnt[x]`（灵神 0904 等题的写法）。

### defaultdict
> 频次：灵神 **172** 篇 · yiduobo **0** 篇

**作用**：访问不存在的 key 时，自动调用工厂函数创建默认值**并插入**。
**签名**：`defaultdict(default_factory)`，常用 `int`（→0）、`list`（→[]）、`set`、`lambda: inf`

```python
from collections import defaultdict
g = defaultdict(list)
for u, v in [(0, 1), (0, 2), (1, 2)]:
    g[u].append(v)
    g[v].append(u)
print(dict(g))        # {0: [1, 2], 1: [0, 2], 2: [0, 1]}
cnt = defaultdict(int)
for c in "hello":
    cnt[c] += 1
print(cnt["l"], len(cnt))   # 2 4
print(cnt["?"], len(cnt))   # 0 5  ← 访问即插入！
```

**刷题中怎么用**：滑动窗口计数 `cnt = defaultdict(int)`（灵神 0003、0030）；建图 `g = defaultdict(list)`；分组 `d = defaultdict(list); d[''.join(sorted(s))].append(s)`（灵神 0049）。yiduobo 普查中**从未使用** defaultdict，全部用 `dict.get(k, 0)` 或手动判断 `if k not in d`。

> **易错点**
> 只是想"查一下"时用 `cnt[x]` 会把 x 插进去，导致 `len()` 变大、遍历时报"dictionary changed size"。只读查询用 `x in cnt` 或 `cnt.get(x, 0)`。

### deque
> 频次：灵神 **64** 篇 · yiduobo **21** 篇

**作用**：双端队列，两端增删都是 O(1)。BFS、单调队列、滑动窗口的标配。按下标访问中间元素是 O(n)。
**签名**：`deque(iterable=(), maxlen=None)`

| 操作 | 方法 | 复杂度 |
|---|---|---|
| 右端入 / 出 | `append(x)` / `pop()` | O(1) |
| 左端入 / 出 | `appendleft(x)` / `popleft()` | O(1) |
| 查看两端 | `q[0]` / `q[-1]` | O(1) |
| 旋转 | `rotate(k)` | O(k) |

```python
from collections import deque
q = deque([1, 2, 3])
q.append(4); q.appendleft(0)
print(q)                    # deque([0, 1, 2, 3, 4])
print(q.popleft(), q.pop()) # 0 4
print(q[0], q[-1])          # 1 3
q.rotate(1)
print(list(q))              # [3, 1, 2]
w = deque(maxlen=2)
for x in [1, 2, 3]:
    w.append(x)
print(list(w))              # [2, 3]  ← 超过 maxlen 自动挤掉另一端
```

**刷题中怎么用**：
- BFS 层序遍历（灵神 0102）：

```py
q = deque([root])
while q:
    node = q.popleft()
    if node.left:  q.append(node.left)
    if node.right: q.append(node.right)
```

- 单调队列（滑动窗口最大值 0239）：右边 `pop` 掉比新元素小的，左边 `popleft` 掉出窗口的。
- yiduobo 0362 敲击计数器 `self.q = deque()` + `self.q.popleft()`；灵神 1670 前中后队列 `self.right.appendleft(self.left.pop())`。

### deque.popleft / appendleft
> 频次：`popleft` 灵神 **63** 篇 · yiduobo **21** 篇；`appendleft` 灵神 **9** 篇 · yiduobo **1** 篇

见上表。`appendleft` 在 0-1 BFS 中常用：边权为 0 的点 `appendleft`，边权为 1 的 `append`（灵神 1406 也用 `q.appendleft(i)`）。

```python
from collections import deque
q = deque()
q.append("w1"); q.appendleft("w0")
print(q.popleft())    # w0
```

### OrderedDict
> 频次：灵神 **2** 篇 · yiduobo **0** 篇（`move_to_end` 灵神 **2** 篇 · yiduobo **0** 篇）

**作用**：记得插入顺序的字典（普通 dict 3.7+ 也保序），额外提供 `move_to_end(key, last=True)` 和 `popitem(last=True)`，两者都是 O(1)。

```python
from collections import OrderedDict
od = OrderedDict.fromkeys("abc")
od.move_to_end("a")                 # 移到末尾
print(list(od))                     # ['b', 'c', 'a']
od.move_to_end("a", last=False)     # 移到开头
print(list(od))                     # ['a', 'b', 'c']
print(od.popitem(last=False))       # ('a', None)
```

**刷题中怎么用**：LRU 缓存一行维护（灵神 0146）：访问时 `self.cache.move_to_end(key, last=False)`，超容量时 `self.cache.popitem()` 去掉最久未用的。LFU（灵神 0460）同理。

### namedtuple（了解）

普查中未出现，但读别人代码会遇到：`P = namedtuple('P', 'x y'); p = P(1, 2); p.x`。

## 4. heapq：堆 / 优先队列

`heapq` 把一个**普通 list** 当成**最小堆**来操作：`h[0]` 永远是最小值。它不是类，而是一组函数，第一个参数总是那个列表。

| 函数 | 作用 | 复杂度 |
|---|---|---|
| `heapify(h)` | 原地把列表变成堆 | O(n) |
| `heappush(h, x)` | 入堆 | O(log n) |
| `heappop(h)` | 弹出并返回最小值 | O(log n) |
| `h[0]` | 查看最小值 | O(1) |
| `heapreplace(h, x)` | 先弹最小、再压入 x | O(log n) |
| `heappushpop(h, x)` | 先压入 x、再弹最小 | O(log n) |
| `nlargest(k, it)` / `nsmallest(k, it)` | 前 k 大 / 小 | O(n log k) |
| `heappush_max` 等 `*_max`（3.14+） | 最大堆版本 | 同上 |

### heapify
> 频次：灵神 **20** 篇 · yiduobo **16** 篇

```python
from heapq import heapify
h = [5, 3, 8, 1, 9, 2]
heapify(h)
print(h)        # [1, 3, 2, 5, 9, 8]  ← 只保证 h[i] <= h[2i+1], h[2i+2]，不是有序
print(h[0])     # 1
```

**刷题中怎么用**：合并 K 个链表先把所有头结点放进列表再 `heapify(h)`（灵神 0023）；yiduobo 0355、0373 `heapq.heapify(heap)`。一次性建堆 O(n)，比逐个 push 的 O(n log n) 快。

### heappush
> 频次：灵神 **57** 篇 · yiduobo **131** 篇

```python
from heapq import heappush, heappop
h = []
for x in [5, 1, 4]:
    heappush(h, x)
print(h[0], len(h))      # 1 3
pq = []
heappush(pq, (3, "c")); heappush(pq, (1, "a")); heappush(pq, (2, "b"))
print([heappop(pq)[1] for _ in range(3)])   # ['a', 'b', 'c']  ← 元组按第一项比较
```

**刷题中怎么用**：
- Dijkstra：`heappush(h, (new_dis, y))`，元组第一项是距离。
- 超级丑数：`heappush(heap, (prime, index))`（yiduobo 0313）。
- 灵神 0037 数独：`heappush(empty_heap, (candidates, i, j))`，候选数最少的格子优先。

> **易错点**
> 元组第一项相同时会比较第二项：如果第二项是 `ListNode` 这种不可比较的对象会报 `TypeError`。解决办法：加一个唯一序号 `(val, idx, node)`，或像灵神 0023 那样给类打补丁 `ListNode.__lt__ = lambda a, b: a.val < b.val`。

### heappop
> 频次：灵神 **56** 篇 · yiduobo **134** 篇

```python
from heapq import heapify, heappop
h = [4, 1, 3]
heapify(h)
print(heappop(h), heappop(h), h)   # 1 3 [4]
```

**刷题中怎么用**：`node = heappop(h)  # 剩余节点中的最小节点`（灵神 0023）；`now, candidate_index = heappop(heap)`（yiduobo 0313）。

**最大堆技巧（3.14 之前）**：存相反数。`heappush(fuel_heap, -fuel)`（灵神 0871 最低加油次数）；`heapq.heappush(self.fisrt_heap, -num)`（yiduobo 0295 数据流中位数）；`heapq.heappush(heap, [-cnt, char])`（yiduobo 0358）。

```python
from heapq import heappush, heappop
h = []
for x in [3, 9, 4]:
    heappush(h, -x)
print(-h[0])          # 9  ← 最大值
print(-heappop(h))    # 9
```

**延迟删除**：堆不支持删除任意元素，常见做法是弹出时检查堆顶是否"过期"：yiduobo 0358 `while heap and (heap[0][1] in last_pos and ...)`。

### heapreplace
> 频次：灵神 **11** 篇 · yiduobo **0** 篇

**作用**：弹出堆顶并压入新元素，比 `heappop` + `heappush` 快（只调整一次）。返回弹出的旧堆顶。注意先弹后压：新元素即使更小也不会被立刻返回。

```python
from heapq import heapify, heapreplace
h = [1, 5, 3]
heapify(h)
print(heapreplace(h, 4), h)   # 1 [3, 5, 4]
print(heapreplace(h, 0), h)   # 3 [0, 5, 4]  ← 0 进堆，但返回的是旧堆顶 3
```

**刷题中怎么用**：合并 K 个有序数组时"替换堆顶" `heapreplace(h, (x, i, j + 1))`（灵神 0632）；保持堆大小为 k 时常用 `if x > h[0]: heapreplace(h, x)`（第 k 大元素）。

### heappushpop
> 频次：灵神 **7** 篇 · yiduobo **0** 篇

**作用**：先压入再弹出最小值。若 x 不比堆顶大，直接返回 x 且堆不变（很快）。

```python
from heapq import heappushpop
h = [2, 5]
print(heappushpop(h, 1), h)   # 1 [2, 5]
print(heappushpop(h, 7), h)   # 2 [5, 7]
```

**刷题中怎么用**：数据流中位数（灵神 0295）：`heappush_max(self.left, heappushpop(self.right, num))`，把 num 先过一遍右堆再把右堆最小值送到左堆；灵神 0480 `return heappushpop(self.heap, x)`。

### nlargest / nsmallest
> 频次：`nlargest` 灵神 **8** 篇 · yiduobo **0** 篇；`nsmallest` 灵神 **3** 篇 · yiduobo **0** 篇

```python
from heapq import nlargest, nsmallest
a = [5, 1, 8, 3, 9]
print(nlargest(2, a), nsmallest(2, a))     # [9, 8] [1, 3]
print(nlargest(1, ["aa", "b"], key=len))   # ['aa']
```

**刷题中怎么用**：每个点保留价值前三大的邻居 `g[i] = nlargest(3, vs)`（灵神 2242）；`sum(nlargest(k, a))`（灵神 2497）；`nums[0] + sum(nsmallest(2, nums[1:]))`（灵神 3010）。灵神 2462 注释：也可以 `sum(nsmallest(k, costs))`，但 k 接近 n 时效率不如直接排序。

### heappush_max / heappop_max / heapify_max / heapreplace_max / heappushpop_max（Python 3.14+）
> 频次：`heapify_max` 灵神 **8** 篇 · yiduobo **0** 篇；`heapreplace_max` 灵神 **8** 篇 · yiduobo **0** 篇；`heappush_max` 灵神 **7** 篇 · yiduobo **0** 篇；`heappop_max` 灵神 **4** 篇 · yiduobo **0** 篇

Python 3.14 终于提供了**最大堆**函数，不用再存相反数。灵神的新题解已经在用（LeetCode 已升级到 3.14）。

```python
# py3.14
from heapq import heapify_max, heappush_max, heappop_max, heapreplace_max
h = [3, 1, 4, 1, 5]
heapify_max(h)
print(h[0])                     # 5
heappush_max(h, 9)
print(heappop_max(h))           # 9
print(heapreplace_max(h, 0))    # 5
print(h[0])                     # 4
```

**刷题中怎么用**：课程表 III（灵神 0630）：`day -= heapreplace_max(h, duration) - duration`，用更短的课替换最长的课；灵神 0295 左半部分用最大堆 `heappush_max(self.left, ...)`。

> **易错点**
> 本地 Python 版本低于 3.14 时会 `ImportError`，此时退回"存相反数"写法。

## 5. bisect：二分查找（以及有序容器 SortedList）

`bisect` 在**已排序**的序列上做二分，O(log n)。只要记住一句话：

- `bisect_left(a, x)`：第一个 **≥ x** 的位置
- `bisect_right(a, x)`：第一个 **> x** 的位置

```
a =      [1, 2, 2, 2, 5]
下标:     0  1  2  3  4
bisect_left(a, 2)  = 1   ← 插在所有 2 的左边
bisect_right(a, 2) = 4   ← 插在所有 2 的右边
```

### bisect_left
> 频次：灵神 **144** 篇 · yiduobo **0** 篇

**签名**：`bisect_left(a, x, lo=0, hi=len(a), *, key=None)` · O(log n)（`key` 参数 3.10+）

```python
from bisect import bisect_left
a = [1, 2, 2, 2, 5]
print(bisect_left(a, 2))            # 1
print(bisect_left(a, 3))            # 4
print(bisect_left(a, 9))            # 5  ← 可能等于 len(a)，访问前要判断
i = bisect_left(a, 2)
print(i < len(a) and a[i] == 2)     # True  ← 判断 2 是否存在
print(bisect_left(a, 2, lo=2))      # 2  ← 只在 a[2:] 里找
```

**刷题中怎么用**：
1. **查找区间**：`start = bisect_left(nums, target)`；`end = bisect_right(nums, target) - 1`（灵神 0034）。
2. **统计 ≥ / < 某值的个数**：`n - bisect_left(a, x)` 是 ≥ x 的个数。
3. **LIS 贪心 + 二分**（0300）：`j = bisect_left(g, x); if j == len(g): g.append(x) else: g[j] = x`。
4. **二分答案（灵神招牌写法）**：把 `range` 当成"有序数组"，用 `key` 把每个候选答案映射成 `False/True`，然后找第一个 `True`：

```py
# 灵神 1283：找最小的除数 d，使得 check(d) 为 True
return bisect_left(range(max(nums)), True, 1, key=check)
# 灵神 0033：在旋转数组中找分界
i = bisect_left(range(len(nums) - 1), True, key=check)
```

```python
from bisect import bisect_left
def check(d):           # 单调：d 越大越容易满足
    return d * d >= 50
print(bisect_left(range(100), True, key=check))   # 8  ← 最小的 d 满足 d*d>=50
print(bisect_left(range(100), True, 1, key=check))  # 8  ← lo=1，从 1 开始
```

普查中 `bisect_left` 的 `key=` 被灵神用了 95 次，几乎都是这种"二分答案"。`range` 支持 O(1) 下标访问，所以不用真的建列表。

> **易错点**
> `key` 只作用于**数组元素**，不作用于 `x`：`bisect_left(a, x, key=f)` 比较的是 `f(a[i])` 和 `x`。所以二分答案时 x 写 `True`，而不是 `check(True)`。

### bisect_right / bisect
> 频次：灵神 **36** 篇 · yiduobo **0** 篇

`bisect.bisect` 就是 `bisect_right` 的别名。

```python
from bisect import bisect_right
letters = ["c", "f", "j"]
i = bisect_right(letters, "c")
print(i, letters[i % len(letters)])    # 1 f  ← 0744 寻找比目标字母大的最小字母
a = [1, 3, 3, 7]
print(bisect_right(a, 3) - 1)          # 2  ← 最后一个 <= 3 的下标
```

**刷题中怎么用**：`i = bisect_right(letters, target)`（灵神 0744）；花期内花的数目（灵神 2251）：`bisect_right(starts, p) - bisect_left(ends, p)`。

### insort
> 频次：普查 0 次（两位作者都用 SortedList 或手写）

**作用**：二分找到位置后插入，保持有序。查找 O(log n) 但插入是 O(n)。

```python
from bisect import insort
a = [1, 4, 6]
insort(a, 5)
print(a)       # [1, 4, 5, 6]
```

### SortedList（sortedcontainers）
> 频次：灵神 **26** 篇 · yiduobo **0** 篇；`SortedSet/SortedDict` 共 3 篇；方法 `.bisect_left` 灵神 **15** 篇 · yiduobo **0** 篇

**作用**：一直保持有序的列表，增删查 O(log n)（近似），支持下标访问。LeetCode 预装了 `sortedcontainers`。Python 标准库没有平衡树，这是最接近 C++ `multiset` / Java `TreeMap` 的东西。

| 操作 | 写法 |
|---|---|
| 插入 | `sl.add(x)` |
| 删除（必须存在） | `sl.remove(x)` |
| 删除（可不存在） | `sl.discard(x)` |
| 第 k 小 | `sl[k]`，最大 `sl[-1]` |
| 弹出 | `sl.pop(i=-1)` |
| 二分 | `sl.bisect_left(x)` / `sl.bisect_right(x)` |
| 区间遍历 | `sl.irange(lo, hi)` |

```python
from sortedcontainers import SortedList
sl = SortedList([5, 1, 3])
sl.add(4)
print(list(sl))             # [1, 3, 4, 5]
print(sl[0], sl[-1])        # 1 5
i = sl.bisect_left(4)
print(i, sl[i])             # 2 4  ← 第一个 >= 4 的元素
sl.discard(100)             # 不存在也不报错
sl.remove(3)
print(list(sl.irange(2, 5)))   # [4, 5]
print(sl.pop(0), list(sl))  # 1 [4, 5]
```

**刷题中怎么用**：
- 避免洪水泛滥：`dry_day = SortedList()` 存未使用的晴天，`i = dry_day.bisect_left(...)` 找第一个合适的晴天，再 `dry_day.discard(d)`（灵神 1488）。
- 最近的房间：`room_ids = SortedList()`（灵神 1847，离线 + 有序集合）。
- 灵神 3510：`s, i = sl.pop(0)  # 删除相邻元素和最小的一对`。

> **易错点**
> `SortedList` 不能 `sl[i] = x` 赋值，也没有 `append/insert`（会破坏有序性）；本地需 `pip install sortedcontainers`。

## 6. itertools：迭代工具

`itertools` 里的函数都返回**惰性迭代器**：不立刻算出结果，用一个算一个。要看结果需要 `list(...)`，或者直接 `for` 遍历。普查结果显示：**itertools 是灵神的专属武器**，yiduobo 一次都没用过。

### accumulate
> 频次：灵神 **83** 篇 · yiduobo **0** 篇

**作用**：累积运算，默认是前缀和；可以传任意二元函数（如 `max`、`operator.xor`）。
**签名**：`accumulate(iterable, func=operator.add, *, initial=None)` · O(n)

```python
from itertools import accumulate
nums = [3, 1, 4, 1]
print(list(accumulate(nums)))               # [3, 4, 8, 9]
print(list(accumulate(nums, initial=0)))    # [0, 3, 4, 8, 9]  ← 前缀和标准写法
print(list(accumulate(nums, max)))          # [3, 3, 4, 4]     ← 前缀最大值
from operator import xor
print(list(accumulate([1, 2, 3], xor, initial=0)))   # [0, 1, 3, 0]
```

**前缀和公式**：`s = list(accumulate(nums, initial=0))` 之后，子数组 `nums[l..r]` 的和 = `s[r + 1] - s[l]`。

```python
from itertools import accumulate
nums = [2, -1, 3, 5]
s = list(accumulate(nums, initial=0))
l, r = 1, 3
print(s, s[r + 1] - s[l])    # [0, 2, 1, 4, 9] 7
```

**刷题中怎么用**：
- 区域和检索：`self.s = list(accumulate(nums, initial=0))`（灵神 0303）。普查中 `accumulate` 的 `initial=` 关键字被用了 86 次。
- 对生成器求前缀和：`acc = list(accumulate((2 - c for c in s), initial=0))`（灵神 0481）。
- 后缀最大值（前后缀分解类题目可以这样一行求出；灵神 0042 用的是显式循环）：`suf_max = list(accumulate(reversed(height), max))[::-1]`。

> **易错点**
> 不加 `initial=0` 时 `s[i]` 是 `nums[0..i]` 之和，公式要改成 `s[r] - s[l-1]` 且要特判 `l = 0`；加了 `initial=0` 长度变成 `n+1`，下标统一，不易错。

### pairwise
> 频次：灵神 **86** 篇 · yiduobo **0** 篇

**作用**：相邻两两配对 `(a[0],a[1]), (a[1],a[2]), ...`（Python 3.10+）。

```python
from itertools import pairwise
print(list(pairwise([1, 3, 6])))   # [(1, 3), (3, 6)]
print(list(pairwise("abc")))       # [('a', 'b'), ('b', 'c')]
nums = [1, 2, 2, 5]
print(sum(x == y for x, y in pairwise(nums)))  # 1  ← 相邻相等的对数
```

**刷题中怎么用**：罗马数字转整数 `for x, y in pairwise(s):  # 遍历 s 中的相邻字符`（灵神 0013）；`for x, y in pairwise(nums):`（灵神 0026）；构造映射 `dict(pairwise("croakc"[::-1]))`（灵神 1419）。替代了容易写错的 `for i in range(1, n): a[i-1], a[i]`。

### count
> 频次：灵神 **23** 篇 · yiduobo **0** 篇

**作用**：无限计数器 `start, start+step, ...`，配合 `break` 当作"不知道上界的 for 循环"。

```python
from itertools import count
for i in count(1):
    if i * i > 30:
        break
print(i)                   # 6
c = count(10, 5)
print(next(c), next(c))    # 10 15
```

**刷题中怎么用**：字符串解码 `for j in count(i + 1):  # 从 i+1 开始向右遍历，找匹配的右括号`（灵神 0394）；灵神 0279 注释"`while True` 也可以写 `for step in count(0)`"。

> **note**
> 普查中名为 `count` 的调用要和变量名、`list.count` 区分：脚本只把**未被重新赋值的裸名** `count(...)` 归到 `itertools.count`。

### permutations
> 频次：灵神 **8** 篇 · yiduobo **0** 篇

**作用**：长度为 r 的所有排列（有序），数量 `n!/(n-r)!`。按**位置**区分元素，有重复值时会产生重复排列。

```python
from itertools import permutations
print(list(permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
print(len(list(permutations(range(4)))))  # 24
print(len(set(permutations("aab"))))      # 3  ← 用 set 去重
```

**刷题中怎么用**：`for perm in permutations(a, i):  # 枚举 a 的长为 i 的排列`（灵神 2014）；`for a, b in permutations(ascii_lowercase, 2):  # 枚举所有小写字母对`（灵神 2272）。面试题"全排列 0046"通常要求手写回溯，不要直接调库。

### combinations
> 频次：灵神 **6** 篇 · yiduobo **0** 篇

**作用**：长度为 r 的所有组合（无序，按输入顺序输出），数量 `C(n, r)`。

```python
from itertools import combinations
print(list(combinations("abcd", 2)))
# [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
print(len(list(combinations(range(5), 3))))  # 10
```

**刷题中怎么用**：最大三角形面积 `for p1, p2, p3 in combinations(points, 3):`（灵神 0812）；`for a, b in combinations(groups.values(), 2):  # 枚举所有组对`（灵神 2306）。

### product
> 频次：灵神 **1** 篇 · yiduobo **0** 篇

**作用**：笛卡尔积，相当于多重 for 循环；`repeat=k` 表示同一个序列自乘 k 次。

```python
from itertools import product
print(list(product([0, 1], "ab")))  # [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]
print(len(list(product(range(3), repeat=4))))  # 81
dirs = [(dx, dy) for dx, dy in product((-1, 0, 1), repeat=2) if dx or dy]
print(len(dirs))                    # 8  ← 八方向
```

**刷题中怎么用**：`sum(map(min, product(row_max, col_max))) - sum(map(sum, grid))`（灵神 0807 保持城市天际线）。

### groupby
> 频次：灵神 **7** 篇 · yiduobo **0** 篇

**作用**：把**连续相同**的元素分成一组。返回 `(key, 组迭代器)`。

```python
from itertools import groupby
s = "aaabccdd"
print([(k, len(list(g))) for k, g in groupby(s)])
# [('a', 3), ('b', 1), ('c', 2), ('d', 2)]
print(["".join(g) for _, g in groupby("1122211")])  # ['11', '222', '11']
```

**刷题中怎么用**：删除字符使字符串变好 `for _, group in groupby(s):`（灵神 1957）；二叉树垂序遍历 `[[d[2] for d in g] for _, g in groupby(data, key=lambda d: d[0])]`（灵神 0987）。

> **易错点**
> 只合并**相邻**的相同元素：`groupby("aba")` 得到 3 组。想按值全局分组要先排序，或者用 `defaultdict(list)`。组迭代器 `g` 在进入下一组后失效，要先 `list(g)`。

### chain / chain.from_iterable
> 频次：灵神 **3** 篇 · yiduobo **0** 篇

**作用**：把多个可迭代对象首尾相接；`chain.from_iterable` 用于"展平一层"。

```python
from itertools import chain
print(list(chain([1, 2], (3,), "ab")))           # [1, 2, 3, 'a', 'b']
print(list(chain.from_iterable([[1], [2, 3]])))  # [1, 2, 3]
```

**刷题中怎么用**：BFS 一行求下一层 `q = list(chain.from_iterable((node.left, node.right) for node in q))`（灵神 2415）。

### zip_longest
> 频次：灵神 **2** 篇 · yiduobo **0** 篇

```python
from itertools import zip_longest
print(list(zip_longest([1, 2, 3], [9], fillvalue=0)))  # [(1, 9), (2, 0), (3, 0)]
print("".join(c for z in zip_longest("ab", "pqrs") for c in z if c))  # apbqrs
```

**刷题中怎么用**：比较版本号 `for ver1, ver2 in zip_longest(a, b, fillvalue=0):`（灵神 0165）；交替合并字符串（灵神 1768，上面第二个例子）。

### 其他：islice / combinations_with_replacement / batched（了解）

```python
from itertools import islice, combinations_with_replacement
print(list(islice(range(100), 2, 10, 3)))                 # [2, 5, 8]
print(len(list(combinations_with_replacement("ab", 2))))  # 3
```

## 7. functools：记忆化搜索与函数工具

### @cache（记忆化）
> 频次：灵神 **223** 篇 · yiduobo **0** 篇（作为装饰器 `@cache`：灵神 **223** 篇 · yiduobo **0** 篇）

**作用**：给函数加一个"字典缓存"：相同参数第二次调用时直接返回上次结果。把指数级的暴力递归变成 O(状态数 × 每个状态的计算量)。Python 3.9+。
**签名**：`@cache` 放在 `def` 上一行；参数必须**可哈希**（int、str、tuple 可以；list、set 不行）

```python
from functools import cache
calls = 0
def fib_slow(n):
    global calls; calls += 1
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)
fib_slow(20)
print(calls)                 # 21891

calls = 0
@cache
def fib(n):
    global calls; calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(20), calls)        # 6765 21
print(fib(100))              # 354224848179261915075
```

**刷题中怎么用**：这是灵神 DP 题解的"第一步"——先写记忆化搜索，再 1:1 翻译成递推（灵神 0062、0070、1143 等，灵神 0010 注释"缓存装饰器，避免重复计算 dfs（一行代码实现记忆化）"）：

```py
# 灵神 0062 不同路径（记忆化搜索版）
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @cache
        def dfs(i: int, j: int) -> int:
            if i < 0 or j < 0:
                return 0
            if i == 0 and j == 0:
                return 1
            return dfs(i - 1, j) + dfs(i, j - 1)
        return dfs(m - 1, n - 1)
```

**yiduobo 的做法**：普查中 yiduobo 从未使用 `@cache`（Python 2 没有），而是自己写字典 / 数组记忆化，或直接写递推 DP：

```python
def dfs(i, memo={}):
    if i in memo:
        return memo[i]
    res = i if i < 2 else dfs(i - 1) + dfs(i - 2)
    memo[i] = res
    return res
print(dfs(50))      # 12586269025
```

> **易错点**
> 1. 递归太深会 `RecursionError`（默认上限约 1000），状态链很长的题要改递推或 `sys.setrecursionlimit`。
> 2. `@cache` 定义在 `class` 外（模块级）时，缓存会在多个测试用例间共享——一般是好事（灵神 0279、0935、1387 把 `@cache def dfs` 写在类外面，多组数据共用缓存），但如果函数依赖了外部变量就会出错。
> 3. 参数里有 list 会报 `TypeError: unhashable type: 'list'`，改成 tuple。

### cache_clear
> 频次：灵神 **19** 篇 · yiduobo **0** 篇

**作用**：清空 `@cache` 的缓存，释放内存。

```python
from functools import cache
@cache
def sq(x):
    return x * x
sq(3); sq(4)
print(sq.cache_info().currsize)   # 2
sq.cache_clear()
print(sq.cache_info().currsize)   # 0
```

**刷题中怎么用**：灵神 1690 `dfs.cache_clear()  # 防止爆内存`、灵神 2435 `dfs.cache_clear()  # 避免超出内存限制`。状态数很大时（如 10^6 级别），在 `return` 之前清空，能避免 MLE。

### @lru_cache
> 频次：两位作者均未使用（普查 0 次），但在 3.8 及更早版本的题解中极常见

**作用**：带容量上限的缓存。`@lru_cache(None)`（或 `maxsize=None`）等价于 `@cache`。

```python
from functools import lru_cache
@lru_cache(maxsize=None)
def C(n, k):
    return 1 if k == 0 or k == n else C(n - 1, k - 1) + C(n - 1, k)
print(C(30, 15))      # 155117520
```

### reduce
> 频次：灵神 **20** 篇 · yiduobo **0** 篇

**作用**：用二元函数把序列"折叠"成一个值：`reduce(f, [a, b, c]) = f(f(a, b), c)`。Python 2 里 `reduce` 是内置函数，Python 3 移到了 functools。

```python
from functools import reduce
from operator import xor, mul, or_
print(reduce(xor, [4, 1, 2, 1, 2]))     # 4  ← 只出现一次的数字
print(reduce(mul, [1, 2, 3, 4]))        # 24
print(reduce(or_, [1, 2, 4], 0))        # 7  ← 第三个参数是初值
from math import gcd
print(reduce(gcd, [12, 18, 24]))        # 6
```

**刷题中怎么用**：只出现一次的数字 `return reduce(xor, nums)`（灵神 0136）；`xor_all = reduce(xor, nums)`（灵神 0260）。

### cmp_to_key
> 频次：灵神 **3** 篇 · yiduobo **0** 篇

**作用**：把"比较函数"（返回负/零/正）转成 `key=` 能用的东西。用于无法写成简单 key 的排序规则。

```python
from functools import cmp_to_key
nums = ["3", "30", "34", "5", "9"]
nums.sort(key=cmp_to_key(lambda a, b: int(b + a) - int(a + b)))
print("".join(nums))      # 9534330
```

**刷题中怎么用**：最大数（灵神 0179，就是上面的例子）；按分数大小排序 `a.sort(key=cmp_to_key(lambda p, q: p[0] * q[1] - q[0] * p[1]))`（灵神 3273，交叉相乘避免浮点）。

对比 yiduobo（Python 2）：`nums = sorted(nums, self.cmp)`（yiduobo 0179）——Python 2 的 `sorted` 第二个位置参数就是 `cmp` 函数，Python 3 已删除，必须改成 `key=cmp_to_key(...)`。

## 8. math / operator / 位运算 / 其他小模块

### 8.1 math

### math.inf
> 频次：灵神 **272** 篇 · yiduobo **0** 篇

**作用**：正无穷浮点数，比任何数都大；`-inf` 比任何数都小。是灵神**最常用的库成员**（共 746 处）。

```python
from math import inf
ans = inf
for x in [5, 3, 8]:
    ans = min(ans, x)
print(ans)                      # 3
print(inf > 10 ** 100, -inf < -10 ** 100)   # True True
print(inf - inf)                # nan  ← 未定义
a = [3, 7]
print([-inf] + a + [inf])       # [-inf, 3, 7, inf]  ← 哨兵
```

**三种"无穷大"写法对比**：

| 写法 | 谁在用 | 优点 | 缺点 |
|---|---|---|---|
| `inf`（`math.inf`） | 灵神 272 篇 | 短，语义清晰 | 是 float，`return ans` 前若可能仍是 inf 要特判 |
| `float('inf')` | 两人都 0 篇 | 无需 import | 长 |
| `10 ** 9`、`10 ** 18` | yiduobo 221 篇（含取模用法） | 保持 int | 要估算上界，太小会出错 |

**刷题中怎么用**：寻找两个正序数组的中位数 `a = [-inf] + a + [inf]`（灵神 0004，加哨兵免边界判断）；最小值初始化 `ans = inf`（灵神 0016）；最后 `return ans if ans < inf else -1`。

### math.gcd / math.lcm
> 频次：`gcd` 灵神 **33** 篇 · yiduobo **0** 篇；`lcm` 灵神 **10** 篇 · yiduobo **0** 篇

**作用**：最大公约数 / 最小公倍数。3.9+ 支持多个参数。O(log min(a,b))。

```python
from math import gcd, lcm
print(gcd(12, 18), lcm(4, 6))   # 6 12
print(gcd(0, 5))                # 5
print(gcd(12, 18, 27))          # 3  ← 3.9+ 多参数
```

**刷题中怎么用**：`step = gcd(b, n)`（灵神 1625）；预处理互质表 `[[j for j in range(1, MX) if gcd(i, j) == 1] ...]`（灵神 1766）；`x = lcm(x, st.pop())`（灵神 2197）。yiduobo 0878、0914 自己写了 `self.gcd(a, b)`（Python 2 的 `math` 早期没有 gcd，只有 `fractions.gcd`）。

### math.isqrt / math.sqrt
> 频次：`isqrt` 灵神 **34** 篇 · yiduobo **0** 篇；`sqrt` 灵神 **7** 篇 · yiduobo **27** 篇

**作用**：`isqrt(n)` 返回 ⌊√n⌋ 的**精确整数**（3.8+）；`sqrt(x)` 返回浮点数。

```python
from math import isqrt, sqrt
n = 10 ** 30 + 1
print(isqrt(n) == 10 ** 15)        # True
print(int(sqrt(n)) == 10 ** 15)    # True
m = (10 ** 15 + 1) ** 2 - 1        # 比完全平方数小 1
print(isqrt(m) == 10 ** 15)        # True
print(int(sqrt(m)) == 10 ** 15)    # False ← 浮点误差，sqrt 给出了错误的整数
print(isqrt(17) ** 2 == 17)        # False ← 判断完全平方数的正确写法
```

**刷题中怎么用**：完全平方数 `return dfs(isqrt(n), n)`（灵神 0279）；yiduobo 0279 `t = int(sqrt(i))`、0319 灯泡开关 `return int(sqrt(n))`（小范围没问题，大数有精度风险）。

### math.comb / math.perm / factorial
> 频次：`comb` 灵神 **22** 篇 · yiduobo **0** 篇；`factorial` 灵神 **1** 篇 · yiduobo **0** 篇

```python
from math import comb, perm, factorial
print(comb(5, 2), perm(5, 2), factorial(5))   # 10 20 120
print(comb(3, 5))                             # 0  ← k > n 返回 0
```

**刷题中怎么用**：不同路径直接用组合数 `return comb(m + n - 2, m - 1)`（灵神 0062 数学解法）；有效三角形 `ans = comb(m, 3)`（灵神 0611）。要取模时 Python 大整数也能算，但 n 很大时应预处理阶乘和逆元。

### math.ceil / math.floor
> 频次：`ceil` 灵神 **7** 篇 · yiduobo **1** 篇；`floor` 灵神 **3** 篇 · yiduobo **1** 篇

```python
from math import ceil, floor
print(ceil(2.1), floor(2.9), floor(-2.1))   # 3 2 -3
a, b = 7, 2
print(ceil(a / b), (a + b - 1) // b, -(-a // b))   # 4 4 4  ← 后两种是纯整数上取整
```

**刷题中怎么用**：`n = ceil((-1 + (8 * target + 1) ** 0.5) / 2)`（灵神 0754 解一元二次方程）。整数上取整推荐 `(a + b - 1) // b` 或 `-(-a // b)`，避免浮点误差。

### math.pi / cbrt / 三角函数 / log（了解）
> 频次：`pi` 灵神 **0** 篇 · yiduobo **4** 篇；`cbrt` 灵神 **3** 篇 · yiduobo **0** 篇；`log` 灵神 **0** 篇 · yiduobo **1** 篇

yiduobo 0478 在圆内随机生成点：`theta = 2 * math.pi * random.random()`；yiduobo 0483 `max_p = int(log(float(n)) / log(2))`。

```python
import math
print(round(math.pi, 4), math.log2(1024), math.log(math.e))   # 3.1416 10.0 1.0
print(math.cbrt(27), round(math.cbrt(27)))   # 3.0000000000000004 3  ← 立方根(3.11+)，有浮点误差，取整前要 round
```

### 8.2 operator / string / random / copy

### operator.xor / or_ / add / mul / itemgetter
> 频次：`xor` 灵神 **13** 篇 · yiduobo **0** 篇；`or_` 灵神 **7** 篇 · yiduobo **0** 篇；`mul` 灵神 **2** 篇 · yiduobo **0** 篇

**作用**：把运算符变成函数，方便传给 `reduce` / `accumulate` / `map`。`or_`、`and_` 带下划线是因为 `or`、`and` 是关键字。

```python
from operator import xor, or_, add, itemgetter
from functools import reduce
from itertools import accumulate
print(reduce(xor, [5, 5, 7]))                # 7
print(reduce(or_, [1, 4]))                   # 5
print(list(accumulate([1, 2, 3], add)))      # [1, 3, 6]
pairs = [(2, "b"), (1, "a")]
print(sorted(pairs, key=itemgetter(0)))      # [(1, 'a'), (2, 'b')]
```

**刷题中怎么用**：`reduce(xor, nums)`（灵神 0136）；按位或的前缀 `accumulate(nums, or_)`。

### string.ascii_lowercase
> 频次：灵神 **24** 篇 · yiduobo **0** 篇

```python
from string import ascii_lowercase, ascii_uppercase, digits
print(ascii_lowercase)        # abcdefghijklmnopqrstuvwxyz
print(len(ascii_uppercase), digits)   # 26 0123456789
```

**刷题中怎么用**：并查集初始化 `fa = {c: c for c in ascii_lowercase}`（灵神 1061）；`score = dict(zip(ascii_lowercase, score))`（灵神 1255）；`permutations(ascii_lowercase, 2)`（灵神 2272）。

### random.randint / randrange / random / shuffle
> 频次：`randint` 灵神 **6** 篇 · yiduobo **14** 篇；`randrange` 灵神 **3** 篇 · yiduobo **0** 篇

```python
import random
random.seed(0)
x = random.randint(1, 6)          # 闭区间 [1, 6]
y = random.randrange(0, 10, 2)    # 左闭右开，步长 2
print(1 <= x <= 6, y % 2 == 0)    # True True
a = [1, 2, 3]; random.shuffle(a)
print(sorted(a))                  # [1, 2, 3]
```

**刷题中怎么用**：随机化快排 / 快速选择的 pivot `i = randint(left, right)`（灵神 0215、0912）；O(1) 插入删除获取随机元素 `self.num_list[random.randint(0, len(self.num_list) - 1)]`（yiduobo 0380，更简洁的是 `random.choice(self.num_list)`）。

> **易错点**
> `randint(a, b)` 是**闭区间**，两端都能取到；`randrange(a, b)` 和 `range` 一样不含 b。

### datetime（了解）
> 频次：灵神 **3** 篇 · yiduobo **0** 篇

日期类题（一周中的第几天 1185、一年中的第几天 1154 等）灵神给出了库函数写法：

```python
from datetime import datetime, date
print(date(2026, 10, 19).strftime("%A"))                    # Monday
print(datetime.strptime("2019-02-10", "%Y-%m-%d").timetuple().tm_yday)  # 41
print((date(2020, 1, 15) - date(2019, 12, 31)).days)        # 15
```

### copy.deepcopy
> 频次：灵神 **0** 篇 · yiduobo **7** 篇

```python
import copy
f = [[1, 2], [3]]
g = copy.deepcopy(f)
g[0][0] = 99
print(f, g)       # [[1, 2], [3]] [[99, 2], [3]]
```

**刷题中怎么用**：yiduobo 3320、3343 `g = copy.deepcopy(f)` 复制二维 DP 表。更快的写法是 `g = [row[:] for row in f]`。

### 8.3 运算符：// % ** 与负数

> 频次：`//` 灵神 **469** 篇 · yiduobo **257** 篇；`%` 灵神 **467** 篇 · yiduobo **783** 篇；`/` 灵神 **42** 篇 · yiduobo **546** 篇；`**` 灵神 **76** 篇 · yiduobo **292** 篇

Python 的 `//` 是**向下取整**（向 −∞），`%` 的结果**符号与除数相同**，并且始终满足 `a == (a // b) * b + a % b`。这与 C++/Java 的"向 0 截断"不同。

```python
print(7 // 2, -7 // 2)        # 3 -4
print(7 % 3, -7 % 3, 7 % -3)  # 1 2 -2
print(int(-7 / 2))            # -3  ← 向 0 截断的写法
print(2 ** 10, 2 ** -1)       # 1024 0.5
print(7 / 2)                  # 3.5  ← Python 3 的 / 永远是浮点除法
MOD = 1_000_000_007
print((3 - 5) % MOD)          # 1000000005  ← 负数取模自动变成非负，不用 +MOD
```

**刷题中怎么用**：
- 取模：普查中 `MOD = 1_000_000_007` 这个常量灵神写了 107 篇，`f[i] = (f[i - 1] * 2 + f[i - 3]) % MOD`（灵神 0790）。yiduobo 写成 `mod = 10 ** 9 + 7`（yiduobo 0552、0576）。
- 二分取中点：灵神 `mid = (left + right) // 2`；yiduobo 习惯 `mid = (left + right) >> 1`（yiduobo 0244、0475）。
- 循环下标：`(i + 1) % n`、`(i - 1) % n`（负数也会正确绕回）。
- **yiduobo 的 `/`**：yiduobo 有 546 篇用了 `/`，在 Python 2 里整数相除就是整除，如 `k = (m + n + 1) / 2`（yiduobo 0004）。照抄到 Python 3 必须改成 `//`，详见第 10 章。

### 8.4 位运算 & | ^ ~ << >>

> 频次：`&` 灵神 **222** 篇 · yiduobo **218** 篇；`|` 灵神 **135** 篇 · yiduobo **90** 篇；`^` 灵神 **128** 篇 · yiduobo **127** 篇；`<<` 灵神 **191** 篇 · yiduobo **135** 篇；`>>` 灵神 **126** 篇 · yiduobo **117** 篇；`~` 灵神 **27** 篇 · yiduobo **3** 篇

| 运算 | 含义 | 常见用途 |
|---|---|---|
| `a & b` | 按位与 | 判断某位 `x >> i & 1`；取最低位 `x & -x` |
| `a \| b` | 按位或 | 置位 `s \| (1 << i)` |
| `a ^ b` | 按位异或 | 翻转某位；找唯一数；`x ^ x == 0` |
| `~a` | 按位取反，等于 `-a - 1` | `~i` 作倒数下标 `a[~i] == a[-i-1]` |
| `a << k` | 左移，乘 2^k | `1 << n` 是全集大小 |
| `a >> k` | 右移，整除 2^k（向下取整） | 二进制逐位处理 `n >>= 1` |

```python
x = 0b10110          # 22
print(x >> 1 & 1, x >> 0 & 1)        # 1 0  ← 第 1 位、第 0 位
print(x & -x)                        # 2   ← lowbit：最低位的 1
print(x & (x - 1))                   # 20  ← 去掉最低位的 1
print(bin(x | 1 << 3))               # 0b11110  ← 置第 3 位
print(bin(x ^ 1 << 1))               # 0b10100  ← 翻转第 1 位
print(~5, [1, 2, 3][~0])             # -6 3
print(-7 >> 1)                       # -4  ← 负数右移也是向下取整
```

**枚举子集**（状压 DP 必备）：

```python
nums = ["a", "b", "c"]
n = len(nums)
subsets = []
for mask in range(1 << n):                       # 灵神 0078
    subsets.append("".join(nums[i] for i in range(n) if mask >> i & 1))
print(subsets)    # ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc']
s = 0b1011        # 枚举 s 的所有非空子集
sub, res = s, []
while sub:
    res.append(bin(sub)[2:])
    sub = (sub - 1) & s
print(res)        # ['1011', '1010', '1001', '1000', '11', '10', '1']
```

**刷题中怎么用**：
- 树状数组：`i += i & -i`（灵神 0307）/ `pos += pos & -pos`（yiduobo 0307）——两人一字不差。
- 只出现一次的数字 III：`lowbit = xor_all & -xor_all`（灵神 0260）/ `lowbit = x & -x`（yiduobo 0260）。
- 快速幂：`while n: if n & 1: ...; x *= x; n >>= 1`（灵神 0050）。
- 字符集压缩成整数：`tmp |= 1 << (ord(char) - 97)`（yiduobo 0318 最大单词长度乘积）。
- 只出现一次的数字 II（状态机）：`a, b = (a ^ x) & (a | b), (b ^ x) & ~a`（灵神 0137）。

> **易错点：运算符优先级**
> Python 的优先级从高到低：`+ -` → `<< >>` → `&` → `^` → `|` → 比较（`== < in`…）。所以：
> - `1 << n - 1` 是 `1 << (n - 1)`（加减先算）；
> - `x & 1 == 0` 是 `(x & 1) == 0`（与 C/Java 相反，C 里 `==` 先算）；
> - `a + b >> 1` 是 `(a + b) >> 1`。
> 拿不准就加括号，yiduobo 0351 写得很保守：`(state & (1 << num)) == (1 << num)`。

```python
n, x = 4, 6
print(1 << n - 1)        # 8
print(x & 1 == 0)        # True
print(3 + 5 >> 1)        # 4
```

### int.bit_length
> 频次：灵神 **109** 篇 · yiduobo **0** 篇

**作用**：二进制表示的位数（不含符号和前导零），`0` 的结果是 0。等价于 `len(bin(abs(x))) - 2`，但快得多。

```python
print((5).bit_length(), (8).bit_length(), (0).bit_length())  # 3 4 0
n = 37
print(1 << (n.bit_length() - 1))   # 32  ← 不超过 n 的最大 2 的幂
print((n - 1).bit_length())        # 6   ← 用于求 ⌈log2 n⌉（n >= 2）
```

**刷题中怎么用**：数字范围按位与 `m = (left ^ right).bit_length()`（灵神 0201）；`shift = xor_all.bit_length() - 1`（灵神 0260）；倍增 / ST 表求层数 `m = n.bit_length()`。

### int.bit_count
> 频次：灵神 **50** 篇 · yiduobo **0** 篇

**作用**：二进制中 1 的个数（popcount），Python 3.10+。

```python
print((7).bit_count(), (8).bit_count())   # 3 1
print(bin(255).count("1"))                # 8  ← 旧写法
```

**刷题中怎么用**：二进制手表 `if h.bit_count() + m.bit_count() == turnedOn:`（灵神 0401）；状压 DP 中已选元素个数 `i = s.bit_count() + 1`（灵神 0526 优美的排列）。

### numpy（灵神的矩阵快速幂）
> 频次：`numpy.array` 灵神 **7** 篇 · yiduobo **0** 篇；`.matrix_power` 灵神 **6** 篇 · yiduobo **0** 篇

灵神在矩阵快速幂题中提供了 numpy 写法（LeetCode 预装 numpy）：

```py
# 灵神 0070 / 0509：f(n) = M^n * f(0)
m = np.array([[1, 1], [1, 0]], dtype=object)   # dtype=object 用 Python 大整数，避免溢出
f0 = np.array([1, 0], dtype=object)
fn = np.linalg.matrix_power(m, n) @ f0        # @ 是矩阵乘法运算符
```

其余配套函数：`np.ones((n,), dtype=object)`（灵神 **4** 篇 · yiduobo **0** 篇）、`np.zeros((n, n), dtype=object)`（灵神 **4** 篇 · yiduobo **0** 篇）初始化向量 / 矩阵（灵神 0935、1931、3337）。普查中 `@` 矩阵乘法运算符出现 8 篇，全部来自这类写法。

## 9. 语法特性与惯用法

这一章统计的是 AST 节点类型（推导式、切片、lambda……），频次同样是"出现的文件数"。

### 列表推导式
> 频次：灵神 **503** 篇 · yiduobo **640** 篇；带 `if` 过滤 灵神 **105** 篇 · yiduobo **3** 篇；多重 `for` 灵神 **33** 篇 · yiduobo **5** 篇

**作用**：一行生成列表：`[表达式 for 变量 in 可迭代对象 if 条件]`。比 `append` 循环更短、更快。

```python
print([x * x for x in range(5)])                   # [0, 1, 4, 9, 16]
print([x for x in range(10) if x % 3 == 0])        # [0, 3, 6, 9]
print([(i, j) for i in range(2) for j in range(2)])  # [(0, 0), (0, 1), (1, 0), (1, 1)]
print([x if x > 0 else 0 for x in [-1, 2, -3]])    # [0, 2, 0]  ← if-else 写在前面
```

**刷题中怎么用**：二维数组初始化 `ans = [[0] * n for _ in range(n)]`（灵神 0059）/ `f = [[0] * (n + 1) for index in range(m + 1)]`（yiduobo 0115）；电话号码组合 `res = [i + j for i in res for j in char_list[int(k)]]`（yiduobo 0017）。

### [x] * n 初始化（以及二维陷阱）
> 频次：灵神 **636** 篇 · yiduobo **610** 篇

```python
f = [0] * 3
print(f)                  # [0, 0, 0]
bad = [[0] * 2] * 3       # 三行是同一个列表对象！
bad[0][0] = 1
print(bad)                # [[1, 0], [1, 0], [1, 0]]
good = [[0] * 2 for _ in range(3)]
good[0][0] = 1
print(good)               # [[1, 0], [0, 0], [0, 0]]
```

> **易错点**
> 二维数组**必须**用推导式 `[[0] * n for _ in range(m)]`，外层用 `*` 会让所有行共享。两位作者的代码里都严格遵守了这一点。

### 生成器表达式
> 频次：灵神 **425** 篇 · yiduobo **8** 篇

**作用**：把列表推导式的 `[]` 换成 `()`，得到惰性生成器，不占 O(n) 内存。直接作为函数唯一参数时可以省略括号。

```python
print(sum(x * x for x in range(4)))         # 14
print(max(len(w) for w in ["a", "abc"]))    # 3
g = (x for x in range(3))
print(list(g), list(g))                     # [0, 1, 2] []  ← 只能遍历一次
```

**刷题中怎么用**：普查中灵神 425 篇 vs yiduobo 8 篇——yiduobo 习惯写 `sum([...])` 先建列表（如 yiduobo 0982），灵神写 `sum(...)`。典型：`return sum(dfs(x) for x in arr) % (10 ** 9 + 7)`（灵神 0823）、`any(dfs(i, j, 0) for i in range(m) for j in range(n))`（灵神 0079）。

### 字典推导式 / 集合推导式
> 频次：字典 灵神 **25** 篇 · yiduobo **53** 篇；集合 灵神 **13** 篇 · yiduobo **1** 篇

```python
nums = [10, 20, 30]
pos = {x: i for i, x in enumerate(nums)}
print(pos)                         # {10: 0, 20: 1, 30: 2}
print({c for c in "hello"} == set("hello"))   # True
print({x % 3 for x in range(10)})  # {0, 1, 2}
```

**刷题中怎么用**：`fa = {c: c for c in ascii_lowercase}`（灵神 1061）；中序遍历值→下标映射 `index = {x: i for i, x in enumerate(inorder)}`（灵神 0105 优化版）。

### 切片 a[i:j:k]
> 频次：灵神 **373** 篇 · yiduobo **690** 篇；反转 `[::-1]` 灵神 **59** 篇 · yiduobo **84** 篇；负数切片 灵神 **45** 篇 · yiduobo **21** 篇；带步长 灵神 **19** 篇 · yiduobo **0** 篇

**作用**：取子序列，**左闭右开**，越界不报错。切片会复制，时间/空间 O(切片长度)。

```python
a = [0, 1, 2, 3, 4, 5]
print(a[1:4], a[:2], a[3:])     # [1, 2, 3] [0, 1] [3, 4, 5]
print(a[-2:], a[:-2])           # [4, 5] [0, 1, 2, 3]
print(a[::2], a[::-1])          # [0, 2, 4] [5, 4, 3, 2, 1, 0]
print(a[10:])                   # []  ← 越界不报错
s = "racecar"
print(s == s[::-1])             # True  ← 回文判断
b = a[:]                        # 浅拷贝
a[:] = [9, 9]                   # 原地替换整个列表内容
print(a, b[:2])                 # [9, 9] [0, 1]
```

**刷题中怎么用**：回文数 `return s == s[::-1]`（灵神 0009）；`word = word[::-1]`（灵神 0079）；`for char in now[::-1]`（yiduobo 0267）；原地修改题 `nums[:] = sorted(set(nums))`（灵神 0026，必须写 `nums[:]` 才能改到调用方传入的列表）。

> **易错点**
> `nums = sorted(nums)` 只是让局部变量指向新列表，LeetCode 检查的原数组不变；"原地修改"题要写 `nums[:] = ...` 或 `nums.sort()`。

### 负下标 a[-1]
> 频次：灵神 **340** 篇 · yiduobo **714** 篇

```python
st = [1, 2, 3]
print(st[-1], st[-2])     # 3 2  ← 栈顶、次栈顶
```

**刷题中怎么用**：单调栈 `while st and nums[st[-1]] <= x:`；`next.append(next[-1].copy())`（yiduobo 0727）。

### 元组解包 / 交换 / 星号解包
> 频次：解包赋值 灵神 **648** 篇 · yiduobo **650** 篇；交换 灵神 **69** 篇 · yiduobo **89** 篇；星号 灵神 0 篇 · yiduobo 0 篇；`for` 中解包 灵神 **994** 篇 · yiduobo **959** 篇

```python
a, b = 1, 2
a, b = b, a                 # 交换，不需要临时变量
print(a, b)                 # 2 1
x, y = divmod(17, 5)
print(x, y)                 # 3 2
first, *rest = [1, 2, 3, 4]
print(first, rest)          # 1 [2, 3, 4]
for i, (u, v) in enumerate([(0, 1), (2, 3)]):
    print(i, u, v)          # 0 0 1 | 1 2 3
f0, f1 = 0, 1
for _ in range(10):
    f0, f1 = f1, f0 + f1    # 右边先全部算完，再同时赋值
print(f0)                   # 55
```

**刷题中怎么用**：DP 空间优化 `f0, f1 = f1, f0 + f1`（灵神 0070、0509）；反转链表 `pre, cur = cur, nxt`；堆元素解包 `_, i, j = heappop(empty_heap)`（灵神 0037）。

> **易错点**
> 链表多重赋值的顺序有讲究：`cur.next, pre, cur = pre, cur, cur.next` 是对的；左边从左到右依次赋值，若先改了 `cur` 再写 `cur.next` 就会写错对象。

### zip(*matrix) 转置 / 调用时解包
> 频次：调用时 `*args` 解包 灵神 **44** 篇 · yiduobo **0** 篇

```python
grid = [[1, 2, 3], [4, 5, 6]]
print([list(col) for col in zip(*grid)])   # [[1, 4], [2, 5], [3, 6]]
print(list(zip(*grid[::-1])))              # [(4, 1), (5, 2), (6, 3)]  ← 顺时针旋转 90°
print(max(*[3, 9, 2]))                     # 9
```

**刷题中怎么用**：`for col in zip(*strs):`（灵神 0014）；矩阵乘法 `for col in zip(*b)`（灵神 0070）。

### 链式赋值 a = b = 0
> 频次：灵神 **493** 篇 · yiduobo **258** 篇

```python
left = ans = 0
print(left, ans)           # 0 0
```

> **易错点**
> `a = b = []` 让 a、b 指向**同一个**列表；对可变对象不要这样写。

### lambda 与 key=
> 频次：`lambda` 灵神 **180** 篇 · yiduobo **165** 篇；`key=lambda` 灵神 **92** 篇 · yiduobo **165** 篇

**作用**：匿名函数 `lambda 参数: 表达式`。最常见的用途是给 `sort / sorted / max / min / bisect` 传 `key`。

```python
people = [[7, 0], [4, 4], [7, 1], [5, 0]]
print(sorted(people, key=lambda p: (-p[0], p[1])))
# [[7, 0], [7, 1], [5, 0], [4, 4]]  ← 身高降序、k 升序（0406）
words = ["bb", "a", "cc"]
print(min(words, key=lambda w: (len(w), w)))   # a
add = lambda x, y: x + y
print(add(2, 3))                               # 5
```

**刷题中怎么用**：
- 多关键字：`envelopes.sort(key=lambda e: (e[0], -e[1]))`（灵神 0354 俄罗斯套娃信封）。
- yiduobo 的统一风格：`key=lambda d:d[0]`（yiduobo 0252、0616），`sorted(people, key=lambda d:(-d[0], d[1]))`（yiduobo 0406）。
- 打补丁：`ListNode.__lt__ = lambda a, b: a.val < b.val`（灵神 0023）。

### 嵌套函数 / nonlocal / global
> 频次：嵌套函数 灵神 **594** 篇 · yiduobo **414** 篇；`nonlocal` 灵神 **109** 篇 · yiduobo **0** 篇；`global` 灵神 **1** 篇 · yiduobo **47** 篇

**作用**：在方法里定义 `dfs`，它能直接读外层变量（闭包）。但**要给外层变量重新赋值**（如 `ans = max(ans, ...)`、`cnt += 1`），必须先声明 `nonlocal ans`，否则 Python 会把 `ans` 当成新的局部变量并报 `UnboundLocalError`。

```python
def diameter(tree):
    ans = 0
    def dfs(node):
        nonlocal ans
        if node is None:
            return -1
        l, r = dfs(tree.get(node, (None, None))[0]), dfs(tree.get(node, (None, None))[1])
        ans = max(ans, l + r + 2)
        return max(l, r) + 1
    dfs(1)
    return ans
print(diameter({1: (2, 3), 2: (4, 5)}))   # 3
def f():
    lst = []
    def g():
        lst.append(1)       # 修改对象内容（不是重新赋值）不需要 nonlocal
    g()
    return lst
print(f())                  # [1]
```

**刷题中怎么用**：
- 灵神：`ans = 0` + 嵌套 `def dfs` + `nonlocal ans`（灵神 0052 N 皇后 II、0104 二叉树最大深度、0543 直径）。
- yiduobo（Python 2 **没有** `nonlocal`）：要么用实例属性 `self.res`，要么写 `self.dfs(...)` 方法传参（yiduobo 0037、0039、0040 `self.dfs(sorted(candidates), 0, target, [], res)`），少数题用 `global res`（yiduobo 0250、0298）。

> **易错点**
> 在 LeetCode 用 `global` 时，全局变量会在多个测试用例之间保留，必须在每次调用开头重置。

### 海象运算符 :=
> 频次：灵神 **15** 篇 · yiduobo **0** 篇

**作用**：在表达式中赋值（Python 3.8+），省掉一行"先算再判断"。

```python
n, i, s = 20, 1, 0
cnt = 0
while (t := s + i * i) <= n:
    cnt += 1; i += 1
print(cnt, t)             # 4 25
data = [3, 8, 1]
if (m := max(data)) > 5:
    print("max", m)       # max 8
```

**刷题中怎么用**：`while (t := s + i * i) <= n:`（灵神 0279）；倍增 `if (p := pa[x][i]) != -1:`（灵神 1483）。

### f-string
> 频次：灵神 **12** 篇 · yiduobo **0** 篇

```python
s = "25525511135"
i, j, k = 3, 6, 9
print(f"{s[:i]}.{s[i:j]}.{s[j:k]}.{s[k:]}")   # 255.255.111.35
x = 3.14159
print(f"{x:.2f} {255:b} {7:03d}")             # 3.14 11111111 007
```

**刷题中怎么用**：复原 IP 地址 `ans.append(f"{s[:i]}.{s[i:j]}.{s[j:k]}.{s[k:]}")`（灵神 0093）；分数到小数 `f"{''.join(ans[:pos])}({''.join(ans[pos:])})"`（灵神 0166）。yiduobo 的 Python 2 代码用 `%` 格式化（灵神 **0** 篇 · yiduobo **14** 篇）。

### 链式比较 a < b < c
> 频次：灵神 **121** 篇 · yiduobo **83** 篇

```python
x = 5
print(1 <= x <= 9)          # True
print(0 <= 10 < 10)         # False
print(1 < 3 > 2)            # True  ← 等价于 1 < 3 and 3 > 2
```

**刷题中怎么用**：缺失的第一个正数 `while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:`（灵神 0041）；网格越界判断 `0 <= x < m and 0 <= y < n`。yiduobo 0125 则写成 `s[l] >= 'a' and s[l] <= 'z'`。

### 三元表达式 x if c else y
> 频次：灵神 **423** 篇 · yiduobo **12** 篇

```python
n = 7
print("odd" if n % 2 else "even")   # odd
print(max(3, 4) if n > 0 else -1)   # 4
```

**刷题中怎么用**：`return merged[k] if s % 2 else (merged[k] + merged[k + 1]) / 2`（灵神 0004）；`c = chr(ord(b) + 1) if b != 'z' else 'a'`（灵神 2825）。普查差异很大：灵神 423 篇 vs yiduobo 12 篇（yiduobo 偏爱写完整的 if/else 语句）。

### and / or 短路 与 in / is
> 频次：`and/or` 灵神 **800** 篇 · yiduobo **1457** 篇；`in` 灵神 **221** 篇 · yiduobo **636** 篇；`is` 灵神 **115** 篇 · yiduobo **467** 篇

```python
st = []
print(bool(st and st[-1] > 0))    # False  ← st 为空时不会访问 st[-1]
print(0 or 5, "" or "default")    # 5 default  ← or 返回第一个真值
node = None
print(node is None)               # True
print(3 in {1, 2, 3}, "ab" in "cabd")   # True True
```

**刷题中怎么用**：单调栈 `while st and x >= st[-1]:`；`if not root: return 0`；yiduobo 的 `is` 使用量远多于灵神（467 vs 115），多为 `if node is None`，灵神多写 `if node is None` 或 `if not node`。

> **易错点**
> 判断"是否为空节点"用 `is None`；判断数值不要用 `is`（`x is 0` 是错误写法）。`if not x` 在 x 为 0 时也成立，DP 值可能为 0 时别用它判断"未计算"。

### for ... else
> 频次：灵神 **11** 篇 · yiduobo **0** 篇；`while ... else` 灵神 **3** 篇 · yiduobo **0** 篇

**作用**：循环**没有被 break** 时执行 `else` 块。

```python
def is_prime(n):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break
    else:
        return n >= 2
    return False
print([x for x in range(20) if is_prime(x)])   # [2, 3, 5, 7, 11, 13, 17, 19]
```

**刷题中怎么用**：灵神常用来表达"全部检查都通过才执行"，如找不到就返回某值；yiduobo 普查中 0 次。

### del
> 频次：灵神 **54** 篇 · yiduobo **4** 篇

```python
cnt = {"a": 1, "b": 0}
del cnt["b"]
a = [1, 2, 3, 4]
del a[1:3]
print(cnt, a)        # {'a': 1} [1, 4]
```

**刷题中怎么用**：LRU `del self.key_to_node[back_node.key]`（灵神 0146）；LFU `del self.freq_to_dummy[node.freq]  # 移除空链表`（灵神 0460）；滑动窗口计数归零时删 key。

### 增量赋值 += -= 等
> 频次：灵神 **1370** 篇 · yiduobo **2424** 篇

```python
a = [1]
b = a
a += [2]          # 对列表是原地 extend，b 也看得到
print(b)          # [1, 2]
s = "x"
s += "y"          # 字符串不可变，生成新对象
print(s)          # xy
```

### 自定义类 / 魔术方法 __lt__
> 频次：自定义类 灵神 **120** 篇 · yiduobo **170** 篇；`__lt__` 灵神 **1** 篇 · yiduobo **1** 篇

**作用**：设计题（LRU、Trie、并查集、线段树）需要写类；定义 `__lt__` 后对象就能放进堆、能被 `sorted` 比较。

```python
from heapq import heappush, heappop
class Pair:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def __lt__(self, other):          # 灵神 1792 / yiduobo 2102 都这样写
        return self.a * other.b < other.a * self.b   # 按 a/b 比较
h = []
for a, b in [(1, 2), (1, 3), (3, 4)]:
    heappush(h, Pair(a, b))
p = heappop(h)
print(p.a, p.b)       # 1 3
```

**其他魔术方法**：灵神有 3 篇定义 `__sub__`（让自定义的向量/点类支持 `p - q`），yiduobo 有 1 篇 `__str__`（调试打印）。

```python
class P:
    def __init__(self, x, y): self.x, self.y = x, y
    def __sub__(self, o): return P(self.x - o.x, self.y - o.y)
d = P(3, 4) - P(1, 1)
print(d.x, d.y)     # 2 3
```

### 类型注解
> 频次：灵神 **2276** 篇 · yiduobo **0** 篇

灵神几乎每篇都带 LeetCode 模板的类型注解（`def twoSum(self, nums: List[int], target: int) -> List[int]:`），yiduobo 的 Python 2 模板用 docstring `:type nums: List[int]`。注解**不影响运行**，只是提示。

```python
from typing import List, Optional
def f(nums: List[int], k: Optional[int] = None) -> int:
    return len(nums)
print(f([1, 2]))     # 2
```

### match / case（了解）
> 频次：灵神 **2** 篇 · yiduobo **0** 篇

Python 3.10 的结构化模式匹配。灵神 0412 Fizz Buzz 用过 `match (i % 3, i % 5):`。

```python
def fizz(i):
    match (i % 3, i % 5):
        case (0, 0): return "FizzBuzz"
        case (0, _): return "Fizz"
        case (_, 0): return "Buzz"
        case _: return str(i)
print([fizz(i) for i in [3, 5, 15, 7]])   # ['Fizz', 'Buzz', 'FizzBuzz', '7']
```

## 10. Python 2 vs 3：读 yiduobo 代码时的坑

yiduobo 的题解几乎全部是 LeetCode "Python"（即 Python 2）模板：普查中 3618 篇以 `class Solution(object):` 开头，3622 篇带 `:type nums: List[int]` 的 docstring。代码逻辑大多数可以直接在 Python 3 跑，但下面这些地方**照抄会出错或变慢**。

| 写法 | Python 2 含义 | Python 3 正确写法 | 普查（yiduobo） |
|---|---|---|---|
| `a / b`（整数） | 整除 | `a // b` | 546 篇用了 `/` |
| `print x` | 打印语句 | `print(x)` | 14 篇 |
| `xrange(n)` | 惰性 range | `range(n)` | 1 篇 |
| `sorted(a, cmp)` / `cmp=` | 比较函数排序 | `key=cmp_to_key(cmp)` | 至少 2 篇（0179、0469） |
| `d.iteritems()` / `d.has_key(k)` | 惰性遍历 / 判断 key | `d.items()` / `k in d` | 0 篇 |
| `reduce(f, a)` | 内置 | `from functools import reduce` | 0 篇 |
| `map / filter / zip` | 返回 list | 返回迭代器，要 `list(...)` | — |
| `d.keys() / values()` | 返回 list | 返回视图 | — |
| `sys.maxint` | 最大 int | `sys.maxsize` 或 `math.inf` | 0 篇（yiduobo 用 `10 ** 9`） |
| `"%d" % x` | 格式化 | 仍可用；推荐 f-string | 14 篇 |
| `round(2.5)` | `3.0` | `2`（银行家舍入） | — |
| `nonlocal` | 不存在 | 可用 | 用 `self.xxx` 代替 |
| `import Queue` | 队列模块 | `import queue` | 3 篇 |

### `/` 整除问题（最大的坑）
> 频次：`/` 运算 灵神 **42** 篇 · yiduobo **546** 篇；`//` 运算 灵神 **469** 篇 · yiduobo **257** 篇

Python 2 中两个 int 相除 `7 / 2 == 3`；Python 3 中 `7 / 2 == 3.5`。yiduobo 的代码大量依赖前者：

```py
k = (m + n + 1) / 2                    # yiduobo 0004：Py2 整除
now_len = f[index] / 2 * 2             # yiduobo 0005
res.append(chr(v / 16 + 97))           # yiduobo 0271
res = sum(x[0] for x in costs) + sum(delta[:len(costs) / 2])   # yiduobo 1029：切片下标必须是 int
```

在 Python 3 里这几行要么得到浮点数（结果错误），要么直接 `TypeError`（浮点数不能做下标/切片/range 参数）：

```python
m, n = 3, 4
print((m + n + 1) / 2, (m + n + 1) // 2)    # 4.0 4
try:
    [1, 2, 3][len("abcd") / 2]
except TypeError as e:
    print(type(e).__name__)                 # TypeError
print(-7 // 2)                              # -4  ← // 是向下取整（Py2 的 int / 也是向下取整）
```

> **迁移口诀**
> 看到 yiduobo 代码里的 `/`，先判断两边是不是整数：是 → 改成 `//`；本来就想要小数（如求平均值、几何题）→ 保留 `/`。

### print 语句
> 频次：灵神 **0** 篇 · yiduobo **14** 篇

```py
print tmp, next, cnt          # yiduobo 0440（调试残留）
print f, g                    # yiduobo 3003
```

Python 3 写成 `print(tmp, next, cnt)`。注意 Python 2 中 `print(a, b)` 会打印一个**元组** `(1, 2)`。本普查脚本遇到这类语法错误时，会自动把 `print x` 改写为 `print(x)` 后再解析（共修复 15 个代码块）。

### xrange
> 频次：灵神 **0** 篇 · yiduobo **1** 篇

Python 2 的 `range` 会真的建一个列表（大 n 时占内存），所以要用惰性的 `xrange`；Python 3 的 `range` 本身就是惰性的，`xrange` 已删除。yiduobo 1115（交替打印 FooBar）`for i in xrange(self.n):`。

```python
r = range(10 ** 12)          # Python 3：O(1) 内存
print(len(r), r[-1])         # 1000000000000 999999999999
```

### cmp 比较函数
> 频次：灵神 **0** 篇 · yiduobo **1** 篇（另有位置参数写法）

```py
nums = sorted(nums, self.cmp)          # yiduobo 0179：Py2 的第二个位置参数是 cmp
def sort_cmp(x, y): ...                # yiduobo 0469
```

Python 3 写法（灵神 0179）：

```python
from functools import cmp_to_key
def cmp(a, b):
    return -1 if a + b > b + a else (1 if a + b < b + a else 0)
print("".join(sorted(["10", "2"], key=cmp_to_key(cmp))))   # 210
```

### class Solution(object) 与 docstring 类型说明
> 频次：灵神 **1** 篇 · yiduobo **3618** 篇

```py
class Solution(object):           # Py2 需要显式继承 object 才是"新式类"
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
```

Python 3 中所有类都是新式类，`(object)` 可省略；这部分照抄不会出错。

### 字典 / map / zip 返回值
Python 2 中 `d.keys()`、`d.values()`、`map(...)`、`zip(...)` 返回**列表**，可以下标访问、可以多次遍历；Python 3 返回视图或迭代器：

```python
d = {"a": 1, "b": 2}
vals = d.values()
try:
    vals[0]
except TypeError:
    print("视图不能下标")           # 视图不能下标
m = map(int, "12")
print(list(m), list(m))           # [1, 2] []  ← 迭代器只能遍历一次
print(list(d.values())[0])        # 1
```

yiduobo 0049 `return res_dict.values()`、yiduobo 0090 `self.dfs(count_dict.keys(), ...)` 都依赖"返回列表"的行为（后者如果在递归里下标访问 keys 就会出错）。

### 没有 nonlocal → self.xxx / global
见第 9 章。yiduobo 的递归大多写成 `self.dfs(...)` 方法，把结果列表 `res` 作为参数传下去（yiduobo 0039），或用 `global res`（yiduobo 0250）。

### 大数当无穷
> 频次：灵神 **32** 篇 · yiduobo **221** 篇

Python 2 有 `sys.maxint`，但 yiduobo 普查中一次都没用，而是写 `10 ** 9 + 1`（yiduobo 2644）、`right = 10 ** 18`（yiduobo 3929 二分上界）。在 Python 3 中这样写依然有效，且保持 int 类型。

### 并发题：threading.Semaphore
> 频次：灵神 **0** 篇 · yiduobo **6** 篇

LeetCode 的多线程题（1114 按序打印、1115 交替打印 FooBar 等）yiduobo 用信号量解决：

```py
self.first_s = threading.Semaphore(0)   # yiduobo 1114
self.first_s.release()                  # 计数 +1，唤醒等待者
self.first_s.acquire()                  # 计数 -1，为 0 时阻塞
```

```python
import threading
order = []
s = threading.Semaphore(0)
def second():
    s.acquire(); order.append("second")
t = threading.Thread(target=second); t.start()
order.append("first"); s.release(); t.join()
print(order)          # ['first', 'second']
```

### Queue 模块
> 频次：`Queue.Queue` 灵神 **0** 篇 · yiduobo **2** 篇；`Queue.PriorityQueue` 灵神 **0** 篇 · yiduobo **1** 篇；`.put()` 灵神 **0** 篇 · yiduobo **3** 篇

Python 2 的 `Queue` 模块在 Python 3 改名为 `queue`。yiduobo 0023 合并 K 个链表用了 `from Queue import PriorityQueue`，`heap.put(...)` / `heap.get()`。它是**线程安全**的（带锁），比 `heapq` 慢很多，刷题时直接用 `heapq` 即可。

```python
from queue import PriorityQueue
pq = PriorityQueue()
for x in [3, 1, 2]:
    pq.put(x)
print(pq.get(), pq.qsize())     # 1 2
```

### 两位作者风格对照（普查结论）

| 场景 | 灵神（Python 3） | yiduobo（Python 2） |
|---|---|---|
| 计数 | `Counter` / `defaultdict(int)` | `d[k] = d.get(k, 0) + 1` |
| 无穷大 | `inf` | `10 ** 9`、`10 ** 18` |
| 记忆化 | `@cache` | 手写 dict / 递推 DP |
| 外层变量 | `nonlocal` | `self.xxx`、`global` |
| 前缀和 | `list(accumulate(a, initial=0))` | 手写循环 |
| 相邻元素 | `pairwise` | `for i in range(1, n)` |
| 二分 | `bisect_left(..., key=)` | 手写 `while left < right`，`mid = (l + r) >> 1` |
| 倒序遍历 | `reversed(range(n))` | `range(n - 1, -1, -1)` |
| 条件表达式 | 三元表达式、生成器表达式 | 完整 if/else、`sum([...])` |
| 求和计数 | `sum(c == x for c in s)` | 显式 `cnt += 1` |

## 11. 速查表

### 内置函数速查

| 函数 | 一句话 | 复杂度 / 备注 |
|---|---|---|
| `len(x)` | 长度 | O(1) |
| `range(a, b, s)` | 左闭右开整数序列 | 惰性；倒序 `range(n-1, -1, -1)` |
| `enumerate(a, start)` | (下标, 元素) | — |
| `zip(*its)` | 拉链配对；`zip(*m)` 转置 | 取最短 |
| `max/min(it, key=, default=)` | 最值 | O(n)；空序列要 `default` |
| `sum(it, start)` | 求和；布尔求和=计数 | O(n) |
| `sorted(it, key=, reverse=)` | 返回新列表 | O(n log n)，稳定 |
| `int(s, base)` | 转整数；向 0 截断 | `int('101', 2)` |
| `str / list / set / dict / tuple` | 类型转换 | tuple 可哈希 |
| `abs(x)` | 绝对值 | — |
| `ord(c) / chr(i)` | 字符 ↔ 码点 | `ord(c) - ord('a')` |
| `map(f, it)` / `filter(f, it)` | 映射 / 过滤 | 惰性 |
| `all(it) / any(it)` | 全真 / 任一真 | 短路 |
| `pow(b, e, m)` | 快速幂取模 | O(log e)；`pow(x, -1, m)` 逆元 |
| `divmod(a, b)` | (商, 余数) | 下标 → 坐标 |
| `reversed(seq)` | 反向迭代器 | O(1) 创建 |
| `iter(x) / next(it, d)` | 迭代器 / 取下一个 | `next(gen, -1)` 找第一个 |
| `bin / hex / oct` | 进制字符串 | 带前缀，`[2:]` 去掉 |
| `round(x, k)` | 银行家舍入 | `round(2.5) == 2` |

### 容器方法速查

| 容器 | 方法 | 复杂度 |
|---|---|---|
| list | `append(x)` `pop()` | O(1) |
| list | `pop(0)` `insert(i, x)` `remove(x)` `index(x)` `count(x)` `x in a` | O(n) |
| list | `sort(key=, reverse=)` | O(n log n)，返回 None |
| list | `reverse()` `copy()` `extend(it)` `clear()` | O(n) / O(k) |
| str | `''.join(it)` `split(sep)` `strip()` `replace(a, b, k)` | O(n) |
| str | `find / rfind`（-1）`index`（抛异常）`startswith(p, i)` | O(n·m) |
| str | `lower upper isdigit isalpha isalnum islower isupper zfill` | O(n) |
| dict | `get(k, d)` `setdefault(k, d)` `pop(k, d)` `k in d` | O(1) |
| dict | `items() keys() values()` | 视图 |
| dict | `update()` `popitem()`（LIFO） | — |
| set | `add discard remove`，`& \| - ^`，`<=` 子集 | O(1) / O(len) |
| deque | `append appendleft pop popleft`，`q[0] q[-1]` | O(1) |
| Counter | `most_common(k)` `total()` `elements()`，`+ - & \|` | — |
| OrderedDict | `move_to_end(k, last)` `popitem(last)` | O(1) |
| SortedList | `add remove discard bisect_left bisect_right irange pop sl[k]` | O(log n) |
| int | `bit_length()` `bit_count()` | O(1)~O(位数) |

### 标准库速查

| 模块 | 函数 | 一句话 |
|---|---|---|
| heapq | `heapify heappush heappop heapreplace heappushpop` | 最小堆；最大堆存负数或用 3.14 `*_max` |
| heapq | `nlargest(k, it, key) nsmallest` | 前 k 个 |
| bisect | `bisect_left`（≥x）`bisect_right`（>x）`insort` | `key=` 3.10+；二分答案 `bisect_left(range(hi), True, lo, key=check)` |
| collections | `Counter defaultdict deque OrderedDict` | 计数 / 默认值 / 双端队列 / LRU |
| itertools | `accumulate(a, f, initial=0)` | 前缀和 / 前缀最值 |
| itertools | `pairwise count permutations combinations product groupby chain zip_longest` | 相邻对 / 无限计数 / 排列组合 / 积 / 连续分组 / 拼接 |
| functools | `@cache` `.cache_clear()` `lru_cache(None)` | 记忆化搜索 |
| functools | `reduce(f, it, init)` `cmp_to_key(cmp)` | 折叠 / 比较函数排序 |
| math | `inf gcd lcm isqrt sqrt comb perm factorial ceil floor log2 pi` | 数学 |
| operator | `xor or_ and_ add mul itemgetter` | 运算符函数 |
| string | `ascii_lowercase ascii_uppercase digits` | 字符表 |
| random | `randint(a, b)`（闭）`randrange` `choice` `shuffle` `random()` | 随机 |
| copy | `deepcopy` | 深拷贝 |

### 语法惯用法速查

| 惯用法 | 例子 |
|---|---|
| 二维数组 | `f = [[0] * n for _ in range(m)]`（不要 `[[0]*n]*m`） |
| 交换 / 滚动 | `a, b = b, a`；`f0, f1 = f1, f0 + f1` |
| 反转 / 回文 | `s[::-1]`；`s == s[::-1]` |
| 原地替换 | `nums[:] = ...` |
| 转置 | `list(zip(*grid))` |
| 多关键字排序 | `a.sort(key=lambda x: (x[0], -x[1]))` |
| 计数 | `sum(c == 'a' for c in s)` |
| 外层变量 | 嵌套 `def dfs` + `nonlocal ans` |
| 海象 | `while (t := f(i)) <= n:` |
| 链式比较 | `0 <= x < m and 0 <= y < n` |
| 取模 | `MOD = 1_000_000_007`；`(a - b) % MOD` 自动非负 |
| 位运算 | `x >> i & 1`、`x & -x`、`x & (x - 1)`、`1 << n`、`for mask in range(1 << n)` |
| 上取整 | `(a + b - 1) // b` 或 `-(-a // b)` |
| 无穷 | `inf` / `-inf`（`from math import inf`） |
| 自定义比较 | `def __lt__(self, other)` 或 `cmp_to_key` |

### 本地运行灵神代码前的 import 模板

LeetCode 已自动导入以下内容，本地运行时需要手动加上：

```python
from typing import List, Optional
from collections import Counter, defaultdict, deque, OrderedDict
from heapq import heapify, heappush, heappop, heapreplace, heappushpop, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from itertools import accumulate, pairwise, permutations, combinations, product, groupby, count, chain, zip_longest
from functools import cache, lru_cache, reduce, cmp_to_key
from math import inf, gcd, lcm, isqrt, sqrt, comb, ceil, floor
from operator import xor, or_, and_, add, mul, itemgetter
from string import ascii_lowercase
print("ok")   # ok
```

