
def _color(S, i, v):
    if 'mid' not in S or 'left' not in S or 'right' not in S:
        return None
    if i == S['mid']:
        return 'yellow'
    if S['left'] <= i < S['mid']:
        return 'blue'
    if S['mid'] < i < S['right']:
        return 'pink'
    return None


def _txt(S):
    if 'mid' not in S or 'mx' not in S:
        return '两条线段一左一右：枚举中间的奖品 `mid`，既当第二条的左端，又当第一条的右端'
    return f"粉：第二条 {S['right'] - S['mid']} 个；蓝：第一条最多 mx = =={S['mx']}=="


CONFIG = dict(
    num=2555, title='两个线段获得的最多奖品', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举中间 + 两个滑动窗口 · mx 前缀最大',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·常用数据结构', '难度分 2081'],
    code='''
class Solution:
    def maximizeWin(self, prizePositions: List[int], k: int) -> int:
        n = len(prizePositions)
        if k * 2 + 1 >= prizePositions[-1] - prizePositions[0]:
            return n
        ans = mx = left = right = 0
        for mid, p in enumerate(prizePositions):
            # 把 prizePositions[mid] 视作第二条线段的左端点，计算第二条线段可以覆盖的最大奖品下标
            while right < n and prizePositions[right] - p <= k:
                right += 1
            # 循环结束后，right-1 是第二条线段可以覆盖的最大奖品下标
            ans = max(ans, mx + right - mid)
            # 把 prizePositions[mid] 视作第一条线段的右端点，计算第一条线段可以覆盖的最小奖品下标
            while p - prizePositions[left] > k:
                left += 1
            # 循环结束后，left 是第一条线段可以覆盖的最小奖品下标
            mx = max(mx, mid - left + 1)
        return ans
''',
    call='Solution().maximizeWin([1,1,2,5,6,9], 1)',
    expect=5,
    views=[
        dict(type='array', var='prizePositions', h=300, label='prizePositions（蓝 = 第一条线段，粉 = 第二条线段，黄 = mid）',
             pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, color=_color, cell=100),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    skip=['right += 1', 'left += 1'],
    watch=[('left', 'left', 'blue'), ('mid', 'mid', 'yellow'), ('right', 'right', 'pink'), ('mx', 'mx', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'if k * 2 + 1 >=': lambda S, B, r: ('两条线段总长 `2k+1` 够盖住所有奖品 → 直接返回 `n`' if S.k * 2 + 1 >= S.prizePositions[-1] - S.prizePositions[0]
                                           else f'`2k+1 = {S.k * 2 + 1} < {S.prizePositions[-1] - S.prizePositions[0]}`：盖不满，需要真正计算'),
        'ans = mx = left = right = 0': '`mx`：第一条线段（在 mid 左侧）最多覆盖的奖品数',
        'for mid, p in enumerate': '枚举中间奖品 `mid = {mid}`（位置 `p = {p}`）：既是第二条的左端，也是第一条的右端',
        'while right < n': lambda S, B, r: (f'`prizePositions[{S.right}] − {S.p} = {S.prizePositions[S.right] - S.p} <= k`：第二条还能盖到它 → `right` 右移一格' if S.right < S.n and S.prizePositions[S.right] - S.p <= S.k
                                            else '第二条盖不到下一个了（或到头）→ `right − 1` 是它覆盖的最远奖品'),
        'right += 1': '`right` → {right}',
        'ans = max': '第二条覆盖 `right − mid = {right - mid}` 个，加第一条 `mx = {mx}` → `ans = max({B.ans}, {mx + right - mid}) = {ans}`（先更新 ans）',
        'while p - prizePositions[left]': lambda S, B, r: (f'`{S.p} − {S.prizePositions[S.left]} = {S.p - S.prizePositions[S.left]} > k`：第一条盖不到 `left` → `left` 右移一格' if S.p - S.prizePositions[S.left] > S.k
                                                          else f'`{S.p} − {S.prizePositions[S.left]} = {S.p - S.prizePositions[S.left]} <= k`：`left` 在第一条范围内，停'),
        'left += 1': '`left` → {left}',
        'mx = max': '第一条以 mid 为右端能盖 `mid − left + 1 = {mid - left + 1}` 个 → `mx = max({B.mx}, {mid - left + 1}) = {mx}`',
        'return ans': '两条线段最多覆盖 =={ans}== 个奖品',
    },
    cards=dict(
        one_liner='枚举中间点：右边那条贪心，左边那条取前缀最大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数轴上有一些奖品（位置有序），选两条长为 `k` 的线段，可以相交', '求最多能覆盖多少个奖品',
                 '原题示例 `[1,1,2,2,3,3,5]`，`k=2` → `7`', '本视频：`[1,1,2,5,6,9]`，`k=1` → `5`（避开「直接返回 n」的捷径）'],
        quote='枚举 mid，既作为第一条线段的 right，又作为第二条线段的 left。……不能先跑第一条线段的滑动窗口，否则 mx + right − mid 可能会把 mid 处的奖品计入两次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两条线段不相交最好：第一条在 `mid` 左边，第二条从 `mid` 往右',
              '第二条：`right` 滑到最远；第一条：`mx` 记录右端 `<= mid` 的最大覆盖数',
              '先用 `mx + right − mid` 更新答案，再更新 `mx`'],
        summary=['时间 `O(n)`，`left`、`right` 各只右移 n 次；空间 `O(1)`',
                 '易错：必须先算 `ans` 再更新 `mx`，否则 mid 被数两次',
                 '线段端点不一定在奖品上：`left` 只是最左被覆盖的奖品',
                 '另有方法一：`mx[]` 数组 DP，空间 `O(n)`；同类题 1031'],
    ),
)
