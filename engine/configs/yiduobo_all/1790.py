CONFIG = dict(
    num=1790, title='仅执行一次字符串交换能否使两个字符串相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 统计不同位',
    code='''
class Solution(object):
    def areAlmostEqual(self, s1, s2):

        n = len(s1)
        cnt = 0
        p = None
        for index in range(n):
            if s1[index] != s2[index]:
                if cnt == 0:
                    p = index
                elif cnt == 1:
                    if s1[p] != s2[index] or s2[p] != s1[index]:
                        return False
                else:
                    return False
                
                cnt += 1
        
        return cnt % 2 == 0
''',
    call="Solution().areAlmostEqual('bank', 'kanb')",
    expect=True,
    views=[
        dict(type='string', var='s1', pointers={'index': 'blue', 'p': 'pink'}, h=190, label='s1',
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and S['s1'][i] != S['s2'][i] else None),
        dict(type='string', var='s2', pointers={'index': 'blue'}, h=190, label='s2',
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and S['s1'][i] != S['s2'][i] else None),
        dict(type='text', size=32, h=100, fn=lambda S: f"不同位数量 `cnt = {S['cnt']}`" + (f"，第一处不同在 `p = {S['p']}`" if S.get('p') is not None else '') if 'cnt' in S else ''),
    ],
    watch=['index', ('cnt', 'cnt', 'yellow'), ('p', 'p', 'pink')],
    captions={
        'n = len': '`n = {n}`，两串等长',
        'cnt = 0': '`cnt` 记录目前遇到几处不同',
        'p = None': '`p` 记住第一处不同的位置',
        'for index': '看第 `{index}` 位：`{s1[index]}` 对 `{s2[index]}`',
        'if s1[index] != s2[index]': lambda S, B, r: (f'`{S.s1[S.index]} != {S.s2[S.index]}`：这一位不同，要处理' if S.s1[S.index] != S.s2[S.index]
                                                       else f'`{S.s1[S.index]} == {S.s2[S.index]}`：相同，跳过'),
        'if cnt == 0': lambda S, B, r: ('`cnt == 0`：第一处不同，先记下位置' if S.cnt == 0 else '`cnt != 0`：之前已有不同位'),
        'p = index': '记下第一处不同的位置 `p = {p}`',
        'elif cnt == 1': lambda S, B, r: ('`cnt == 1`：这是第二处不同，要检查能否互换' if S.cnt == 1 else '`cnt` 不是 1：已有两处以上不同'),
        'if s1[p] != s2[index]': lambda S, B, r: (f'交叉比较：`s1[{S.p}]={S.s1[S.p]}` 对 `s2[{S.index}]={S.s2[S.index]}`，`s2[{S.p}]={S.s2[S.p]}` 对 `s1[{S.index}]={S.s1[S.index]}` → '
                                                  + ('有一对对不上，不是恰好错位，返回 False' if (S.s1[S.p] != S.s2[S.index] or S.s2[S.p] != S.s1[S.index]) else '都对得上：恰好错位，交换一次能修复')),
        'cnt += 1': '不同位数加一：`cnt` → =={cnt}==',
        'return cnt % 2': '`cnt = {cnt}`：0 表示本来就相等，2 表示恰好错位；==1 不行==（单独一处不同换不了）→ {ret}',
    },
    cards=dict(
        one_liner='一次交换要么本来就相等，要么恰好两处错位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给两个等长字符串 `s1`、`s2`，最多对其中一个串交换一次两个位置的字符',
                 '能让两串相等返回 `True`，否则 `False`',
                 '示例：`s1="bank"`，`s2="kanb"` → `True`（交换 `s2` 的首尾）'],
        quote='于是可以一趟扫描，统计当前不同字符的数目cnt。当出现一处不相等的字符时：若之前没有出现过不同的字符，那么将cnt加1，并使用一个变量p记录这一处字符',
        quote_src='—— yiduobo 题解原文',
        idea=['第一处不同：只记位置 `p`',
              '第二处不同：检查 `s1[p]==s2[i]` 且 `s2[p]==s1[i]`，即恰好错位',
              '第三处不同：直接返回 `False`；扫完后 `cnt` 只能是 0 或 2'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`cnt == 1` 时不能返回 True，一处不同无法靠交换修复',
                 '易错：第二处不同要交叉比较，不是只看字符是否不同',
                 '原文代码在 Python 3 下无需修改即可运行'],
    ),
)
