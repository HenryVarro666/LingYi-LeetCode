STU = [1, 1, 1, 0, 0, 1]
SAN = [1, 0, 0, 0, 1, 1]

CONFIG = dict(
    num=1700, title='无法吃午餐的学生数量', difficulty='Easy', category='模拟',
    author='yiduobo', technique='计数代替模拟',
    tags=[],
    code='''
class Solution(object):
    def countStudents(self, students, sandwiches):

        n = len(students)
        one_students = sum(students)
        zero_students = n - one_students

        one = zero = 0
        for index in range(n):
            sandwich = sandwiches[index]
            if sandwich == 0:
                zero += 1
            else:
                one += 1
            
            if one > one_students or zero > zero_students:
                return n - index
        
        return 0
''',
    call='Solution().countStudents([1,1,1,0,0,1], [1,0,0,0,1,1])',
    expect=3,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"学生需要：喜欢 1 的 `{S['one_students']}` 人，喜欢 0 的 `{S['zero_students']}` 人" if 'zero_students' in S else '')),
        dict(type='array', var='students', label='students（队列里的学生，喜欢 0 或 1）', h=200),
        dict(type='array', var='sandwiches', label='sandwiches（栈顶在左边）', pointers={'index': 'blue'}, h=260,
             color=lambda S, i, v: ('green' if 'index' in S and i < S['index'] else None),
             dim=lambda S, i, v: False),
        dict(type='text', size=26, fn=lambda S: (f"从栈顶数到现在：三明治 1 有 `{S['one']}` 个（学生 {S['one_students']}），三明治 0 有 `{S['zero']}` 个（学生 {S['zero_students']}）" if 'one' in S and 'zero_students' in S else '')),
    ],
    watch=[('one_students', 'one_students', 'cyan'), ('zero_students', 'zero_students', 'orange'),
           ('one', 'one', 'cyan'), ('zero', 'zero', 'orange'), ('index', 'index', 'blue')],
    captions={
        'n = len': '一共 `{n}` 个学生、`{n}` 个三明治',
        'one_students = sum': '喜欢 1 的学生有 `{one_students}` 人（students 求和）',
        'zero_students = n': '剩下的都喜欢 0：`{n} - {one_students} = {zero_students}` 人',
        'one = zero = 0': '`one`、`zero`：从栈顶往下，已经出现的两种三明治各有多少个',
        'for index': '看第 `{index}` 个三明治（从栈顶数起）',
        'sandwich = ': '这个三明治是 `{sandwich}`',
        'zero += 1': '三明治 0 又多一个：`zero` = {zero}',
        'one += 1': '三明治 1 又多一个：`one` = {one}',
        'if one > one_students': lambda S, B, r: (
            f'`one = {S.one} > {S.one_students}` 或 `zero = {S.zero} > {S.zero_students}` → ==成立==：这种三明治比想吃的学生还多，学生轮流看一圈也没人要，栈顶卡死'
            if (S.one > S.one_students or S.zero > S.zero_students)
            else f'`one = {S.one} ≤ {S.one_students}`，`zero = {S.zero} ≤ {S.zero_students}` → 不成立：想吃的学生还够，这个三明治总会被吃掉'),
        'return n - index': '从第 `{index}` 个三明治起都没人吃：剩下 `{n} - {index}` = =={n - index}== 个，学生也剩这么多',
        'return 0': '三明治全被吃完，返回 `0`',
    },
    cards=dict(
        one_liner='学生轮流查看，数一数就知道哪个三明治会卡住',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['学生排成队列，三明治叠成栈，只有 `0`（圆）和 `1`（方）两种',
                 '队首学生喜欢栈顶就拿走，否则排到队尾；没人再愿意拿时停止',
                 '求最后吃不上午餐的学生数。示例：`[1,1,1,0,0,1]`、`[1,0,0,0,1,1]` → `3`'],
        quote='只有当栈顶三明治为1，学生全都是0，或者栈顶三明治为0，学生全都是1时才会出现无法吃午餐的状况。',
        quote_src='—— yiduobo 题解原文',
        idea=['学生会轮流查询：只要还有一位学生喜欢栈顶的种类，这个三明治就一定被吃掉',
              '所以从栈顶往下数，==某种三明治的个数超过喜欢它的学生数==，就卡住了',
              '卡住时剩下的三明治数，就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`，不用真的模拟排队',
                 '学生顺序完全不影响结果，只和两种喜好的人数有关',
                 '判断用 `>`：个数相等时恰好够吃，不会卡',
                 '全部吃完时循环不会 return，最后返回 `0`'],
    ),
)
