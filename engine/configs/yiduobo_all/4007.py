CONFIG = dict(
    num=4007, title='栅栏的最宽宽度', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 单独 + 拼接',
    tags=[],
    code='''
class Solution(object):
    def maximumWidth(self, planks):
        
        single = {}
        for v in planks:
            single[v] = single.get(v, 0) + 1
        
        pair = {}
        for first in single.keys():
            for second in single.keys():
                if first > second:
                    continue
                
                s = first + second
                if first == second:
                    pair[s] = pair.get(s, 0) + single[first] // 2
                else:
                    pair[s] = pair.get(s, 0) + min(single[first], single[second])
        

        res = 0
        for final in single:
            res = max(res, single[final] + pair.get(final, 0))
        for final in pair:
            res = max(res, pair[final] + single.get(final, 0))
        
        return res
''',
    call='Solution().maximumWidth([1, 2, 3, 2, 1])',
    expect=3,
    views=[
        dict(type='array', var='planks', label='planks（木板高度）', cell=80, h=150),
        dict(type='map', var='single', label='single：高度 → 单独使用的块数', fmt=lambda k, v: f'{k}: {v}块', h=150, font=30),
        dict(type='map', var='pair', label='pair：拼接后的高度 → 拼出的块数', fmt=lambda k, v: f'{k}: {v}块', h=220, font=30),
        dict(type='text', size=28, h=70, fn=lambda S: (
            f"高度组合 `({S['first']}, {S['second']})`，拼接高度 `s = {S['first']} + {S['second']}` = =={S['first'] + S['second']}=="
            if 'first' in S and 'second' in S and 'res' not in S and S['_line'] >= 15 else
            f"候选最终高度 `{S['final']}`：单独 `{S['single'].get(S['final'], 0)}` + 拼接 `{S['pair'].get(S['final'], 0)}` 块"
            if 'final' in S else '')),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('final', 'final', 'orange'), ('res', 'res', 'green')],
    skip=['pair = {}', 'res = 0', 'single = {}', '                    continue'],
    max_steps=80,
    captions={
        'single[v] = single.get': '高度 `{v}` 又出现一块 → `single[{v}] = {single[v]}`',
        'for first in single.keys()': lambda S, B, ret: (f'第一块的高度 `first = {S.first}`' if 'first' not in B or S.first != B.first
                                                         else '拼接的组合都算完了'),
        'for second in single.keys()': lambda S, B, ret: (f'第二块的高度 `second = {S.second}`' if 'second' not in B or S.second != B.second or S.first != B.first
                                                          else f'`first = {S.first}` 的组合枚举完了'),
        'if first > second': lambda S, B, ret: (f'`first = {S.first} > second = {S.second}`：这个组合反过来已算过 → 跳过，防止重复'
                                                if S.first > S.second else
                                                f'`first = {S.first} <= second = {S.second}`：是新组合，往下算'),
        's = first + second': '拼接高度 `s = {first} + {second} = {s}`',
        'if first == second': lambda S, B, ret: (f'高度相同（都是 `{S.first}`，共 `{S.single[S.first]}` 块）→ 块与块之间两两拼接'
                                                 if S.first == S.second else
                                                 f'高度不同 → 每种各取一块拼，数量取较小的一种'),
        'single[first] // 2': '同高 `{first}` 的 `{single[first]}` 块两两拼，得 `{single[first]} // 2 = {single[first] // 2}` 块 → `pair[{s}] = {pair[s]}`',
        'min(single[first]': '`{first}` 有 `{single[first]}` 块，`{second}` 有 `{single[second]}` 块 → 取较小的 `{min(single[first], single[second])}` 块 → `pair[{s}] = {pair[s]}`',
        'res = max(res, single[final]': '高 `{final}`：单独 `{single[final]}` + 拼接 `{pair.get(final, 0)}` = `{single[final] + pair.get(final, 0)}`，`res` → `{res}`',
        'res = max(res, pair[final]': '高 `{final}`：拼接 `{pair[final]}` + 单独 `{single.get(final, 0)}` = `{pair[final] + single.get(final, 0)}`，`res` → `{res}`',
        'for final in single': lambda S, B, ret: (f'候选最终高度（原板高度）`final = {S.final}`' if 'final' not in B or S.final != B.final else '原板高度都试过了'),
        'for final in pair': lambda S, B, ret: (f'候选最终高度（拼接高度）`final = {S.final}`' if S.final != B.get('final') else '拼接高度都试过了'),
        'return res': '最宽 `{res}` 块',
    },
    cards=dict(
        one_liner='分别算出单独用、拼接用各能得到几块，再逐个高度相加',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`planks` 是木板高度，宽度都是 1；栅栏的木板必须==同高==',
                 '可以直接用原木板，或把两块不同的原木板拼成一块，高度相加',
                 '每块原木板只能用一次，不能三块拼在一起',
                 '本视频：`[1,2,3,2,1]` → `3`'],
        quote='可以分别计算单独使用以及拼接使用得到的每种高度的数目，然后取这两项之和最大的高度作为最终高度。',
        quote_src='—— yiduobo 题解原文',
        idea=['`single` 记录每种原木板高度出现几次',
              '两两遍历高度组合：高度相同拼 `总量 // 2` 块；不同则取两者较小值',
              '限定 `first <= second` 避免组合重复；最后对每个高度取 单独 + 拼接 的最大值'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`（`n` 为 `planks` 长度）',
                 '最后要==对 single 和 pair 的键各扫一遍==：有的高度只能靠拼接得到',
                 '同高度拼接是 `// 2`，别漏；不同高度取 `min`',
                 '对比灵神：灵神把 `cnt[x]` 直接记进 `cnt_pair`，最后一次 `max`；yiduobo 分开存、分开扫',
                 '原文为 Python 2 风格（`class Solution(object)`），无需修改即可在 Python 3 运行'],
    ),
)
