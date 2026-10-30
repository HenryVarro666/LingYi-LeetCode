CONFIG = dict(
    num=3285, title='找到稳定山的下标', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历模拟',
    code='''
class Solution(object):
    def stableMountains(self, height, threshold):

        res = []
        for index in range(1, len(height)):
            if height[index - 1] > threshold:
                res.append(index)

        return res
''',
    call='Solution().stableMountains([10,1,10,1,10,2,2], 3)',
    expect=[1, 3, 5],
    views=[
        dict(type='array', var='height', label='height（红 = 这一步看的左邻居）', pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if v > S['threshold'] else 'pink') if 'index' in S and 'threshold' in S and i == S['index'] - 1 else None,
             h=260),
        dict(type='array', var='res', label='res（稳定山的下标）', h=160),
    ],
    watch=['threshold', 'index', ('res', 'res', 'green')],
    captions={
        'for index in range': lambda S, B, r: '从下标 1 开始：下标 0 没有左邻居，不可能稳定' if S.index == 1 else f'`index` → {S.index}',
        'if height[index - 1] > threshold': '看第 `{index}` 座山的左邻居 `height[{index-1}] = {height[index-1]}`，`> {threshold}`？{"成立" if height[index-1] > threshold else "不成立，跳过"}',
        'res.append(index)': '左邻居够高 → 第 `{index}` 座山稳定，加入 `res` = =={res}==',
        'return res': '遍历完，稳定的山：=={res}==',
    },
    cards=dict(
        one_liner='直接照题意一趟遍历：左邻居高于阈值就收下',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['左邻居 ==严格大于== `threshold` 的山是稳定的，下标 0 不算',
                 '返回所有稳定山的下标',
                 '本视频：`[10,1,10,1,10,2,2], threshold=3` → `[1,3,5]`'],
        quote='直接按照题目要求，从下标1开始向后一趟遍历模拟计算就行了：对于当前遍历到的第index座山，若height[index] > threshold，那么就将index加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`index` 从 1 到 `n-1`，逐座山检查',
              '代码里查的是 `height[index - 1]`，即左邻居，和题意一一对应',
              '满足就 `res.append(index)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：循环从 1 开始，否则 `height[-1]` 会取到最后一座山',
                 '易错点：严格大于，不是大于等于',
                 '原文为 Python 2 风格写法，代码无需改动'],
    ),
)
