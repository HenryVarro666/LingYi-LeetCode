def _diff(S):
    t = S['target']
    return [t[0]] + [t[i] - t[i - 1] for i in range(1, len(t))]


def _txt(S):
    if 'x' not in S:
        return '差分 `d[i] = target[i] - target[i-1]`，答案 = ==d 中所有正数之和=='
    return f"`ans` = target[0] + 之后每一步的 max(y−x, 0)，当前 `ans` = =={S['ans']}=="


CONFIG = dict(
    num=1526, title='形成目标数组的子数组最少增加次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 正数之和',
    tags=['难度分 1872'],
    code='''
class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        ans = target[0]
        for x, y in pairwise(target):
            ans += max(y - x, 0)
        return ans
''',
    call='Solution().minNumberOperations([3,1,5,4,2])',
    expect=7,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='target', label='target（蓝 = x，粉 = y，相邻一对）',
             h=220,
             color=lambda S, i, v: ('blue' if 'x' in S and v == S['x'] else 'pink' if 'y' in S and v == S['y'] else None)),
        dict(type='array', var=_diff, label='差分数组 d（正数 = 必须单独「加一」的次数）', h=190,
             color=lambda S, i, v: ('green' if v > 0 and ('x' not in S or i == 0 or S['target'].index(S['y']) >= i) else None)),
    ],
    watch=['x', 'y', ('ans', 'ans', 'green')],
    captions={
        'ans = target[0]': '`d[0] = target[0] = {target[0]}`：第一个差分一定是正数，先计入 `ans = {ans}`',
        'pairwise': lambda S, B, r: (f'取相邻两数 `x = {S.x}`，`y = {S.y}`：差分 `d = y - x = {S.y - S.x}`' if 'x' in S and (S.get('x') != B.get('x') or S.get('y') != B.get('y')) else '相邻对遍历完毕'),
        'ans += max': lambda S, B, r: (f'`y - x = {S.y - S.x} > 0`：差分为正，要多一次操作 → `ans` {B.ans} → =={S.ans}==' if S.y > S.x else f'`y - x = {S.y - S.x} ≤ 0`：差分非正，可与左边的正数配对（左加右减），不增加次数 → `ans` 仍是 =={S.ans}=='),
        'return ans': '`ans = {ans}` 就是 `d` 中所有正数之和',
    },
    cards=dict(
        one_liner='区间加一 = 差分数组里「左边 +1、右边 −1」，次数 = 正数之和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`initial` 全为 0，每次选一个子数组整体加 `1`',
                 '求变成 `target` 的最少操作次数',
                 '示例：`target = [3,1,5,4,2]` → `7`'],
        quote='无论每次操作修改的是两个数还是一个数，一定会把一个数加一。所以最小操作次数等于加一的次数，即 d 中所有正数之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['区间加一在差分上只改两处：==左端 +1，右端后一位 −1==；后缀加一则只有 +1',
              '负数可以和左边的正数配对，不用额外操作；剩下的正数单独算',
              '`d[i] = target[i] - target[i-1]`，所以 `ans = target[0] + Σ max(y - x, 0)`'],
        summary=['时间 `O(n)`，空间 `O(1)`：不必真的建差分数组，`pairwise` 现算',
                 '`ans` 先取 `target[0]`（`d[0]`），别漏掉',
                 '`target[i] > 0` 保证负数一定能和左边正数配对',
                 '另有 Python3 一行写法：`target[0] + sum(max(y - x, 0) for ...)`',
                 '相似题：3229 使数组等于目标数组所需的最少操作次数'],
    ),
)
