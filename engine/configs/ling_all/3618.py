NUMS = [2, 3, 4, 5, -1, 7, 0, 6]
_PR = [False, False, True, True, False, True, False, True]   # 下标 0..7 是否质数
_IDX = list(range(8))


def _txt(S):
    if 'ans' not in S:
        return '质数下标（2、3、5、7）的元素 ==加==，其余元素 ==减==，最后取绝对值'
    a = sum(x for x, p in zip(NUMS, _PR) if p)
    b = sum(x for x, p in zip(NUMS, _PR) if not p)
    return f"`sum(A) = {a}`，`sum(B) = {b}`：`ans = {a} − {b} = {a - b}`"


CONFIG = dict(
    num=3618, title='根据质数下标分割数组', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='埃氏筛 + 正负累加',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1227'],
    code='''
MX = 100_000
is_prime = [False] * 2 + [True] * (MX - 2)  # 0 和 1 不是质数
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = False  # j 是质数 i 的倍数

class Solution:
    def splitArray(self, nums: List[int]) -> int:
        ans = sum(x if p else -x for x, p in zip(nums, is_prime))
        return abs(ans)
''',
    call=f'Solution().splitArray({NUMS})',
    expect=18,
    views=[
        dict(type='array', var=_IDX, label='下标 i', h=150, cell=90, index=False,
             color=lambda S, i, v: 'pink' if _PR[i] else None),
        dict(type='array', var='nums', label='nums（粉 = 质数下标，归 A；其余归 B）', h=190, cell=90,
             color=lambda S, i, v: 'pink' if _PR[i] else None),
        dict(type='text', size=30, h=120, fn=_txt),
    ],
    watch=[('ans', 'ans', 'green')],
    max_steps=40,
    captions={
        'MX = 100_000': '`n <= 10^5`，下标最大 `99999`，筛到 `MX = 100000` 就够',
        'ans = sum': lambda S, B, r: f'质数下标的 `x` 加进来，其余的减掉：`A − B` = =={S.ans}==',
        'return abs': '题目要的是 `|sum(A) − sum(B)|`，取绝对值：`abs({ans})` = =={ret}==',
    },
    cards=dict(
        one_liner='筛出质数下标，质数下标加、其余下标减',
        complexity='时间 `O(n)`，空间 `O(1)`（不计预处理）',
        problem=['`nums` 中==质数下标==的元素放进 `A`，其余放进 `B`',
                 '返回 `|sum(A) − sum(B)|`；质数是大于 1、只有 1 和自身两个因子的数',
                 '示例：`[2,3,4]` → `1`；`[-1,5,7,0]` → `3`',
                 '本视频：`[2,3,4,5,-1,7,0,6]` → `18`'],
        quote='用埃氏筛预处理 [0,n-1] 中的每个数是不是质数。累加质数下标的元素，减去非质数下标的元素，取绝对值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`sum(A) − sum(B)` 一遍就能算：质数下标 `+x`，否则 `−x`',
              '难点只是“下标是不是质数”：预处理 `is_prime`，`zip` 一起扫',
              '最后取绝对值'],
        before=[dict(heading='预处理：埃氏筛', lines=['`is_prime = [False]*2 + [True]*(MX-2)`：0 和 1 不是质数', '遇到质数 `i`，把 `i*i` 起的所有倍数标成非质数', '`i` 只需枚举到 `isqrt(MX)`', '筛一次，之后每次查询 `O(1)`']),
                dict(heading='本例的质数下标', lines=['`n = 8`，下标 `0..7`', '质数下标：`2, 3, 5, 7`', '`A = [4, 5, 7, 6]`，`B = [2, 3, -1, 0]`'])],
        summary=['时间 `O(n)`，空间 `O(1)`；预处理的时间和空间不计入',
                 '易错点：==0 和 1 不是质数==，下标 0、1 归 B',
                 '易错点：==差值要取绝对值==，`ans` 可能为负',
                 '同类题：204. 计数质数，3591. 检查元素频次是否为质数'],
    ),
)
