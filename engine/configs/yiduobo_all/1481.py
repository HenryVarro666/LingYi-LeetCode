CONFIG = dict(
    num=1481, title='不同整数的最少数目', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='计数 · 先删出现次数少的',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findLeastNumOfUniqueInts(self, arr, k):

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = len(cnt_dict)
        for cnt in sorted(cnt_dict.values()):
            if cnt <= k:
                res -= 1
                k -= cnt
        
        return res
''',
    call='Solution().findLeastNumOfUniqueInts([4,3,1,1,3,3,2], 3)',
    expect=2,
    views=[
        dict(type='array', var='arr', label='arr（恰好删掉 k 个元素）', h=150, cell=90),
        dict(type='map', var='cnt_dict', label='cnt_dict（数值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"还能删 `k = {S['k']}` 个，剩余不同整数 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=[('num', 'num', 'pink'), ('cnt', 'cnt', 'blue'), ('k', 'k', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '先统计每个整数出现了几次',
        'for num in arr': lambda S, B, r: (f'读入 `{S.num}`' if sum(S.cnt_dict.values()) < len(S.arr) else '数组读完了，计数完成'),
        'cnt_dict[num] =': '`cnt_dict[{num}] = {cnt_dict[num]}`',
        'res = len(cnt_dict)': '一开始有 `{res}` 种不同整数。删光某个整数的所有出现，才能让 `res` 减一',
        'for cnt in sorted': lambda S, B, r: (f'按出现次数从小到大看：这个整数出现 `{S.cnt}` 次，次数越少越==便宜==' if not ('cnt' in B and B.cnt == S.cnt and S.cnt == max(S.cnt_dict.values())) else '所有整数都看过了'),
        'if cnt <= k': lambda S, B, r: (f'`cnt = {S.cnt} <= k = {S.k}`：删得起，把它删光' if S.cnt <= S.k
                                         else f'`cnt = {S.cnt} > k = {S.k}`：删不光，这种整数保留'),
        'res -= 1': '少了一种整数：`res = {res}`',
        'k -= cnt': '用掉 `{cnt}` 次删除：`k = {k}`',
        'return res': '最少剩下 `{res}` 种不同整数',
    },
    max_steps=60,
    cards=dict(
        one_liner='要让种类最少：先把出现次数少的整数删光',
        complexity='时间 `O(n + m log m)`，空间 `O(m)`（m = 不同整数个数）',
        problem=['给一个整数数组 `arr` 和整数 `k`，==恰好删除 k 个元素==',
                 '求删除后==不同整数的最少种类数==',
                 '本视频：`arr = [4,3,1,1,3,3,2], k = 3` → `2`'],
        quote='为了使得剩下的不同整数数目最少，显然应该优先移除出现次数较少的那些整数。',
        quote_src='—— yiduobo 题解原文',
        idea=['种类只有在某个整数被删光时才会减少',
              '删光一种整数的代价是它的出现次数，次数少的更划算',
              '统计次数后升序遍历，`cnt <= k` 就删光，直到 `k` 不够'],
        summary=['时间 `O(n + m log m)`，空间 `O(m)`',
                 '`k` 不够删光某一种时，剩下的次数只能删这种的一部分，种类不变',
                 '遍历不需要 break：后面的次数更大，`cnt <= k` 不会再成立',
                 '本题题面库里缺失，题意按 LeetCode 1481 与原文推断'],
    ),
)
