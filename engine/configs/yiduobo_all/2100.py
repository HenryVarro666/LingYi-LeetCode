CONFIG = dict(
    num=2100, title='适合野炊的日子', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举山谷 + 预处理两侧长度',
    tags=['灵神题单·动态规划', '难度分 1702'],
    code='''
class Solution(object):
    def goodDaysToRobBank(self, security, time):

        n = len(security)
        left = [0] * n
        for index in range(1, n):
            if security[index - 1] >= security[index]:
                left[index] = left[index - 1] + 1

        right = [0] * n
        for index in range(n - 2, -1, -1):
            if security[index + 1] >= security[index]:
                right[index] = right[index + 1] + 1

        res = []
        for index in range(n):
            if left[index] >= time and right[index] >= time:
                res.append(index)
        
        return res
''',
    call='Solution().goodDaysToRobBank([5,3,3,3,5,6,2], 2)',
    expect=[2, 3],
    views=[
        dict(type='array', var='security', label='security', h=200, cell=80, pointers={'index': 'blue'},
             color=lambda S, j, v: 'green' if j in S.get('res', []) else None),
        dict(type='array', var='left', label='left[i]：以 i 结尾、连续下降的天数', h=150, cell=80),
        dict(type='array', var='right', label='right[i]：以 i 开头、连续上升的天数', h=150, cell=80),
    ],
    watch=[('index', 'index', 'blue'), 'time', ('res', 'res', 'green')],
    captions={
        'left = [0] * n': '`left[i]`：到 `i` 为止连续不增的天数（相邻对数），第 0 天前面没有，记 0',
        'if security[index - 1] >= security[index]': '前一天 `{security[index-1]}` 与今天 `{security[index]}`：{"前一天不低，下降段延长" if security[index-1] >= security[index] else "今天更高，下降段断开，left 保持 0"}',
        'left[index] = left[index - 1] + 1': '`left[{index}] = left[{index-1}] + 1` = =={left[index]}==',
        'right = [0] * n': '`right[i]`：从 `i` 起连续不减的天数，要从右往左扫',
        'if security[index + 1] >= security[index]': '后一天 `{security[index+1]}` 与今天 `{security[index]}`：{"后一天不低，上升段延长" if security[index+1] >= security[index] else "后一天更低，上升段断开，right 保持 0"}',
        'right[index] = right[index + 1] + 1': '`right[{index}] = right[{index+1}] + 1` = =={right[index]}==',
        'res = []': '预处理完毕，开始枚举每个山谷位置',
        'for index in range(n)': '枚举第 `{index}` 天作为山谷',
        'if left[index] >= time': '`left[{index}] = {left[index]}`，`right[{index}] = {right[index]}`，time = {time}：{"两边都 ≥ time，适合" if left[index] >= time and right[index] >= time else "有一边不足 time，不适合"}',
        'res.append(index)': '第 `{index}` 天适合 → `res = {res}`',
        'return res': '适合的日子：`{res}`',
    },
    cards=dict(
        one_liner='枚举每个山谷，看两侧的下降和上升够不够 time',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`security[i]` 是第 `i` 天的出行指数，给定 `time`',
                 '第 `i` 天前 `time` 天不增、后 `time` 天不减，则适合野炊（原题叫打劫银行）',
                 '示例：`[5,3,3,3,5,6,2], time = 2` → `[2,3]`'],
        quote='题目要求找出所有的山谷，要求山谷两侧下降的长度都大于等于time，那么一个自然的想法就是枚举所有山谷的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left[i]`：以 `i` 结尾的连续下降长度，`security[i-1] >= security[i]` 就继承加一，否则为 0',
              '`right[i]`：以 `i` 开头的连续上升长度，反向一趟求出',
              '枚举每一天，`left` 与 `right` 都 `>= time` 就收下'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这里 `left/right` 记的是相邻对数，断开时为 0，所以和 `time` 直接比较',
                 '`time = 0` 时每一天都满足，`left/right` 默认的 0 恰好够用',
                 '原文为 Python 2 写法，本份代码无需修改即可在 Python 3 运行',
                 '和 2420 同模板：2420 的计数从 1 起算，边界差一格'],
    ),
)
