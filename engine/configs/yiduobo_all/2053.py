ARR = ['d', 'b', 'c', 'b', 'c', 'a']

CONFIG = dict(
    num=2053, title='数组中第 K 个独一无二的字符串', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 + 顺序扫描',
    tags=[],
    code='''
class Solution(object):
    def kthDistinct(self, arr, k):

        s_dict = {}
        for index, s in enumerate(arr):
            s_dict[s] = s_dict.get(s, 0) + 1
        
        cnt = 0
        for s in arr:
            if s_dict[s] == 1:
                cnt += 1
                if cnt == k:
                    return s
        
        return ""
''',
    call=f'Solution().kthDistinct({ARR}, 2)',
    expect='a',
    views=[
        dict(type='array', var='arr', label='arr（第一遍：蓝箭头 = 下标；第二遍：黄 = 正在看的字符串）', cell=96, h=190,
             pointers={'index if _line <= 6 else None': 'blue'},
             color=lambda S, i, v: 'yellow' if S['_line'] >= 9 and S.get('s') == v else None),
        dict(type='map', var='s_dict', label='s_dict（字符串 → 出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"已找到 `cnt = {S['cnt']}` 个独一无二，目标 `k = {S['k']}`" if 'cnt' in S else ''),
    ],
    watch=[('k', 'k'), ('s', 's', 'blue'), ('cnt', 'cnt', 'green')],
    captions={
        's_dict = {}': '先建一个空哈希表，用来统计每个字符串出现几次',
        's_dict[s] = s_dict.get': "`'{s}'` 出现次数 +1 → `{s_dict[s]}`",
        'cnt = 0': '统计完了，==再按原数组顺序==扫一遍（题目要按出现顺序的第 k 个）；`cnt` 记录已遇到几个独一无二的',
        'for s in arr': '按原顺序看下一个字符串',
        'if s_dict[s] == 1': lambda S, B, r: (f"`'{S.s}'` 只出现 1 次 → 独一无二" if S.s_dict[S.s] == 1
                                             else f"`'{S.s}'` 出现了 {S.s_dict[S.s]} 次 → 不是独一无二，跳过"),
        'cnt += 1': '又找到一个独一无二的字符串：`cnt` → {cnt}',
        'if cnt == k': lambda S, B, r: (f'`cnt = {S.cnt} == k = {S.k}`：就是它' if S.cnt == S.k
                                       else f'`cnt = {S.cnt}` ≠ `k = {S.k}`，还不够，继续往后找'),
        'return s': "第 `{k}` 个独一无二的字符串是 `'{s}'`",
        'return ""': '扫完都不够 k 个 → 返回空字符串',
    },
    cards=dict(
        one_liner='先哈希表数次数，再按原顺序数第 k 个只出现一次的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['只出现 ==一次== 的字符串叫独一无二',
                 '返回数组中按原顺序的第 `k` 个独一无二字符串，不足 `k` 个返回 `""`',
                 '示例：`["d","b","c","b","c","a"]`，`k = 2` → `"a"`'],
        quote='由于字符串的长度都很小，那么可以直接使用哈希表统计每个字符串出现的次数，然后遍历原数组，若找到第k个只在哈希表中出现一次的字符串即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：`s_dict` 记下每个字符串出现的次数',
              '第二遍：按原数组顺序，次数为 1 的就让 `cnt` 加一',
              '`cnt == k` 时当前字符串就是答案'],
        summary=['时间 `O(n)`（字符串很短，哈希为常数），空间 `O(n)`',
                 '易错：必须按原数组顺序数，不能遍历哈希表（顺序不对应）',
                 '不足 `k` 个独一无二时，循环结束后返回 `""`',
                 '代码与原文一致，只保留了 Python 3 可运行的写法'],
    ),
)
