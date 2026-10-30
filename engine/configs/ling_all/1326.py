def _txt(S):
    if 'cur_right' not in S:
        return ''
    return f"已建造的桥右端 `cur_right = {S['cur_right']}`　　下一座桥最远能到 `next_right = {S['next_right']}`　　已造 `ans = {S['ans']}`"


def _color(S, i, v):
    if 'cur_right' not in S or 'i' not in S:
        return None
    if i == S['i']:
        return 'yellow'
    return None


def _if_cur(S, B, ret):
    if S.i == S.cur_right:
        return f'`i = {S.i}` == `cur_right = {S.cur_right}`：==走到已建桥的右端点==，必须再造一座桥才能继续'
    return f'`i = {S.i}` < `cur_right = {S.cur_right}`：还在已建的桥上，不用造新桥，只记录能到的最远处'


CONFIG = dict(
    num=1326, title='灌溉花园的最少水龙头数目', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='造桥式贪心 · 区间覆盖', tags=['贪心算法', '区间贪心', '难度分 1885'],
    code='''
class Solution:
    def minTaps(self, n: int, ranges: List[int]) -> int:
        right_most = [0] * (n + 1)
        for i, r in enumerate(ranges):
            left = max(i - r, 0)
            right_most[left] = max(right_most[left], i + r)

        ans = 0
        cur_right = 0  # 已建造的桥的右端点
        next_right = 0  # 下一座桥的右端点的最大值
        for i in range(n):  # 如果走到 n-1 时没有返回 -1，那么必然可以到达 n
            next_right = max(next_right, right_most[i])
            if i == cur_right:  # 到达已建造的桥的右端点
                if i == next_right:  # 无论怎么造桥，都无法从 i 到 i+1
                    return -1
                cur_right = next_right  # 造一座桥
                ans += 1
        return ans
''',
    call='Solution().minTaps(6, [1, 2, 1, 0, 2, 1, 0])',
    expect=2,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='ranges', pointers={'i': 'yellow'}, label='ranges[i]：水龙头 i 的灌溉半径', h=200),
        dict(type='array', var='right_most', pointers={'i': 'yellow', 'cur_right': 'blue', 'next_right': 'pink'},
             label='right_most[x]：左端点为 x 的所有区间中，最远能到的右端点', h=260, color=_color),
    ],
    watch=[('i', 'i', 'yellow'), ('cur_right', 'cur_right', 'blue'), ('next_right', 'next_right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'right_most = [0]': '`right_most[x]` 记录：左端点为 `x` 的水龙头，最远能灌溉到哪里',
        'for i, r in enumerate': lambda S, B, r_: ('所有水龙头处理完毕，`right_most` 建好' if B.get('i') == S.i and 'i' in B else f'水龙头 `{S.i}`，半径 `{S.r}`'),
        'left = max': '水龙头 `{i}` 灌溉区间 `[{i} - {r}, {i} + {r}]`，左端点 `max({i - r}, 0) = {left}`（花园从 0 开始）',
        'right_most[left] = max': '`right_most[{left}] = max({B.right_most[left]}, {i + r}) = {right_most[left]}`：同一左端点只留最远的右端点',
        'ans = 0': '`ans` = 造桥（打开水龙头）的数量',
        'cur_right = 0': '`cur_right`：目前已经铺到的位置',
        'next_right = 0': '`next_right`：再造一座桥最远能铺到的位置',
        'for i in range(n)': lambda S, B, r_: (f'从位置 `{S.i}` 往右走一步，检查能否继续' if S.i < S.n and (B.get('i') is None or B.get('i') != S.i or S.i == 0) else '走完 `0..n-1`，一路没卡住 → 必然到达 n'),
        'next_right = max': '以 `{i}` 为左端点的区间最远到 `{right_most[i]}` → `next_right = max({B.next_right}, {right_most[i]}) = {next_right}`',
        'if i == cur_right': _if_cur,
        'if i == next_right': lambda S, B, r_: (f'`i = {S.i}` == `next_right = {S.next_right}`：==没有任何区间能越过 {S.i}==，覆盖不了 → 返回 -1' if S.i == S.next_right else f'`next_right = {S.next_right}` > `i = {S.i}`：有区间能继续往右'),
        'cur_right = next_right': '造一座桥：`cur_right` 推到 =={cur_right}==（选 `next_right` 对应的那个区间）',
        'ans += 1': '`ans = {ans}`',
        'return ans': '最少需要 `{ret}` 个水龙头',
    },
    cards=dict(
        one_liner='把区间覆盖看成“造桥”：走到桥头才造，造最远的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n + 1` 个水龙头在 `0..n`，水龙头 `i` 能灌溉 `[i - ranges[i], i + ranges[i]]`',
                 '求灌溉整个花园 `[0, n]` 的最少水龙头数，覆盖不了返回 `-1`',
                 '整个花园包含小数位置，所以示例 `[0,0,0,0]` 是 `-1`',
                 '本视频：`n = 6, ranges = [1,2,1,0,2,1,0]` → `2`'],
        quote='无论怎么造桥，都无法从 i 到 i+1。……如果走到 n-1 时没有返回 -1，那么必然可以到达 n。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先预处理 `right_most[left]`：左端点为 `left` 的区间，右端点最远是多少',
              '从左往右走，一边更新 `next_right`（下一座桥最远能到哪）',
              '只有走到 `cur_right`（桥头）才必须造桥；此时若 `next_right` 还是 `i`，就走不下去 → `-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '左端点要 `max(i - r, 0)`，否则下标越界',
                 '不用初始化 `right_most[i] = i`：能走到 `i` 时 `next_right >= i`，不影响结果',
                 '循环到 `n - 1` 即可：没返回 -1 就一定能到 n',
                 '同类题：45. 跳跃游戏 II、1024. 视频拼接'],
    ),
)
