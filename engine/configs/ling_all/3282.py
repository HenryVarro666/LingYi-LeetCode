def _idx(S):
    if 'x' not in S:
        return None
    return S['nums'].index(S['x'])


def _txt(S):
    if 'ans' not in S:
        return '每跳 1 格得分 = 起跳点的值：==把 n-1 个宽为 1 的矩形，高度取到目前为止的最大值=='
    i = _idx(S)
    if i is None:
        return '还没开始：`mx` 记录已遍历数的最大值，`ans` 累加每个矩形的高'
    return f"第 {i} 格的矩形：宽 1 × 高 `mx = {S['mx']}`，累计 `ans = {S['ans']}`"


CONFIG = dict(
    num=3282, title='到达数组末尾的最大得分', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='脑筋急转弯 · 前缀最大值',
    tags=['灵神题单', '难度分 1772'],
    code='''
class Solution:
    def findMaximumScore(self, nums: List[int]) -> int:
        ans = mx = 0
        for x in nums[:-1]:  # 也可以先 pop 掉最后一个数
            mx = max(mx, x)
            ans += mx
        return ans
''',
    call='Solution().findMaximumScore([2,5,3,6,1,4])',
    expect=24,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='bars', var='nums', h=420, label='nums（最后一个数不作起跳点）',
             color=lambda S, i, v: ('blue' if i == _idx(S) else ('orange' if _idx(S) is not None and i < _idx(S) and v == S['mx'] else None)),
             dim=lambda S, i, v: i == len(S['nums']) - 1,
             pointers={}),
    ],
    watch=[('x', 'x', 'blue'), ('mx', 'mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = 0': '`ans` 累计总得分，`mx` 记录目前见过的最大值',
        'for x in': lambda S, B, r: ('只遍历 `nums[:-1]`：最后一个数只是终点，不作起跳点；取下一个数 `x = %d`' % S.x) if 'x' in S else '`nums[:-1]` 遍历完，所有起跳点都算过了',
        'mx = max': lambda S, B, r: ('`x = %d` 比 `mx = %d` 大 → 起跳点升级，==mx 更新为 %d==' % (S.x, B.mx, S.mx)) if S.x > B.mx else ('`x = %d` 不比 `mx = %d` 大 → 还是用 mx 当高，mx 不变' % (S.x, B.mx)),
        'ans += mx': '加上宽 1、高 `{mx}` 的矩形：`ans = {ans}`',
        'return ans': '所有 `n-1` 个矩形面积之和 = ==最大得分 {ans}==',
    },
    cards=dict(
        one_liner='把得分看成 n-1 个宽 1 的矩形，每个都取最大高度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从下标 0 跳到 `n-1`，从 `i` 跳到 `j` 得分 `(j-i)*nums[i]`，求最大总得分',
                 '示例：`[1,3,1,5]` → `7`；`[4,3,1,3,2]` → `16`',
                 '本视频：`[2,5,3,6,1,4]` → `24`'],
        quote='代码实现时，可以视作有 n-1 个底边长为 1 的矩形。最大化每个矩形的高，即可最大化所有矩形的面积之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`(j-i)*nums[i]` 拆成 `j-i` 个宽为 1 的格子，每格得分是起跳点的值',
              '第 `k` 格能用的起跳点只能在它左边，所以高度取==前缀最大值=='
              ,'从左到右维护 `mx`，累加即可；也有 `sum(accumulate(nums[:-1], max))` 的一行写法'],
        summary=['时间 `O(n)`，空间 `O(1)`（Python 切片忽略不计）',
                 '遍历 `nums[:-1]`：最后一个数不能当起跳点',
                 '每个矩形取到当前为止的最大值，不是整个数组的最大值',
                 '灵神也给了 `sum(accumulate(nums[:-1], max))` 的一行写法；思考题：改成最小得分？'],
    ),
)
