CONFIG = dict(
    num=1207, title='独一无二的出现次数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 + 集合判重',
    code='''
class Solution(object):
    def uniqueOccurrences(self, arr):

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        cnt_set = set()
        for cnt in cnt_dict.values():
            if cnt in cnt_set:
                return False
            cnt_set.add(cnt)
        
        return True
''',
    call='Solution().uniqueOccurrences([1,2,2,1,1,3])',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr', cell=84, h=170, pointers={'__i': 'blue'}),
        dict(type='map', var='cnt_dict', label='cnt_dict（数字 → 出现次数）', fmt=lambda k, v: f"{k}: {v}", h=190, font=34),
        dict(type='set', var='cnt_set', label='cnt_set（已见过的次数）', fmt=lambda x: str(x), h=170, font=34),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'orange')],
    captions={
        'cnt_dict = {}': '空字典：记录每个数出现了几次',
        'for num in arr': lambda S, B, r: ('数组遍历完，次数统计好了' if sum(S.cnt_dict.values()) == len(S.arr) else f'取下一个数 `{S.num}`'),
        'cnt_dict[num] =': '`{num}` 的次数加一 → `{cnt_dict[num]}`',
        'cnt_set = set()': '次数统计完了。再建一个集合，装已经出现过的“次数”',
        'for cnt in cnt_dict.values()': lambda S, B, r: ('次数都检查完了，没有重复' if len(S.cnt_set) == len(S.cnt_dict) else f'看下一个次数 `{S.cnt}`'),
        'if cnt in cnt_set': lambda S, B, r: (f'次数 `{S.cnt}` 已经在集合里 → 有两个数出现次数相同' if S.cnt in S.cnt_set else f'次数 `{S.cnt}` 还没出现过'),
        'return False': '次数重复，不独一无二 → 返回 `False`',
        'cnt_set.add(cnt)': '把次数 `{cnt}` 记进集合：`{cnt_set}`',
        'return True': '所有次数都互不相同 → 返回 ==`True`==',
    },
    cards=dict(
        one_liner='先数每个数的次数，再用集合检查次数有没有重复',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `arr`，若每个数的出现次数都==互不相同==，返回 `true`，否则 `false`',
                 '示例：`[1,2,2,1,1,3]` → `true`（1 出现 3 次，2 出现 2 次，3 出现 1 次）',
                 '示例：`[1,2]` → `false`（两个数都只出现 1 次）'],
        quote='统计每个数出现的次数，然后再使用哈希表来判断这些次数当中是否存在重复即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一步：字典 `cnt_dict` 数出每个数的次数',
              '第二步：遍历所有次数，放进集合 `cnt_set`',
              '放入前发现已存在 → 有重复，直接返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '判重用集合：次数的个数最多等于不同数字的个数',
                 '易错：集合里放的是==次数==，不是数字本身',
                 '代码与原文一致，无需改动（Python 2/3 通用）'],
    ),
)
