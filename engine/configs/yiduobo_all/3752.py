CONFIG = dict(
    num=3752, title='字典序最小和为目标值且绝对值是排列的数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶判断 + 从大到小凑 diff',
    tags=['灵神题单·贪心与思维', '难度分 1827'],
    code='''
class Solution(object):
    def lexSmallestNegatedPerm(self, n, target):
        
        s = (1 + n) * n // 2
        if target < -s or target > s:
            return []
        
        diff = s - target
        if diff % 2 == 1:
            return []
        
        diff //= 2
        part1 = []
        part2 = []
        for v in range(n, 0, -1):
            if diff >= v:
                part1.append(-v)
                diff -= v
            else:
                part2.append(v)
        
        return part1 + part2[::-1]
''',
    call='Solution().lexSmallestNegatedPerm(5, 1)',
    expect=[-5, -2, 1, 3, 4],
    views=[
        dict(type='text', size=26, fn=lambda S: (
            f"`s = {S['s']}`" + (f"，`diff = {S['diff']}`（还要凑的负数绝对值之和）" if 'diff' in S else '')) if 's' in S else ''),
        dict(type='array', var='part1', label='part1：取负的数（从大到小）', cell=96, h=160,
             color=lambda S, i, v: 'blue'),
        dict(type='array', var='part2', label='part2：不取负的数（从大到小，最后反转）', cell=96, h=160,
             color=lambda S, i, v: 'pink'),
        dict(type='text', size=26, fn=lambda S: f"当前 `v = {S['v']}`：`diff = {S['diff']}` {'≥' if S['diff'] >= S['v'] else '<'} `{S['v']}`" if 'v' in S and 'part2' in S else ''),
    ],
    watch=['s', 'diff', 'v'],
    captions={
        's = (1': '`s = 1+2+…+n = {s}`：全取正数时的和',
        'if target < -s': lambda S, B, r: (f'`target = {S.target}` 超出 `[-{S.s}, {S.s}]` → 无解' if S.target < -S.s or S.target > S.s
                                           else f'`target = {S.target}` 在 `[-{S.s}, {S.s}]` 内，继续'),
        'diff = s - target': '`diff = s - target = {diff}`：要从 s 里减掉的量',
        'if diff % 2': lambda S, B, r: ('`diff` 是奇数：取反一个 `x` 恰好减 `2x`，奇偶性不变 → 无解' if S.diff % 2 == 1
                                        else '`diff` 是偶数：取反一个 `x` 减 `2x`，所以可能有解'),
        'diff //= 2': '取反 `x` 等于减 `2x` → 只要凑出一些数，和为 `diff // 2 = {diff}`',
        'part1 = []': '`part1` 放取负的数，会排在答案头部',
        'part2 = []': '`part2` 放不取负的数，排在答案尾部',
        'for v in': '从大到小枚举 `v`：优先让大的数取负，开头才最小',
        'if diff >= v': lambda S, B, r: (f'`diff = {S.diff} ≥ v = {S.v}` → ==先取 {S.v}==，问题变成 `1..{S.v - 1}` 凑 `{S.diff - S.v}`' if S.diff >= S.v
                                         else f'`diff = {S.diff} < v = {S.v}` → {S.v} 取不了，留作正数'),
        'part1.append': '`-{v}` 加入 `part1`',
        'diff -= v': '`diff` 变成 `{diff}`',
        'part2.append': '`{v}` 加入 `part2`（正数）',
        'return part1': '负数在前 + 正数从小到大 = `{part1}` + `{part2[::-1]}`',
    },
    cards=dict(
        one_liner='先判奇偶凑出 diff，大的数优先取负',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给正整数 `n` 和整数 `target`，把 `1..n` 排成数组并给部分数加负号',
                 '要求和等于 `target`，字典序最小；无解返回 `[]`',
                 '本视频：`n = 5, target = 1` → `[-5,-2,1,3,4]`'],
        quote='优先让较大的数取相反数，然后将所有的负数按从小到大的顺序放在答案的头部，将其他元素按照从小到大的顺序放在答案的尾部，这样一来才能使得字典序最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['全取正和为 `s`；一个元素 `x` 取反，相当于从 `s` 中减去 `2x`',
              '所以 `s - target` 必须是偶数，要凑出的数之和 `diff // 2`',
              '从 `v = n` 往下：`diff >= v` 就取 `v`，否则 `v` 留作正数；剩下的 `diff < v` 总可以直接取值为 `diff` 的数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '无解：`target` 超出 `[-s, s]`，或 `s - target` 为奇数',
                 'part2 是从大到小加入的，最后用 `part2[::-1]` 反转',
                 '对比灵神：灵神用左右两个指针原地填数组，yiduobo 用两个列表再拼接'],
    ),
)
