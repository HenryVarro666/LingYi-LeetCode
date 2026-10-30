def _txt(S):
    if 'p' not in S or 's' not in S:
        return ''
    p, n = S['p'], len(S['p'])
    i = S.get('i')
    if S['_line'] >= 12 and isinstance(i, int) and 1 <= i < n:
        return f"`s += (2×{i} − {n}) × ({p[i]} − {p[i-1]})` = =={S['s']}=="
    return f"这组位置 `p = {p}`，第一个元素的间隔和 `s = {S['s']}`"


CONFIG = dict(
    num=2121, title='相同元素的间隔之和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='分组 + 逐个右移的变化量',
    tags=[],
    code='''
class Solution:
    def getDistances(self, arr: List[int]) -> List[int]:
        pos = defaultdict(list)
        for i, v in enumerate(arr):
            pos[v].append(i)  # 记录相同元素的位置
        ans = [0] * len(arr)
        for p in pos.values():  # 遍历每个组
            ans[p[0]] = s = sum(i - p[0] for i in p)  # 该组第一个元素的间隔和
            n = len(p)
            for i in range(1, n):
                s += (2 * i - n) * (p[i] - p[i - 1])  # 计算该组下一个元素的间隔和（考虑变化量）
                ans[p[i]] = s
        return ans
''',
    call='Solution().getDistances([2,1,3,1,2,3,3])',
    expect=[4, 2, 7, 2, 4, 4, 5],
    skip=['ans = [0]'],
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 当前这一组的元素，粉 = 正在算的元素）', cell=90, h=190,
             color=lambda S, i, v: ('pink' if S['_line'] >= 12 and 'p' in S and isinstance(S.get('i'), int) and 'n' in S and S['i'] < len(S['p']) and S['p'][S['i']] == i
                                    else 'blue' if S['_line'] >= 9 and 'p' in S and i in S['p'] else None)),
        dict(type='map', var='pos', label='pos（值 → 下标列表）', fmt=lambda k, v: f'{k}: {v}', font=30, h=190),
        dict(type='array', var='ans', label='ans（间隔和）', cell=90, h=170,
             color=lambda S, i, v: 'green' if 'p' in S and i in S['p'] and v else None),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=[('p', 'p', 'blue'), ('n', 'n'), ('i', 'i', 'pink'), ('s', 's', 'green')],
    captions={
        'pos[v].append(i)': '把下标 `{i}` 放进值 `{v}` 的组：`pos[{v}] = {pos[v]}`',
        'for p in pos.values()': '处理一组值相同的元素，位置 `p = {p}`',
        'ans[p[0]] = s': '先暴力算出组内第一个元素到其余元素的间隔和：`s = {s}`，写入 `ans[{p[0]}]`',
        'n = len(p)': '这组一共 `n = {n}` 个元素',
        'for i in range(1, n)': '向右处理这组的第 `{i}` 个元素，位置 `{p[i]}`',
        's += (2 * i': lambda S, B, r: (f'从 `{S.p[S.i-1]}` 移到 `{S.p[S.i]}`，间隔变化 `{S.p[S.i]-S.p[S.i-1]}`：左边 `{S.i}` 个变大、右边 `{S.n-S.i}` 个变小'
                                        f' → `s += (2×{S.i} − {S.n}) × {S.p[S.i]-S.p[S.i-1]}` = =={S.s}=='),
        'ans[p[i]] = s': '位置 `{p[i]}` 的间隔和就是 `{s}`',
        'return ans': '每个位置都算好了：`{ret}`',
    },
    cards=dict(
        one_liner='同组元素从左到右移动，间隔和的变化量是 (2i−n)×位置差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`intervals[i]` = `arr[i]` 与数组中每个相同元素的下标差的绝对值之和',
                 '示例：`[2,1,3,1,2,3,3]` → `[4,2,7,2,4,4,5]`',
                 '本视频用的就是这个示例'],
        quote='左边有 i 个元素的间隔变大了 p[i]-p[i-1]；右边有 n-i 个元素的间隔变小了 p[i]-p[i-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用哈希表把值相同的元素分组，记录各自的下标 `p`',
              '遍历一次 `p`，算出第一个元素到其余元素的间隔和',
              '向右移一个元素：左边 `i` 个变远、右边 `n−i` 个变近，==变化量 = (2i−n)×(p[i]−p[i−1])=='],
        summary=['时间 `O(n)`，空间 `O(n)`，每个元素只在自己的组里处理一次',
                 '易错点：变化量里的 `i` 是组内下标，不是原数组下标',
                 '组内只有一个元素时，`sum` 为 0，内层循环不执行，答案是 0',
                 '同题：2615 等值距离和'],
    ),
)
