CONFIG = dict(
    num=3993, title='交替数列的最大元素', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='构造 + 公式',
    tags=[],
    code='''
class Solution:
    def maximumValue(self, n: int, s: int, m: int) -> int:
        if n == 1:
            return s
        return s + m + (m - 1) * (n // 2 - 1)
''',
    call='Solution().maximumValue(8, 3, 5)',
    expect=20,
    views=[
        dict(type='text', size=34, h=140, fn=lambda S: (
            f"构造：`3, 8, 7, 12, 11, 16, 15, 20`（先 `+m`，再 `−1`，交替）")),
        dict(type='text', size=34, h=140, fn=lambda S: (
            f"`s + m + (m−1)×(n//2−1)` = `{S['s']} + {S['m']} + {S['m']-1}×{S['n']//2-1}` = =={S['s']+S['m']+(S['m']-1)*(S['n']//2-1)}==" if 'n' in S and S['n'] > 1 else '')),
    ],
    watch=['n', 's', 'm'],
    captions={
        'if n == 1': '`n = {n}`：只有 `n == 1` 时序列才是 `[s]`；这里 `n ≥ 2`，用公式',
        'return s + m': '先 `+m` 到 `s+m`，之后每两步（`−1` 再 `+m`）净增 `m−1`，共 `n//2−1 = {n//2-1}` 次 → =={ret}==',
    },
    cards=dict(
        one_liner='先加 m，再减 1、加 m 交替，每两步净增 m−1',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度为 `n` 的序列 `seq[0] = s`，相邻元素严格交替升降，且相邻差的绝对值 `≤ m`',
                 '求所有有效序列中可能出现的最大元素',
                 '示例：`n=4, s=3, m=5` → `12`，序列 `[3,8,7,12]`'],
        quote='依此类推，从 n=2 开始，n 每增加 2，最大值就增加 m-1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n=1` 只有 `[s]`；`n=2` 最优是 `[s, s+m]`',
              '`n≥3` 先递增更优：下一个只需比 `s+m` 小 1，再下一个又能加 `m`',
              '于是 `n` 每多 2，最大值多 `m−1`；公式对 `n=2` 也成立'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：`n == 1` 要单独返回 `s`，公式里 `n//2-1` 会变成 −1',
                 '下降只降 1，是为了把「再上升 m」的起点留得尽量高'],
    ),
)
