CONFIG = dict(
    num=3450, title='一张长椅上的最多学生', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 + 集合去重', tags=[],
    code='''
class Solution(object):
    def maxStudentsOnBench(self, students):
        
        cnt = {}
        for student, bench in students:
            if bench not in cnt:
                cnt[bench] = set()
            cnt[bench].add(student)
        
        res = 0
        for bench in cnt:
            res = max(res, len(cnt[bench]))
        return res
''',
    call='Solution().maxStudentsOnBench([[1,2],[2,2],[3,3],[1,3],[2,2],[4,3]])',
    expect=3,
    views=[
        dict(type='array', var='students', label='students（[学生, 长椅]）', cell=130, h=170,
             pointers={}, color=lambda S, i, v: 'blue' if 'student' in S and 'res' not in S and v == [S['student'], S['bench']] and i == S.get('_i', i) else None),
        dict(type='map', var='cnt', label='cnt（长椅 → 学生集合）', fmt=lambda k, v: f"长椅 {k}: {sorted(v)}", h=200, font=32),
        dict(type='text', h=80, size=30, fn=lambda S: f"当前最多的人数 ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=['student', 'bench', ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记录每张长椅上坐过哪些学生',
        'for student, bench in students': '取出一条记录：学生 `{student}` 坐在长椅 `{bench}`',
        'if bench not in cnt': '长椅 `{bench}` {"还没出现过" if bench not in B.cnt else "已经有集合了"}',
        'cnt[bench] = set()': '第一次见长椅 `{bench}`：建一个空集合',
        'cnt[bench].add(student)': '把学生 `{student}` 加入长椅 `{bench}` 的集合：{"集合自动去重，重复的不会增加" if len(cnt[bench]) == len(B.cnt.get(bench, set())) else "人数变成 " + str(len(cnt[bench]))}',
        'res = 0': '`res` 记录单张长椅上不同学生的最大人数',
        'for bench in cnt': '看长椅 `{bench}`',
        'res = max': '长椅 `{bench}` 有 `{len(cnt[bench])}` 个不同学生：`res = max({B.res}, {len(cnt[bench])}) = {res}`',
        'return res': '最多的一张长椅上有 =={ret}== 个不同学生',
    },
    cards=dict(
        one_liner='每张长椅一个集合，重复的学生自动去重',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`students[i] = [学生, 长椅]`，表示该学生坐在这张长椅上',
                 '求==单张长椅上不同学生==的最大数量，没有记录返回 `0`',
                 '同一学生在同一长椅可能出现多次，只算一次',
                 '本视频：`[[1,2],[2,2],[3,3],[1,3],[2,2],[4,3]]` → `3`'],
        quote='一趟遍历，对每张长椅都使用一个集合记录当前长椅上有哪些学生，其中最大的集合大小就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表的键是长椅，值是学生的 `set`',
              '`set.add` 重复元素不会增加大小，正好满足“每个学生只算一次”',
              '最后遍历每张长椅，取集合大小的最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '不能用列表计数：同一学生重复出现会被多算',
                 '没有任何记录时 `cnt` 为空，`res` 保持 `0`',
                 '原文已是 Python 3 可运行写法，仅保留代码不改'],
    ),
)
