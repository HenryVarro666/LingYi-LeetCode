def _pos(S):
    return len(S['non_zero']) - (2 if S.get('_line') in (15, 18) else 1)


def _arr(name, label, cell=84):
    return dict(type='array', var=name, label=label, h=108, cell=cell, index=True,
                color=lambda S, i, v: 'green' if i == len(S[name]) - 1 and S.get('_line') in (11, 12, 13, 15, 16, 17) else None)


CONFIG = dict(
    num=3754, title='连接非零数字并乘以其数字和 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='前缀和 + 前缀值（取模）',
    code='''
class Solution(object):
    def sumAndMultiply(self, s, queries):
        
        ss = [0]
        v = [0]
        p10 = [1]
        non_zero = [0]
        mod = 10 ** 9 + 7
        for c in s:
            d = int(c)
            ss.append((ss[-1] + d) % mod)
            p10.append(p10[-1] * 10 % mod)
            if c != '0':
                v.append((v[-1] * 10 + d) % mod)
                non_zero.append(non_zero[-1] + 1)
            else:
                v.append(v[-1])
                non_zero.append(non_zero[-1])

        res = []
        for x, y in queries:
            ds = (ss[y + 1] - ss[x] + mod) % mod
            dv = (v[y + 1] - v[x] * p10[non_zero[y + 1] - non_zero[x]] % mod + mod) % mod
            res.append(ds * dv % mod)
        return res
''',
    call="Solution().sumAndMultiply('10203', [[0, 4], [1, 3]])",
    expect=[738, 4],
    skip=['mod = 10', 'res = []'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s', h=140, cell=84, window=('x', 'y'),
             color=lambda S, i, v: 'blue' if 'c' in S and 'x' not in S and i == _pos(S) else None),
        _arr('ss', 'ss（数位和前缀）'),
        _arr('v', 'v（去零后的前缀值）'),
        _arr('non_zero', 'non_zero（非零个数前缀）'),
        _arr('p10', 'p10（10 的幂）', 98),
    ],
    watch=[('c', 'c', 'blue'), 'd', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ds', 'ds', 'yellow'), ('dv', 'dv', 'orange'), ('res', 'res', 'green')],
    captions={
        'ss = [0]': '`ss[i]`：s 前 i 个数位之和，0 不影响和，所以直接做前缀和',
        'v = [0]': '`v[i]`：s 前 i 位去掉 0 之后拼成的数（取模）',
        'p10 = [1]': '`p10[i]` = 10 的 i 次方（取模）',
        'non_zero = [0]': '`non_zero[i]`：前 i 位里非零数位的个数',
        'for c in s': lambda S, B, r: (f'看第 {_pos(S)} 位 `c = {S.c!r}`' if _pos(S) < len(S.s) else '`s` 的每一位都处理完了，前缀数组建好'),
        'ss.append': '`ss` 追加：前缀和 → {ss[-1]}',
        'p10.append': '`p10` 追加 10 的 {len(p10) - 1} 次方 = {p10[-1]}',
        "if c != '0'": lambda S, B, r: ('`c` 不是 0：要拼进 v' if S.c != '0' else '`c` 是 0：不能计入 v，沿用上一项'),
        'v.append((v[-1]': '`v` 追加：`{B.v[-1]} × 10 + {d}` = {v[-1]}',
        'non_zero.append(non_zero[-1] + 1)': '非零个数 +1 → {non_zero[-1]}',
        'v.append(v[-1])': '`v` 直接沿用：{v[-1]}（零被忽略）',
        'non_zero.append(non_zero[-1])': '非零个数不变 → {non_zero[-1]}',
        'for x, y in queries': lambda S, B, r: (f'处理查询 `[{S.x}, {S.y}]`' if len(S.res) < len(S.queries) else '查询处理完毕'),
        'ds =': '数位和 = `ss[{y + 1}] − ss[{x}]` = =={ds}==',
        'dv =': '去零后的数 = `v[{y + 1}] − v[{x}] × 10^(非零个数 {non_zero[y + 1] - non_zero[x]})` = =={dv}==。==指数是区间内非零个数，不是区间长度==',
        'res.append': '答案 `ds × dv` = {ds} × {dv} = =={res[-1]}==',
        'return res': '全部查询的答案：`{res}`',
    },
    cards=dict(
        one_liner='三个前缀数组：数位和、去零后的前缀值、非零个数',
        complexity='时间 `O(m + q)`，空间 `O(m)`',
        problem=['字符串 `s` 只含数字，每次查询 `[l, r]`：取子串，去掉 0 拼成整数 `x`',
                 '答案 = `x × (x 的数位和)`，对 `10^9 + 7` 取模',
                 '本题 I 是 `queries = [[0, len(s)-1]]` 的特例；本视频演示带查询的通用写法',
                 '示例：`s = "10203"`，查询 `[0,4]` → `123 × 6 = 738`'],
        quote='若某个数位 s[index] 为 0，v[index + 1] 只需直接沿用 v[index]……x 就应该是 v[right + 1] - v[left] * 10^(non_zero[right + 1] - non_zero[left])。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位和：0 不影响，普通前缀和 `ss`',
              '去零后的数：`v[i+1] = v[i] × 10 + d`，遇到 0 就沿用；区间值 = 前缀之差，要减去的前缀要“左移”区间内非零个数位',
              '左移位数用 `non_zero` 前缀之差得到，`p10` 预存 10 的幂'],
        summary=['时间 `O(m + q)`，空间 `O(m)`',
                 '易错：`p10` 的下标是区间内==非零==数位个数，不是区间长度',
                 '减法取模后要 `+ mod` 再 `% mod`，避免负数',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串，无需其它改动'],
    ),
)
