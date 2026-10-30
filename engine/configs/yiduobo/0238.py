NUMS = [2, 3, 4, 5]
ANS = [60, 40, 30, 24]


def _nums_color(S, j, v):
    k = S.get('index')
    if k is None:
        return None
    if 'now' in S:                      # 第 2 趟：左边在 res[k-1] 里，右边在 now 里
        return 'blue' if j < k else ('pink' if j > k else None)
    return 'blue' if j <= k else None   # 第 1 趟：res[k] 是 nums[0..k] 之积


def _res_color(S, j, v):
    if 'now' in S and 'index' in S and v == ANS[j] and (j >= S['index'] or j == 0):
        return 'green'
    return None


def _info(S):
    k = S.get('index')
    if k is None or 'res' not in S:
        return ''
    if 'now' in S:
        return f'蓝 = 左边（`res[{k - 1}]` 里的前缀积），粉 = 右边（`now = {S["now"]}`）'
    return f'蓝 = `res[{k}]` 覆盖的前缀 `nums[0..{k}]`'


CONFIG = dict(
    num=238, title='除了自身以外数组的乘积', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='前缀积存答案数组 + 后缀积变量',
    code='''
class Solution(object):
    def productExceptSelf(self, nums):
        if len(nums) < 2:
            return nums

        res = [nums[0]]
        for index in range(1, len(nums)):
            res.append(res[index - 1] * nums[index])

        now = 1
        for index in range(len(nums) - 1, 0, -1):
            res[index] = res[index - 1] * now
            now *= nums[index]

        res[0] = now

        return res
''',
    call=f'Solution().productExceptSelf({NUMS})',
    expect=ANS,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var='nums', pointers={'index': 'yellow'}, color=_nums_color, cell=110, h=200),
        dict(type='array', var='res', label='res（绿 = 已经是最终答案）', pointers={'index': 'yellow'}, color=_res_color,
             min_slots=4, cell=110, h=200),
    ],
    watch=[('index', 'index', 'yellow'), ('now', 'now', 'pink'), ('res', 'res', 'blue')],
    captions={
        'if len(nums) < 2': '长度 ≥ 2，正常处理',
        'res = [nums[0]]': '第 1 趟：`res[k]` 存==前缀乘积== `nums[0] × … × nums[k]`（包含 `nums[k]`）',
        'for index in range(1': lambda S, B, ret: (f'从头到尾：`index = {S.index}`' if 'index' not in B or S.index != B.index
                                                   else '前缀乘积算好了'),
        'res.append': '`res[{index}] = res[{index - 1}] × nums[{index}] = {res[index - 1]} × {nums[index]} = {res[index]}`',
        'now = 1': '第 2 趟：不再开数组，用==一个数 now== 维护后缀乘积，从 1 开始',
        'for index in range(len(nums) - 1': lambda S, B, ret: ('循环只到 `index = 1`，`res[0]` 单独处理'
                                                               if S.index == B.index and B.now != 1 else f'从尾到头：`index = {S.index}`'),
        'res[index] = res[index - 1] * now': '`res[{index - 1}]`（前缀积 `{res[index - 1]}`）× `now`（后缀积 `{now}`）→ `res[{index}] = {res[index]}`，==这一位算完了==',
        'now *= nums[index]': '`now = {B.now} × {nums[index]} = {now}`：后缀积再往左扩一个',
        'res[0] = now': '`res[0]` 左边没有数：答案就是整段后缀积 `now = {now}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='先把前缀乘积存进答案数组，再从尾到头用一个数 now 乘上后缀乘积',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['返回数组 `answer`：`answer[i]` = 除 `nums[i]` 外其余各元素的乘积',
                 '==不能用除法==，时间要求 `O(n)`',
                 '示例：`[1,2,3,4]` → `[24,12,8,6]`',
                 '演示用 `[2,3,4,5]` → `[60,40,30,24]`'],
        quote='要达成题目要求的O(1)空间，那么可以运用答案数组来储存其中一个乘积的结果，然后从另一侧使用一个数维护当前的乘积来替代数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 k 个答案从 k 处分开，是==两个连续乘法==：前缀积 × 后缀积',
              '第 1 趟：答案数组 `res[k]` 先存前缀积 `nums[0] × … × nums[k]`',
              '第 2 趟从尾到头：`res[k] = res[k-1] × now`，`now` 是 `k+1` 到末尾的后缀积'],
        summary=['时间 `O(n)`，空间 `O(1)`：答案数组不算额外空间',
                 '必须==从尾到头==：这样用到的 `res[k-1]` 还没被覆盖，仍是前缀积',
                 '循环只到 `index = 1`，最后 `res[0] = now` 别忘了',
                 '对比灵神：灵神先存后缀积再正着乘前缀；yiduobo 方向相反，前缀积还含自身',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
