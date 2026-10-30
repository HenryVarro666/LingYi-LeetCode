def _grid(S):
    return [list(s) for s in S['strs']]


def _cell(S, i, j, v):
    if 'i' not in S:
        return None
    if j == S['i']:
        if 'j' in S and S['_line'] in (9, 10, 11) and i in (S['j'], S['j'] + 1):
            return 'red' if S['strs'][S['j']][S['i']] > S['strs'][S['j'] + 1][S['i']] else 'green'
        return 'blue'
    return None


def _txt(S):
    if 'res' not in S:
        return ''
    if 'i' not in S:
        return ''
    return f"检查第 `{S['i']}` 列，已发现 ==res== = {S['res']} 列要删"


CONFIG = dict(
    num=944, title='删列造序', difficulty='Easy', category='字符串',
    author='yiduobo', technique='枚举每一列 + 相邻比较',
    code='''
class Solution(object):
    def minDeletionSize(self, strs):

        n = len(strs)
        l = len(strs[0])
        
        res = 0
        for i in range(l):
            for j in range(n - 1):
                if strs[j][i] > strs[j + 1][i]:
                    res += 1
                    break
        
        return res
''',
    call='Solution().minDeletionSize(["cba","daf","ghi"])',
    expect=1,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var=_grid, color=_cell, h=330, cell=90, label=''),
    ],
    watch=['n', 'l', 'i', 'j', ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`：有 {n} 行字符串',
        'l = len': '`l = {l}`：每个字符串长 {l}，也就是有 {l} 列',
        'res = 0': '`res` 统计要删的列数',
        'for i in range': lambda S, B, r: (f'枚举第 `{S.i}` 列' if B.get('i') != S.i else '所有列都枚举完'),
        'for j in range': lambda S, B, r: (f'从上往下，比较第 `{S.j}` 行和第 `{S.j+1}` 行' if not (S.j == S.n - 2 and B.get('j') == S.j) else '这一列所有相邻行都比完，没有违规'),
        'if strs[j][i]': lambda S, B, r: (f"`{S.strs[S.j][S.i]} > {S.strs[S.j+1][S.i]}`：上面比下面大 → ==这列不是升序=="
                                          if S.strs[S.j][S.i] > S.strs[S.j+1][S.i]
                                          else f"`{S.strs[S.j][S.i]} <= {S.strs[S.j+1][S.i]}`：这一对没问题，继续往下"),
        'res += 1': '这列要删：`res` → {res}',
        'break': '这列已经确定要删，不用再看下面的行，跳到下一列',
        'return res': '要删的列数 `{res}`',
    },
    cards=dict(
        one_liner='枚举每一列，检查是否按升序排列',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['`n` 个等长小写字符串排成网格，删掉不是非严格递增的列',
                 '返回删除的列数',
                 '示例：`["cba","daf","ghi"]` → `1`'],
        quote='比较基础的题目， 直接枚举每一列，然后检测该列是否按升序排列即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举列 `i`，内层从上到下比较相邻两行',
              '只要有一对 `strs[j][i] > strs[j+1][i]`，这列就要删',
              '找到后 `break`，避免同一列重复计数'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '易错：`break` 必须有，否则一列可能被加多次',
                 '相等不算违规，用 `>` 而不是 `>=`',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
