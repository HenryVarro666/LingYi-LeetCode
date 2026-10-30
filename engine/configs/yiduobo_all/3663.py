CONFIG = dict(
    num=3663, title='出现频率最低的数字', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='模 10 分离数位 + 哈希表',
    tags=[],
    code='''
class Solution(object):
    def getLeastFrequentDigit(self, n):

        cnt = {}
        while n:
            d = n % 10
            n //= 10
            cnt[d] = cnt.get(d, 0) + 1
        
        res = None
        for d in cnt:
            if res is None or cnt[d] < cnt[res] or (cnt[d] == cnt[res] and d < res):
                res = d
        return res
''',
    call='Solution().getLeastFrequentDigit(1553322)',
    expect=1,
    views=[
        dict(type='text', h=90, size=34, fn=lambda S: f"剩下的 n = ==`{S['n']}`==" if 'n' in S else ''),
        dict(type='map', var='cnt', label='cnt（数位 → 出现次数）', fmt=lambda k, v: f"{k}: {v}", h=260, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"当前答案 res = ==`{S['res']}`==（出现 {S['cnt'][S['res']]} 次）" if S.get('res') is not None else '')),
    ],
    watch=['n', 'd', ('res', 'res', 'green')],
    captions={
        'cnt = {}': '用哈希表 `cnt` 记录每个数位出现的次数',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没取完，继续' if S.n else '`n = 0`，每一位都取完了'),
        'd = n % 10': '`n % 10` 取出最低位：`d = {d}`',
        'n //= 10': '去掉最低位：`n` → {n}',
        'cnt[d] = ': '`cnt[{d}] = {cnt[d]}`',
        'res = None': '第二步：遍历哈希表里出现过的数位，找频率最低且最小的',
        'for d in cnt': '看数位 `{d}`（出现 {cnt[d]} 次）',
        'if res is None': lambda S, B, r: (
            ('还没有候选 → ==直接选它==' if B.res is None else
             f'`cnt[{S.d}] = {S.cnt[S.d]}` < `cnt[{B.res}] = {S.cnt[B.res]}` → ==更少，换掉==' if S.cnt[S.d] < S.cnt[B.res] else
             f'次数相同且 `{S.d} < {B.res}` → ==更小，换掉==' if S.cnt[S.d] == S.cnt[B.res] and S.d < B.res else
             f'`{S.d}` 不比当前 `{B.res}` 更好，保留 {B.res}')),
        'res = d': '`res` 换成 `{res}`',
        'return res': '答案是 `{res}`',
    },
    cards=dict(
        one_liner='模 10 拆数位计数，再按「次数小、数字小」挑一个',
        complexity='时间 `O(log n)`，空间 `O(1)`（最多 10 个键）',
        problem=['给整数 `n`，找十进制表示中 ==出现频率最低== 的数字',
                 '频率相同时选 ==最小== 的数字',
                 '本视频：`n = 1553322` → `1`（1 只出现一次，其余都两次）'],
        quote='通过模10除以10的方法分离出n的每一位数字，同时使用一个哈希表记录这些数字出现的次数。接下来对哈希表中出现的数字进行一趟遍历，选取其中频率最低且最小的数字作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % 10` 是最低位，`n //= 10` 去掉最低位，循环到 `n` 为 0',
              '每个数位在哈希表里计数',
              '遍历哈希表打擂台：次数更少，或次数相同而数字更小，就换掉 `res`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '比较条件要同时写「次数更少」和「次数相同且数字更小」',
                 '`res` 用 `None` 起步，不能用 0，否则会把没出现的 0 当成候选',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
