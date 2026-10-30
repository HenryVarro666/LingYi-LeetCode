def _col(S, i, v):
    r = S.get('remove')
    if r is None:
        return None
    if r[i]:
        return 'red'
    return None


def _info(S):
    r = S.get('remove')
    if r is None:
        return ''
    ln = S.get('_line')
    ph = '正向扫描：左边有更大的数 → 删' if 'mi' not in S else '反向扫描：右边有更小的数 → 删'
    if 'res' in S:
        ph = '统计没被标记的数'
    ma, mi = S.get('ma'), S.get('mi')
    t = f'`ma` = {ma}' if ma is not None else ''
    if mi is not None:
        t += f'　`mi` = {mi}'
    return f'{ph}　{t}'


CONFIG = dict(
    num=1966, title='未排序数组中的可被二分搜索的数', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='正反两趟扫描 · 前缀最大 / 后缀最小',
    tags=['灵神题单·单调栈'],
    code='''
class Solution(object):
    def binarySearchableNumbers(self, nums):

        n = len(nums)
        remove = [False] * n
        ma = nums[0]
        for index in range(1, n):
            if nums[index] < ma:
                remove[index] = True
            ma = max(ma, nums[index])
        
        mi = nums[-1]
        for index in range(n - 2, -1, -1):
            if nums[index] > mi:
                remove[index] = True
            mi = min(mi, nums[index])
        
        res = n
        for index in range(n):
            if remove[index]:
                res -= 1
        
        return res
''',
    call='Solution().binarySearchableNumbers([1,3,2,4,6,5,7])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（红 = 已被标记为找不到）', h=230,
             color=lambda S, i, v: 'red' if S.get('remove') and S['remove'][i] else None),
        dict(type='array', var='remove', label='remove', h=200,
             color=lambda S, i, v: 'red' if v else None),
    ],
    watch=['index', ('ma', 'ma', 'cyan'), ('mi', 'mi', 'orange'), ('res', 'res', 'green')],
    captions={
        'remove = [False]': '`remove[i]` 记录：数 `nums[i]` ==会不会被二分误删==，先全设为 False',
        'ma = nums[0]': '`ma` 记录==左侧最大值==，从 `nums[0] = {ma}` 开始',
        'if nums[index] < ma': lambda S, B, r: (
            f'左边有更大的 `{S.ma}` > `{S.nums[S.index]}` → 如果 pivot 选到那个大数，目标就被误删 → ==标记删除=='
            if S.nums[S.index] < S.ma else
            f'`{S.nums[S.index]}` ≥ 左侧最大 `{S.ma}` → 左边没有更大的，这一趟不删'),
        'remove[index] = True': '`remove[{index}] = True`：`{nums[index]}` 不能被保证搜到',
        'ma = max': '`ma` 更新为 `{ma}`（前缀最大）',
        'mi = nums[-1]': '`mi` 记录==右侧最小值==，从最后一个数 `{mi}` 开始往左扫',
        'if nums[index] > mi': lambda S, B, r: (
            f'右边有更小的 `{S.mi}` < `{S.nums[S.index]}` → pivot 选到那个小数会误删目标 → ==标记删除=='
            if S.nums[S.index] > S.mi else
            f'`{S.nums[S.index]}` ≤ 右侧最小 `{S.mi}` → 右边没有更小的，这一趟不删'),
        'mi = min': '`mi` 更新为 `{mi}`（后缀最小）',
        'for index in range(n):': '遍历 `remove`，数出没被标记的数',
        'res = n': '先假设 `n = {n}` 个数都能搜到，再减去被标记的',
        'if remove[index]': lambda S, B, r: (
            f'`remove[{S.index}]` 为真 → `{S.nums[S.index]}` 不能保证被搜到'
            if S.remove[S.index] else f'`remove[{S.index}]` 为假 → `{S.nums[S.index]}` 一定能被搜到'),
        'res -= 1': '去掉一个：`res` = {res}',
        'return res': '无论 pivot 怎么选都能搜到的数共 `{res}` 个',
    },
    cards=dict(
        one_liner='左边没有更大、右边没有更小的数，才一定能被搜到',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 无序、元素互不相同。用「随机选 pivot，按大小丢掉一半」的二分去找 target',
                 '问有多少个值作为 target，==无论 pivot 怎么选==都一定能找到',
                 '示例：`[1,3,2,4,6,5,7]` → `3`'],
        quote='只有一个数v左侧存在比v更大的数，或者右侧存在比v更小的数，那么v就无法被搜索到，于是只需正反两趟遍历就可以确定数组中的每个数是否可以被搜索到了。',
        quote_src='—— yiduobo 题解原文',
        idea=['pivot 在 target 左边且比它大，会把 target 所在的右半丢掉；右边且更小同理',
              '所以正向维护前缀最大 `ma`：`nums[i] < ma` 就标记',
              '反向维护后缀最小 `mi`：`nums[i] > mi` 就标记，最后数没被标记的'],
        summary=['时间 `O(n)`，空间 `O(n)`（`remove` 数组）',
                 '正反两趟互相独立，==任一趟标记就算删==，所以 `remove` 只置 True 不置回',
                 '没被标记的数 = 左边都比它小、右边都比它大，位置恰好已「排好」',
                 '原文是 Python 2 风格，但没有用到需要改动的写法，代码原样运行'],
    ),
)
