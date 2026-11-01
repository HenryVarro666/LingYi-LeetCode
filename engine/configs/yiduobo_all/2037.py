CONFIG = dict(
    num=2037, title='使每位学生都有座位的最少移动次数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='排序后逐个安排',
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
    call='Solution().minMovesToSeat([3,1,5,8,2], [2,7,4,1,9])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"学生 `{S['sorted_students'][S['index']]}` → 座位 `{S['sorted_seats'][S['index']]}`，距离 `|{S['sorted_seats'][S['index']]} − {S['sorted_students'][S['index']]}|` = =={abs(S['sorted_seats'][S['index']] - S['sorted_students'][S['index']])}=="
                                        if 'index' in S and 'sorted_students' in S else '最靠边的学生坐最靠边的座位')),
        dict(type='array', var='sorted_seats', pointers={'index': 'blue'}, label='sorted_seats', h=150),
        dict(type='array', var='sorted_students', pointers={'index': 'pink'}, label='sorted_students', h=150),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'sorted_seats = sorted': '座位从小到大：`{sorted_seats}`',
        'sorted_students = sorted': '学生从小到大：`{sorted_students}`，最靠边的对最靠边的',
        'res = 0': '`res` 累计移动次数',
        'res += abs': '第 `{index}` 个学生去第 `{index}` 个座位：`|{sorted_seats[index]} − {sorted_students[index]}| = {abs(sorted_seats[index] - sorted_students[index])}`，`res` → =={res}==',
        'return res': '逐个安排完毕，一共移动 `{res}` 次',
    },
    cards=dict(
        one_liner='最靠边的学生坐最靠边的座位',
        complexity='时间 `O(n log n)`，空间 `O(n)`（排序副本）',
        problem=['数轴上 `n` 个座位、`n` 名学生，每次移动 1 格',
                 '每人一个座位，求最少总移动次数',
                 '本视频：`seats=[3,1,5,8,2]`, `students=[2,7,4,1,9]` → `4`'],
        quote='将最靠边的学生安排到最靠边的座位上是非常直观的，因此可以将座位和学生都从小到大排序，然后一趟遍历逐个将学生安排到对应的座位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['从最边上看：最左的学生只能配某个座位，配最左的座位最省',
              '依次往里推，就是排序后同下标配对',
              '用 `sorted` 生成副本，不改原数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：座位和学生都要排序',
                 '代码本身已是 Python 3 可运行写法，无需改动'],
    ),
)
