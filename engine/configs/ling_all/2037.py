CONFIG = dict(
    num=2037, title='使每位学生都有座位的最少移动次数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序后一一配对（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1357'],
    code='''
class Solution:
    def minMovesToSeat(self, seats: List[int], students: List[int]) -> int:
        ans = 0
        seats.sort()
        students.sort()
        for i, p in enumerate(seats):
            ans += abs(p - students[i])
        return ans
''',
    call='Solution().minMovesToSeat([4,1,5,9], [1,3,2,6])',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 对：座位 `{S['p']}`，学生 `{S['students'][S['i']]}` → 移动 `|{S['p']} − {S['students'][S['i']]}|` = =={abs(S['p'] - S['students'][S['i']])}=="
                                        if 'p' in S and 'i' in S else '先把座位和学生都排好序')),
        dict(type='array', var='seats', pointers={'i': 'blue'}, label='seats（座位）', h=150),
        dict(type='array', var='students', pointers={'i': 'pink'}, label='students（学生）', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'seats.sort()': '座位从小到大排序：`{seats}`',
        'students.sort()': '学生也从小到大排序：`{students}`。==第 i 个学生坐第 i 个座位==',
        'ans += abs': '学生 `{students[i]}` 走到座位 `{p}`，用 `{abs(p - students[i])}` 步；`ans = {B.ans} + {abs(p - students[i])} = {ans}`',
        'return ans': '每一对的距离加起来就是最少移动次数：`{ans}`',
    },
    cards=dict(
        one_liner='座位、学生各自排序，第 i 个对第 i 个',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['数轴上有 `n` 个座位、`n` 名学生，每次可把一名学生左右挪 1 格',
                 '要让每人一个座位，求最少总移动次数',
                 '示例：`seats=[4,1,5,9]`, `students=[1,3,2,6]` → `7`'],
        quote='将座位和学生位置排序后，第 i 个学生可以对应第 i 个座位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['座位和学生一样多，==一个萝卜一个坑==',
              '交换任意两个学生的座位不会更少（画一画可证），所以排序后一一对应最优',
              '累加位置之差的绝对值即答案'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（Go 里自写的 abs 用 Python 内置 abs）',
                 '时间 `O(n log n)`，主要是排序',
                 '易错点：两个数组都要排序，只排一个会配错',
                 '同类：双序列配对，先排序再贪心'],
    ),
)
