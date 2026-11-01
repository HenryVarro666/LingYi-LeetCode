CONFIG = dict(
    num=1889, title='装包裹的最小浪费空间', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 二分划分包裹（Go 原文转写）',
    tags=['贪心与思维', '双序列配对', '难度分 2214'],
    code='''
class Solution:
    def minWastedSpace(self, a: List[int], boxes: List[List[int]]) -> int:
        a.sort()  # 将包裹按尺寸排序，方便后面按照箱子尺寸划分包裹
        ans = inf
        for box in boxes:
            box.sort()
            if box[-1] < a[-1]:  # 最大的箱子不够装最大的包裹
                continue
            res = l = 0
            for v in box:
                # 划分包裹：当前箱子 v 可以装入下标在 [l, r) 区间内的包裹
                r = bisect_left(a, v + 1)
                res += (r - l) * v  # 统计箱子尺寸之和
                l = r
            ans = min(ans, res)
        if ans < inf:
            for v in a:
                ans -= v  # 减去每个包裹尺寸
            return ans % (10 ** 9 + 7)
        return -1
''',
    setup='from bisect import bisect_left',
    call='Solution().minWastedSpace([3,5,8,10,11,12], [[12],[11,9],[10,5,14]])',
    expect=9,
    views=[
        dict(type='array', var='a', label='包裹（已排序）', h=150,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'green' if 'l' in S and 'r' in S and S['l'] <= i < S['r'] else None),
        dict(type='array', var='box', label='当前供应商的箱子（已排序）', h=130,
             color=lambda S, i, v: 'yellow' if S.get('v') == v else None),
        dict(type='text', h=70, fn=lambda S: (f"箱子 `{S['v']}` 装下标 [{S['l']}, {S['r']}) 的包裹，箱子尺寸和累计 ==`{S['res']}`==" if 'r' in S and 'v' in S else '')),
    ],
    watch=['l', 'r', 'v', ('res', 'res', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'a.sort()': '包裹排序：这样「能装进某个箱子的包裹」是一段连续区间',
        'box.sort()': '箱子也排序，从小到大依次划分包裹：`box = {box}`',
        'if box[-1] < a[-1]': lambda S, B, r: (f'最大箱子 `{S.box[-1]}` < 最大包裹 `{S.a[-1]}` → 这个供应商装不下，换下一个' if S.box[-1] < S.a[-1] else f'最大箱子 `{S.box[-1]}` ≥ 最大包裹 `{S.a[-1]}` → 全部装得下，继续'),
        'r = bisect_left': '二分找第一个 `> {v}` 的包裹下标 `r = {r}`：包裹 [{l}, {r}) 都 ≤ {v}，都放进这个箱子',
        'res += (r - l)': '这 `{r - l}` 个箱子都用尺寸 `{v}`：`res += {r - l} × {v}` → =={res}==',
        'l = r': '下一个箱子从 `{l}` 开始接着装',
        'ans = min': '这个供应商箱子尺寸总和 `{res}`，`ans = min({B.ans}, {res}) = {ans}`',
        'ans -= v': '总浪费 = 箱子尺寸和 − 包裹尺寸和：减去包裹 `{v}` → {ans}',
        'return ans %': '浪费空间最小 `{ret}`（再对 10^9+7 取余）',
    },
    cards=dict(
        one_liner='包裹总尺寸固定，只需最小化箱子尺寸之和',
        complexity='时间 `O(n log n + M log n)`，M 为箱子总数，空间 `O(1)`',
        problem=['`n` 个包裹，每个箱子装一个；只能选一个供应商，其箱子无限多',
                 '浪费 = 箱子尺寸 − 包裹尺寸，求总浪费最小，装不下返回 `-1`',
                 '示例：`[3,5,8,10,11,12]`，`[[12],[11,9],[10,5,14]]` → `9`'],
        quote='由于包裹的尺寸之和是固定的，因此目标转换为最小化箱子的尺寸之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['包裹排序后，每个包裹装进「能装它的最小箱子」，箱子尺寸和最小',
              '箱子也排序，用二分求每个箱子能装到哪个包裹，区间 `[l, r)`',
              '最后总浪费 = 尺寸和 − 包裹尺寸和，只需在最后取一次余'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n log n + M log n)`，M 为所有箱子数之和',
                 '易错点：最大箱子装不下最大包裹要直接跳过；取余放在最后，因为要先比较真实大小',
                 '同类：双序列配对型贪心，排序后一一对应'],
    ),
)
