CONFIG = dict(
    num=3688, title='偶数的按位或运算', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='遍历 · 偶数累积 OR',
    tags=['灵神题单'],
    code='''
class Solution:
    def evenNumberBitwiseORs(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            if x % 2 == 0:
                ans |= x
        return ans
''',
    call='Solution().evenNumberBitwiseORs([1,8,16,3])',
    expect=24,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: ('green' if v % 2 == 0 else 'pink') if 'x' in S and v == S['x'] else None,
             dim=lambda S, i, v: v % 2 == 1),
        dict(type='text', h=120, size=34, fn=lambda S: f"`ans` = `{S['ans']:08b}` = =={S['ans']}==" if 'ans' in S else ''),
    ],
    watch=['x', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`0 | x = x`，所以 0 是 OR 的单位元，用它当初始值（也自然覆盖「没有偶数」→ 0）',
        'for x in nums': lambda S, B, r: (f'取下一个数 `x = {S.x}`' if S.x != B.get('x') else '数组遍历完了'),
        'if x % 2 == 0': lambda S, B, r: (f'`{S.x} % 2 == 0` → 是偶数，要参与 OR' if S.x % 2 == 0 else f'`{S.x} % 2 = 1` → 奇数，跳过'),
        'ans |= x': '`ans = {B.ans:b} | {x:b}` → `{ans:b}` = =={ans}==',
        'return ans': '没有偶数时 `ans` 还是 0，正好满足题意；这里返回 `{ans}`',
    },
    cards=dict(
        one_liner='0 是 OR 的单位元：从 0 开始，遇到偶数就 OR 进去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回 `nums` 中所有偶数的按位或',
                 '没有偶数就返回 `0`',
                 '示例：`[1,8,16]` → `24`；本视频用 `[1,8,16,3]`'],
        quote='偶数就是模 2 等于 0 的数。由于 0 或 x 等于 x，所以可以用 0 作为答案的初始值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历数组，`x % 2 == 0` 才处理', '`ans |= x` 累积 OR', '初值 0 不改变结果，也兜住「无偶数」'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：初始值要是 0；如果改成按位与，初始值应为全 1（`-1`）',
                 '思考题：对每个子数组求值再累加，要用拆位 / 贡献法'],
    ),
)
