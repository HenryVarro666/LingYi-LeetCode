def _b(x, w=4):
    return list(format(x, '0%db' % w))

CONFIG = dict(
    num=2220, title='转换数字的最少位翻转次数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='异或 + 逐个去掉最低位 1',
    tags=['位运算', '基础题', '难度分 1282'],
    code='''
class Solution(object):
    def minBitFlips(self, start, goal):

        res = 0
        diff = start ^ goal
        while diff:
            res += 1
            diff -= diff & -diff
        
        return res
''',
    call='Solution().minBitFlips(10, 7)',
    expect=3,
    views=[
        dict(type='string', var=lambda S: _b(S['start'] ^ S['goal']), label='start ^ goal（初始的 diff）',
             color=lambda S, i, v: 'yellow' if v == '1' else None, h=140),
        dict(type='string', var=lambda S: _b(S['diff']) if 'diff' in S else _b(0), label='diff（还剩的不同位）',
             color=lambda S, i, v: 'pink' if v == '1' else None, h=140),
        dict(type='text', fn=lambda S: f"`diff & -diff` = {S['diff'] & -S['diff']}（最低位的 1）" if S.get('diff') else '', size=32),
    ],
    watch=['start', 'goal', 'diff', ('res', 'res', 'green')],
    captions={
        'diff = start ^ goal': '异或：不同的位变 1 → `diff = {diff}`，二进制 `{diff:04b}`',
        'while diff': lambda S, B, r: (f'`diff = {S.diff}` 还有 1 → 继续' if S.diff else '`diff = 0`：不同的位都处理完了 → 结束'),
        'res += 1': '又找到一个不同的位，要翻转一次：`res` → {res}',
        'diff -= diff & -diff': '`diff & -diff` 只留下最低位的 1，减掉它 → 去掉一个 1：`diff` = {diff}',
        'return': '一共翻转 =={res}== 次',
    },
    cards=dict(
        one_liner='异或后数有几个 1，就要翻几次',
        complexity='时间 `O(k)`（k 为 1 的个数），空间 `O(1)`',
        problem=['每次只能翻转一位，求 `start` 变成 `goal` 的最少次数',
                 '示例：`start=10, goal=7` → `3`'],
        quote='由于每次只能翻转一位，那么实际上就是问start和goal不同的位有多少，那么可以将二者异或，再计算异或结果中1的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先异或，得到 `diff`，1 的位置就是不同的位',
              '数 1 的个数：每轮用 `diff & -diff` 取出最低位的 1 并减掉',
              '循环几轮，答案就是几'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '`diff & -diff` 是 lowbit，只保留最低位的 1',
                 '原文本身就是 Python 3 可运行的，没有改动'],
    ),
)
