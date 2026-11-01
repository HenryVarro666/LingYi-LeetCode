CONFIG = dict(
    num=2100, title='适合野炊的日子', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='预处理左右递减/递增长度',
    tags=['专题：前后缀分解', '难度分 1702'],
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
        dict(type='array', var='security', label='security', pointers={'index': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if 'res' in S and i in S['res'] else None),
        dict(type='array', var='left', label='left：以它结尾的递减长度', pointers={'index': 'blue'}, h=170,
             color=lambda S, i, v: 'cyan' if v >= S['time'] else None),
        dict(type='array', var='right', label='right：以它开头的递增长度', pointers={'index': 'pink'}, h=170,
             color=lambda S, i, v: 'cyan' if v >= S['time'] else None),
        dict(type='array', var='res', label='res', h=150),
    ],
    watch=['index', ('time', 'time', 'cyan'), ('res', 'res', 'green')],
    captions={
        'left = [0] * n': '`left[index]`：以第 index 天结尾的最长递减（非递增）长度，先全设 0',
        'if security[index - 1] >= security[index]': '前一天 `{security[index - 1]}` 与今天 `{security[index]}`：{"前一天不小于今天，递减能延续" if security[index - 1] >= security[index] else "递减断了，left 保持 0"}',
        'left[index] = left[index - 1] + 1': '`left[{index}] = left[{index - 1}] + 1` → =={left[index]}==',
        'right = [0] * n': '`right[index]`：以第 index 天开头的最长递增（非递减）长度，反向一趟遍历求',
        'if security[index + 1] >= security[index]': '后一天 `{security[index + 1]}` 与今天 `{security[index]}`：{"后一天不小于今天，递增能延续" if security[index + 1] >= security[index] else "递增断了，right 保持 0"}',
        'right[index] = right[index + 1] + 1': '`right[{index}] = right[{index + 1}] + 1` → =={right[index]}==',
        'for index in range(n):': '枚举每个位置当山谷',
        'if left[index] >= time and right[index] >= time': '`left = {left[index]}`，`right = {right[index]}`，都 `>= {time}`？→ {"是，山谷成立" if left[index] >= time and right[index] >= time else "否"}',
        'res.append(index)': '第 `{index}` 天两侧下降/上升长度都够 → 加入 `{res}`',
    },
    cards=dict(
        one_liner='枚举每个山谷，看两侧下降、上升的长度够不够 time',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['第 i 天前 time 天非递增、后 time 天非递减，就适合打劫（野炊）',
                 '返回所有这样的日子',
                 '示例：`[5,3,3,3,5,6,2], time=2` → `[2,3]`'],
        quote='题目要求找出所有的山谷，要求山谷两侧下降的长度都大于等于time，那么一个自然的想法就是枚举所有山谷的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left[i]`：以 i 结尾的递减子串长度，前一天不小于今天就 `+1`，否则归 0',
              '`right[i]`：以 i 开头的递增子串长度，从后往前同理',
              '最后一遍扫描，两个长度都 `>= time` 的位置就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个数组）',
                 '易错点：相等也算递减/递增，所以比较用 `>=`',
                 '`time = 0` 时每一天都满足，不用特判',
                 '对比灵神：灵神把 pre 压成一个变量，并只枚举到 `n - time`'],
    ),
)
