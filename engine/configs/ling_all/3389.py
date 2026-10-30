def _top(S):
    if 'target' not in S:
        return '先统计 26 个字母的出现次数 `cnt`'
    return f"枚举 `target = {S['target']}`：每种字母的个数要么变成 0，要么变成 {S['target']}"


def _fi(S):
    if 'target' not in S or 'i' not in S or 'f' not in S:
        return ''
    return f"`f[i]` = 操作第 i 到 25 种字母的最少操作数；当前 `i = {S['i']}`"


def _fcolor(S, i, v):
    if 'i' in S and i == S['i'] and S.get('_line', 0) > 0:
        return 'yellow'
    return None


def _ccolor(S, i, v):
    if 'i' in S and 'x' in S and i == S['i']:
        return 'blue'
    if 'i' in S and 'x' in S and i == S['i'] + 1:
        return 'pink'
    return None


CONFIG = dict(
    num=3389, title='使字符频率相等的最少操作次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='枚举 target + 线性 DP',
    tags=['其他线性 DP', '难度分 2940'],
    code='''
class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = Counter(s)
        cnt = [cnt[c] for c in ascii_lowercase]

        targets = set(cnt)
        for x, y in pairwise(cnt):
            targets.add(x + y)
            targets.add((x + y) // 2)
            targets.add((x + y + 1) // 2)

        ans = len(s)  # target = 0 时的答案
        f = [0] * 27
        for target in targets:
            f[25] = min(cnt[25], abs(cnt[25] - target))
            for i in range(24, -1, -1):
                x = cnt[i]
                if x == 0:
                    f[i] = f[i + 1]
                    continue
                # 单独操作 x（变成 target 或 0）
                f[i] = f[i + 1] + min(x, abs(x - target))
                # x 变成 target 或 0，y 变成 target
                y = cnt[i + 1]
                if 0 < y < target:  # 只有当 y 需要变大时，才去执行第三种操作
                    t = target if x > target else 0
                    f[i] = min(f[i], f[i + 2] + max(x - t, target - y))
            ans = min(ans, f[0])
        return ans
''',
    call='Solution().makeStringGood("aaabc")',
    expect=2,
    skip=['x = cnt[i]', 'continue', 'y = cnt[i + 1]', 'for x, y in pairwise', 'targets.add', 'for i in range', 'if x == 0', 19, 't = target if', 'f[25] = min', 'f = [0] * 27', 'cnt = Counter', 'targets = set'],
    max_steps=80,
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var='cnt', label='cnt（26 个字母的次数，蓝 = 当前 x，粉 = 下一个 y）', cell=36,
             pointers={'i': 'blue'}, color=_ccolor, h=190),
        dict(type='array', var='f', label='f（从后往前算，f[26] = 0）', cell=36, pointers={'i': 'yellow'}, color=_fcolor, h=190),
        dict(type='text', fn=lambda S: f"候选 target：`{sorted(S['targets'])}`" if 'targets' in S else '', size=24, h=50),
        dict(type='text', fn=lambda S: f"当前最小答案 `ans = {S['ans']}`" if 'ans' in S else '', size=26, h=60),
    ],
    watch=[('target', 'target', 'orange'), ('i', 'i', 'blue'), 'x', 'y', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '统计每个字母的出现次数',
        'cnt = [cnt[c]': '统计每个字母的次数，转成长为 26 的数组：`cnt[0]` 是 a 的次数',
        'targets = set': '候选 target 先收下 `cnt` 里出现过的数；再加上相邻两数的 `x+y` 和平均数（上下取整）',
        'ans = len(s)': '候选 target 先收 `cnt` 里的数，再加相邻两数的 `x+y` 和平均数（上下取整），共 `{len(targets)}` 个：`{sorted(targets)}`。`target = 0` 即全删，答案先取 `len(s) = {ans}`（出现次数为 0 的字母不用操作，下面自动略过）。`f[26] = 0`，`f[25]` 是初始值',
        'f = [0] * 27': '`f[26] = 0`：没有字母要操作了',
        'for target in targets': lambda S, B, r: (f'不用枚举到 max(cnt)，只试关键值：`target = {S.target}`' if S.get('target') != B.get('target') or 'target' not in B else 'target 都试完了'),
        'f[i] = f[i + 1] + min': '字母 `{chr(97 + i)}` 出现 `x = {x}` 次，单独操作：变成 0 要 `{x}` 次，变成 target 要 `{abs(x - target)}` 次，取小 → `f[{i}] = {f[i]}`',
        'if 0 < y < target': lambda S, B, r: (f'`y = {S.y} < target = {S.target}`：y 需要变大 → ==可以用操作三==' if 0 < S.y < S.target
                                              else f'`y = {S.y}`，不需要把 y 变大 → 只能单独操作 x'),
        'f[i] = min(f[i], f[i + 2]': '`x = {x}` {"大于" if x > target else "不大于"} `target` → x 变成 `{t}`；`y` 变 `target`，操作三用 `max({x - t}, {target - y}) = {max(x - t, target - y)}` 次 → `f[{i}] = {f[i]}`',
        'ans = min(ans, f[0])': '`target = {target}` 的最少操作 `f[0] = {f[0]}`，`ans` → =={ans}==',
        'return ans': '所有 target 试完，最少操作 `{ans}`',
    },
    cards=dict(
        one_liner='枚举 target，字母个数只能变 0 或 target，相邻字母用操作三省步数',
        complexity='时间 `O(n + 26²)`，空间 `O(26)`',
        problem=['字符串 `s`，每种字母出现次数相等就是==好的==；可删一个字符、加一个字符、把字母变成下一个字母（z 不行）',
                 '求把 `s` 变好的最少操作次数',
                 '示例：`"aaabc"` → `2`（a 变 b，再插入 c）'],
        quote='每种字母的个数要么变成 0，要么变成 target。……关键在于，通过恰当地使用操作三，节省操作次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]`：操作第 i 到 25 种字母的最小操作数，单独操作 x 要 `min(x, |x−target|)`',
              '`y < target` 时，x 可以把多余的字母==变成下一个字母==补给 y，这时再算 `f[i+2]`',
              '操作三不会连用三个字母，所以只看相邻两个'],
        summary=['时间 `O(n + 26²)`，空间 `O(26)`',
                 '易错：`target = 0` 的答案 `len(s)` 要单独算；`f[25]` 是初始值',
                 '只有 `y < target` 才用操作三，`y ≥ target` 时单独操作更好',
                 '优化二：target 只需试 `cnt[i]`、`cnt[i]+cnt[i+1]` 及其上下取整的平均值',
                 '原文还给了两种较慢写法：枚举 target = 1..max(cnt)'],
    ),
)
