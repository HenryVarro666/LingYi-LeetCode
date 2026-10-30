def _text(S):
    if 'n' not in S:
        return '每一轮：相邻两数相加取模 10，数组短一格'
    n = S['n']
    nums = S['nums']
    if 'i' in S and S.get('_line') in (5, 6) and S['i'] < n:
        i = S['i']
        return f'这一轮还剩 `{n + 1}` 个数，要算 `{n}` 个新值；当前 `({nums[i]} + {nums[i + 1]}) % 10`'
    return f'本轮有效区间是 `nums[0..{n}]`（亮色），后面的格子已经没用了'


CONFIG = dict(
    num=2221, title='数组的三角和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='原地模拟',
    tags=['灵神题单'],
    code='''
class Solution:
    def triangularSum(self, nums: List[int]) -> int:
        # 每循环一轮，数组长度就减一
        for n in range(len(nums) - 1, 0, -1):
            for i in range(n):
                nums[i] = (nums[i] + nums[i + 1]) % 10
        return nums[0]
''',
    call='Solution().triangularSum([1,2,3,4,5])',
    expect=8,
    views=[
        dict(type='text', fn=_text),
        dict(type='array', var='nums', pointers={'i': 'blue'}, window=(0, 'n'), h=300, cell=100,
             dim=lambda S, i, v: 'n' in S and i > S['n'],
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] and S.get('_line') in (5, 6) else None),
    ],
    watch=[('n', 'n', 'purple'), ('i', 'i', 'blue'), ('nums', 'nums', 'green')],
    captions={
        'for n in range': lambda S, B, ret: ('`n` 已经走完 `1`，所有轮次结束' if 'n' in B and B.n == S['n'] and S['n'] == 1 else f'开始新的一轮：本轮要处理 `nums[0..{S["n"]}]`，会得到 `{S["n"]}` 个新数'),
        'for i in range': lambda S, B, ret: (f'`i` 走完 `0..{S["n"] - 1}`，这一轮结束，数组有效长度少 1' if 'i' in B and B.i == S['n'] - 1 and S['i'] == B.i else f'`i = {S["i"]}`：把 `nums[{S["i"]}]` 和右邻合成一项'),
        'nums[i] = (': lambda S, B, ret: f'`({B.nums[S["i"]]} + {B.nums[S["i"] + 1]}) % 10 = {S["nums"][S["i"]]}`：覆盖 `nums[{S["i"]}]`' + ('，==不用新数组==：右邻 `nums[i+1]` 这一轮还没被覆盖' if S['i'] == 0 else ''),
        'return nums[0]': '长度缩到 1，三角和就是 `nums[0] = {nums[0]}`',
    },
    cards=dict(
        one_liner='原地覆盖，每一轮数组短一格',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`nums` 每个数 0–9。每轮把相邻两数之和取模 10 得到长度少 1 的新数组',
                 '重复到只剩一个数，返回它',
                 '示例：`[1,2,3,4,5]` → `8`'],
        quote='无需 newNums，直接原地把 nums[i] 更新为 (nums[i] + nums[i+1]) mod 10。每循环一次，把 nums 的长度减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右覆盖：写 `nums[i]` 时，右边 `nums[i+1]` 还是旧值，所以安全',
              '外层 `n` 表示本轮要写的个数：4, 3, 2, 1',
              '第一轮 `[1,2,3,4,5]` → `[3,5,7,9]`，再一轮 → `[8,2,6]`'],
        after=[dict(heading='另一种写法：组合数学', lines=[
            '灵神方法二：`nums[i]` 的系数是 `C(n-1, i)`，像杨辉三角',
            '答案 = `sum(C(n-1,i) * nums[i]) % 10`，`O(n)` 时间',
            '模 10 不是质数，要分离因子 2 和 5 再用欧拉定理求逆元'])],
        summary=['时间 `O(n^2)`，空间 `O(1)`（原地）',
                 '易错点：==内层循环从左往右==才能保证 `nums[i+1]` 还是旧值',
                 '外层从 `len-1` 递减到 1，别写成 `range(len(nums))`',
                 '另有组合数学做法（杨辉三角系数），同类题：3463'],
    ),
)
