def _tgt(S):
    ln, j, rod = S.get('_line'), S.get('j'), S.get('rod')
    if j is None or rod is None:
        return None
    if ln in (12, 13):
        return j
    if ln in (15, 16, 17):
        return j + rod
    if ln in (19, 20, 21):
        return abs(j - rod)
    return None


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    t = _tgt(S)
    if i is None or j is None or t is None:
        return None
    if r == i + 1 and c == t:
        return 'yellow'
    if r == i and c == j:
        return 'blue'
    return None


def _txt(S):
    i, j, rod = S.get('i'), S.get('j'), S.get('rod')
    if i is None or j is None or S.get('_line') not in range(11, 22) or S['f'][i][j] is None:
        return '`f[i][d]` = 前 i 根钢筋、两侧高度差为 `d` 时的==最大高度之和==（None = 做不到）'
    base = S['f'][i][j]
    return f'`f[{i}][{j}] = {base}` + 钢筋 `{rod}` → 新高度和 `{base + rod}`，差 `{j}` / `{j + rod}` / `{abs(j - rod)}`'


CONFIG = dict(
    num=956, title='最高的广告牌', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包 · 状态记录两侧高度差',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def tallestBillboard(self, rods):

        s = sum(rods)
        max_len = s // 2
        f = [[None] * (max_len + 1) for _ in range(len(rods) + 1)]
        f[0][0] = 0

        for i, rod in enumerate(rods):
            for j in range(0, max_len + 1):
                if f[i][j] is not None:
                    if f[i + 1][j] is None or f[i + 1][j] < f[i][j]:
                        f[i + 1][j] = f[i][j]

                    if j + rod <= max_len:
                        if f[i + 1][j + rod] is None or f[i + 1][j + rod] < f[i][j] + rod:
                            f[i + 1][j + rod] = f[i][j] + rod
                    
                    if abs(j - rod) <= max_len:
                        if f[i + 1][abs(j - rod)] is None or f[i + 1][abs(j - rod)] < f[i][j] + rod:
                            f[i + 1][abs(j - rod)] = f[i][j] + rod
        
        return f[-1][0] // 2
''',
    call='Solution().tallestBillboard([1, 2, 3])',
    expect=3,
    skip=['for j in range', 's = sum', 'f[0][0] = 0'],
    views=[
        dict(type='array', var='rods', label='rods', h=170, cell=80,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='text', fn=_txt, size=22, h=100),
        dict(type='table', var='f', label='f[i][d]（值=两侧高度和，黄=写入，蓝=来源）',
             h=360, cell=84, rows=lambda S: [f'前{k}根' for k in range(len(S['rods']) + 1)],
             cols=lambda S: [f'd={k}' for k in range(S['max_len'] + 1)], color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('rod', 'rod', 'pink'), ('j(差)', 'j', 'yellow'), ('max_len', 'max_len', 'cyan')],
    captions={
        'max_len = s': '差 `d` 不会超过总和的一半：`max_len = {s} // 2 = {max_len}`',
        'f = [[None]': '`f[i][d]`：前 i 根钢筋、两侧差为 d 时==两侧高度之和==的最大值；None 表示做不到',
        'f[0][0] = 0': '一根都不用：差为 0，高度和为 0',
        'for i, rod': lambda S, B, r: (f'处理第 `{S.i}` 根钢筋 `{S.rod}`，从 `f[{S.i}][·]` 推出 `f[{S.i + 1}][·]`' if S.i != B.get('i') or S.get('rod') != B.get('rod') else '钢筋都处理完了'),
        'if f[i][j] is not None': lambda S, B, r: (f'`f[{S.i}][{S.j}] = {S.f[S.i][S.j]}`：差 {S.j} 可达，往下三种放法' if S.f[S.i][S.j] is not None
                                                   else f'`f[{S.i}][{S.j}]` 做不到，跳过'),
        'if f[i + 1][j] is None or f[i + 1][j] <': '情况 1：==不选==这根，差不变 `d={j}`，高度和保持 `{f[i][j]}`，取较大者',
        'f[i + 1][j] = f[i][j]': '`f[{i + 1}][{j}] = {f[i + 1][j]}`',
        'if j + rod <= max_len': '情况 2：焊到==较高==的一侧，差变成 `{j} + {rod} = {j + rod}`，没超过 `max_len` 才记录',
        'if f[i + 1][j + rod] is None': '比较 `f[{i + 1}][{j + rod}]` 与 `{f[i][j]} + {rod}`，取大',
        'f[i + 1][j + rod] = f[i][j] + rod': '`f[{i + 1}][{j + rod}] = {f[i + 1][j + rod]}`：两侧高度和增加 `{rod}`',
        'if abs(j - rod) <= max_len': '情况 3：焊到==较矮==的一侧，差变成 `abs({j} - {rod}) = {abs(j - rod)}`',
        'if f[i + 1][abs(j - rod)] is None': '比较 `f[{i + 1}][{abs(j - rod)}]` 与 `{f[i][j]} + {rod}`，取大',
        'f[i + 1][abs(j - rod)] = f[i][j] + rod': '`f[{i + 1}][{abs(j - rod)}] = {f[i + 1][abs(j - rod)]}`（差可能缩小，矮侧追上或反超）',
        'return f[-1][0]': '最后一行差为 0：两侧等高，高度和 `{f[-1][0]}`，除以 2 得单侧高度 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='只记两侧高度差，值存高度之和',
        complexity='时间 `O(n·s)`，空间 `O(n·s)`（s 为钢筋总和）',
        problem=['给一组钢筋，焊成两根等高支架，求==最大的支架高度==',
                 '每根钢筋可放左、放右或不用，两侧必须等高',
                 '示例：`[1,2,3]` → `3`；本视频：`[1,2,3]` → `3`（1+2 = 3）'],
        quote='可以将状态改造成f[i][d]表示前i根钢筋，构造出两侧绝对值之差为d的支架时，两侧高度之和是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接 `f[i][j][k]` 记左 j 右 k，状态太多，浪费了一个维度',
              '最终要 j = k，所以只关心差 `d` 和 `j + k`：差是限制，和是目标',
              '每根钢筋三种放法：不选、加到高侧、加到矮侧（差取绝对值）'],
        summary=['时间/空间 `O(n·s)`，差最大只需到 `s // 2`',
                 '易错：焊到矮侧时差是 `abs(d - rod)`，可能反超',
                 '答案是 `f[n][0] // 2`：存的是两侧之和',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（两处）',
                 '对比常规做法：直接 3^n 搜索会超时'],
    ),
)
