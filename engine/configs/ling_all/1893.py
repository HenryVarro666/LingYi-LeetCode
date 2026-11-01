CONFIG = dict(
    num=1893, title='检查是否区域内所有整数都被覆盖', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='一维差分 + 前缀和（Go 原文转写）',
    tags=['灵神题单', '常用数据结构', '难度分 1307'],
    code='''
class Solution:
    def isCovered(self, a: List[List[int]], l: int, r: int) -> bool:
        d = [0] * 52
        for p in a:
            d[p[0]] += 1
            d[p[1] + 1] -= 1
        s = 0
        for v in d[:l]:
            s += v
        for v in d[l:r + 1]:
            s += v
            if s == 0:
                return False
        return True
''',
    call='Solution().isCovered([[1,2],[3,4],[5,6]], 2, 5)',
    expect=True,
    snap_maxlen=9,
    views=[
        dict(type='text', fn=lambda S: ('差分数组 `d`：区间 `[x, y]` → `d[x] += 1`，`d[y+1] -= 1`；前缀和 `s` = 该点被覆盖的次数' if 'v' not in S and 's' not in S else f"前缀和 `s` = 当前点被几个区间覆盖 = =={S['s']}==" if 's' in S else '')),
        dict(type='array', var='d', label='d（只画前 9 项）', pointers={}, h=260,
             color=lambda S, i, v: 'green' if v > 0 else ('pink' if v < 0 else None)),
        dict(type='array', var='a', label='区间 a', h=140, cell=150),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'p', 'v', ('s', 's', 'green')],
    captions={
        'd = [0] * 52': '差分数组 `d`，下标最大到 `50 + 1`，开 52 个格子',
        'd[p[0]] += 1': '区间 `{p}` 的左端点：`d[{p[0]}]` 加 1，表示从这里开始多了一个区间',
        'd[p[1] + 1] -= 1': '区间 `{p}` 右端点的下一个位置：`d[{p[1]+1}]` 减 1，表示这里起不再被它覆盖',
        's = 0': '`s` 用来累加前缀和',
        'for v in d[:l]': '先把 `l` 之前的差分全部加起来，得到点 `l-1` 处被覆盖的次数',
        'for v in d[l:r + 1]': '再逐个看 `[l, r]` 内的每个点',
        'if s == 0': lambda S, B, r_: (f"`s = {S['s']} == 0` → 这个点没人覆盖，返回 False" if S['s'] == 0 else f"`s = {S['s']} > 0` → 这个点被覆盖，继续看下一个"),
        9: '`s += {v}` → `s = {s}`：累加 `l` 之前的差分',
        11: '`s += {v}` → `s = {s}`：这就是 `[l, r]` 内当前这个点被覆盖的次数',
        'return True': '`[l, r]` 内每个点的覆盖次数都大于 0 → 返回 True',
        'return False': '有点没被覆盖 → 返回 False',
    },
    cards=dict(
        one_liner='差分数组一加，前缀和就是每个点被覆盖几次',
        complexity='时间 `O(n + r)`，空间 `O(1)`（数组大小固定 52）',
        problem=['给若干闭区间 `ranges`，判断 `[left, right]` 内每个整数是否都被至少一个区间覆盖',
                 '示例：`[[1,2],[3,4],[5,6]]`，`left=2, right=5` → `True`'],
        quote='func isCovered(a [][]int, l, r int) bool { d := [52]int{} ... d[p[0]]++ ; d[p[1]+1]-- ...',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['区间 `[x, y]`：在 `d[x]` 加 1，在 `d[y+1]` 减 1',
              '对 `d` 求前缀和，第 `i` 项就是点 `i` 被覆盖的次数',
              '先累加到 `l` 之前，再检查 `[l, r]` 内每个前缀和是否为 0'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n + r)`，空间 `O(1)`',
                 '`d[p[1] + 1]`：右端点是闭的，所以减在 `y+1`，数组要多开一格',
                 '`for v in d[:l]` 要先累加 `l` 之前的所有差分，不能直接从 `l` 开始',
                 '同类题：1094 拼车、1109 航班预订统计'],
    ),
)
