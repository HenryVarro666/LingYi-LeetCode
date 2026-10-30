CONFIG = dict(
    num=798, title='得分最高的最小轮调', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='差分系统 · 统计区间最大重叠',
    tags=['灵神题单·常用数据结构', '难度分 2130'],
    code='''
class Solution(object):
    def bestRotation(self, A):

        n = len(A)
        cnt = [0] * (n + 1)

        for index, num in enumerate(A):
            if index >= num:
                delta = index - num
                cnt[0] += 1
                cnt[delta + 1] -= 1
            else:
                cnt[index + 1 + n - num] -= 1
            cnt[index + 1] += 1
        
        s = now = cnt[0]
        res = 0
        for index in range(1, len(cnt)):
            now += cnt[index]
            if now > s:
                s = now
                res = index
        
        return res
''',
    call='Solution().bestRotation([2,3,1,4,0])',
    expect=3,
    views=[
        dict(type='array', var='A', label='A（本轮处理 A[index]）', h=200,
             pointers={'index if _line < 14 else None': 'blue'}, pointer_labels={'index if _line < 14 else None': 'index'}),
        dict(type='array', var='cnt', label='cnt（差分标记，前缀和 = 旋转 k 次的得分）', h=250,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if S.get('res') is not None and i == S.get('res') and S.get('s') is not None else None),
        dict(type='text', size=30, h=90, fn=lambda S: (
            f"前缀和 `now` = 旋转 `{S['index']}` 次的得分 = =={S['now']}==，最高 `{S['s']}`（k = {S['res']}）"
            if 'res' in S and 'now' in S else
            (f"A[`{S['index']}`] = `{S['num']}`：{'A[index] ≤ index，有两段区间' if S['index'] >= S['num'] else 'A[index] > index，只有一段区间'}"
             if 'num' in S and 'index' in S else ''))),
    ],
    watch=['index', 'num', ('now', 'now', 'blue'), ('s', 's', 'green'), ('res', 'res', 'orange')],
    captions={
        'cnt = [0]': '`cnt` 就是原文的 `f`：差分标记，长 `n+1`',
        'if index >= num': '`A[{index}] = {num}`，{"num ≤ index" if index >= num else "num > index"}：{"两段区间 [0, index-num] 和 [index+1, n-1]" if index >= num else "只能转到数组后面，一段区间"}',
        'delta = ': '`delta = {index} - {num} = {delta}`：旋转 0 到 `{delta}` 次都得分',
        'cnt[0] += 1': '第一段区间 `[0, {delta}]` 的起点：`cnt[0] += 1`',
        'cnt[delta + 1] -= 1': '区间结束，从 `{delta+1}` 起不再得分：`cnt[{delta+1}] -= 1`',
        'cnt[index + 1 + n - num] -= 1': '区间 `[{index+1}, {index+n-num}]` 的终点后一位：`cnt[{index+1+n-num}] -= 1`',
        'cnt[index + 1] += 1': '转到末尾那一段从 `{index+1}` 次开始：`cnt[{index+1}] += 1`',
        's = now = cnt[0]': '`now` 从 `cnt[0] = {cnt[0]}` 起：旋转 0 次的得分；`s` 记最高分',
        'now += cnt[index]': '前缀和：`now += {cnt[index]}` → =={now}==（旋转 `{index}` 次的得分）',
        'if now > s': '`{now} > {s}` → {"更高，更新" if now > s else "不更高，保留较小的 k"}',
        'res = index': '最高分 `{s}`，对应旋转 `{res}` 次（严格大于才更新，k 最小）',
        'return res': '返回得分最高的最小旋转次数 `{res}`',
    },
    cards=dict(
        one_liner='把每个数的得分区间叠起来，看哪个 k 被盖得最多',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组向左旋转 `k` 次，值 `<=` 下标的项得 1 分',
                 '返回得分最高的最小 `k`',
                 '示例：`[2,3,1,4,0]` → `3`'],
        quote='问题就变成了给出若干段区间，问这些区间最多会重叠多少次。……可以反过来利用前缀和的思想，使用差分系统来处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A[index] > index`：只能转到末尾，区间 `[index+1, index+n-A[index]]`',
              '`A[index] <= index`：`[0, index-A[index]]` 和 `[index+1, n-1]` 两段',
              '区间起点 +1、终点后一位 -1，再扫一遍前缀和取最大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文第二段区间 `[index+1, n-1]` 在代码里合并成每轮的 `cnt[index+1] += 1`',
                 'A[index] = 0 时 `delta+1 = index+1`，两个标记抵消，不影响答案',
                 '`now > s` 严格大于，保证返回最小的 k',
                 '对比灵神：灵神把「先全体加 1 再减」写成三行 diff，这里把两段区间分开记'],
    ),
)
