CONFIG = dict(
    num=1247, title='交换字符使得字符串相同', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='x 的数目配平 + 位置差别',
    tags=['贪心算法', '思维题', '难度分 1597'],
    code='''
class Solution(object):
    def minimumSwap(self, s1, s2):

        l = len(s1)
        x1 = x2 = 0
        diff = 0
        for index in range(l):
            char1 = s1[index]
            char2 = s2[index]
            if char1 == 'x':
                x1 += 1
            if char2 == 'x':
                x2 += 1
            if char1 != char2:
                diff += 1
        
        if (x1 + x2) % 2 != 0:
            return -1
        
        res = abs(x1 - x2) // 2
        diff -= abs(x1 - x2)
        if diff < 0:
            diff = 0
        res += diff // 4 * 2
        if diff % 4 > 0:
            res += 2
        return res
''',
    call='Solution().minimumSwap("xxxyx", "yyyxx")',
    expect=3,
    views=[
        dict(type='string', var='s1', h=210, label='s1', pointers={'index': 'blue'},
             color=lambda S, i, v: 'orange' if S['s1'][i] != S['s2'][i] else None),
        dict(type='string', var='s2', h=170, label='s2（橙色 = 这一位两串不同）',
             color=lambda S, i, v: 'orange' if S['s1'][i] != S['s2'][i] else None),
        dict(type='text', size=32, h=80, fn=lambda S: f"s1 中 x 有 `x1 = {S['x1']}` 个，s2 中 x 有 `x2 = {S['x2']}` 个，位置不同 `diff = {S['diff']}` 处" if 'diff' in S else ''),
        dict(type='text', size=32, h=80, fn=lambda S: f"答案累计 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('x1', 'x1', 'blue'), ('x2', 'x2', 'pink'), ('diff', 'diff', 'orange'), ('res', 'res', 'green')],
    skip=['char1 = s1', 'char2 = s2'],
    captions={
        'x1 += 1': '`s1[{index}]` 是 x：`x1` → =={x1}==',
        'x2 += 1': '`s2[{index}]` 是 x：`x2` → =={x2}==',
        'if char1 == ': lambda S, B, ret: f"`s1[{S.index}] = '{S.char1}'`" + (' 是 x，计入 x1' if S.char1 == 'x' else ' 不是 x'),
        'if char2 == ': lambda S, B, ret: f"`s2[{S.index}] = '{S.char2}'`" + (' 是 x，计入 x2' if S.char2 == 'x' else ' 不是 x'),
        'if char1 != char2': lambda S, B, ret: f"`'{S.char1}'` 和 `'{S.char2}'`" + (' 不同，位置差别 +1' if S.char1 != S.char2 else ' 相同，不用管'),
        '(x1 + x2) % 2': lambda S, B, ret: f"x 的总数 `x1 + x2 = {S.x1 + S.x2}`：" + ('是奇数，两串的 x 数永远配不平 → ==返回 -1==' if (S.x1 + S.x2) % 2 else '是偶数，可以让两串的 x 数相等'),
        'res = abs': '两串 x 数差 `p = |{x1} - {x2}| = {abs(x1 - x2)}`，每次交换调平 2 个：`res` = =={res}==，同时顺带修好 `p` 个位置差别',
        'diff -= abs': '顺带修掉 `{abs(x1 - x2)}` 处，位置差别剩 `diff` = =={diff}==',
        'if diff < 0': lambda S, B, ret: ('`diff` 不足 0：配平时已经全部修好，置为 0' if S.diff < 0 else '`diff` 没有变负，保持不变'),
        'res += diff // 4': '每 `4` 个位置差别用 `2` 次操作解决：`res += {diff // 4} * 2` → =={res}==',
        'if diff % 4': lambda S, B, ret: (f"`diff % 4 = {S.diff % 4}` > 0：还剩零头，要再花 ==2== 次" if S.diff % 4 else '`diff % 4 = 0`：正好整除，不用额外操作'),
        'res += 2': '剩下的零头再用 2 次操作解决：`res` → =={res}==',
        'return res': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='先让两串 x 的数目相等，再按 4 个差别 2 次操作处理',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s1`、`s2` 只含 `x`、`y`，每次交换 `s1` 的一个字符和 `s2` 的一个字符',
                 '求使两串相同的最少交换次数，不可能则返回 `-1`',
                 '示例：`"xy","yx"` → `2`'],
        quote='只要将两个字符串的x调整成一样，那么其他的y必然都是一样的。……若x1 + x2为奇数，那么无论如何都不可能让两个字符串中的x数目一致，因此直接返回-1即可。',
        quote_src='—— yiduobo 题解',
        idea=['统计两串 x 的数目 `x1`、`x2` 和位置不同的个数 `diff`；`x1 + x2` 为奇数就无解',
              '两串 x 数相差 `p`，需要 `p / 2` 次交换配平，同时顺带解决 `p` 处差别',
              '剩下的 `diff` 用 2 次操作解决 4 处，零头再加 2 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判 `(x1 + x2) % 2`，奇数无解',
                 '`diff` 减 `p` 后可能为负，要当 0 处理',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 2 处）'],
    ),
)
