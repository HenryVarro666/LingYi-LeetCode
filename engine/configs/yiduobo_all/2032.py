CONFIG = dict(
    num=2032, title='至少在两个数组中出现的值', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='值域枚举 + 三个集合',
    code='''
class Solution(object):
    def twoOutOfThree(self, nums1, nums2, nums3):

        set1 = set(nums1)
        set2 = set(nums2)
        set3 = set(nums3)

        res = []
        for num in range(1, 101):
            score = 0
            if num in set1:
                score += 1
            if num in set2:
                score += 1
            if num in set3:
                score += 1
            
            if score >= 2:
                res.append(num)

        return res
''',
    call='Solution().twoOutOfThree([1,1,3,2], [2,3], [3])',
    expect=[2, 3],
    views=[
        dict(type='text', fn=lambda S: (f"枚举 `num = {S['num']}`：出现在 =={S['score']}== 个数组里" if 'num' in S and 'score' in S else '先把三个数组变成集合'), size=28, h=60),
        dict(type='set', var='set1', label='set1（nums1 去重）', fmt=lambda x: str(x), h=110),
        dict(type='set', var='set2', label='set2（nums2 去重）', fmt=lambda x: str(x), h=110),
        dict(type='set', var='set3', label='set3（nums3 去重）', fmt=lambda x: str(x), h=110),
        dict(type='array', var='res', label='res（答案，至少在两个数组出现）', h=150, cell=70),
    ],
    watch=[('num', 'num', 'blue'), ('score', 'score', 'orange'), ('res', 'res', 'green')],
    max_steps=60,
    captions={
        'set1 = set': '`nums1` 去重成集合：判断“出现过吗”只要 `O(1)`',
        'set2 = set': '`nums2` 去重成集合',
        'set3 = set': '`nums3` 去重成集合',
        'res = []': '`res` 存答案',
        'for num in range': '值域只有 1 到 100，==直接枚举每个可能的值== `num = {num}`',
        'score = 0': '`score` 统计 `{num}` 出现在几个数组里，先清零',
        'if num in set1': lambda S, B, ret: f"`{S.num}` 在 set1 里吗？" + ('在 → 计一次' if S.num in S.set1 else '不在'),
        'if num in set2': lambda S, B, ret: f"`{S.num}` 在 set2 里吗？" + ('在 → 计一次' if S.num in S.set2 else '不在'),
        'if num in set3': lambda S, B, ret: f"`{S.num}` 在 set3 里吗？" + ('在 → 计一次' if S.num in S.set3 else '不在'),
        'score += 1': '`score` → {score}',
        'if score >= 2': lambda S, B, ret: (f'`score = {S.score} >= 2` → ==至少在两个数组里=={"，要加入答案" if S.score >= 2 else ""}' if S.score >= 2 else f'`score = {S.score} < 2` → 不要'),
        'res.append(num)': '`{num}` 加入答案：`res = {res}`（每个值只枚举一次，天然不重复）',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='值域只有 1 到 100：逐个枚举，数一数它出现在几个数组里',
        complexity='时间 `O(V + n)`，`V = 100`；空间 `O(n)`',
        problem=['给三个整数数组，返回==至少在两个数组中出现==的所有值，答案元素互不相同，顺序任意',
                 '示例：`[1,1,3,2]`、`[2,3]`、`[3]` → `[3,2]`',
                 '本视频运行的就是这组输入，答案 `[2,3]`'],
        quote='由于题目中数值的范围在1到100以内，那么可以直接从1到100开始进行枚举，判断当前这个数是否出现在至少两个数组内，如果满足就将其加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `set` 去重：同一个数组里出现多次只算一次',
              '从 1 枚举到 100，`score` 记它在几个集合里',
              '`score >= 2` 就加入答案；枚举本身保证了答案不重复'],
        summary=['时间 `O(V + n)`，空间 `O(n)`',
                 '易错：题面“不同”指的是答案内部元素互不相同；重复出现在同一数组不能算两次，所以要先转集合',
                 '值域枚举后每个值只会被处理一次，所以不用再去重',
                 '视频中枚举到 100 的中间步骤做了快进，结果在枚举到 3 时就已经齐了'],
    ),
)
