def _fr(a, b):
    g = math.gcd(a, b)
    return f'{a // g}/{b // g}'


def _txt(S):
    if 'a' in S and 'b' in S:
        a, b = S['a'], S['b']
        return f'第一个集合乘积 `a = {a}`，第二个集合乘积 `b = {b}`，比值 `a/b = {_fr(a, b)}`（target = {S["target"]}）'
    if 'set1' in S and 'set2' in S:
        f = lambda s: '{' + ', '.join(_fmt(x) for x in sorted(s)) + '}'
        return f'左半 `set1` = {f(S["set1"])}，右半 `set2` = {f(S["set2"])}，交集 `{f(S["set1"] & S["set2"])}`'
    if 'set1' in S:
        return '左半枚举完，`set1` 已存好；接着枚举右半'
    return '拆成两半：每半枚举“放第一个 / 第二个集合”，记录 a/b 的最简分数'


def _fmt(t):
    return f'{t[0]}/{t[1]}'


def _cap_if(S, B, ret):
    a, b, t = S.a, S.b, S.target
    if a > t or b > t:
        return f'`a = {a}`、`b = {b}`，有一个 ==超过 target = {t}==：乘积只会越乘越大 → 剪枝'
    if S.i == len(S.nums):
        return f'`a = {a}`、`b = {b}` 没超过 `target = {t}`；`i = {S.i}` = 这一半的长度，这一半全分完了'
    return f'`a = {a}`、`b = {b}` 都不超过 `target = {t}` → 继续分配 `nums[{S.i}] = {S.nums[S.i]}`'


CONFIG = dict(
    num=3566, title='等积子集的划分方案', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='折半枚举 + 最简分数哈希集合',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1459'],
    code='''
class Solution:
    def calc(self, nums: List[int], target: int) -> set[tuple[int, int]]:
        st = set()

        def dfs(i: int, a: int, b: int) -> None:
            if a > target or b > target:
                return
            if i == len(nums):
                g = gcd(a, b)
                st.add((a // g, b // g))  # 最简分数
                return
            dfs(i + 1, a * nums[i], b)
            dfs(i + 1, a, b * nums[i])

        dfs(0, 1, 1)
        return st

    def checkEqualPartitions(self, nums: List[int], target: int) -> bool:
        if prod(nums) != target ** 2:
            return False

        m = len(nums) // 2
        set1 = self.calc(nums[:m], target)
        set2 = self.calc(nums[m:], target)
        return len(set1 & set2) > 0  # 交集不为空
''',
    setup="from math import prod",
    call='Solution().checkEqualPartitions([3, 1, 6, 8, 4], 24)',
    expect=True,
    views=[
        dict(type='text', h=84, fn=_txt, size=24),
        dict(type='array', var=lambda S: S['nums'], label='nums（当前这一半）', h=130, cell=70, pointers={'i': 'blue'}),
        dict(type='calls', h=230, hide=('self',)),
        dict(type='set', var=lambda S: S.get('st'), label='st：这一半出现过的 a/b（最简分数）', h=110, fmt=_fmt),
    ],
    watch=[('i', 'i', 'blue'), ('a', 'a', 'cyan'), ('b', 'b', 'orange'), ('target', 'target', 'green')],
    skip=['st = set()', 'm = len(nums)', '                return', 'g = gcd', 'if i == len(nums)'],
    captions={
        'if prod(nums)': lambda S, B, r: (f'所有数乘积 `{math.prod(S.nums)}`，`target² = {S.target ** 2}` → 相等才可能（必要条件，不充分）'),
        'set1 = self.calc': '左半 `nums[:m]` = `{nums}`：枚举每个数放第一个 / 第二个集合',
        'set2 = self.calc': '右半 `nums[m:]` = `{nums}`：同样枚举，记录 `a/b`',
        'dfs(0, 1, 1)': '从 `dfs(0, 1, 1)` 开始：两个集合乘积都从 `1` 起',
        'if a > target': _cap_if,
        'st.add': '约分：`gcd({a}, {b}) = {g}`，把最简分数 `{a // g}/{b // g}` 记进 `st`（不用浮点数，避免精度误差）',
        'dfs(i + 1, a * nums[i], b)': '`nums[{i-1}] = {nums[i-1]}` 放进第一个集合：`a = {a}`',
        'dfs(i + 1, a, b * nums[i])': '`nums[{i-1}] = {nums[i-1]}` 放进第二个集合：`b = {b}`',
        'return st': '这一半枚举完：`st = {sorted(st)}`',
        'return len(set1 & set2)': lambda S, B, r: f'交集 `{sorted(S.set1 & S.set2)}` ' + ('==非空== → 左右拼起来能让两个集合乘积相等' if r else '为空 → 无解'),
    },
    max_steps=110,
    cards=dict(
        one_liner='把 a₁·b₂ = b₁·a₂ 变形成 a₁/b₁ = a₂/b₂，左右各存一个分数集合',
        complexity='时间 `O(2^(n/2)·log target)`，空间 `O(2^(n/2))`',
        problem=['数组 `nums`（元素互不相同），整数 `target`',
                 '能否分成两个==非空、不相交==的子集，乘积都等于 `target`',
                 '本视频：`[3,1,6,8,4]`, `24` → `true`（`3×8` 与 `1×6×4`）'],
        quote='题目要求 a₁·b₂ = b₁·a₂，变形得 a₁/b₁ = a₂/b₂。我们可以用一个哈希集合维护所有 a₁/b₁ 的最简分数，另一个哈希集合维护所有 a₂/b₂ 的最简分数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先判断总乘积是否等于 `target²`，不等直接 `false`',
              '左半：第一集合乘积 `a₁`、第二集合乘积 `b₁`；右半：第一集合 `b₂`、第二集合 `a₂`',
              '两半各枚举 `2^(n/2)` 种，把 `a/b` 约成最简分数放进集合，看交集',
              '`a` 或 `b` 超过 `target` 就剪枝'],
        result='交集非空，返回 true ✓',
        summary=['时间 `O(2^(n/2)·log target)`，空间 `O(2^(n/2))`',
                 '先查 `prod == target²`；分数用最简形式做 key，不用浮点',
                 '原文还有递归、二进制枚举两种 `O(2^n)` 写法，这里选折半枚举',
                 '运行环境没有 `Set`、`prod`：返回值标注改成了 `set[tuple[int, int]]`，`prod` 在 setup 里导入']
    ),
)
