def _info(S):
    if 'now' not in S:
        return '相邻两数之间缺多少个：`num - now - 1`，和 k 比，不够就把 k 减掉'
    return f'上一个数 `now = {S["now"]}`（蓝格），当前 `num`（黄格），还要找第 `k = {S["k"]}` 个缺失的数'


CONFIG = dict(
    num=1539, title='第 k 个缺失的正整数', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='模拟 · 相邻差值判断缺失个数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findKthPositive(self, arr, k):

        arr.append(2001)
        now = 0
        for num in arr:
            if num - now - 1 >= k:
                return now + k
            else:
                k -= num - now - 1
            now = num
''',
    call='Solution().findKthPositive([2, 3, 4, 7, 11], 5)',
    expect=9,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='arr', cell=96, h=330,
             color=lambda S, i, v: ('yellow' if 'num' in S and v == S['num'] else 'blue' if S.get('now') == v else None)),
    ],
    watch=[('now', 'now', 'blue'), ('num', 'num', 'yellow'), ('k', 'k', 'green')],
    captions={
        'arr.append(2001)': '末尾加一个哨兵 `2001`（题目最大 1000+1000），保证答案一定落在某两数之间',
        'now = 0': '`now` 是上一个数，一开始是 `0`',
        'for num in arr': '看相邻两数 `{now}` 和 `{num}`',
        'if num - now - 1 >= k': lambda S, B, r: (
            f'`{S.num}` 和 `{S.now}` 之间缺 `{S.num} - {S.now} - 1 = {S.num - S.now - 1}` 个 >= `k = {S.k}` → ==答案就在这段里=='
            if S.num - S.now - 1 >= S.k else
            f'之间只缺 `{S.num - S.now - 1}` 个 < `k = {S.k}` → 这段不够，==整段跳过=='),
        'return now + k': '从 `now = {now}` 往后数 `k = {k}` 个：`{now} + {k}` = =={ret}==',
        'k -= num - now - 1': '这段的缺失全部用掉：`k` 减去 `{B.k - k}`，还剩 `k = {k}`',
        'now = num': '`now = {now}`，继续看下一段',
    },
    cards=dict(
        one_liner='相邻两数之间缺几个，不够就从 k 里扣掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['严格升序的正整数数组 `arr`，求第 `k` 个缺失的正整数',
                 '示例：`arr=[2,3,4,7,11]`，`k=5` → `9`',
                 '本视频用同一示例'],
        quote='由于这里的k的范围很小，因此直接模拟也是可行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr[i]` 与 `arr[i+1]` 之间缺 `arr[i+1]-arr[i]-1` 个整数',
              '这个数 `>= k`：答案就是从 `arr[i]` 往后数 `k` 个',
              '否则 `k` 减去这个数，继续看下一对'],
        summary=['时间 `O(n)`，`k` 和 `n` 都不大，模拟足够',
                 '`arr.append(2001)` 是哨兵，保证最后一定能返回；也会修改传入的数组',
                 '`now` 初值 `0` 让第一个数之前的缺失（`1..arr[0]-1`）也被统计',
                 '对比灵神：灵神二分 `arr[i]-1-i`，`O(log n)`'],
    ),
)
