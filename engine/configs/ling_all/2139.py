CONFIG = dict(
    num=2139, title='得到目标值的最少行动次数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='逆向思维 · 倒推时能除就除（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1417'],
    code='''
class Solution:
    def minMoves(self, v: int, maxDoubles: int) -> int:
        ans = 0
        while v > 1:
            if maxDoubles == 0:
                return ans + v - 1
            if v % 2 > 0:
                v -= 1
                ans += 1
            maxDoubles -= 1
            v //= 2
            ans += 1
        return ans
''',
    call='Solution().minMoves(19, 2)',
    expect=7,
    views=[
        dict(type='text', size=44, h=120, fn=lambda S: f"倒推：当前 `v = {S['v']}`，剩余加倍 `{S['maxDoubles']}` 次，已用 `{S['ans']}` 步" if 'ans' in S else ''),
        dict(type='text', size=34, h=120, fn=lambda S: (f"若现在不能再加倍：还差 `{S['v']} − 1 = {S['v']-1}` 次递增 → 总数 `{S['ans'] + S['v'] - 1}`" if 'ans' in S and S['v'] > 1 else '')),
    ],
    watch=[('v', 'v', 'blue'), ('maxDoubles', 'maxDoubles', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'while v > 1': lambda S, B, r: (f'`v = {S.v} > 1`，还没倒推回起点 1，继续' if S.v > 1 else '`v = 1`：已经回到起点，结束'),
        'if maxDoubles == 0': lambda S, B, r: ('没有加倍次数了：剩下只能一步步 +1，直接算出答案' if S.maxDoubles == 0 else f'还剩 `{S.maxDoubles}` 次加倍，继续倒推'),
        'return ans + v - 1': '从 1 递增到 `{v}` 需要 `{v} - 1` 步，加上已用的 `{ans}` 步 = =={ret}==',
        'if v % 2 > 0': lambda S, B, r: (f'`{S.v}` 是奇数 → 只能由 `{S.v - 1}` 递增得到' if S.v % 2 else f'`{S.v}` 是偶数 → 可以由 `{S.v // 2}` 加倍得到'),
        'v -= 1': '倒推一步递增：`v` → {v}，`ans` 将加 1',
        'maxDoubles -= 1': '用掉一次加倍：剩 `{maxDoubles}` 次（越大的数加倍越划算，所以==能加倍就加倍==）',
        'v //= 2': '倒推一次加倍：`v` 折半 → =={v}==',
        'ans += 1': '记一步操作：`ans = {ans}`',
        'return ans': '回到 1，一共 =={ans}== 步',
    },
    cards=dict(
        one_liner='倒着想：加倍留给大数，能除 2 就除 2',
        complexity='时间 `O(min(maxDoubles, log target))`，空间 `O(1)`',
        problem=['从 `1` 出发，每步 `+1` 或 `×2`，`×2` 至多用 `maxDoubles` 次',
                 '求得到 `target` 的最少步数',
                 '示例：`target = 19, maxDoubles = 2` → `7`'],
        quote='由于加倍次数有限，我们应该将其留在数字更大的时候加倍，这样可以节省更多的行动次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 `v = target` 倒推：奇数只能由 `v-1` 递增来，偶数能加倍就加倍',
              '加倍次数用完，剩下全是递增，一次算出 `v - 1`',
              '倒推相当于把加倍放在数最大的时候用'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`v /= 2` 对应 `v //= 2`）',
                 '时间 `O(min(maxDoubles, log target))`，空间 `O(1)`',
                 '易错点：先判断 `maxDoubles == 0` 再处理奇偶；奇数先减 1 再折半，共 2 步',
                 '同类逆向思维：把正向难做的操作倒过来想'],
    ),
)
