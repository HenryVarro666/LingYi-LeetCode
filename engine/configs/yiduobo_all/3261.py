def _q(S):
    return 'start' in S


CONFIG = dict(
    num=3261, title='统计满足 K 约束的子字符串数量 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='left_bound 单调 + 前缀和 + 二分分界点',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2659'],
    code='''
class Solution(object):
    def countKConstraintSubstrings(self, s, k, queries):

        length = []
        left_bound = []

        p = 0
        one = 0
        zero = 0
        for index, char in enumerate(s):
            if char == '1':
                one += 1
            else:
                zero += 1
            
            while one > k and zero > k:
                if s[p] == '0':
                    zero -= 1
                else:
                    one -= 1
                p += 1
            
            left_bound.append(p)
            length.append(index - p + 1)

        sum_of_length = []
        for index in range(len(s)):
            if index == 0:
                sum_of_length.append(length[0])
            else:
                sum_of_length.append(sum_of_length[-1] + length[index])

        res = []
        for start, end in queries:
            left = start
            right = end
            while left < right:
                mid = (left + right + 1) // 2
                if left_bound[mid] >= start:
                    right = mid - 1
                else:
                    left = mid
                
            res.append(sum_of_length[end] - sum_of_length[left] + (1 + left - start + 1) * (left - start + 1) // 2)
        

        return res
''',
    call='Solution().countKConstraintSubstrings("0101", 1, [[0,3],[1,2]])',
    expect=[9, 3],
    views=[
        dict(type='string', var='s', label='s（框：滑窗 [p, index]；查询阶段为 [start, end]）', cell=64, h=250,
             pointers={'index': 'blue', 'p': 'pink'},
             window=(lambda S: S['start'] if _q(S) else S.get('p', 0), lambda S: S['end'] if _q(S) else S.get('index', 0))),
        dict(type='array', var='left_bound', label='left_bound[i]：以 i 为右边界时最小的合法左边界（单调不减）', cell=64, h=140,
                          color=lambda S, i, v: 'yellow' if _q(S) and i == S.get('left') else None),
        dict(type='array', var='length', label='length[i] = i - left_bound[i] + 1', cell=64, h=120),
        dict(type='array', var='sum_of_length', label='sum_of_length（length 的前缀和）', cell=64, h=120),
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"查询 `[{S['start']}, {S['end']}]`：二分区间 [{S['left']}, {S['right']}]，找分界点 p（之后 `left_bound ≥ {S['start']}`）"
                           if _q(S) and 'right' in S else
                           (f"1 的个数 {S['one']}，0 的个数 {S['zero']}，k = {S['k']}" if 'one' in S and 'start' not in S and S['_line'] < 26 else ''))),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('left', 'left', 'yellow'), ('right', 'right', 'cyan'), ('res', 'res', 'green')],
    captions={
        'length = []': '`length[i]`：以 `i` 为终点的合法子串个数；`left_bound[i]`：对应的最小起点',
        'p = 0': '`p` 是滑窗左边界，`one`、`zero` 统计窗口里 1 和 0 的个数',
        'if char ==': '`{char}` 进入窗口',
        'one += 1': '`one` = {one}',
        'zero += 1': '`zero` = {zero}',
        'while one > k': lambda S, B, r: (f'`one = {S.one}`、`zero = {S.zero}` 都 `> k = {S.k}` → ==窗口不满足 k 约束==，左边界右移'
                                          if S.one > S.k and S.zero > S.k else f'`one = {S.one}`、`zero = {S.zero}`，至少一个 `≤ {S.k}` → 窗口合法'),
        'if s[p] ==': '移出左边界字符 `s[{p}] = {s[p]}`',
        'zero -= 1': '`zero` → {zero}',
        'one -= 1': '`one` → {one}',
        'p += 1': '`p` → {p}',
        'left_bound.append': '`left_bound[{index}] = {p}`，且右端点为 {index} 时合法起点有 `{index} - {p} + 1` = =={index - p + 1}== 个',
        'length.append': '`length[{index}] = {length[index]}`',
        'sum_of_length.append(length[0])': '前缀和从 `length[0]` 开始',
        'sum_of_length[-1] + length[index]': '`sum_of_length[{index}] = {sum_of_length[-1]}`',
        'for start, end in queries': lambda S, B, r: (f'查询 `[{S.start}, {S.end}]`：要数起点终点都在其中的 k 约束子串' if len(S.res) < len(S.queries) else '查询全部处理完'),
        'left = start': '找分界点 `p`：终点 `≤ p` 时合法起点被 `start` 截断，终点 `> p` 时不受影响。在 `[start, end]` 上二分',
        'mid = (left': '`mid = ({left} + {right} + 1) // 2` = =={mid}==，看 `left_bound[{mid}] = {left_bound[mid]}`',
        'if left_bound[mid] >= start': lambda S, B, r: (
            f'`left_bound[{S.mid}] = {S.left_bound[S.mid]} ≥ start = {S.start}`：终点 {S.mid} 的合法起点不会被 start 截断 → 它属于后半，==p 要更小==，`right = mid - 1`' if S.left_bound[S.mid] >= S.start
            else f'`left_bound[{S.mid}] = {S.left_bound[S.mid]} < start = {S.start}`：合法起点比 start 还靠左，被 start 截断 → 属于前半，==p 至少是 mid==，`left = mid`'),
        'right = mid - 1': '`right` → {right}',
        'left = mid': '`left` → {left}',
        'res.append': lambda S, B, r: (f'分界点 `p = {S.left}`：终点在 `[start, p]` 内，`left_bound ≤ start`，共 `{S.left - S.start + 2} × {S.left - S.start + 1} / 2` = '
                                       f'`{(1 + S.left - S.start + 1) * (S.left - S.start + 1) // 2}` 个；终点在 `(p, end]` 内用前缀和 '
                                       f'`{S.sum_of_length[S.end]} − {S.sum_of_length[S.left]}` = `{S.sum_of_length[S.end] - S.sum_of_length[S.left]}` → ==这次答案 {S.res[-1]}=='),
        'return res': '全部查询答案：`{res}`',
    },
    skip=['length = []', 'left_bound = []', 'sum_of_length = []', 'one = 0', 'zero = 0', 'zero += 1', 'one += 1', 'zero -= 1', 'one -= 1', 'p += 1',
          'if index == 0', 'for index in range(len(s))', 'right = mid - 1', 'left = mid'],
    max_steps=70,
    cards=dict(
        one_liner='left_bound 单调不减：二分出分界点，前半用公式，后半用前缀和',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['二进制串 `s`，0 的个数 ≤ k 或 1 的个数 ≤ k 的子串叫 k 约束子串',
                 '每个查询 `[start, end]`：数起点终点都在其中的 k 约束子串个数',
                 '本视频：`s="0101", k=1, queries=[[0,3],[1,2]]`'],
        quote='因为是基于单调性使用变长滑动窗口计算出来的，因此其一定是单调不减的，这一点后续可以利用上来。',
        quote_src='—— yiduobo 题解原文',
        idea=['先滑窗得到 `left_bound[index]`，并记 `length[index] = index - left_bound[index] + 1`，再做前缀和',
              '按终点拆解：`left_bound[index] ≤ start` 时贡献 `index - start + 1`，否则贡献 `length[index]`',
              '`left_bound` 单调 → 在 `[start, end]` 二分分界点 `p`；前半是等差和，后半是 `sum_of_length` 的区间和'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '二分 `mid` 向上取整，因为分支里是 `left = mid`；找的是最后一个 `left_bound ≤ start` 的位置',
                 '代码里判断用 `left_bound[mid] >= start`；相等时两种公式结果一样，所以不影响答案',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神预处理 `right[l]` 直接定位分界点，无需二分，查询 `O(1)`'],
    ),
)
