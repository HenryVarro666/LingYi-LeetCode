def _col(S, i, v):
    return 'purple' if v == '1' else None


CONFIG = dict(
    num=2938, title='区分黑球与白球', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='遍历 · 每个 0 加上左边 1 的个数',
    code='''
class Solution:
    def minimumSteps(self, s: str) -> int:
        ans = cnt1 = 0
        for c in s:
            if c == '1':
                cnt1 += 1
            else:
                ans += cnt1
        return ans
''',
    call='Solution().minimumSteps("1011001")',
    expect=7,
    views=[
        dict(type='string', var='s', label='s（紫 = 黑球 1，白 = 白球 0）', pointers={'i': 'blue'}, color=_col, h=300),
        dict(type='text', fn=lambda S: f"左边已有 `cnt1` = =={S['cnt1']}== 个黑球；累计交换 `ans` = =={S['ans']}==" if 'cnt1' in S else '', h=80),
    ],
    watch=[('c', 'c', 'blue'), ('cnt1', 'cnt1', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt1 = 0': '`cnt1` 统计目前见过的 1 的个数，`ans` 累计交换次数',
        'for c in s': '看下一个球：`{c}`',
        "if c == '1'": lambda S, B, r: (f"`c = '1'` 是黑球 → 先记下来，它要去右边" if S.c == '1' else "`c = '0'` 是白球 → 它左边的黑球都得和它换"),
        'cnt1 += 1': '黑球多一个：`cnt1` = =={cnt1}==',
        'ans += cnt1': '这个 0 要和它左边的 `{cnt1}` 个 1 各交换一次：`ans` = `{B.ans} + {cnt1}` = =={ans}==',
        'return': '所有 0 都到了 1 的左边，最少交换 ==`{ret}`== 次',
    },
    cards=dict(
        one_liner='每个 0 要越过它左边的所有 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 中 `1` 是黑球、`0` 是白球，每次交换相邻两球，求把黑球全移到右侧的最少步数',
                 '示例：`"100"` → `2`', '本视频：`"1011001"` → `7`'],
        quote='遍历 s 的同时，统计 1 的个数 cnt1。遇到 0 时，这个 0 和它左边 cnt1 个 1 都要交换，把 cnt1 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['目标是 0 全在 1 的左边', '每个 0 都要换过它左边的每个 1，每对 `(1 在左, 0 在右)` 恰好换一次',
              '所以边扫边数 1，遇到 0 就累加（也就是逆序对个数）'],
        summary=['时间 `O(n)`，空间 `O(1)`', '本质是统计「1 在 0 左边」的逆序对数',
                 '`n` 可到 `10^5`，答案可达约 `2.5×10^9`，Python 无溢出问题'],
    ),
)
