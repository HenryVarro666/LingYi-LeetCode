def _eq(S):
    if 'index' not in S or 'res' not in S:
        return ''
    i = S['index']
    p = S['pref']
    if S.get('_line', 0) >= 6:
        return f"`arr[{i}] = pref[{i}] ^ pref[{i-1}]` = `{p[i]} ^ {p[i-1]}` = =={p[i] ^ p[i-1]}=="
    return f"现在处理下标 `index = {i}`：`pref[{i}] = pref[{i-1}] ^ arr[{i}]`"


CONFIG = dict(
    num=2433, title='找出前缀异或的原始数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='相邻前缀异或', tags=['灵神题单', '难度分 1367'],
    code='''
class Solution(object):
    def findArray(self, pref):

        res = [pref[0]]
        for index in range(1, len(pref)):
            res.append(pref[index] ^ pref[index - 1])

        return res
''',
    call='Solution().findArray([5, 2, 0, 3, 1])',
    expect=[5, 7, 2, 3, 2],
    views=[
        dict(type='array', var='pref', h=170, label='pref（前缀异或）',
             color=lambda S, i, v: 'yellow' if 'index' in S and i in (S['index'], S['index'] - 1) else None),
        dict(type='text', size=28, fn=_eq),
        dict(type='array', var='res', h=170, label='res = arr',
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = [pref[0]]': '`pref[0] = arr[0]`，第一个数直接照抄：`res = {res}`',
        'for index in range': lambda S, B, r: (f'处理下标 `index = {S.index}`' if len(S.res) < len(S.pref) else '所有下标处理完'),
        'res.append': '`pref[{index}]` 比 `pref[{index} - 1]` 多异或了 `arr[{index}]`，两者再异或就只剩它：`{pref[index]} ^ {pref[index - 1]}` = =={res[-1]}==',
        'return res': '一趟遍历完成，返回 `{res}`',
    },
    cards=dict(
        one_liner='相邻两个前缀异或再异或一次，就剩下中间那个数',
        complexity='时间 `O(n)`，空间 `O(1)`（不算结果数组）',
        problem=['已知 `pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]`，还原 `arr`',
                 '答案唯一',
                 '示例：`pref=[5,2,0,3,1]` → `[5,7,2,3,2]`'],
        quote='pref[index] = pref[index - 1] ^ arr[index]，于是就有 arr[index] = pref[index] ^ pref[index - 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['`index = 0` 时显然 `arr[0] = pref[0]`',
              '把 `pref[index]` 和 `pref[index-1]` 两个式子对照：前者只比后者多一个 `arr[index]`',
              '再异或一次，前面所有项成对抵消，只剩 `arr[index]`'],
        summary=['时间 `O(n)`，空间 `O(1)`（不算结果）',
                 '易错点：`index` 从 1 开始，`arr[0]` 要单独放',
                 '和前缀和的「差分」同一回事，只是加减换成了异或',
                 '相关：1720. 解码异或后的数组'],
    ),
)
