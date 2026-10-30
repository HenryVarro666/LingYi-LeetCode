def _idx(S):
    x = S.get('x')
    if x is None or 'nums' not in S:
        return None
    return S['nums'].index(x)


def _txt(S):
    if 'f0' not in S:
        return '三个阶段：`f0` 不修改 · `f1` 修改了 nums[i] · `f2` 修改在左边、nums[i] 不修改'
    mode = '乘 k' if S.get('is_mul') else '除 k'
    if 'y' not in S or S.get('x') is None:
        return f'本轮枚举：子数组修改部分 =={mode}=='
    return f"本轮 =={mode}==：`x = {S['x']}`，修改后 `y = {S['y']}`"


CONFIG = dict(
    num=3976, title='乘以系数后最大子数组和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 三阶段',
    tags=['灵神核心路线', '难度分 1981'],
    code='''
class Solution:
    def maxSubarraySum(self, nums: list[int], k: int) -> int:
        def solve(is_mul: bool) -> int:
            f0 = f1 = f2 = 0
            res = -inf

            for x in nums:
                # 不想用浮点数的话，可以把 int(x/k) 换成 x//k if x>=0 else -(-x//k)
                y = x * k if is_mul else int(x / k)
                f2 = max(f1, f2) + x
                f1 = max(f0, f1, 0) + y
                f0 = max(f0, 0) + x
                res = max(res, f1, f2)

            return res

        return max(solve(True), solve(False))
''',
    call='Solution().maxSubarraySum([-2, 3, 4, -5], 2)',
    expect=14,
    skip=['f0 = f1 = f2 = 0', 'res = -inf'],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='nums', label='nums', h=190, cell=90, pointers={'x': 'blue'},
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='text', h=70, size=26,
             fn=lambda S: (f"`f0 = {S['f0']}`（不改）  `f1 = {S['f1']}`（改了当前）  `f2 = {S['f2']}`（改在左边）" if 'f0' in S else '')),
    ],
    watch=['x', 'y', ('f0', 'f0', 'cyan'), ('f1', 'f1', 'orange'), ('f2', 'f2', 'purple'), ('res', 'res', 'green')],
    captions={
        'y = x * k': lambda S, B, r: f"`x = {S.x}` 修改后的值 `y = {S.y}`（{'乘' if S.is_mul else '除'} k，向零取整）",
        'f2 = max': '阶段 3：不改 x，接在 `f1`/`f2` 之后：`max({B.f1}, {B.f2}) + {x}` = =={f2}==。==先算 f2，免得 f1 被覆盖==',
        'f1 = max': '阶段 2：改 x，可接阶段 1/2，或自己开头：`max({B.f0}, {B.f1}, 0) + {y}` = =={f1}==',
        'f0 = max': '阶段 1：不改，同 53 题：`max({B.f0}, 0) + {x}` = =={f0}==',
        'res = max': '子数组可在阶段 2 或 3 结束：`res = max({B.res}, {f1}, {f2}) = {res}`',
        'return res': '这一轮（{"乘" if is_mul else "除"}）的最大和 `{res}`',
        'return max(solve': lambda S, B, ret: '先跑乘法版 `solve(True)`，再跑除法版 `solve(False)`' if ret is None else f'乘、除两种都试，取较大的 `{ret}`',
    },
    cards=dict(
        one_liner='子数组从左到右：不改 → 改 → 不改，三阶段状态机',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给 `nums` 和 `k`：选一段子数组，每个数 ==乘 k== 或 ==除 k==（取整向零）',
                 '再选一段非空子数组求和，求最大和（两段可以不同）',
                 '示例：`[1,-2,3,4,-5], k=2`；本视频用 `[-2,3,4,-5]` → `14`（`[3,4]` 乘 2）'],
        quote='子数组中的元素，从左到右，至多会经过三个阶段：1. 不修改。2. 修改。3. 不修改。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f0`：没修改；`f1`：当前数被修改；`f2`：修改发生在当前数左边',
              '和 53 题一样，前面和为负就丢掉，自己重新开头：`max(…, 0)`',
              '乘、除各跑一遍，取较大者；无操作版本一定不优，不用单独算'],
        summary=['时间 `O(n)`，空间 `O(1)`；优化前写法是 `f[i+1][j]` 的二维数组',
                 '==更新顺序 f2 → f1 → f0==，否则会用到被覆盖的旧值',
                 '不能只靠最大子数组和：`[2,-1,-1,2,-1,-1,2]` 除 2 才得 5',
                 '`int(x/k)` 用到浮点；也可写 `x//k if x>=0 else -(-x//k)`'],
    ),
)
