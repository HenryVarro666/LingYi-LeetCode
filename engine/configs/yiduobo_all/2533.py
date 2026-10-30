CONFIG = dict(
    num=2533, title='好二进制字符串的数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 末尾追加一整组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def goodBinaryStrings(self, minLength, maxLength, oneGroup, zeroGroup):

        f = [0] * (maxLength + 1)
        f[0] = 1
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, maxLength + 1):
            if index >= oneGroup:
                f[index] += f[index - oneGroup]
                if f[index] >= mod:
                    f[index] -= mod

            if index >= zeroGroup:
                f[index] += f[index - zeroGroup]
                if f[index] >= mod:
                    f[index] -= mod

            if index >= minLength:
                res += f[index]
                if res >= mod:
                    res -= mod

        return res
''',
    call='Solution().goodBinaryStrings(3, 6, 2, 3)',
    expect=6,
    views=[
        dict(type='text', h=70, size=26, fn=lambda S: (
            f"`f[{S['index']}]` = `f[{S['index']}-{S['oneGroup']}]` + `f[{S['index']}-{S['zeroGroup']}]`（末尾补一组 1 / 一组 0）"
            if 'index' in S else '`f[i]` = 长度为 i 的好字符串个数；`f[0] = 1`（空串）')),
        dict(type='array', var='f', label='f[i]：长度为 i 的好字符串数', h=300, cell=100,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if 'index' in S and i in (S['index'] - S['oneGroup'], S['index'] - S['zeroGroup']) and i >= 0 and S.get('_line') in (10, 11, 15, 16) else None)),
        dict(type='text', h=60, size=26, fn=lambda S: (
            f"答案 = `f[{S['minLength']}] … f[{S['maxLength']}]` 之和，目前 res = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('oneGroup', 'oneGroup', 'cyan'), ('zeroGroup', 'zeroGroup', 'orange'), ('res', 'res', 'green')],
    captions={
        'f = [0]': '`f` 长度 `maxLength + 1`，下标就是字符串长度',
        'f[0] = 1': '空串算一种方案，是所有转移的起点：`f[0] = 1`',
        'res = 0': '`res` 累加 长度在 `[minLength, maxLength]` 内的方案数',
        'mod =': '答案要取模 `10^9 + 7`；每次只加一次，所以用 ==减法代替取模==',
        'for index in range': lambda S, B, r: ('`index` 已到 `maxLength`，循环结束' if B.get('index') == S.index else f'依次算长度 `index` = {S.index}'),
        'if index >= oneGroup': lambda S, B, r: (f'`{S.index} >= {S.oneGroup}`：末尾能放下一组 1（{S.oneGroup} 个）→ 成立' if S.index >= S.oneGroup
                                                 else f'`{S.index} < {S.oneGroup}`：放不下一整组 1，跳过'),
        'f[index] += f[index - oneGroup]': '末尾是一组 1：前面是长 `{index - oneGroup}` 的好串 → `f[{index}] += f[{index - oneGroup}]` = =={f[index]}==',
        'if index >= zeroGroup': lambda S, B, r: (f'`{S.index} >= {S.zeroGroup}`：末尾能放下一组 0（{S.zeroGroup} 个）→ 成立' if S.index >= S.zeroGroup
                                                  else f'`{S.index} < {S.zeroGroup}`：放不下一整组 0，跳过'),
        'f[index] += f[index - zeroGroup]': '末尾是一组 0：前面是长 `{index - zeroGroup}` 的好串 → `f[{index}] += f[{index - zeroGroup}]` = =={f[index]}==',
        'if index >= minLength': lambda S, B, r: (f'`{S.index} >= {S.minLength}`：长度合法，`f[{S.index}]` 计入答案' if S.index >= S.minLength
                                                  else f'`{S.index} < {S.minLength}`：太短，不计入答案'),
        'res += f[index]': '`res += f[{index}]` → =={res}==',
        'return res': '`f[{minLength}]` 到 `f[{maxLength}]` 累加完毕，答案 `{ret}`',
    },
    skip=['if f[index] >= mod', 'f[index] -= mod', 'if res >= mod', 'res -= mod'],
    cards=dict(
        one_liner='好串 = 一组组的 1 或 0 拼起来，看最后一组是什么',
        complexity='时间 `O(maxLength)`，空间 `O(maxLength)`',
        problem=['二进制串里每段连续的 1 长度是 `oneGroup` 的倍数，每段连续的 0 长度是 `zeroGroup` 的倍数',
                 '统计长度在 `[minLength, maxLength]` 内的好串个数，结果取模 `10^9+7`',
                 '本视频：`min=3, max=6, one=2, zero=3`'],
        quote='令f[i]表示长度为i的好字符串数目。初始状况下有f[0] = 1，接下来对于i > 0：若i >= oneGroup，那么就可以将这个字符串的最后oneGroup个字符设置为1，因此就有f[i] += f[i - oneGroup]',
        quote_src='—— yiduobo 题解原文',
        idea=['好串的结尾只有两种：最后补 `oneGroup` 个 1，或最后补 `zeroGroup` 个 0',
              '去掉这一组，前面剩下的仍是好串 → 加上 `f[i - oneGroup]`、`f[i - zeroGroup]`',
              '一趟算完 `f[1..maxLength]`，再把 `f[minLength..maxLength]` 加起来'],
        summary=['时间、空间 `O(maxLength)`',
                 '`f[0] = 1` 不能漏：一整组恰好填满时要靠它',
                 'oneGroup、zeroGroup 相等时两个转移都要加，不会重复计数（末尾字符不同）',
                 '取模用减法：每次只加一个小于 mod 的数'],
    ),
)
