STONES = [10, 4, 3, 1]


def _cap_if(S, B, ret):
    l, st = S.l, S.stone
    if B.f[l - st]:
        return f'`f[{l} − {st}] = f[{l - st}]` 为真：凑出 {l - st} 再加上石头 `{st}` → 能凑出 =={l}=='
    return f'`f[{l - st}]` 为假：选这块石头也凑不出 `{l}`'


def _cap_for_stone(S, B, ret):
    if S.get('stone') == B.get('stone') and 'stone' in B:
        return '所有石头都考虑过了'
    st, t = S.stone, S.target
    if st > t:
        return f'考虑石头 `{st}`：比 target `{t}` 还重，放不进这一半 → 内层循环一次都不跑'
    return f'考虑石头 `{st}`：j ==从大到小==枚举 `{t}…{st}`，保证每块石头只用一次'


CONFIG = dict(
    num=1049, title='最后一块石头的重量II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='0-1 背包 · 可行性 DP',
    tags=['字节30天'],
    code='''
class Solution(object):
    def lastStoneWeightII(self, stones):

        n = len(stones)
        s = sum(stones)
        target = s // 2

        f = [False] * (target + 1)
        f[0] = True
        for stone in stones:
            for l in range(target, stone - 1, -1):
                if f[l - stone]:
                    f[l] = True

        while not f[target]:
            target -= 1

        return s - target - target
''',
    call=f'Solution().lastStoneWeightII({STONES})',
    expect=2,
    skip=['n = len', 'for l in range'],
    views=[
        dict(type='array', var='stones', label='stones（黄 = 正在考虑的石头）', h=150, cell=80,
             color=lambda S, i, v: 'yellow' if S.get('stone') == v and S.get('_line', 0) <= 13 else None),
        dict(type='text', fn=lambda S: (f"总重 `s = {S['s']}`，目标：选一些石头，重量尽量接近 `s // 2`" if 's' in S else ''), size=26, h=60),
        dict(type='array', var='f', label='f[j]：能否选出一些石头，重量恰好为 j（T = 能）', h=250, cell=70,
             pointers={'l if _line <= 13 else None': 'pink', 'l - stone if _line <= 13 else None': 'blue',
                       'target if _line >= 15 else None': 'green'},
             pointer_labels={'l if _line <= 13 else None': 'l', 'l - stone if _line <= 13 else None': 'l−stone',
                             'target if _line >= 15 else None': 'target'},
             color=lambda S, i, v: 'green' if v is True else None),
        dict(type='text', fn=lambda S: ('另一堆重 `s − target`，两堆之差就是最后剩下的重量' if S.get('_line', 0) >= 15
                                        else '石头分成两堆，相互抵消 → 差值越小越好'), size=24, h=56),
    ],
    watch=[('s', 's'), ('target', 'target', 'green'), ('stone', 'stone', 'yellow'), ('l', 'l', 'pink')],
    captions={
        's = sum(stones)': '所有石头总重 `s = {s}`',
        'target = s // 2': '`target = s // 2 = {target}`：较轻的那一堆最多这么重（原文 `s / 2`，Python 3 改为 `//`）',
        'f = [False]': '`f[j]`：能否凑成重量 j；一开始都不能',
        'f[0] = True': '`f[0] = True`：什么都不选，重量 0',
        'for stone in stones': _cap_for_stone,
        'if f[l - stone]': _cap_if,
        'f[l] = True': '`f[{l}] = True`',
        'while not f[target]': lambda S, B, r: (f'`f[{B.target}]` 为假：凑不出 `{B.target}` → 往下找' if not B.f[B.target]
                                                else f'`f[{B.target}]` 为真：最接近 s/2 的重量就是 =={B.target}=='),
        'target -= 1': '`target` → {target}',
        'return s - target - target': '两堆分别重 `{target}` 和 `{s} − {target} = {s - target}` → 差 `{s} − {target} − {target}` = =={ret}==',
    },
    cards=dict(
        one_liner='把石头分成两堆，让两堆重量之差最小 —— 0-1 背包',
        complexity='时间 `O(n · s)`，空间 `O(s)`',
        problem=['每回合选两块石头 `x ≤ y` 相撞：相等都粉碎，否则剩下 `y − x`',
                 '最多只剩一块石头，返回它==可能的最小重量==（没有石头返回 0）',
                 '示例：`[2,7,4,1,8,1]` → `1`',
                 f'本视频：`{STONES}` → `2`'],
        quote='由于每一轮可以任意选取两块石头，那么这里的问题实际上就是==如何将石头划分成两个部分，使这两个部分重量之差最小==。于是又转化成了经典的背包问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['目标：选出一些石头，重量尽可能接近 `target = s / 2`',
              '`f[i][j] = f[i−1][j] or f[i−1][j − stones[i−1]]`',
              '只与上一轮有关 → 省去 i 这一维，==从大到小枚举 j=='],
        summary=['时间 `O(n · s)`，空间 `O(s)`',
                 '易错：j 必须==倒序==，正序会让同一块石头被用多次（变成完全背包）',
                 'DP 完成后从 target 往下找第一个为真的，答案 `(s − target) − target`',
                 '原文为 Python 2 写法：`target = s / 2` 已改为 `s // 2`，并删去了类型说明文档字符串'],
    ),
)
