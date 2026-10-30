CONFIG = dict(
    num=2262, title='字符串的总引力', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子串按末尾分组 · 增量法',
    tags=['灵神题单', '动态规划', '难度分 2033'],
    code='''
class Solution:
    def appealSum(self, s: str) -> int:
        last = {}
        ans = sum_g = 0
        for i, c in enumerate(s):
            sum_g += i - last.get(c, -1)  # 将提示 2-2 中的两种情况合并成一个公式
            ans += sum_g
            last[c] = i
        return ans
''',
    call='Solution().appealSum("abbca")',
    expect=28,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前末尾 i，粉 = 上次出现的同字符）', h=190, cell=90,
             pointers={'i': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else
                                    'pink' if 'i' in S and 'c' in S and S['last'].get(S['c'], -1) == k and k != S['i'] and S.get('_line') in (6, 7, 8) else None),
             dim=lambda S, k, v: 'i' in S and k > S['i']),
        dict(type='text', size=26, h=70, fn=lambda S: (f"`sum_g` = =={S['sum_g']}==（以 `s[{S['i']}]` 结尾的子串引力和），`ans` = {S['ans']}" if 'i' in S and 'c' in S else '`sum_g` = 所有以 `s[i]` 结尾的子串的引力之和；`last` 记每个字符上次出现的下标')),
        dict(type='map', var='last', label='last[c]：字符 c 上次出现的下标', h=170, fmt=lambda k, v: f'{k}:{v}'),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'pink'), ('sum_g', 'sum_g', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'last = {}': '`last` 记录每个字符上次出现的下标，没出现过按 `-1` 算',
        'sum_g += ': lambda S, B, r: (
            f"`s[{S.i}] = {S.c}` 第一次出现：以 `s[{S.i-1}]` 结尾的 {S.i} 个子串引力各 +1，再加自己单独一个，共 `{S.i} + 1 = {S.i+1}`，`sum_g` = =={S.sum_g}==" if S.last.get(S.c, -1) == -1 and S.i > 0 else
            f"`s[{S.i}] = {S.c}` 上次在 `{S.last[S.c]}`：只有起点在 `{S.last[S.c]+1}..{S.i}` 的 {S.i-S.last[S.c]} 个子串引力 +1，`sum_g` 增加 `{S.i}-{S.last[S.c]}` → =={S.sum_g}==" if S.c in S.last else
            f"`s[{S.i}] = {S.c}` 第一次出现：`i - (-1) = {S.i+1}`，`sum_g` = =={S.sum_g}=="),
        'ans += sum_g': '把以 `s[{i}]` 结尾的所有子串的引力加进答案：`ans` = =={ans}==',
        'last[c] = i': '记下 `{c}` 最近一次出现在 `{i}`',
        'return ans': '所有子串的总引力 = =={ret}==',
    },
    cards=dict(
        one_liner='按末尾分组：新字符只给“没包含它”的子串加 1',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['字符串的==引力==是其中不同字符的个数',
                 '求 `s` 所有子串的引力之和',
                 '示例：`s = "abbca"` → `28`'],
        quote='以 s[i] 结尾的子串，可以看成是以 s[i-1] 结尾的子串，在末尾添加上 s[i] 组成。上面这一串提示是思考子串统计类问题的通用技巧之一。',
        quote_src='—— 灵茶山艾府题解（方法二：增量法）',
        idea=['把所有子串按末尾下标分组，`sum_g` = 以 `s[i]` 结尾的子串引力和',
              '加上 `s[i]` 后：已经含有 `s[i]` 的子串引力不变，其余的各 +1',
              '起点在 `last+1 .. i` 的子串不含 `s[i]`，所以增加 `i - last`'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '易错：字符没出现过时 `last` 取 `-1`，增量是 `i + 1`',
                 '==ans 每轮都要加 sum_g==，不是只在字符重复时加',
                 '方法一「贡献法」：每个字符只算第一次出现的贡献 `(i - last) * (n - i)`'],
    ),
)
