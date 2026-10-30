def _fb():
    raise ValueError  # 让引擎退回默认字幕


def _first_right(S, B, ret):
    if S.index == len(S.nums) - 1:
        return f'第二趟从右往左：`index = {S.index}`，`ma` 现在表示右侧已见的最大值'
    _fb()


def _first_collect(S, B, ret):
    if S.index == 0:
        return f'第三趟：正序收集，`index = 0`，看 `flag[0]` 是否被标记'
    _fb()


def _text(S):
    if 'ma' not in S:
        return ''
    return f"当前最大值 `ma = {S['ma']}`，有效标记 `flag` 中 True 的位置会留下来"


def _color(S, i, v):
    if 'index' not in S or 'flag' not in S:
        return None
    if i == S['index']:
        return 'blue'
    return 'green' if S['flag'][i] else None


CONFIG = dict(
    num=3912, title='数组中的有效元素', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='正反两趟前缀/后缀最大值',
    tags=['灵神题单', '动态规划', '难度分 1273'],
    code='''
class Solution(object):
    def findValidElements(self, nums):
        
        n = len(nums)
        flag = [False] * n
        ma = 0
        for index in range(n):
            if nums[index] > ma:
                flag[index] = True
                ma = nums[index]
        
        ma = 0
        for index in range(n - 1, -1, -1):
            if nums[index] > ma:
                flag[index] = True
                ma = nums[index]
        
        res = []
        for index in range(n):
            if flag[index]:
                res.append(nums[index])
        
        return res
''',
    call='Solution().findValidElements([3,1,4,1,5,2,2])',
    expect=[3, 4, 5, 2],
    views=[
        dict(type='text', fn=_text, size=28),
        dict(type='array', var='nums', label='nums', h=300, pointers={'index': 'blue'}, color=_color),
        dict(type='array', var='flag', label='flag（True = 有效）', h=200,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='res', label='res', h=200),
    ],
    watch=[('index', 'index', 'blue'), ('ma', 'ma', 'purple'), ('res', 'res', 'green')],
    captions={
        'if nums[index] > ma': '`nums[{index}] = {nums[index]}` 和已见最大值 `ma = {ma}` 比：{"==严格更大，是新的最大值=="  if nums[index] > ma else "不比它大，什么都不做"}',
        'flag[index] = True': '`nums[{index}]` 严格大于前面（或后面）所有元素 → `flag[{index}] = True`',
        'ma = nums[index]': '最大值更新：`ma = {ma}`',
        12: '第一趟结束（左侧最大值），清零 `ma`，准备从右往左再走一趟',
        13: _first_right,
        19: _first_collect,
        'if flag[index]': '`flag[{index}]` 是 {flag[index]}：{"==有效，收进答案==" if flag[index] else "无效，跳过"}',
        'res.append': '加入答案：`res = {res}`',
        'return res': '按原来的顺序收齐了有效元素，返回 `{res}`',
    },
    cards=dict(
        one_liner='有效元素 = 前缀里的新最大值，或后缀里的新最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums[i]` 严格大于左边所有元素，或严格大于右边所有元素，就是有效元素',
                 '要求按原顺序返回所有有效元素',
                 '示例：`[1,2,4,2,3,2]` → `[1,2,4,3,2]`'],
        quote='有效元素的条件，实际上就是要求这个元素要么是以该元素结尾的前缀的最大值，要么是以该元素开头的后缀的最大值。',
        quote_src='—— yiduobo 题解',
        idea=['正着扫一趟，维护前缀最大值 `ma`，比它大就标记并更新',
              '反着扫一趟，同样维护后缀最大值，再标记一次',
              '最后按下标顺序，把被标记的元素收进 `res`'],
        summary=['时间 `O(n)`，空间 `O(n)`（`flag` 数组）',
                 '两趟之间别忘了把 `ma` 重置为 0',
                 '严格大于：和已见最大值相等时不算新的最大值',
                 '标记和收集分开写，保证答案顺序和原数组一致'],
    ),
)
