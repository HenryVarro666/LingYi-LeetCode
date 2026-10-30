def _c(S, k):
    a = S['nums']
    return {1: a[-3] - a[0], 2: a[-2] - a[1], 3: a[-1] - a[2]}[k]


def _color(S, i, v):
    n = len(S['nums'])
    if 'cand3' in S:
        return 'green' if i in (n - 1, 2) else ('dim' if False else None)
    if 'cand2' in S:
        return 'green' if i in (n - 2, 1) else None
    if 'cand1' in S:
        return 'green' if i in (n - 3, 0) else None
    return None


CONFIG = dict(
    num=2567, title='修改两个元素的最小分数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序后三种修改方案',
    tags=['灵神题单', '难度分 1609'],
    code='''
class Solution(object):
    def minimizeSum(self, nums):

        nums.sort()

        cand1 = nums[-3] - nums[0]
        cand2 = nums[-2] - nums[1]
        cand3 = nums[-1] - nums[2]
        return min(cand1, cand2, cand3)
''',
    call='Solution().minimizeSum([1,4,7,8,5,10,3])',
    expect=5,
    views=[
        dict(type='text', size=28, fn=lambda S: ('最小得分改成 0 很容易，难的是压低“最大值 − 最小值”' if 'cand1' not in S else
            f"方案 1 改最大和次大 → `{S['cand1']}`" + (f"　方案 2 改最大和最小 → `{S['cand2']}`" if 'cand2' in S else '') + (f"　方案 3 改最小和次小 → `{S['cand3']}`" if 'cand3' in S else ''))),
        dict(type='array', var='nums', h=260, color=_color, label='nums（绿 = 本方案里留下的最大、最小值）'),
    ],
    watch=[('cand1', 'cand1', 'cyan'), ('cand2', 'cand2', 'blue'), ('cand3', 'cand3', 'pink')],
    captions={
        'nums.sort()': '排序：`{nums}`，最大、最小、次大、次小一目了然',
        'cand1 =': '方案 1：改掉最大和次大 → 剩下的最大是第三大 `{nums[-3]}`，最小是 `{nums[0]}`，差 =={cand1}==',
        'cand2 =': '方案 2：改掉最大和最小 → 剩下第二大 `{nums[-2]}` 减第二小 `{nums[1]}`，差 =={cand2}==',
        'cand3 =': '方案 3：改掉最小和次小 → 最大 `{nums[-1]}` 减第三小 `{nums[2]}`，差 =={cand3}==',
        'return min': '三种方案取最小 `min({cand1}, {cand2}, {cand3})` = =={ret}==（最小得分已被改成 0）',
    },
    cards=dict(
        one_liner='最小得分改成 0，再在三种改法里压低最大得分',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['分数 = 两数之差绝对值的最大值 + 最小值，最多改 2 个数',
                 '求能得到的最小分数',
                 '示例：`[1,4,7,8,5]` → `3`；本视频用 `[1,4,7,8,5,10,3]` → `5`'],
        quote='让两数之差绝对值的最小值最小是很容易的，只需让修改后数组中存在两个相同的数，这样一来两数之差绝对值的最小值就必然为0了。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小值部分：改出两个相同的数，直接是 `0`',
              '最大值部分：只能靠改掉最大或最小的数来缩小',
              '改两个数一共三种：改最大两个 / 一大一小 / 最小两个'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '三种方案分别对应 `nums[-3]-nums[0]`、`nums[-2]-nums[1]`、`nums[-1]-nums[2]`',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神用反证法说明为何只看两端；yiduobo 直接列三种方案'],
    ),
)
