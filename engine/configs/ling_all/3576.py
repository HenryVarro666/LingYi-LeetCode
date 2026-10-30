def _eff(S):
    return S['x'] * S['mul'] if 'x' in S and 'mul' in S else None


def _top(S):
    if 'target' not in S:
        return ''
    t = S['target']
    if 'i' not in S or 'mul' not in S:
        return f'目标：全部变成 ==`{t}`=='
    return f"目标 `{t}`｜`nums[{S['i']}]` 实际值 = `{S['x']}` × `{S['mul']}` = =={S['x'] * S['mul']}=="


CONFIG = dict(
    num=3576, title='数组元素相等转换', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='从左到右贪心 · mul 记录取反',
    tags=['灵神题单', '难度分 1489'],
    code='''
class Solution:
    def canMakeEqual(self, nums: List[int], k: int) -> bool:
        def check(target: int) -> bool:
            n = len(nums)
            left = k
            mul = 1
            for i, x in enumerate(nums):
                if x * mul == target:
                    mul = 1  # 不操作，下一个数不用乘 -1
                    continue
                if left == 0 or i == n - 1:
                    return False
                left -= 1
                mul = -1  # 操作，下一个数要乘 -1
            return True
        return check(-1) or check(1)
''',
    call='Solution().canMakeEqual([1,-1,1,-1,1], 3)',
    expect=True,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260,
             color=lambda S, i, v: (('green' if v * (S['mul'] if i == S['i'] else 1) == S['target'] else 'pink') if i == S.get('i') and 'target' in S and 'mul' in S else None)),
    ],
    watch=[('target', 'target', 'cyan'), ('left', 'left', 'orange'), ('mul', 'mul', 'pink'), ('i', 'i', 'blue')],
    captions={
        'left = k': '剩余操作次数 `left = {left}`',
        6: '`mul` 表示当前数要乘的符号：没被前一次操作影响就是 `1`',
        'if x * mul == target': lambda S, B, r: (f"`{S['x']} × {S['mul']} = {S['x'] * S['mul']}`，等于目标 `{S['target']}` → 不用操作"
                                                  if S['x'] * S['mul'] == S['target'] else
                                                  f"`{S['x']} × {S['mul']} = {S['x'] * S['mul']}`，不等于目标 `{S['target']}` → 必须操作"),
        9: '不操作，下一个数不受影响：`mul = 1`',
        'if left == 0 or i == n - 1': lambda S, B, r: ('没有剩余次数或已是最后一个数，操作不了 → ==失败=='
                                                       if (S['left'] == 0 or S['i'] == S['n'] - 1) else
                                                       f"还有 `{S['left']}` 次，且右边有数可一起取反 → 可以操作"),
        'left -= 1': '操作 `i` 和 `i+1`：次数减一，剩 `{left}`',
        'mul = -1': '`nums[i]` 以后不再看，只需让下一个数记得取反：`mul = -1`',
        'return False': '这个目标失败，换另一个目标试',
        'return True': '一路走到末尾 → ==这个目标可行==',
        'return check': '先检查能否全变 `-1`，不行再检查全变 `1`',
    },
    cards=dict(
        one_liner='从左往右，遇到不对的就操作它和右邻居',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组只含 `1` 和 `-1`，一次操作把相邻两数同时乘 `-1`',
                 '最多 `k` 次，能否让所有元素相等',
                 '示例：`[1,-1,1,-1,1], k=3` → `true`'],
        quote='如果要操作的时候，剩余操作次数等于 0，或者 i=n-1，那么无法操作，返回 false。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只可能全变 `1` 或全变 `-1`，两个目标各扫一遍',
              '扫到 `nums[i]` 不对，只能靠操作 `i` 来修正，而且之后不会再看 `i`',
              '所以用 ==mul== 记下“下一个数被取反”，不必真改数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '两次 `check` 各自从 `mul = 1` 开始，所以不直接修改 `nums`',
                 '易错点：最后一个数不对时没有右邻居可操作，直接失败',
                 '同类：从最左开始贪心，每个位置只有一种修正方式'],
    ),
)
