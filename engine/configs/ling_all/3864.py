_I = lambda S, k: S['_inner'].get(k)


def _txt(S):
    I = S['_inner']
    if 'l' not in I or 'pre' not in S:
        return ''
    l, r = I['l'], I['r']
    out = f'子串 `[{l}, {r})` 长 `{r - l}`'
    if 'x' in I:
        out += f'，敏感元素 `x = {I["x"]}`'
        if I['x'] and 'res' in I:
            out += f'，不拆分费用 `{r - l} × {I["x"]} × {S["encCost"]}` = =={I["res"]}=='
        elif not I['x']:
            out += f'，无敏感元素 → 费用 `flatCost = {S["flatCost"]}`'
    return out


CONFIG = dict(
    num=3864, title='划分二进制字符串的最小费用', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='分治 + 前缀和（x=0 直接返回）',
    tags=['灵神题单·链表树与回溯', '难度分 2032'],
    code='''
class Solution:
    def minCost(self, s: str, encCost: int, flatCost: int) -> int:
        n = len(s)
        pre = list(accumulate(map(int, s), initial=0))

        # 计算子串 [l, r) 的最小费用，注意区间是左闭右开，方便计算
        def dfs(l: int, r: int) -> int:
            x = pre[r] - pre[l]
            if x == 0:
                return flatCost           

            # 不拆分
            res = (r - l) * x * encCost

            # 拆分
            if (r - l) % 2 == 0:
                m = (l + r) // 2
                res = min(res, dfs(l, m) + dfs(m, r))

            return res

        return dfs(0, n)
''',
    call='Solution().minCost("10100000", 2, 3)',
    expect=11,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='string', var='s', label='s（蓝框 = 当前子串 [l, r)）', cell=70, h=170, window=(lambda S: S['_inner'].get('l'), lambda S: S['_inner'].get('r', 0) - 1),
             color=lambda S, i, v: ('red' if v == '1' else None) if 'pre' in S else None,
             dim=lambda S, i, v: S['_inner'].get('l') is not None and not (S['_inner']['l'] <= i < S['_inner']['r'])),
        dict(type='array', var='pre', label='pre（前缀和，子串里 1 的个数 = pre[r] - pre[l]）', cell=60, h=140),
        dict(type='calls', h=260),
    ],
    watch=[('l', lambda S: _I(S, 'l'), 'blue'), ('r', lambda S: _I(S, 'r'), 'pink'), ('x', lambda S: _I(S, 'x'), 'yellow'),
           ('res', lambda S: _I(S, 'res'), 'green')],
    skip=['n = len(s)'],
    max_steps=75,
    captions={
        'pre = list': '前缀和 `pre`：`pre[r] - pre[l]` 就是子串 `[l, r)` 里 1 的个数',
        'def dfs': '`dfs(l, r)`：子串 `[l, r)` 的最小费用，区间左闭右开',
        'x = pre[r]': '`x = pre[{r}] - pre[{l}] = {x}`：子串里有 `{x}` 个敏感元素',
        'if x == 0': lambda S, B, r: (f'`x = 0`：没有敏感元素，不拆分费用 `flatCost`；拆分后每段都至少 `flatCost`，只会更贵' if S.x == 0
                                      else f'`x = {S.x} > 0`：有敏感元素，需要比较「不拆分」和「拆分」'),
        'return flatCost': '==直接返回 `flatCost = {flatCost}`==，不必再往下拆',
        'res = (r - l)': '不拆分：`长度 × x × encCost = {r - l} × {x} × {encCost}` = =={res}==',
        'if (r - l) % 2': lambda S, B, r: (f'长度 `{S.r - S.l}` 是偶数，可以==对半拆分==' if (S.r - S.l) % 2 == 0
                                           else f'长度 `{S.r - S.l}` 是奇数，不能拆分，只能整段算'),
        'm = (l + r)': '切分点 `m = ({l} + {r}) // 2 = {m}`，拆成 `[{l}, {m})` 和 `[{m}, {r})`',
        'res = min': '拆分：递归算两半 `dfs(l, m) + dfs(m, r)`，再和不拆分的费用取较小值',
        'return res': '`dfs({l}, {r})` 返回 `{res}`',
        'return dfs(0, n)': lambda S, B, r: (f'最小总费用 `{r}`' if r is not None else f'入口 `dfs(0, {S.n})`：先算整个字符串的最小费用'),
    },
    cards=dict(
        one_liner='对半拆分很像二叉树：每段「不拆」和「拆」取最小，全零段直接停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制字符串 `s`，`1` 表示敏感元素；一段长 `L`、含 `X` 个敏感元素的费用：`X = 0` 为 `flatCost`，否则 `L·X·encCost`',
                 '偶数长度的段可以对半拆成两段，费用变成两段之和',
                 '示例：`s = "1010"`，`encCost = 2`，`flatCost = 1` → `6`；本视频：`"10100000"`，`2`，`3` → `11`'],
        quote='写个分治：定义 dfs(l,r) 表示子串 [l,r) 的最小费用。……如果子串 [l,r) 的长度是偶数，可以拆分，对应的费用为 dfs(l,m)+dfs(m,r)。两种情况取最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每段只有两种选择：整段算，或（长度为偶数时）对半拆开分别算',
              '子串里 1 的个数用==前缀和==一步得到',
              '优化：`x = 0` 时拆分只会让费用越拆越多（`2·flatCost` > `flatCost`），所以直接返回 `flatCost`'],
        summary=['时间 `O(n)`：搜索树高 `O(log n)`，每层节点数 1,2,4,…,n，总共 `O(n)` 个节点',
                 '空间 `O(n)`（前缀和数组）',
                 '易错点：区间左闭右开，长度 `r - l`；奇数长度没法拆，递归自然在这里结束',
                 '优化前写法先算不拆分的费用再拆，`x = 0` 时也继续拆；优化后提前返回',
                 '同类题：分治类题目，常用前缀和快速求区间和'],
    ),
)
