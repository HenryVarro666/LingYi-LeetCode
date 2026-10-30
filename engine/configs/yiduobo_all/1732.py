def _alt(S):
    if 'now' not in S:
        return ''
    g = S['gain']
    pre = [0]
    for x in g:
        pre.append(pre[-1] + x)
    k = g.index(S['g']) + 1 if 'g' in S else 0
    done = pre[:k + 1] if S['now'] == pre[k] else pre[:k]
    return '海拔： ' + ' → '.join(f'`{x}`' for x in done) + f'　最高 ==`{S["res"]}`=='


CONFIG = dict(
    num=1732, title='找到最高海拔', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描 · 累加海拔',
    code='''
class Solution:
    def largestAltitude(self, gain):

        res = 0
        now = 0
        for g in gain:
            now += g
            res = max(res, now)
        
        return res
''',
    call='Solution().largestAltitude([-5,1,5,2,-7])',
    expect=3,
    views=[
        dict(type='array', var='gain', label='gain（相邻两点的海拔差）', h=170,
             color=lambda S, i, v: 'blue' if 'g' in S and i == S['gain'].index(S['g']) else None),
        dict(type='text', h=90, fn=_alt),
    ],
    watch=[('g', 'g', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 是最高海拔，起点海拔 `0` 也算',
        'now = 0': '`now` 是当前海拔，从 `0` 出发',
        'for g in gain': '下一段海拔差 `g = {g}`',
        'now += g': '当前海拔 = 上一点海拔 + 差值：`{B.now} + ({g})` = =={now}==',
        'res = max': '`res = max({B.res}, {now})` = =={res}==',
        'return res': '最高海拔 `{res}`',
    },
    cards=dict(
        one_liner='每一点海拔 = 上一点海拔 + 海拔差，边走边记最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['骑行路线有 `n+1` 个点，起点海拔为 `0`',
                 '`gain[i]` 是点 `i` 到点 `i+1` 的海拔差，求最高点的海拔',
                 '示例：`[-5,1,5,2,-7]` → `3`'],
        quote='由于每个位置的海拔都可以通过上一个位置的海拔以及海拔差值计算得到，那么可以从头开始一趟扫描，计算出每个位置的海拔并用这个海拔更新最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 当前海拔，每步加上 `g`',
              '每到一个点就用 `now` 更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 初值为 `0`：起点本身也是候选，所以不会出现“全程下坡返回负数”',
                 '原文为 Python 2 风格，仅把 `Solution(object)` 改为 `Solution`'],
    ),
)
