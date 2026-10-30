CONFIG = dict(
    num=3184, title='构成整天的下标对数目 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='模 24 · 哈希表计数', tags=[],
    code='''
class Solution(object):
    def countCompleteDayPairs(self, hours):

        freq = Counter()
        res = 0
        for h in hours:
            v = h % 24
            if v == 0:
                res += freq[v]
            else:
                res += freq[24 - v]

            freq[v] += 1

        return res
''',
    call='Solution().countCompleteDayPairs([72,48,24,3,21])',
    expect=4,
    views=[
        dict(type='array', var='hours', label='hours', h=170),
        dict(type='map', var='freq', fmt=lambda k, v: f'{k}: {v}', label='freq（余数 → 出现次数）', h=300),
        dict(type='text', fn=lambda S: (f"当前 `{S['h']} % 24 = {S['v']}`，需要配对的余数 =={0 if S['v'] == 0 else 24 - S['v']}==" if 'v' in S else ''), size=30),
    ],
    watch=[('h', 'h', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'freq = Counter': '`freq` 记录已经出现过的余数各有几个',
        'res = 0': '`res` 累计满足条件的下标对数',
        'for h in hours': lambda S, B, r: '所有小时数都处理完，循环结束' if sum(S.freq.values()) == len(S.hours) else f'看下一个小时数 `h = {S.h}`',
        'v = h % 24': '只有余数有用：`{h} % 24 = ` ==`{v}`==',
        'if v == 0': '`v = {v}`：{"余数为 0，要找另一个余数为 0 的人配对" if v == 0 else "余数不为 0，要找余数为 24 - v 的人配对"}',
        'res += freq[v]': '前面已有 `{freq[v]}` 个余数 0 的数，各能和它配成整天：`res` → =={res}==',
        'res += freq[24 - v]': '前面已有 `{freq[24-v]}` 个余数 `{24-v}` 的数，各能和它配成整天：`res` → =={res}==',
        'freq[v] += 1': '先配对、后入表（保证 i < j）：`freq[{v}]` → {freq[v]}',
        'return res': '一共 `{res}` 对',
    },
    cards=dict(
        one_liner='先模 24，再用哈希表找互补的余数',
        complexity='时间 `O(n)`，空间 `O(1)`（余数最多 24 种）',
        problem=['给一个小时数组 `hours`，数 `i < j` 且 `hours[i]+hours[j]` 是 24 的倍数的下标对',
                 '示例：`[72,48,24,3]` → `3`',
                 '本视频：`[72,48,24,3,21]` → `4`'],
        quote='对于其中的某个元素v，若v等于0，那么就需要找到另一个0与之配对，否则需要找到24 - v与之配对。',
        quote_src='—— yiduobo 题解原文',
        idea=['和是 24 的倍数 ⇔ 两个余数之和为 0 或 24',
              '`v == 0` 找 0，否则找 `24 - v`',
              '一趟遍历：先把 `freq` 里的配对数加进答案，再把自己记进去'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==余数 0 要单独处理==：`24 - 0 = 24` 不是有效余数',
                 '==先累加再 +1==：这样只数 `i < j` 的对，不会和自己配对',
                 '3185（II）数据更大，同一写法直接通过',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
