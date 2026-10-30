CONFIG = dict(
    num=248, title='中心对称数 III', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='预生成所有长度 + 遍历计数',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def strobogrammaticInRange(self, low, high):

        f = []
        f.append([''])
        f.append(['0', '1', '8'])

        n = len(high)

        for index in range(2, n + 1):
            f.append([])
            for s in f[index - 2]:
                f[-1].append('0' + s + '0')
                f[-1].append('1' + s + '1')
                f[-1].append('6' + s + '9')
                f[-1].append('8' + s + '8')
                f[-1].append('9' + s + '6')
    
        res = 0
        low, high = int(low), int(high)
        for index in range(1, n + 1):
            for s in f[index]:
                if index == 1 or s[0] != '0':
                    if low <= int(s) <= high:
                        res += 1     

        return res
''',
    call="Solution().strobogrammaticInRange('50', '99')",
    expect=3,
    skip=['f.append([])', "f[-1].append('1'", "f[-1].append('6'", "f[-1].append('8'", "f[-1].append('9'"],
    max_steps=80,
    views=[
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"范围 `[{S['low']}, {S['high']}]`，只需构造长度 ≤ `{S['n']}` 的" if S['_line'] <= 11 and 'n' in S and isinstance(S['low'], str)
                           else (f"当前 `{S['s']}` = `{int(S['s'])}`，范围 `[{S['low']}, {S['high']}]`" if 's' in S and 'low' in S and S['_line'] >= 22 and not isinstance(S['low'], str) else ''))),
        dict(type='queue', var=lambda S: S['f'][1] if 'f' in S and len(S['f']) > 1 else None, label='f[1]', font=20, h=110),
        dict(type='queue', var=lambda S: S['f'][2] if 'f' in S and len(S['f']) > 2 else None, label='f[2]（由 f[0] 套数对，含前导 0 的 00）', font=20, h=110),
        dict(type='queue', var=lambda S: [S['s']] if 's' in S and S['_line'] >= 22 else None, label='正在检查的 s', font=24, h=110),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'yellow'), ('res', 'res', 'green'), ('low', 'low', 'cyan'), ('high', 'high', 'orange')],
    captions={
        'f = []': '`f[len]` 保存所有长度为 len 的中心对称数',
        "f.append([''])": '长度 0：空串，作为长度 2 的里层',
        "f.append(['0', '1', '8'])": '长度 1：`0`、`1`、`8`',
        'n = len(high)': '`high` 有 `{n}` 位 → 只要构造长度 ≤ `{n}` 的中心对称数，更长的一定超过 high',
        'for index in range(2, n + 1)': lambda S, B, r: ('长度 `2..n` 都构造完了' if S.index == B.get('index') else f'构造长度 `{S.index}` 的：由长度 `{S.index - 2}` 的头尾加数对而来'),
        'for s in f[index - 2]': lambda S, B, r: ('长度 `{}` 的里层都用完了'.format(S.index - 2) if 's' in B and B.s == S.s and B.get('index') == S.index else f'取里层 `s = {S.s!r}`'),
        "f[-1].append('0' + s + '0')": '给 `{s!r}` 的头尾加 5 种数对：`0…0` `1…1` `6…9` `8…8` `9…6`',
        'res = 0': '`res` 统计落在 `[low, high]` 里的个数',
        'low, high = int(low), int(high)': '字符串转成整数，才能比较大小：`low = {low}`，`high = {high}`',
        'for index in range(1, n + 1)': lambda S, B, r: ('所有长度都统计完了' if S.index == B.get('index') else f'统计长度 `{S.index}` 的所有中心对称数'),
        'for s in f[index]': lambda S, B, r: ('长度 `{}` 的候选都检查完了'.format(S.index) if 's' in B and B.s == S.s and B.get('index') == S.index else f'检查候选 `{S.s}`'),
        'if index == 1 or s[0]': lambda S, B, r: ('`{}` 有前导 0 且长度大于 1 → 不是合法数字，跳过'.format(S.s) if not (S.index == 1 or S.s[0] != '0') else f'`{S.s}` 没有前导 0（或只是单个数字）→ 合法'),
        'if low <= int(s) <= high': lambda S, B, r: (f'`{S.low} <= {int(S.s)} <= {S.high}` 成立 → ==计入=='
                                                     if S.low <= int(S.s) <= S.high else f'`{int(S.s)}` 不在 `[{S.low}, {S.high}]` 内 → 不计'),
        'res += 1': '`res` → {res}',
        'return res': '`[{low}, {high}]` 内共有 `{res}` 个中心对称数',
    },
    cards=dict(
        one_liner='长度 14 才 6 万多个：全部造出来再逐个数',
        complexity='时间/空间 `O(5^(L/2))`，`L = len(high)`',
        problem=['统计 `[low, high]` 范围内的中心对称数个数（`low`、`high` 是字符串）',
                 '中心对称数：旋转 180° 后不变，如 `69`、`88`、`96`',
                 '本视频：`low = "50"`，`high = "99"` → `3`（`69`、`88`、`96`）'],
        quote='注意到之前247题，最终长度为14的中心对称数也才62500个，那么完全可以根据high的长度n计算出所有长度小于等于n的中心对称数，然后一趟遍历，统计大小处于low到high之间的数就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位 DP 或分情况计数也行，但这里数据规模允许暴力',
              '用 247 题的递推造出长度 `1..len(high)` 的所有中心对称数',
              '去掉前导 0 的，剩下的逐个和 `low`、`high` 比大小'],
        summary=['时间/空间 `O(5^(L/2))`，`L ≤ 15` 时可以直接枚举',
                 '易错：比较前要把 `low`、`high` 转成整数，不能比字符串',
                 '易错：长度为 1 的 `0` 合法，长度 > 1 的前导 0 要丢弃',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
