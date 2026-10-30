F = [1, 0, 0, -1, 0, 0, 0, 0, 1]


def _txt(S):
    if 'i' not in S or 'pre' not in S:
        return ''
    f = S['forts']
    if S['pre'] < 0:
        return '还没遇到非零元素（pre = -1 表示不存在）'
    p, i = S['pre'], S['i']
    if f[i] and f[p] != f[i] and i > p:
        return f'`{f[p]}` 和 `{f[i]}` 一正一负，中间 `{i} − {p} − 1` = =={i-p-1}== 个 0'
    return f'上一个非零在 `{p}`，当前 `i = {i}`'


CONFIG = dict(
    num=2511, title='最多可以摧毁的敌人城堡数目', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='遍历 · 记录上一个非零位置',
    tags=[],
    code='''
class Solution:
    def captureForts(self, forts: List[int]) -> int:
        ans = 0
        pre = -1  # 表示不存在
        for i, x in enumerate(forts):
            if x:  # 1 或 -1
                if pre >= 0 and x != forts[pre]:  # 一个是 1，另一个是 -1
                    ans = max(ans, i - pre - 1)
                pre = i
        return ans
''',
    call=f'Solution().captureForts({F!r})',
    expect=4,
    views=[
        dict(type='array', var='forts', label='forts（1 = 我方，-1 = 空位，0 = 敌方）', pointers={'pre': 'pink', 'i': 'blue'}, cell=90, h=260,
             color=lambda S, i, v: ('green' if v == 1 else 'orange' if v == -1 else None)),
        dict(type='text', fn=_txt, size=30, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录最多能摧毁的城堡数',
        'pre = -1': '`pre` 是上一个非零元素的下标，-1 表示还没有',
        'if x:': lambda S, B, r: (f'`forts[{S.i}] = {S.x}` 非零 → 是我方城堡或空位，处理' if S.x else f'`forts[{S.i}] = 0` 敌方城堡，直接跳过'),
        'if pre >= 0 and x != forts[pre]': lambda S, B, r: (
            '`pre = -1`，前面没有非零元素 → 不能算' if S.pre < 0 else
            (f'`{S.x} != {S.forts[S.pre]}` 一个 1 一个 -1 → ==成立==，中间全是 0' if S.x != S.forts[S.pre] else f'`{S.x}` 和上一个非零 `{S.forts[S.pre]}` 相同 → 不能算')),
        'ans = max': '中间有 `{i} − {pre} − 1` = `{i-pre-1}` 个 0：`ans = max({B.ans}, {i-pre-1}) = {ans}`',
        'pre = i': '`pre` 更新为 `{pre}`：下一个非零只和它比较',
    },
    cards=dict(
        one_liner='两个相邻的非零元素，一个 1 一个 -1，中间的 0 就是可摧毁数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`1` 我方城堡，`-1` 空位，`0` 敌方城堡',
                 '军队从 1 出发走到 -1，途中只能经过 0，全部摧毁',
                 '示例：`[1,0,0,-1,0,0,0,0,1]` → `4`'],
        quote='在 -1 和 1 之间全是 0 的前提下，最多可以有多少个 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右遍历，只关心非零元素，`pre` 是上一个非零的下标',
              '`forts[i] != forts[pre]` 说明一个是 1、一个是 -1',
              '中间 0 的个数 `i − pre − 1` 去更新答案最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`，一次遍历',
                 '易错点：`pre` 初始 -1 表示不存在，别漏掉 `pre >= 0` 的判断',
                 '两个相邻 1 之间的 0 不算（同号不能走）',
                 '不管 1 在左还是在右，都是同一个条件 `x != forts[pre]`'],
    ),
)
