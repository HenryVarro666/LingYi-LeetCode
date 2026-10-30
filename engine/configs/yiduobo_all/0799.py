def _fn(S):
    if 'flag' not in S:
        return '`f[flag]` 是正在算的下一层，`f[1 - flag]` 是已经算好的上一层'
    i = S.get('i')
    if i is None:
        return ''
    return f"正在由第 `{i - 1}` 层（`f[{1 - S['flag']}]`）推第 `{i}` 层（`f[{S['flag']}]`）"


def _mk(k):
    return lambda S, a, v: ('green' if S.get('flag') == k and v > 0 else
                            'blue' if 'flag' in S and S.get('flag') != k and v > 1 else None)


CONFIG = dict(
    num=799, title='香槟塔', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='逐层递推 · 01 滚动数组',
    tags=[],
    code='''
class Solution(object):
    def champagneTower(self, poured, query_row, query_glass):
        
        f = [[float(poured)], []]
        flag = 1
        for i in range(1, query_row + 1):
            f[flag] = [0.0] * (i + 1)
            for j, c in enumerate(f[1 - flag]):
                if c > 1:
                    delta = c - 1
                    f[flag][j] += delta / 2.0
                    f[flag][j + 1] += delta / 2.0
            flag ^= 1
            

        res = f[query_row & 1][query_glass]
        if res > 1:
            return 1.0
        return res
''',
    call='Solution().champagneTower(8, 3, 1)',
    expect=0.875,
    views=[
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='array', var=lambda S: S['f'][0] if 'f' in S else None, label='f[0]', cell=110, h=170, color=_mk(0)),
        dict(type='array', var=lambda S: S['f'][1] if 'f' in S else None, label='f[1]', cell=110, h=170, color=_mk(1)),
    ],
    watch=[('i', 'i', 'blue'), ('flag', 'flag', 'purple'), ('j', 'j', 'blue'), ('delta', 'delta', 'yellow')],
    captions={
        'f = [[float': '`f[i][j]` 表示第 i 层第 j 个杯子的量；只靠前一层，所以用两行滚动。顶层 `f[0][0] = poured = {poured}`',
        'flag = 1': '`flag` 在 0 和 1 之间翻转：`f[flag]` 写下一层，`f[1 - flag]` 读上一层',
        'for i in range': lambda S, B, r: ('每一层都推完了' if 'i' in B and B.i == S.i else f'推第 `{S.i}` 层'),
        'f[flag] = [0.0]': '下一层有 `{i + 1}` 个杯子，先全部清零',
        'for j, c in enumerate': lambda S, B, r: (f'看上一层第 `{S.j}` 个杯子，量 `c = {S.c}`' if 'c' in S and 'j' in S and ('c' not in B or 'j' not in B or (B.j, B.c) != (S.j, S.c)) else '上一层看完了'),
        'if c > 1': lambda S, B, r: (f'`c = {S.c} > 1`：杯子装满，多出来的会往下流' if S.c > 1 else f'`c = {S.c} ≤ 1`：没满，不往下溢'),
        'delta = c - 1': '溢出量 `delta = {c} − 1 = {delta}`',
        'f[flag][j] += delta': '一半 `{delta / 2}` 流给左下杯子 `f[{flag}][{j}]` → {f[flag][j]}',
        'f[flag][j + 1] += delta': '另一半 `{delta / 2}` 流给右下杯子 `f[{flag}][{j + 1}]` → {f[flag][j + 1]}',
        'flag ^= 1': '这一层算完，`flag` 异或 1 翻转：刚写好的那一行变成「上一层」',
        'res = f[query_row & 1]': '答案在 `f[query_row & 1]`（行号奇偶决定它在哪一行）：第 `{query_row}` 层第 `{query_glass}` 杯 = {res}',
        'if res > 1': lambda S, B, r: ('超过 1 说明溢出，杯子只能装满 → 1.0' if S.res > 1 else f'`res = {S.res}` 不超过 1，直接返回'),
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='二项式用不了（各杯进度不同），只能逐层递推',
        complexity='时间 `O(query_row^2)`，空间 `O(query_row)`',
        problem=['杯子摆成金字塔，第 `i` 层有 `i+1` 个，容量都是 1',
                 '从顶层倒 `poured` 杯，满了的杯子溢出的酒平分给左下、右下',
                 '求第 `query_row` 层第 `query_glass` 个杯子的量（最多 1）',
                 '本视频：`poured=8, row=3, glass=1` → `0.875`'],
        quote='乍一看感觉可以直接使用二项式定理来做，但是需要注意的是，这里每一层的杯子的进度是不一样的……因此无法直接套用二项式定理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 第 i 行第 j 个杯子最终的量，`f[0][0] = poured`',
              '`f[i][j] > 1` 时 `delta = f[i][j] - 1`，各分 `delta/2` 给 `f[i+1][j]` 和 `f[i+1][j+1]`',
              '转移只用到前一行 → 01 滚动数组，`flag` 来回翻转'],
        summary=['时间 `O(query_row^2)`，空间 `O(query_row)`',
                 '易错：答案在 `f[query_row & 1]`，不是固定某一行',
                 '易错：杯子最多装 1，结果大于 1 要返回 1.0',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：他倒序遍历 j，在一个数组里原地推'],
    ),
)
