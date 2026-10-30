CONFIG = dict(
    num=3208, title='交替组 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='复制成线性 · start/p 双指针', tags=[],
    code='''
class Solution(object):
    def numberOfAlternatingGroups(self, colors, k):

        n = len(colors)
        colors += colors
        start = 0
        p = 1
        res = 0
        while start < n:
            while p - start < k and colors[p] != colors[p - 1]:
                p += 1

            if p - start == k:
                res += 1
                while start + 1 < n and colors[p] != colors[p - 1]:
                    p += 1
                    start += 1
                    res += 1
                
            if start < n:
                start = p
                p += 1
        
        return res
''',
    call='Solution().numberOfAlternatingGroups([0,1,0,0,1,0,1], 4)',
    expect=4,
    views=[
        dict(type='array', var='colors', label='colors 复制成两份（粗框 = 当前窗口 start..p-1）', h=250, cell=60,
             pointers={'start': 'blue', 'p': 'pink'}, window=('start', 'p - 1'),
             color=lambda S, i, v: 'blue' if v == 1 else 'pink'),
        dict(type='text', fn=lambda S: (f"窗口 `colors[{S['start']}:{S['p']}]` 长 {S['p'] - S['start']}，k = {S['k']}" if 'p' in S and 'start' in S else ''), size=28, h=60),
    ],
    watch=['n', ('start', 'start', 'blue'), ('p', 'p', 'pink'), 'k', ('res', 'res', 'green')],
    max_steps=80,
    captions={
        'n = len': '`n = {n}`',
        'colors += colors': '把 `colors` 复制一份接在后面：==环 → 线性==，长度变成 `{len(colors)}`',
        'start = 0': '`start` 是当前交替组的起点',
        'p = 1': '`p` 从 `start + 1` 往后检测',
        'res = 0': '`res` 统计交替组个数',
        'while start < n': lambda S, B, r: ('起点还在原数组范围内，继续' if S.start < S.n else f'`start = {S.start}` 到了 n → 结束'),
        'while p - start < k and': lambda S, B, r: (f"窗口长 `{S.p - S.start}`，" +
                    ('还不够 k' if S.p - S.start < S.k else '已够 k，停止') +
                    ('；`colors[p]` 与 `colors[p-1]` ' + ('不同 → p 右移' if S.colors[S.p] != S.colors[S.p - 1] else '相同 → 交替断了，停止'))
                    if S.p - S.start < S.k else f"窗口长 `{S.p - S.start}` 已到 k，停止扩张"),
        'p += 1': lambda S, B, r: (f'`colors[p]` 与前一块不同，窗口右扩：`p` → {S.p}' if S._line == 11 else f'`p` 跟着挪到 {S.p}，准备检测下一段'),
        'if p - start == k': lambda S, B, r: (f"窗口长 `{S.p - S.start}`" + (' == k → ==找到一个交替组==' if S.p - S.start == S.k else ' < k：中途遇到相同颜色，这段起点都不行')),
        'res += 1': '`res` → =={res}==',
        'while start + 1 < n and': lambda S, B, r: ('`colors[p]` 与前一块不同 → 窗口整体右移一格也是交替组' if S.start + 1 < S.n and S.colors[S.p] != S.colors[S.p - 1] else '右移不下去了（撞到相同颜色或到头）'),
        'start += 1': '窗口左端右移：`start` → {start}',
        'if start < n': '起点还在范围内就从断点重新开始',
        'start = p': '交替在 `p-1` 与 `p` 处断开，包含这两块的窗口都不行 → `start = p` = {start}',
        'return res': '共 `{res}` 个交替组',
    },
    cards=dict(
        one_liner='把环复制成两份变线性，start 和 p 找交替窗口',
        complexity='时间 `O(n)`，空间 `O(n)`（复制数组）',
        problem=['0/1 数组 `colors` 围成环，连续 `k` 块颜色交替算一个交替组',
                 '求交替组个数',
                 '本视频：`[0,1,0,0,1,0,1], k = 4`'],
        quote='方便起见，现将colors原样复制一份，这样一来就就环形问题转化成了线性问题。使用一个变量start表示当前交替组的起点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `p` 从 `start+1` 往后扩，直到长度为 `k` 或撞到相同颜色',
              '撞到相同颜色：窗口里所有起点都不行 → `start` 直接跳到 `p`',
              '凑满 `k` 后，只要下一块颜色不同，窗口右移一格再得一个'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`start` 要小于 `n`，否则会重复统计复制出来的那份',
                 '易错：撞到相同颜色时 `start = p`，不是 `start + 1`',
                 '和灵神的 `cnt` 计数相比，这里显式维护起点与右端点两个指针',
                 '原文本身已是 Python 3 可运行，未做改动'],
    ),
)
