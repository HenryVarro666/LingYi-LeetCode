def _alt(S):
    if 'h' not in S:
        return ''
    g = S['gain']
    pre = [0]
    for x in g:
        pre.append(pre[-1] + x)
    k = g.index(S['d']) + 1 if 'd' in S else 0
    done = pre[:k + 1] if S['h'] == pre[k] else pre[:k]
    return 'h（前缀和）： ' + ' → '.join(f'`{x}`' for x in done) + f'　ans ==`{S["ans"]}`=='


CONFIG = dict(
    num=1732, title='找到最高海拔', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='差分数组的前缀和',
    code='''
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        ans = h = 0
        for d in gain:
            h += d
            ans = max(ans, h)
        return ans
''',
    call='Solution().largestAltitude([-5,1,5,2,-7])',
    expect=3,
    views=[
        dict(type='array', var='gain', label='gain = 海拔数组 h 的差分数组', h=170,
             color=lambda S, i, v: 'blue' if 'd' in S and i == S['gain'].index(S['d']) else None),
        dict(type='text', h=90, fn=_alt),
    ],
    watch=[('d', 'd', 'blue'), ('h', 'h', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = h = 0': '`h[0] = 0` 就是起点海拔，`ans` 也从 `0` 开始',
        'for d in gain': '取差分 `d = {d}`，即 `h[i] - h[i-1]`',
        'h += d': '前缀和：`h[i] = h[i-1] + gain[i-1]` → `{B.h} + ({d})` = =={h}==',
        'ans = max': '`ans = max({B.ans}, {h})` = =={ans}==',
        'return ans': '`max(h)` = =={ans}==',
    },
    cards=dict(
        one_liner='gain 是海拔的差分数组，前缀和还原海拔，再取最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['骑行路线有 `n+1` 个点，起点海拔 `0`；`gain[i]` 是点 `i` 与点 `i+1` 的净海拔差',
                 '返回最高点的海拔',
                 '示例：`[-5,1,5,2,-7]` → `3`（海拔 0,-5,-4,1,3,-4）'],
        quote='本质上，gain 是 h 的差分数组。计算差分数组的前缀和，就得到了 h。',
        quote_src='—— 灵茶山艾府题解',
        idea=['由 `h[i] - h[i-1] = gain[i-1]` 逐项累加，得 `h` 是 `gain` 的==前缀和==',
              '答案是 `max(h)`；一边累加一边取最大，就不用开数组了'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ans` 初始为 `0`，因为起点 `h[0] = 0` 也算在内',
                 '灵神主推写法一：`max(accumulate(gain, initial=0))`，只有一行；本视频演示等价的写法二，便于看到每步海拔'],
    ),
)
