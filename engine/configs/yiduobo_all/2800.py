CONFIG = dict(
    num=2800, title='包含三个字符串的最短字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举 6 种排列 · 逐个合并',
    tags=['灵神题单·字符串', 'KMP'],
    code='''
class Solution(object):
    def minimumString(self, a, b, c):

        def merge(x, y, z):
            xy = ''
            for index in range(len(x)):
                compare_len = min(len(x) - index, len(y))
                if x[index: index + compare_len] == y[:compare_len]:
                    if compare_len < len(y):
                        xy = x[:index] + y
                    else:
                        xy = x
                    break
            
            if xy == '':
                xy = x + y

            for index in range(len(xy)):
                compare_len = min(len(xy) - index, len(z))
                if xy[index: index + compare_len] == z[:compare_len]:
                    if compare_len < len(z):
                        return xy[:index] + z
                    else:
                        return xy

            return xy + z

        candidate = [merge(a, b, c), merge(a, c, b), merge(b, a, c), merge(b, c, a), merge(c, a, b), merge(c, b, a)]
        return sorted(candidate, key=lambda d:(len(d), d))[0]
''',
    call='Solution().minimumString("ab", "ba", "aba")',
    expect='aba',
    views=[
        dict(type='text', fn=lambda S: (f"合并顺序 `x = {S['_inner']['x']}` → `y = {S['_inner']['y']}` → `z = {S['_inner']['z']}`"
                                        if 'x' in S['_inner'] else f"a = `{S.get('a','')}`　b = `{S.get('b','')}`　c = `{S.get('c','')}`"),
             size=28, h=70),
        dict(type='string', var=lambda S: S['_inner'].get('x', ''), label='x（最左边的串）', cell=60, h=200,
             pointers={'index': 'blue'}),
        dict(type='string', var=lambda S: S['_inner'].get('xy', '') or S['_inner'].get('y', ''),
             label='xy（未合并时显示 y）', cell=60, h=170),
        dict(type='string', var=lambda S: S['_inner'].get('z', ''), label='z（最右边的串）', cell=60, h=150),
    ],
    watch=[('x', "_inner.get('x')", 'blue'), ('y', "_inner.get('y')", 'pink'), ('z', "_inner.get('z')", 'cyan'),
           ('xy', "_inner.get('xy')", 'green'), ('index', "_inner.get('index')", 'yellow')],
    captions={
        "xy = ''": '`xy` 先置空，表示还没找到重叠',
        'for index in range(len(x))': '枚举 x 里 y 开始的位置：`index = {index}`',
        'compare_len = min(len(x) - index, len(y))': '从 `x[{index}:]` 到 x 末尾最多能和 y 的前缀比较 `{compare_len}` 个字母',
        'if x[index: index + compare_len] == y[:compare_len]': lambda S, B, r: (
            f"`x[{S.index}:{S.index + S.compare_len}] = {S.x[S.index:S.index + S.compare_len]!r}` == `y[:{S.compare_len}] = {S.y[:S.compare_len]!r}` → ==找到最早的重叠=="
            if S.x[S.index:S.index + S.compare_len] == S.y[:S.compare_len]
            else f"`{S.x[S.index:S.index + S.compare_len]}` ≠ `{S.y[:S.compare_len]}`，换下一个起点"),
        'if compare_len < len(y)': lambda S, B, r: (f'y 还有剩余 → `xy = x 的前 {S.index} 个 + y`' if S.compare_len < len(S.y)
                                                   else 'y 整个落在 x 里面 → `xy = x`'),
        'xy = x[:index] + y': '`xy = {xy}`',
        12: '`xy = {xy}`',
        'break': '已找到，停止枚举',
        "if xy == ''": lambda S, B, r: ('`xy` 仍为空 → x 和 y 没有重叠，直接拼接' if S.xy == '' else '`xy` 已有，不用拼接'),
        'xy = x + y': '`xy = {xy}`',
        'for index in range(len(xy))': '再把 z 合并进 xy：枚举 `index = {index}`',
        'compare_len = min(len(xy) - index, len(z))': '`xy[{index}:]` 最多与 z 的前缀比较 `{compare_len}` 个',
        'if xy[index: index + compare_len] == z[:compare_len]': lambda S, B, r: (
            f"`{S.xy[S.index:S.index + S.compare_len]}` == `z[:{S.compare_len}] = {S.z[:S.compare_len]}` → ==z 可以接在这里=="
            if S.xy[S.index:S.index + S.compare_len] == S.z[:S.compare_len]
            else f"`{S.xy[S.index:S.index + S.compare_len]}` ≠ `{S.z[:S.compare_len]}`，换下一个起点"),
        'if compare_len < len(z)': lambda S, B, r: ('z 超出 xy 的末尾 → 取 `xy` 的前面一段再接上 z' if S.compare_len < len(S.z)
                                                   else 'z 整个落在 xy 里 → 直接用 `xy`'),
        'return xy[:index] + z': '这个顺序的结果：`{ret}`',
        24: '这个顺序的结果：`{ret}`',
        'return xy + z': '没有重叠，直接拼接：`{ret}`',
        'candidate = [': '6 种排列都合并完，得到 6 个备选：`{candidate}`',
        'return sorted': '6 种排列的候选：`{candidate}`；按（长度, 字典序）排序取第一个 → `{ret}`',
    },
    skip=['compare_len = min'],
    max_steps=120,
    cards=dict(
        one_liner='6 种顺序各合并一次，取（长度，字典序）最小的',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['找一个最短的字符串，使 `a`、`b`、`c` 都是它的子串；有多个就取字典序最小',
                 '本视频：`a="ab"`，`b="ba"`，`c="aba"` → `"aba"`'],
        quote='对于本题三个字符串的情况，则只需枚举出三个字符串的排列顺序，一共是6种。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个串：左边串的后缀与右边串的前缀重叠最多，拼出来最短',
              '`merge(x, y, z)` 先把 y 接到 x 上，再把 z 接到结果上；枚举 index 找第一个能对上的位置',
              '6 种排列得到 6 个候选，`sorted(key=(len, 字典序))` 取第一个'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：y 完全落在 x 里时 `xy = x`，不能再拼 y',
                 '从小到大枚举 index，最先对上的位置就是最大重叠',
                 '对比灵神：灵神每次从长到短枚举重叠长度；yiduobo 从前到后枚举起点',
                 '原文为 Python 2 写法，题解里的代码无需改动'],
    ),
)
