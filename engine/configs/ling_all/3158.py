def _vis_txt(S):
    if 'vis' not in S:
        return ''
    v = S['vis']
    items = [k for k in range(64) if v >> k & 1]
    return f"集合 `vis` = {{{', '.join(map(str, items))}}}　二进制 `{v:b}`　答案 `ans` = ==`{S['ans']}`=="


CONFIG = dict(
    num=3158, title='求出出现两次数字的 XOR 值', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='二进制数当集合 · 异或',
    code='''
class Solution:
    def duplicateNumbersXOR(self, nums: List[int]) -> int:
        ans = vis = 0
        for x in nums:
            if vis >> x & 1:  # x 在 vis 中
                ans ^= x
            else:
                vis |= 1 << x  # 把 x 加到 vis 中
        return ans
''',
    call='Solution().duplicateNumbersXOR([3, 1, 2, 3, 5, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前 x）', cell=96, h=190,
             color=lambda S, i, v: 'yellow' if 'x' in S and v == S['x'] else None),
        dict(type='text', h=110, size=28, fn=_vis_txt),
    ],
    watch=[('x', 'x', 'yellow'), ('vis', 'vis', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = vis = 0': '`ans` 是异或结果，`vis` 是==用二进制表示的集合==：第 `x` 位为 1 表示 `x` 见过。都从 0 开始',
        'for x in nums': lambda S, B, ret: ('`nums` 遍历完了，循环结束' if B.get('x') == S.x else f'看下一个数 `x = {S.x}`'),
        'if vis >> x & 1': lambda S, B, ret: (f'`vis` 的第 {S.x} 位是 1：`{S.x}` 之前出现过，这是==第二次==遇到' if (S.vis >> S.x & 1)
                                              else f'`vis` 的第 {S.x} 位是 0：`{S.x}` ==第一次==出现'),
        'ans ^= x': '第二次遇到（每个数至多出现两次）→ 异或进答案：`ans = {B.ans} ^ {x} = {ans}`',
        'vis |= 1 << x': '第一次遇到 → 把第 `{x}` 位置 1，加入集合：`vis = {vis:b}`（二进制）',
        'return ans': '遍历完，出现两次的数异或起来是 ==`{ans}`==',
    },
    cards=dict(
        one_liner='用一个整数的二进制位当“见过”集合，第二次见到就异或',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 中每个数要么出现一次，要么出现两次',
                 '返回所有出现两次的数的按位异或；没有则返回 `0`',
                 '示例：`[1,2,1,3]` → `1`；`[1,2,2,1]` → `3`'],
        quote='代码实现时，由于 nums[i]≤50，可以用二进制数表示集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['边遍历边记录“见过的数”：第一次见加入集合，第二次见说明它出现了两次',
              '值域只有 50，集合可以压成一个整数 `vis`：`vis >> x & 1` 查询，`vis |= 1 << x` 插入',
              '出现两次的数 `ans ^= x`，只会异或一次'],
        summary=['时间 `O(n)`，空间 `O(1)`（`vis` 最多 51 位）',
                 '易错：查询是 `vis >> x & 1`，插入是 `vis |= 1 << x`，位序别写反',
                 '因为每个数至多出现两次，第二次遇到才异或，不会重复异或',
                 '值域大时可换成普通 `set`，思路不变'],
    ),
)
