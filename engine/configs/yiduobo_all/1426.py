def _cur(S):
    if 'num' not in S:
        return '先把所有数放进集合，之后每个数只需 O(1) 查 `num + 1`'
    ok = S['num'] + 1 in S['num_set']
    return f"当前 `num = {S['num']}`：`{S['num'] + 1}` {'==在==' if ok else '==不在=='}集合中，目前 `res = {S['res']}`"


CONFIG = dict(
    num=1426, title='数元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 查 num+1',
    tags=[],
    code='''
class Solution(object):
    def countElements(self, arr):

        num_set = set(arr)
        res = 0
        for num in arr:
            if num + 1 in num_set:
                res += 1
        
        return res
''',
    call='Solution().countElements([1, 3, 2, 6, 0, 8, 5])',
    expect=4,
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 当前数，绿 = 它的 +1 在集合里）', cell=90, h=200,
             color=lambda S, i, v: (None if 'num' not in S else ('green' if S['num'] + 1 in S['num_set'] else 'pink') if v == S['num'] else None)),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: str(x), h=170, font=34),
        dict(type='text', h=100, size=30, fn=_cur),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'num_set = set(arr)': '用集合装下所有数，`num_set` = {sorted(num_set)}：查找一个数只要 `O(1)`',
        'res = 0': '`res` 统计满足条件的元素个数',
        'for num in arr': '遍历 arr 中的每个元素，包括重复的：`num = {num}`',
        'if num + 1 in num_set': lambda S, B, r: (f'`{S.num} + 1 = {S.num + 1}` 在集合里 → 成立，`{S.num}` 要被计数'
                                                  if S.num + 1 in S.num_set else f'`{S.num} + 1 = {S.num + 1}` 不在集合里 → 不成立，不计数'),
        'res += 1': '`{num}` 有 `{num + 1}` 作伴，`res` = =={res}==',
        'return res': '一共有 `{ret}` 个元素满足 `x + 1` 也在 arr 中',
    },
    cards=dict(
        one_liner='先用集合存下所有数，再逐个查 num + 1 在不在',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `arr`，统计有多少个元素 `x` 满足 `x + 1` 也在 `arr` 中',
                 '重复的元素要分别统计',
                 '示例：`[1,2,3]` → `2`；`[1,1,3,3,5,5,7,7]` → `0`',
                 '本视频：`[1,3,2,6,0,8,5]` → `4`'],
        quote='使用集合统计所有出现的数，接下来一趟遍历，对于当前遍历到的数num，检测num + 1是否存在与集合中并更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组里要反复问「某个数在不在」，用集合把查询降到 `O(1)`',
              '遍历的是原数组 `arr`，所以重复元素各算一次',
              '集合只记存在性，不影响计数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '遍历 `arr` 而不是 `num_set`，否则重复元素会漏算',
                 '题面为根据文章和 LeetCode 原题补写（本库未收录题面）',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
