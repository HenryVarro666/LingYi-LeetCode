CONFIG = dict(
    num=3682, title='公共元素的最小索引和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表记首次位置',
    code='''
class Solution(object):
    def minimumSum(self, nums1, nums2):
        
        p = {}
        for index, v in enumerate(nums1):
            if v not in p:
                p[v] = index
        
        res = -1
        for index, v in enumerate(nums2):
            if v in p and (res == -1 or res > index + p[v]):
                res = index + p[v]
        
        return res
''',
    call='Solution().minimumSum([3,1,2,1,4], [5,4,1,2,6])',
    expect=3,
    views=[
        dict(type='array', var='nums1', label='nums1', h=150,
             pointers={'index if _line <= 8 else None': 'blue'}, pointer_labels={'index if _line <= 8 else None': 'index'}, color=lambda S, i, v: 'blue' if S['_line'] <= 8 and S.get('index') == i else None),
        dict(type='array', var='nums2', label='nums2', h=150,
             pointers={'index if _line >= 10 else None': 'pink'}, pointer_labels={'index if _line >= 10 else None': 'index'}, color=lambda S, i, v: 'pink' if S['_line'] >= 10 and S.get('index') == i else None),
        dict(type='map', var='p', fmt=lambda k, v: f'{k}→{v}', h=170, label='p（值 → nums1 首次下标）'),
        dict(type='text', fn=lambda S: f"当前最小索引和 res = =={S['res']}==" if 'res' in S else '', h=50),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        'p = {}': '`p` 记录 nums1 中每个值第一次出现的下标（下标越小越好）',
        'if v not in p': '`{v}` 之前出现过吗？{"没有，记下它的下标" if v not in p else "出现过，保留更小的旧下标"}',
        'p[v] = index': '`p[{v}] = {index}`：首次位置最小，所以只记第一次',
        'res = -1': '`res = -1` 表示还没找到公共元素',
        'if v in p and': '`{v}` 在 p 里吗？{"在，候选和 = " + str(index) + " + " + str(p[v]) + " = " + str(index + p[v]) if v in p else "不在，不是公共元素"}；当前 res = {res}',
        'res = index': '更新最小索引和：`res = {index} + {p[v]} = {res}`',
        'return': '遍历结束，最小索引和为 =={ret}==',
    },
    cards=dict(
        one_liner='nums1 记首次位置，nums2 逐个查表更新最小和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个长度为 n 的数组，`nums1[i] == nums2[j]` 称 `(i, j)` 为好数对',
                 '求所有好数对中 `i + j` 的最小值，没有则返回 `-1`',
                 '示例：`[3,1,2,1,4]` 与 `[5,4,1,2,6]` → `3`'],
        quote='对nums1进行一趟遍历，使用哈希表记录nums1中每种元素首次出现的位置，接下来再对nums2进行一趟遍历，使用当前元素在哈希表中记录的下标与当前下标之和更新答案即可。',
        quote_src='—— yiduobo 题解',
        idea=['同一个值在 nums1 中取最靠前的下标，和才最小', '遍历 nums2，每个 j 只需配 nums1 里的首次下标',
              '用 `res == -1` 判断是否还没有答案'],
        summary=['时间 `O(n)`，空间 `O(n)`', '易错点：哈希表只记==首次==位置，别被后面的重复值覆盖',
                 '没有公共元素时保持 `-1`', '原文为 Python 2 写法，本题无需改动，仅保留代码'],
    ),
)
