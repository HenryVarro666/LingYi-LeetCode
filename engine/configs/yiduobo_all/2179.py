CONFIG = dict(
    num=2179, title='统计数组中好三元组数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举中间 + left×right + 树状数组',
    tags=['树状数组', '难度分 2272'],
    code='''
class Solution(object):
    def goodTriplets(self, nums1, nums2):

        mapping = {}
        for index, num in enumerate(nums2):
            mapping[num] = index + 1
        
        res = 0
        n = len(nums1)
        suffix_array = [0] * (n + 1)
        for index, num in enumerate(nums1):
            p = mapping[num]
            
            left = 0
            now = p - 1
            while now > 0:
                left += suffix_array[now]
                now -= (now & -now)
            
            right = (n - index - 1) - (p - left - 1)
            res += left * right

            now = p
            while now <= n:
                suffix_array[now] += 1
                now += (now & -now)
        
        return res
''',
    call='Solution().goodTriplets([0,1,2,3], [0,2,1,3])',
    expect=2,
    views=[
        dict(type='array', var='nums1', label='nums1：从左到右枚举中间元素', pointers={'index': 'blue'}, h=200),
        dict(type='array', var='nums2', label='nums2（mapping[num] = 位置 + 1）',
             color=lambda S, i, v: 'yellow' if S.get('p') == i + 1 and S.get('_line', 0) >= 12 else None, h=150),
        dict(type='array', var='suffix_array', label='suffix_array：树状数组，下标 1..n，记录 nums2 位置已出现', pointers={'now': 'pink'}, h=210),
        dict(type='text', fn=lambda S: ('先把 nums2 每个值的位置存进 mapping（从 1 开始）' if S.get('_line', 0) < 11 else
             (f"当前位置 p = {S['p']}，已出现且位置 < p 的个数 left = =={S.get('left', 0)}==" if S.get('_line', 0) < 20 and 'p' in S else
              (f"位置 p = {S['p']}：左侧 left = =={S['left']}==，右侧 right = =={S['right']}== → 贡献 `{S['left']}×{S['right']}` = {S['left']*S['right']}" if 'right' in S else ''))), h=70),
    ],
    watch=['index', 'p', 'left', 'right', ('res', 'res', 'green')],
    captions={
        'mapping[num] = index + 1': '`mapping[{num}] = {index}+1`：值 {num} 在 nums2 的位置，下标改成从 1 开始（树状数组需要）',
        'suffix_array = [0]': '树状数组，全 0：位置 1..n 都还没出现',
        'p = mapping[num]': '当前中间元素 `nums1[{index}] = {num}`，它在 nums2 的位置 `p = {p}`',
        'now = p - 1': '要数「位置 < p」的已出现个数：从 `now = {now}` 开始求前缀和',
        'left += suffix_array[now]': '`left += suffix_array[{now}]` → =={left}==',
        'now -= (now & -now)': '`now -= now & -now` → {now}：去掉最低位的 1，继续拼前缀和',
        'right = (n - index - 1)': '右侧共 `{n}-{index}-1` = {n-index-1} 个数；nums2 里 p 前面共有 `p-1` = {p-1} 个位置，其中 `left` 个已被左侧占用 → ==right = {right}==',
        'res += left * right': '左侧 `{left}` 个选一个 × 右侧 `{right}` 个选一个：`res` = =={res}==',
        'now = p': '把位置 `{p}` 标记为已出现：从 `now = {now}` 往上更新',
        'suffix_array[now] += 1': '`suffix_array[{now}]` += 1',
        'now += (now & -now)': '`now += now & -now` → {now}：跳到下一个管着它的格子',
        'return res': '好三元组一共 `{res}` 个',
    },
    skip=['while now', 'res = 0', 'n = len', 'left = 0', 'mapping = {}'],
    max_steps=90,
    cards=dict(
        one_liner='枚举 nums1 的中间元素：左边 left 个 × 右边 right 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums1`、`nums2` 是 `0..n-1` 的排列',
                 '好三元组：三个值在两个数组里的先后顺序一致',
                 '本视频：`[0,1,2,3]` 与 `[0,2,1,3]` → `2`'],
        quote='对于这类有前后顺序的三元组问题，通常的处理方法是枚举中间元素的位置，然后想办法高效计算左右两侧两个元素的相关性质最后得出答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 nums1，当前数在 nums2 的位置记为 `p`',
              '`left`：前面的数里，在 nums2 位置 `< p` 的个数，用 ==01 数组的前缀和== = 树状数组查',
              '`right` 不用再查：nums2 里 `p` 前有 `p-1` 个位置，扣掉 left 个，剩下的都在后面，再用总数反推'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '位置要 +1：树状数组下标从 1 开始',
                 '`right = (n-index-1) - (p-left-1)`：后面的数减去「位置在 p 前却不在左侧」的',
                 '对比灵神：灵神把 nums1 重命名成 0..n-1 后只数 nums2；这里直接用 nums2 位置',
                 '原文代码无需改动即可在 Python 3 运行'],
    ),
)
