def _ci(S):
    return S['runes'].index(S['cur']) if 'cur' in S else None


def _win(S):
    if 'cur' not in S:
        return None
    c = _ci(S)
    return (c - S['cnt'] + 1, c)


CONFIG = dict(
    num='LCP 77', title='符文储备', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 连续段计数', tags=[],
    code='''
class Solution:
    def runeReserve(self, runes: List[int]) -> int:
        runes.sort()
        ans = cnt = 1
        for pre, cur in pairwise(runes):
            if cur - pre > 1:
                cnt = 1  # 重新统计
            else:
                cnt += 1
                ans = max(ans, cnt)
        return ans
''',
    call='Solution().runeReserve([8,3,5,1,4,10,2])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"当前一段长度 `cnt` = =={S['cnt']}==，历史最长 `ans` = {S['ans']}" if 'cnt' in S else '')),
        dict(type='array', var='runes', h=300,
             pointers={'runes.index(pre)': 'blue', 'runes.index(cur)': 'pink'},
             pointer_labels={'runes.index(pre)': 'pre', 'runes.index(cur)': 'cur'},
             window=('runes.index(cur) - cnt + 1', 'runes.index(cur)'),
             color=lambda S, i, v: ('pink' if 'cur' in S and i == _ci(S) else None)),
    ],
    watch=[('pre', 'pre', 'blue'), ('cur', 'cur', 'pink'), ('cnt', 'cnt', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'runes.sort()': '先排序：魔力值相差不超过 1 的符文会挨在一起，排成 `{runes}`',
        'ans = cnt = 1': '至少能带一枚：`ans = cnt = 1`',
        'for pre, cur': lambda S, B, r: ('没有更多相邻对了，循环结束' if B.get('cur') == S.cur and B.get('pre') == S.pre and 'pre' in B and S.cur == 10 else f'看相邻两枚：`pre = {S.pre}`，`cur = {S.cur}`'),
        'if cur - pre > 1': '`{cur} - {pre} = {cur - pre}`，相差 {"大于 1 ==断开==" if cur - pre > 1 else "不超过 1 → 可以接上"}',
        'cnt = 1': '断开了，这一段结束：`cnt` 重新从 1 数起',
        'cnt += 1': '接上了：当前段长度 `cnt` → =={cnt}==',
        'ans = max': '`ans = max({B.ans}, {cnt})` → =={ans}==，历史最长更新',
        'return ans': '最长的一段有 `{ans}` 枚，返回 =={ans}==',
    },
    cards=dict(
        one_liner='排序后，数最长的「相邻差 ≤ 1」连续段',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`runes[i]` 是符文魔力值，选一些并重排，使相邻魔力值相差不超过 `1`',
                 '求最多能带多少枚符文',
                 '示例：`[1,3,5,4,1,7]` → `3`（选 3,4,5）'],
        quote='排序后，统计相邻相差不超过 1 的元素个数：如果相邻相差大于 1，那么重新统计。否则计数器加一，更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，能同时选的符文必然是==排序数组里的一段连续区间==',
              '相邻差 `> 1` 就断开，`cnt` 归 1；否则 `cnt + 1` 并刷新 `ans`',
              '重复的数相差 0，也算接上'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '`ans` 和 `cnt` 都从 1 开始：只有一枚符文也能带',
                 '断开时只重置 `cnt`，`ans` 在 `cnt` 增长时更新，所以最后一段也不会漏',
                 '本视频示例：`[8,3,5,1,4,10,2]` 排序后 1~5 连续，答案 5'],
    ),
)
