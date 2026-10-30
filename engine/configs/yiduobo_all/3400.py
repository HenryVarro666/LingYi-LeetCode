def _txt(S):
    if 'rnd' not in S:
        return '枚举右移轮数 `rnd`，把 `nums1[index]` 对到 `nums2[(index+rnd) % n]`'
    if 'target' not in S:
        return f'右移 ==第 {S["rnd"]} 轮==：已匹配 `hit = {S.get("hit", 0)}`'
    ok = S['nums1'][S['index']] == S['nums2'][S['target']]
    return (f'右移 ==第 {S["rnd"]} 轮==：`nums1[{S["index"]}] = {S["nums1"][S["index"]]}` 对 '
            f'`nums2[{S["target"]}] = {S["nums2"][S["target"]]}` → ' + ('==相等==' if ok else '不等'))


CONFIG = dict(
    num=3400, title='右移后的最大匹配索引数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力枚举右移轮数',
    tags=['灵神题单·常用数据结构', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def maximumMatchingIndices(self, nums1, nums2):
        
        n = len(nums1)
        res = 0

        for rnd in range(n):
            hit = 0
            for index in range(n):
                target = (index + rnd) % n
                if nums1[index] == nums2[target]:
                    hit += 1
            res = max(res, hit)
        
        return res
''',
    call='Solution().maximumMatchingIndices([3,1,2,3], [1,2,3,1])',
    expect=3,
    views=[
        dict(type='text', h=90, size=30, fn=_txt),
        dict(type='array', var='nums1', label='nums1（index 指向当前元素）', pointers={'index': 'blue'}, cell=110, h=210,
             color=lambda S, i, v: ('green' if 'target' in S and i == S['index'] and v == S['nums2'][S['target']] else None)),
        dict(type='array', var='nums2', label='nums2（target = (index + rnd) % n）', pointers={'target': 'pink'}, cell=110, h=210,
             color=lambda S, i, v: ('green' if 'target' in S and 'index' in S and i == S['target'] and v == S['nums1'][S['index']] else None)),
    ],
    watch=[('rnd', 'rnd', 'yellow'), ('index', 'index', 'blue'), ('target', 'target', 'pink'), ('hit', 'hit', 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`：右移 `n` 轮等于没动，所以只需枚举 `rnd = 0 … n-1`',
        'res = 0': '`res` 记录各轮里最多的匹配数',
        'for rnd': lambda S, B, r: ('==所有轮数都试完了==' if getattr(B, 'rnd', None) == S.rnd else f'==试第 {S.rnd} 轮右移=='),
        'hit = 0': '这一轮重新数匹配：`hit = 0`',
        'target = ': '`nums1[{index}]` 右移 {rnd} 轮后落在下标 `({index} + {rnd}) % {n}` = =={target}==',
        'if nums1[index]': lambda S, B, r: (f'`nums1[{S.index}] = {S.nums1[S.index]}`，`nums2[{S.target}] = {S.nums2[S.target]}` → '
                                           + ('==相等，这个下标匹配==' if S.nums1[S.index] == S.nums2[S.target] else '不等，不计')),
        'hit += 1': '匹配数加一：`hit = {hit}`',
        'res = max': '这一轮结束：`res = max({B.res}, {hit})`，现在 `res` 是 =={res}==',
        'return res': '所有右移轮数里最多匹配 `{res}` 个',
    },
    skip=['for index'],
    max_steps=110,
    cards=dict(
        one_liner='数据规模小，直接枚举右移轮数，每轮数一遍匹配',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['两个等长整数数组，下标 `i` 上 `nums1[i] == nums2[i]` 就算匹配',
                 '对 `nums1` 任意次右移（`i` 的元素移到 `(i+1) % n`），求最多匹配数',
                 '本视频：`nums1=[3,1,2,3]`，`nums2=[1,2,3,1]` → `3`'],
        quote='右移的轮次必然小于数组的长度n，因为右移n次相当于无事发生。又由于题目的数据规模并不大，那么就可以直接暴力枚举右移的轮次rnd。',
        quote_src='—— yiduobo 题解原文',
        idea=['右移 `rnd` 轮后，`nums1[index]` 落到下标 `(index + rnd) % n`',
              '不用真的移动数组：直接拿它和 `nums2[(index+rnd) % n]` 比较',
              '每轮数出 `hit`，用它更新 `res`'],
        summary=['时间 `O(n²)`（n ≤ 3000 可过），空间 `O(1)`',
                 '轮数只需 `0 … n-1`，右移 `n` 轮会回到原位',
                 '易错：下标要对 `n` 取模；方向是右移，所以是 `index + rnd`',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
