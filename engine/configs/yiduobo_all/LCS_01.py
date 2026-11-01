CONFIG = dict(
    num='LCS 01', title='下载插件', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='模拟：带宽翻倍到不小于 n',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def leastMinutes(self, n):
        res = 1
        now = 1
        while now < n:
            now += now
            res += 1
        
        return res
''',
    call='Solution().leastMinutes(13)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"目标 `n = {S['n']}`　当前带宽 `now = {S.get('now', '?')}`　已用分钟 `res = {S.get('res', '?')}`", size=28),
        dict(type='bars', var='[2 ** k for k in range(5)]', label='带宽 1, 2, 4, 8, 16（目标 n = 13）', cell=100,
             color=lambda S, k, v: ('green' if v == S.get('now') else None) if 'now' in S else None,
             dim=lambda S, k, v: 'now' in S and v > S['now']),
        dict(type='text', fn=lambda S: ('`now ≥ n`：带宽够了，再下载 1 次即可' if 'now' in S and S['now'] >= S['n'] else '`now < n`：一次下不完，先翻倍'), size=26),
    ],
    watch=[('now', 'now', 'green'), ('res', 'res', 'blue'), ('n', 'n')],
    captions={
        'res = 1': '`res` 记总分钟数，先算上最后那次下载的 1 分钟',
        'now = 1': '`now` 是当前带宽，初始为 1',
        'while now < n': lambda S, B, r: (f'`now = {S.now} < n = {S.n}`：一次下不完 → 继续翻倍' if S.now < S.n
                                           else f'`now = {S.now} ≥ n = {S.n}`：带宽够了 → 停止翻倍'),
        'now += now': '带宽翻倍，`now` → {now}',
        'res += 1': '翻倍花了 1 分钟，`res` → {res}',
        'return res': '翻倍 `{res - 1}` 次 + 下载 1 次，共 =={res}== 分钟',
    },
    cards=dict(
        one_liner='先翻倍到带宽不小于 n，再一次下载完',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['带宽初始每分钟下载 1 个插件；每分钟可下载，或把带宽加倍',
                 '下载数量可以超过 `n`，求最少几分钟',
                 '本视频：`n = 13` → `5`'],
        quote='如果操作序列中存在 扩容->下载->扩容 这种情况，那么完全可以先进行扩容再下载，这样可以下载更多的东西。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扩容再下载更划算，所以只需决定最终带宽 `2^k`',
              '`n = 2^k + p` 时，带宽 `2^k` 要下载两次，共 `k + 2` 次操作；带宽 `2^(k+1)` 也是 `k + 2` 次',
              '结论：带宽翻倍到 `≥ n`，再下载 1 次'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`res` 初值 1 就是最后那次下载',
                 '带宽可以大于 `n`：下载 7 个也可以用 8 的带宽一次下完',
                 '原文是 Python 2 风格，只删去了类型说明文档字符串，其余不变'],
    ),
)
