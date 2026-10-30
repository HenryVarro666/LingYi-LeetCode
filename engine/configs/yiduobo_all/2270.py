def _text(S):
    if 'now' not in S or 'index' not in S:
        return f"总和 `s = {S['s']}`" if 's' in S else ''
    return f"左边 `now = {S['now']}`，右边 `s - now = {S['s'] - S['now']}`，已找到 `res = {S['res']}` 个"


def _color(S, i, v):
    if 'index' not in S or 'now' not in S:
        return None
    if i == S['index']:
        return 'blue'
    return 'green' if i < S['index'] else None


CONFIG = dict(
    num=2270, title='分割数组的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='总和 − 前缀和 = 右侧和',
    tags=['灵神题单', '动态规划', '难度分 1334'],
    code='''
class Solution(object):
    def waysToSplitArray(self, nums):

        s = sum(nums)
        res = 0
        now = 0
        for index in range(len(nums) - 1):
            now += nums[index]
            if now >= s - now:
                res += 1
        
        return res
''',
    call='Solution().waysToSplitArray([3,-1,4,1,-2,5])',
    expect=3,
    views=[
        dict(type='text', fn=_text, size=28),
        dict(type='array', var='nums', label='nums（蓝 = 当前切点，绿 = 已在左边）', h=330, pointers={'index': 'pink'},
             color=_color, dim=lambda S, i, v: i == len(S['nums']) - 1),
    ],
    watch=[('s', 's', 'purple'), ('now', 'now', 'blue'), ('s - now', 's - now', 'orange'), ('res', 'res', 'green')],
    captions={
        's = sum': '先求出数组总和 `s = {s}`，以后右侧之和不用再加，直接 `s - 左侧和`',
        'now += ': '把 `nums[{index}] = {nums[index]}` 并入左边：`now = {B.now} + ({nums[index]}) = {now}`',
        'if now >=': '左边 `{now}`，右边 `s - now = {s} - {now} = {s - now}`：{"==左 ≥ 右，合法分割==" if now >= s - now else "左边更小，这个切点不行"}',
        'res += 1': '多一种合法分割：`res = {res}`',
        'return res': '`index` 只走到 `n-2`，保证右边非空；合法分割共 ==`{res}`== 种',
    },
    cards=dict(
        one_liner='右边之和 = 总和 − 左边之和，一趟遍历就够',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在下标 `i` 切开，前 `i+1` 个数之和 ≥ 其余数之和，即合法分割',
                 '`i` 右边至少要有一个元素；求合法分割的个数',
                 '示例：`[2,3,1,0]` → `2`'],
        quote='分割点左侧数字之和是一个典型的前缀和问题，而右侧数字之和则可以通过数组总和减去左侧数字之和得到。',
        quote_src='—— yiduobo 题解',
        idea=['先算好总和 `s`，再从左向右一趟遍历，用 `now` 记前缀和',
              '每一轮先把当前数加进 `now`，再比较 `now` 与 `s - now`',
              '遍历范围到 `len(nums) - 2` 为止，最后一个数的右边没有元素，不能当切点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`range(len(nums) - 1)`，保证右边至少有一个元素',
                 '先更新 `now` 再比较，因为切点 `i` 的左边包含 `nums[i]`',
                 '条件是「大于等于」，相等也算合法'],
    ),
)
