
def _color(S, i, v):
    if 'right' not in S or 'left' not in S or S['right'] >= len(S['prizePositions']) or S['left'] > S['right']:
        return None
    if S['left'] <= i <= S['right']:
        return 'pink'
    if i < S['left'] and S['f'][i] > 0:
        return 'blue'
    return None


CONFIG = dict(
    num=2555, title='两个线段获得的最多奖品', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长窗口 + 前缀最大 f[]',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·常用数据结构', '难度分 2081'],
    code='''
class Solution(object):
    def maximizeWin(self, prizePositions, k):

        n = len(prizePositions)
        f = [0] * n

        left = right = 0
        res = 0
        while right < n:
            while prizePositions[right] - prizePositions[left] > k:
                left += 1
            
            now = right - left + 1
            if left > 0:
                now += f[left - 1]
            
            res = max(res, now)
            f[right] = right - left + 1
            if right > 0 and f[right] < f[right - 1]:
                f[right] = f[right - 1]
            right += 1
        
        return res
''',
    call='Solution().maximizeWin([1,1,2,4,5,8,9], 1)',
    expect=5,
    views=[
        dict(type='array', var='prizePositions', h=250, label='prizePositions（粉 = 当前窗口，蓝 = 窗口左边已算 f 的奖品）',
             pointers={'left': 'blue', 'right': 'pink'}, color=_color, cell=100),
        dict(type='array', var='f', h=200, label='f[i]：右端 <= 第 i 个奖品的单条线段，最多覆盖几个', cell=100,
             color=lambda S, i, v: 'cyan' if 'left' in S and i == S['left'] - 1 else None),
        dict(type='text', h=80, size=28, fn=lambda S: ((f"窗口 {S['right'] - S['left'] + 1} 个 + f[{S['left'] - 1}] = {S['f'][S['left'] - 1]}" if S['left'] > 0 else f"窗口 {S['right'] - S['left'] + 1} 个，左边没有奖品")
                                                         if 'left' in S and 'right' in S and S['right'] < len(S['f']) else '')),
    ],
    skip=['right += 1', 'left += 1', 'while right < n'],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'now', ('res', 'res', 'green')],
    captions={
        'f = [0] * n': '`f[i]`：线段右端不超过第 `i` 个奖品时，单条线段最多覆盖几个',
        'left = right = 0': '窗口 `[left, right]`：以 `prizePositions[right]` 为右边界的线段覆盖的奖品',
        'while right < n': '`right` 从左到右当作第二条线段的右边界',
        'while prizePositions[right] - prizePositions[left] > k': lambda S, B, r: (f'`{S.prizePositions[S.right]} − {S.prizePositions[S.left]} = {S.prizePositions[S.right] - S.prizePositions[S.left]} > k`：长度超了 → `left` 右移一格' if S.prizePositions[S.right] - S.prizePositions[S.left] > S.k
                                                                                    else f'`{S.prizePositions[S.right]} − {S.prizePositions[S.left]} = {S.prizePositions[S.right] - S.prizePositions[S.left]} <= k`：窗口合法'),
        'left += 1': '`left` → {left}',
        'now = right - left + 1': '当前窗口覆盖 `{right} − {left} + 1` = =={now}== 个',
        'if left > 0': lambda S, B, r: ('窗口左边还有奖品：再加上它们能拿到的最多个数' if S.left > 0 else '`left = 0`，左边没有奖品，第一条线段拿不到'),
        'now += f[left - 1]': '加上第一条线段最多覆盖 `f[{left - 1}] = {f[left - 1]}` → `now` = =={now}==（保证两条不相交）',
        'res = max': '`res = max({B.res}, {now}) = {res}`',
        'f[right] = right - left + 1': '`f[{right}]` 先取当前窗口 `{right - left + 1}`',
        'if right > 0 and f[right] <': lambda S, B, r: (f'`f[{S.right}] = {S.f[S.right]} < f[{S.right - 1}] = {S.f[S.right - 1]}`：前缀最大不能变小' if S.right > 0 and S.f[S.right] < S.f[S.right - 1]
                                                       else '不比前一个小，`f[right]` 保持'),
        'f[right] = f[right - 1]': '`f[{right}]` 取 `f[{right - 1}]` = =={f[right]}==',
        'right += 1': '`right` → {right}',
        'return res': '两条线段最多覆盖 =={res}== 个奖品',
    },
    cards=dict(
        one_liner='两条线段不相交最好：窗口个数 + 窗口左边的最优单线段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数轴上有一些奖品（位置有序），选两条长为 `k` 的线段，可以相交', '求最多能覆盖多少个奖品',
                 '原题示例 `[1,1,2,2,3,3,5]`，`k=2` → `7`', '本视频：`[1,1,2,4,5,8,9]`，`k=1` → `5`'],
        quote='对于一个以prizePositions[right]为右边界的窗口，设其包含的最左侧的奖品的下标为left，那么在这里只需要知道所有右边界在prizePositions[0]到prizePositions[left - 1]的窗口中，最多包含了多少奖品',
        quote_src='—— yiduobo 题解原文',
        idea=['`right` 为右边界的窗口是第二条线段，窗口大小 `right − left + 1`',
              '第一条线段只看 `left` 左边：`f[left − 1]`，这样一定不相交',
              '`f[right] = max(f[right − 1], 窗口大小)`，是个动态规划'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`left = 0` 时没有 `f[left − 1]`，要先判断',
                 '`f` 必须取前缀最大，否则左边的最优窗口会被漏掉',
                 '没有「2k+1 覆盖全部就返回 n」的优化，但结果一致',
                 '对比灵神：灵神枚举中间点用常数空间，这里存 `f[]` 数组'],
    ),
)
