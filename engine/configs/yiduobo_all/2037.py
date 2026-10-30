CONFIG = dict(
    num=2037, title='使每位学生都有座位的最少移动次数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='双数组排序 · 按序配对',
    tags=['灵神题单', '贪心与思维', '难度分 1357'],
    code='''
class Solution(object):
    def minMovesToSeat(self, seats, students):

        sorted_seats = sorted(seats)
        sorted_students = sorted(students)

        res = 0
        for index in range(len(sorted_seats)):
            res += abs(sorted_seats[index] - sorted_students[index])
        
        return res
''',
    call='Solution().minMovesToSeat([4,1,5,9], [1,3,2,6])',
    expect=7,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"第 {S['index']} 对：座位 `{S['sorted_seats'][S['index']]}`，学生 `{S['sorted_students'][S['index']]}`，要走 ==`{abs(S['sorted_seats'][S['index']] - S['sorted_students'][S['index']])}`== 步" if 'index' in S and 'sorted_students' in S else '先把座位和学生都按位置排序')),
        dict(type='array', var=lambda S: S.get('sorted_seats', S['seats']), pointers={'index': 'blue'}, h=200, label='座位（排序后）' ,
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
        dict(type='array', var=lambda S: S.get('sorted_students', S['students']), pointers={'index': 'pink'}, h=200, label='学生（排序后）',
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'sorted_seats = sorted': '座位从小到大排序 → `{sorted_seats}`',
        'sorted_students = sorted': '学生从小到大排序 → `{sorted_students}`：最靠边的学生对最靠边的座位',
        'res = 0': '`res` 累计总移动次数',
        'for index in range': lambda S, B, r: ('每一对都处理完，循环结束' if B.get('index') == S.index else f'处理第 `{S.index}` 对：`{S.sorted_seats[S.index]}` 号座位 ← `{S.sorted_students[S.index]}` 号学生'),
        'res += abs': '学生走到座位的距离 `|{sorted_seats[index]} − {sorted_students[index]}| = {abs(sorted_seats[index] - sorted_students[index])}` → `res` = =={res}==',
        'return res': '总共最少移动 =={res}== 次',
    },
    cards=dict(
        one_liner='最靠边的学生坐最靠边的座位',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数轴上有 `n` 个座位和 `n` 名学生，每次可把学生移动 1 格',
                 '每人一个座位，求最少总移动次数',
                 '示例：`seats=[4,1,5,9]`，`students=[1,3,2,6]` → `7`'],
        quote='将最靠边的学生安排到最靠边的座位上是非常直观的，因此可以将座位和学生都从小到大排序，然后一趟遍历逐个将学生安排到对应的座位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['座位和学生各排一次序，第 `i` 小的学生坐第 `i` 小的座位',
              '一趟遍历，累加每对的距离 `abs(座位 − 学生)`',
              '示例排序后：座位 `[1,4,5,9]`，学生 `[1,2,3,6]` → `0 + 2 + 2 + 3 = 7`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（两个排序后的新列表）',
                 '不能直接按输入顺序配对，必须先排序',
                 '交叉配对不会更优：交换任意两人的座位，总距离不会变小',
                 '原文为 Python 2 风格，本视频无需修改，直接运行'],
    ),
)
