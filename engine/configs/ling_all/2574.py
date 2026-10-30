CONFIG = dict(
    num=2574, title='左右元素和的差值', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 原地写答案', tags=['难度分 1206'],
    code='''
class Solution:
    def leftRightDifference(self, nums: List[int]) -> List[int]:
        total = sum(nums)

        left_sum = 0
        for i, x in enumerate(nums):
            nums[i] = abs(left_sum * 2 + x - total)
            left_sum += x
        return nums
''',
    call='Solution().leftRightDifference([10,4,8,3])',
    expect=[15, 1, 11, 22],
    views=[
        dict(type='text', fn=lambda S: f"右和 = `{S['total']} − {S['left_sum']} − {S['x']}` = {S['total']-S['left_sum']-S['x']}；差 = `|{S['left_sum']} − {S['total']-S['left_sum']-S['x']}|` = =={abs(S['left_sum']*2+S['x']-S['total'])}==" if S.get('_line') == 7 and 'x' in S else '右和 = 总和 − 左和 − 当前数'),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=300, label='nums（左边已被答案覆盖）',
             color=lambda S, i, v: ('blue' if i == S['i'] else 'green' if i < S['i'] else None) if 'i' in S else None),
    ],
    watch=['total', ('left_sum', 'left_sum', 'cyan'), ('x', 'x', 'blue')],
    captions={
        'total = sum': '先求总和 `total = {total}`，右和不用再算：`右和 = total − 左和 − nums[i]`',
        'left_sum = 0': '`left_sum`：下标 `i` 左边的元素和，一开始是 0',
        'nums[i] = abs': '`|左和 − 右和|` 化简为 `|2·左和 + x − total|` = `|{left_sum*2} + {x} − {total}|` = =={nums[i]}==，直接写回 `nums[{i}]`',
        'left_sum += x': '`x = {x}` 变成下一个位置的左侧：`left_sum` = {left_sum}（原值已读走，覆盖安全）',
        'return nums': '`nums` 本身已经是答案，返回 `{nums}`',
    },
    cards=dict(
        one_liner='右和 = 总和 − 左和 − 当前，差值一步算出',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`answer[i] = |左侧元素和 − 右侧元素和|`', '示例：`[10,4,8,3]` → `[15,1,11,22]`'],
        quote='所以 |leftSum[i] − rightSum[i]| = |2·leftSum[i] + nums[i] − total|。代码实现时，可以直接把答案保存到 nums 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`左 + 当前 + 右 = total`，右和用不着单独求', '边遍历边累加 `left_sum`，答案原地写进 `nums`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先用 `x` 算答案、写回 `nums[i]`，再累加 `x`，顺序不能反',
                 '原地修改了输入；不想改输入就另开 `answer` 数组',
                 '同类：1991、724，前后缀分解专题'],
    ),
)
