N0, A0, B0 = 11, 2, 4


def _players(cv, x0, x1, y, n, a, b, T, r=21, arcs=False, label=None, lx=None):
    gap = min(2 * r + 12, (x1 - x0) / max(n, 1))
    sx = x0 + ((x1 - x0) - gap * n) / 2 + gap / 2
    pos = lambda i: sx + (i - 1) * gap
    if arcs:
        for i in range(1, n // 2 + 1):
            j = n + 1 - i
            hot = (i, j) == (a, b) or (j, i) == (a, b) or i in (a, b) or j in (a, b)
            col = T['yellow'] if hot else T['border']
            cv.arc_arrow((pos(i), y - r - 4), (pos(j), y - r - 4), 14 + 14 * (j - i) * gap / 120, col, width=3 if hot else 2, head=1)
    for i in range(1, n + 1):
        if i == a:
            fill, tc = T['blue'], T['bg']
        elif i == b:
            fill, tc = T['pink'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((pos(i) - r, y - r, pos(i) + r, y + r), fill=fill, outline=T['border'], width=1, r=r)
        cv.text((pos(i), y), i, 22, tc, anchor='mm', bold=True)
        if i in (a, b):
            cv.text((pos(i), y + r + 6), 'A' if i == a else 'B', 22, fill, anchor='mt', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'第 1 回合：{N0} 人，第 i 个对第 n+1−i 个（黄线 = A、B 的对手）', 24, T['muted'], bold=True)
    _players(cv, x0 + 20, x1 - 20, y0 + 160, N0, A0, B0, T, arcs=True)
    cur = S.get('n')
    a, b = S.get('first'), S.get('second')
    if isinstance(cur, int) and isinstance(a, int) and isinstance(b, int) and 'earliest' not in S:
        cv.text((x0 + 18, y0 + 240), f'当前考虑：剩 {cur} 人，A 在第 {a} 位，B 在第 {b} 位', 24, T['muted'], bold=True)
        _players(cv, x0 + 20, x1 - 20, y0 + 340, cur, a, b, T, arcs=True)
    e, l = S.get('earliest'), S.get('latest')
    if e is not None:
        cv.text((x0 + 18, y0 + 240), '结果', 24, T['muted'], bold=True)
        cv.text((x0 + 40, y0 + 290), f'最早回合 {e}', 40, T['green'], bold=True)
        if l is not None:
            cv.text((x0 + 40, y0 + 350), f'最晚回合 {l}', 40, T['orange'], bold=True)


CONFIG = dict(
    num=1900, title='最佳运动员的比拼回合', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='分类讨论 · 位运算 O(1)',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 2455'],
    code='''
class Solution:
    def earliestAndLatest(self, n: int, first: int, second: int) -> List[int]:
        if first + second == n + 1:
            return [1, 1]
        if first + second > n + 1:
            first, second = n + 1 - second, n + 1 - first
        def calc_earliest_rounds(n: int) -> int:
            res = 1
            if first + second <= (n + 1) // 2:
                # 计算满足 first+second > ceil(n / 2^(k+1)) 的最小 k，推导过程见题解
                k = ((n - 1) // (first + second - 1)).bit_length() - 1
                n = ((n - 1) >> k) + 1  # n = ceil(n / 2^k)
                res += k
                if second - first > 1:
                    return res + 1
            # 情况 1 和情况 3 合并，情况 2 合并到最后的 return
            if second - first == 1 or second > (n + 1) // 2 and second - first == 2:
                # 先把 n 变成 ceil(n/2)，然后计算需要多少次 ceil(n/2) 的操作才能把 n 变成偶数，推导过程见题解
                # 这里把 (n+1)/2 和 n-1 合并，得到 (n+1)/2-1 = (n-1)/2
                n = (n - 1) // 2
                # n 的二进制尾零个数等价于 lowbit(n) 的二进制长度减一，由于还要加一回合，加一减一抵消了
                return res + (n & -n).bit_length()
            if second > (n + 1) // 2 and first % 2 == 0 and first + second == n:
                res += 1
            return res + 1
        earliest = calc_earliest_rounds(n)
        latest = min((n - 1).bit_length(), n + 1 - second)
        return [earliest, latest]
''',
    call='Solution().earliestAndLatest(11, 2, 4)',
    expect=[3, 4],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"最早 ==第 {S['earliest']} 回合==，最晚 ==第 {S['latest']} 回合==" if 'latest' in S else ''), h=50),
    ],
    watch=['first', 'second', 'n', 'res', ('earliest', 'earliest', 'green'), ('latest', 'latest', 'orange')],
    captions={
        'if first + second == n + 1': '`first + second = {first + second}`，`n + 1 = {n + 1}`：和为 `n+1` ⇔ 两人互为镜像 ⇔ ==第 1 回合就相遇==',
        'if first + second > n + 1': '`{first + second} ≤ {n + 1}`：A 左边的人数不多于 B 右边，不用镜像。若大于，就把 A、B 换成镜像位置，保证 ==A 在中轴线左侧==',
        'earliest = calc': '先算最早回合',
        'res = 1': '`res = 1`：先算上第一回合',
        'if first + second <= (n + 1) // 2': '`first + second = {first + second}` ≤ 下一回合人数 `{(n + 1) // 2}`：A、B ==都太靠左==，这一回合不可能在新排里相遇，要先让人数折半',
        'k = ((n - 1)': '最小的 `k` 使 `first+second > ceil(n/2^(k+1))`：`k = {k}`（用位运算 `bit_length` 算，不用循环）',
        'n = ((n - 1) >> k)': '折半 `{k}` 次后剩 `ceil(n/2^k) = {n}` 人（`((n-1)>>k)+1` 就是上取整）',
        'res += k': '这 `{k}` 回合也要算进去：`res = {res}`',
        'if second - first > 1': '`second - first = {second - first}`：A、B ==不相邻== → 总能安排他们下回合恰好相遇，答案再 +1',
        'return res + 1': '`res + 1 = {ret}`：最早 =={ret}== 回合',
        'if second - first == 1': '相邻或中间隔一人时，要看人数奇偶，下面用二进制尾零个数一步算出',
        'n = (n - 1) // 2': '合并后的 `n = (n-1)//2`',
        'return res + (n & -n)': '`(n & -n).bit_length()` = `n` 的二进制尾零数 + 1 → 返回 `{ret}`',
        'if second > (n + 1) // 2 and first % 2 == 0': '',
        'latest = min': '最晚回合：不会超过理论最大 `ceil(log2 n) = {(n - 1).bit_length()}`，同时受 `n+1−second = {n + 1 - second}` 限制，取两者较小 → `latest = {latest}`',
        'return [earliest, latest]': '答案 =={ret}==',
    },
    max_steps=40,
    cards=dict(
        one_liner='不模拟比赛，按 A、B 的位置分类讨论，O(1) 出答案',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 人排成一排，每回合第 `i` 个对倒数第 `i` 个，奇数人时中间轮空',
                 '`firstPlayer`、`secondPlayer` 是两位最强者，其余人胜负可任意裁定',
                 '示例：`n=11, first=2, second=4` → `[3, 4]`（最早第 3 回合，最晚第 4 回合）'],
        quote='方法二可以解决 n≤10^18 的数据范围。保证 A 左边人数比 B 右边人数少，然后分类讨论。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先镜像：让 A 在中轴线左侧，只需讨论一半的情形',
              '最晚回合：理论最大回合 `⌈log2 n⌉`，且不能晚于 `n+1−second`',
              '最早回合：A、B 太靠左就先让人数折半 `k` 次；相邻时看 `n−1` 的二进制尾零个数，用位运算一步算出'],
        summary=['时间 `O(1)`；方法一是 `dfs(n, first, second)` 记忆化，复杂度 `O(n^4)`',
                 '易错：先判断「一开始就相遇」返回 `[1,1]`，再做镜像交换',
                 '`ceil(n/2^k)` 用 `((n-1) >> k) + 1` 计算，避免浮点',
                 '相似题：1040 移动石子直到连续 II'],
    ),
)
