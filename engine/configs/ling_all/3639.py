def _star(S, i):
    """check 里 i 是否已被标成星号"""
    st, m = S.get('star'), S.get('m')
    if st is None or m is None or 'order' not in S:
        return False
    if S.get('_inner', {}).get('m') is None:
        return False
    return st[i] == m


def _in_check(S):
    return 'star' in S and S.get('_inner', {}).get('m') is not None and 'cnt' in S.get('_inner', {})


def _txt(S):
    inn = S.get('_inner', {})
    if 'cnt' in inn:
        n = len(S['s'])
        return f"每个右端点 `i` 贡献 `last + 1` 个有效子串：累计 `cnt = {inn['cnt']}`，目标 `k = {S['k']}`"
    if 'm' in inn:
        return f"试 `t = {inn['m'] - 1}`：把 `order` 前 `{inn['m']}` 个位置改成星号"
    if 'left' in S and 'right' in S and 'm' not in inn:
        return f"开区间 `({S['left']}, {S['right']})`：答案在 `right` 或更左（`right` 一定满足）"
    return f"总共 `{len(S['s'])}` 个字符，全是星号时有 `n(n+1)/2` 个有效子串"


def _color(S, i, v):
    if _in_check(S) and _star(S, i):
        return 'yellow'
    return None


CONFIG = dict(
    num=3639, title='变为活跃状态的最小时间', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 枚举右端点计数',
    tags=['二分答案', '求最小', '逆向思维', '难度分 1853'],
    code='''
class Solution:
    def minTime(self, s: str, order: List[int], k: int) -> int:
        n = len(s)
        if n * (n + 1) // 2 < k:
            return -1

        star = [0] * n  # 避免在二分内部反复创建/初始化列表

        def check(m: int) -> bool:
            m += 1
            for j in range(m):
                star[order[j]] = m
            cnt = 0
            last = -1  # 上一个 '*' 的位置
            for i, x in enumerate(star):
                if x == m:  # s[i] 是 '*'
                    last = i
                cnt += last + 1
                if cnt >= k:  # 提前退出循环
                    return True
            return False

        left, right = -1, n - 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call='Solution().minTime("abcd", [2,0,3,1], 9)',
    expect=2,
    skip=['for j in range(m)', 'star[order[j]] = m', 'last = i', 'cnt = 0', 'for i, x in enumerate(star)'],
    views=[
        dict(type='text', size=24, fn=_txt),
        dict(type='string', var='s', label='s（黄 = 当前试探时已变成 * 的位置）', h=250,
             pointers={'i': 'blue', 'last': 'pink'}, color=_color),
        dict(type='array', var='order', label='order（下标 = 时间 t；left / mid / right 在时间轴上二分）', h=270,
             pointers={'left': 'cyan', 'mid': 'yellow', 'right': 'orange'}),
    ],
    watch=[('left', 'left', 'cyan'), ('mid', 'mid', 'yellow'), ('right', 'right', 'orange'),
           ('cnt', 'cnt', 'green'), ('last', 'last', 'pink')],
    captions={
        'if n * (n + 1) // 2 < k': lambda S, B, r: f"全改成星号也只有 `n(n+1)/2 = {len(S.s) * (len(S.s) + 1) // 2}` 个有效子串；`k = {S.k}` " +
                                                  ('更大 → 返回 -1' if len(S.s) * (len(S.s) + 1) // 2 < S.k else '不更大 → 一定有解'),
        'star = [0] * n': '`star[i] = m` 表示 `s[i]` 在本次试探里是星号；用整数标记，==不必每次重新初始化==',
        'm += 1': '试探 `t = {m - 1}`：令 `m = {m}`，把 `order` 前 `{m}` 个位置 `{order[:m]}` 在 `star` 里标成 `{m}`（星号）',
        'star[order[j]] = m': '把 `order[{j}] = {order[j]}` 这个位置标成星号',
        'last = -1': '`cnt = 0` 开始数有效子串：枚举==右端点== `i`；`last` = 最近一个星号的下标，初始 `-1`',
        'if x == m': lambda S, B, r: (f"`star[{S.i}] = {S.x}` == `{S.m}` → `s[{S.i}]` 是 ==星号==，`last = {S.i}`" if S.x == S.m
                                      else f"`s[{S.i}]` 不是星号，`last` 仍是 `{S.last}`"),
        'cnt += last + 1': '右端点 `{i}`：左端点可取 `0..last`，共 `last + 1 = {last + 1}` 个有效子串 → `cnt = {cnt}`',
        'if cnt >= k': lambda S, B, r: (f"`cnt = {S.cnt}` >= `k = {S.k}` → 够了，提前返回 ==True==" if S.cnt >= S.k
                                        else f"`cnt = {S.cnt}` < `k = {S.k}` → 还不够，继续"),
        'return True': '这个时间点已满足 → `check` 为 True，答案 `<= t`',
        'return False': '数完所有右端点还是不够 → `check` 为 False，答案 `> t`',
        'left, right = -1, n - 1': '开区间 `({left}, {right})`：`left = -1` 一定不满足（没星号），`right = n − 1` 一定满足（已特判）',
        'while left + 1 < right': lambda S, B, r: (f'`left + 1 = {S.left + 1} < right = {S.right}`：开区间里还有候选，继续二分' if S.left + 1 < S.right
                                                  else f'开区间里没有数了：答案就是 `right = {S.right}`'),
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`：试 `t = {mid}`',
        'if check(mid)': '调用 `check({mid})`：时间 `{mid}` 时，有效子串够 `k = {k}` 个吗？',
        'right = mid': '`check({mid})` 为 True：答案 `<= {mid}`，更新的是 `right` → `{right}`',
        'left = mid': '`check({mid})` 为 False：答案 `> {mid}`，更新的是 `left` → `{left}`',
        'return right': '开区间二分：`check(mid) == true` 时更新的是谁就返回谁 → 答案 =={right}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='时间越大星号越多、有效子串越多：对时间二分，每次 O(n) 数子串',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`order` 是排列，时刻 `t` 把 `s[order[t]]` 换成 `*`；含至少一个 `*` 的子串称为有效',
                 '有效子串数 `>= k` 时字符串「活跃」，求最小活跃时间，不可能返回 `-1`',
                 '示例：`s="abc", order=[1,0,2], k=2` → `0`',
                 '本视频：`s="abcd", order=[2,0,3,1], k=9` → `2`'],
        quote='由于答案（时间）越大，s 中的星号越多，有效子串越多，越能够 ≥ k；反之则越无法 ≥ k。据此，可以二分猜答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`check(m)`：前 `m + 1` 个时刻改成星号，数有效子串是否 `>= k`',
              '枚举==右端点== `i`，维护最近星号 `last`，左端点 `0..last` 都有效 → 加 `last + 1`',
              '开区间二分：`left = -1`（一定不行），`right = n − 1`（一定可以）'],
        after=[dict(heading='灵神的另一种写法：逆向 + 链表', lines=[
            '从全是星号倒着还原：每还原一个 `i`，失去 `(i − L)(R − i)` 个有效子串',
            '`L / R` 是左右最近的星号，用数组模拟双向链表删除节点，总共 `O(n)`',
        ])],
        summary=['时间 `O(n log n)`，空间 `O(n)`；先特判 `n(n+1)/2 < k` 返回 `-1`',
                 '二分里不能直接改 `s`：用 `star[i] = m` 的整数标记，省去反复初始化',
                 '易错：`m += 1` 后才是「改了几个」；`cnt` 提前退出可以省时间',
                 '开区间写法：`check(mid)` 为真更新 `right`，最后返回 `right`'],
    ),
)
