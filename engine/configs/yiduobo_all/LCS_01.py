CONFIG = dict(
    num='LCS 01', title='下载插件', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='带宽翻倍到不小于 n',
    tags=['灵神题单'],
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
    call='Solution().leastMinutes(10)',
    expect=5,
    views=[
        dict(type='text', h=170, size=40, fn=lambda S: f"带宽 now = =={S['now']}==，目标 n = {S['n']}，已用 res = =={S['res']}== 分钟" if 'now' in S else ''),
        dict(type='text', h=120, size=32,
             fn=lambda S: ('带宽 ' + ' → '.join(str(2**k) for k in range(S['res'])) + '（最后一分钟用来下载）') if 'res' in S and 'now' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 1': '最后一定要有 1 分钟用来下载，所以 `res` 从 1 开始',
        'now = 1': '初始带宽 `now = 1`',
        'while now < n': lambda S, B, r: (f'`now = {S.now} < n = {S.n}`：一次下不完，还得扩容' if S.now < S.n
                                          else f'`now = {S.now} >= n = {S.n}`：带宽够了，一次下载就能下完（可以超过 n）'),
        'now += now': '带宽加倍 → `now = {now}`（先扩容再下载，总比先下载再扩容划算）',
        'res += 1': '扩容花了 1 分钟 → `res = {res}`',
        'return res': '扩容 {res - 1} 次 + 下载 1 次，最少 `{res}` 分钟',
    },
    cards=dict(
        one_liner='先把带宽翻倍到不小于 n，再下载一次',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['带宽初始每分钟下载 1 个插件，每分钟可「下载」或「带宽加倍」',
                 '求下载至少 `n` 个插件的最少分钟数（可以多下）',
                 '示例：`n = 4` → `3`'],
        quote='可以先将带宽扩容到大于等于n的水平，然后执行一次下载操作就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['「扩容 → 下载 → 扩容」可以调整为先扩容再下载，下载量只多不少',
              '所以操作序列一定是若干次扩容，最后下载',
              '最小的 `2^k >= n`：k 次扩容 + 1 次下载 = `k + 1` 分钟'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`res` 从 1 开始（含最后一次下载）',
                 '带宽允许超过 n，例如 n = 7 用带宽 8',
                 '原文代码可直接在 Python 3 运行，未做修改'],
    ),
)
