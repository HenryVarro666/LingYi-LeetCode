CONFIG = dict(
    num=413, title='等差数列划分', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='找最长等差段 · 求和公式', tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def numberOfArithmeticSlices(self, A):

        if len(A) < 3:
            return 0

        res = 0
        start = 0
        end = 2
        while end < len(A):
            diff = A[end - 1] - A[end - 2]
            while end < len(A) and A[end] - A[end - 1] == diff:
                end += 1
            
            length = end - start
            res += (1 + length - 2) * (length - 2) // 2
            start = end - 1
            end = end + 1

        return res
''',
    call='Solution().numberOfArithmeticSlices([1,2,3,4,6,8,10])',
    expect=6,
    views=[
        dict(type='array', var='A', pointers={'start': 'blue', 'end': 'pink'}, window=('start', 'end - 1'), h=300,
             color=lambda S, i, v: ('blue' if i == S['start'] else None) if 'start' in S else None),
        dict(type='text', h=90, fn=lambda S: (f"当前等差段长 `length` = =={S['length']}==，新增 `({S['length']}−2)×({S['length']}−1)/2` = =={(S['length']-2)*(S['length']-1)//2}== 个" if 'length' in S else '')),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), 'diff', 'length', ('res', 'res', 'green')],
    captions={
        'if len(A) < 3': '`len(A) = {len(A)}`：不足 3 个数，凑不出等差数列 → {"直接返回 0" if len(A) < 3 else "继续"}',
        'start = 0': '`start = 0`：当前等差段的起点',
        'end = 2': '`end = 2`：从前三个数开始判断，`end` 指向待检查的位置',
        'diff = A[end - 1]': '这一段的公差 `diff = A[{end-1}] - A[{end-2}]` = =={diff}==',
        'while end < len(A) and': lambda S, B, r: (f"`A[{S.end}] - A[{S.end-1}] = {S.A[S.end]-S.A[S.end-1]}` == diff {S.diff}？{'相等，等差段还能延长' if S.A[S.end]-S.A[S.end-1]==S.diff else '不等，这一段到此为止'}" if S.end < len(S.A) else '`end` 到头了，这一段结束'),
        'end += 1': '等差段延长：`end` → {end}',
        'length = end - start': '这一段 `[{start}, {end-1}]` 的长度 `length = {end} - {start}` = =={length}==',
        'res += (1 + length': '长 `{length}` 的等差段里，所有长度 ≥ 3 的子段共 `1+…+({length}-2)` = `(1+{length}-2)×({length}-2)/2` = =={(1+length-2)*(length-2)//2}==，`res` → {res}',
        'start = end - 1': '下一段从 `end-1` 开始：相邻两段共用一个端点，`start` → {start}',
        'end = end + 1': '`end` 跳到 `start+2`，再取新的公差：`end` → {end}',
        'return res': '一共 `{res}` 个等差子数组',
    },
    cards=dict(
        one_liner='尽量长地找等差段，用求和公式一次算完它的所有子段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `A`，求长度 ≥ 3 的等差子数组（连续）个数',
                 '相邻两项之差都相同才算等差',
                 '示例：`[1,2,3,4]` → `3`；本视频：`[1,2,3,4,6,8,10]` → `6`'],
        quote='一般地，1~m，2~m+1，…，k-m+1~k 项拎出来必然是长度为 m 的等差数列，一共有 ==k-m+1== 种可能。',
        quote_src='—— yiduobo 题解原文',
        idea=['长为 `k` 的等差段，里面长为 `m` 的子段有 `k-m+1` 个',
              'm 从 3 取到 k：`(k-2)+(k-3)+…+1 = (k-2)(k-1)/2`',
              '一趟扫描：每次先把等差段拉到最长，再套一次公式'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '相邻两段共用端点：`start = end - 1`，别写成 `end`',
                 '长度 < 3 直接返回 0；段长为 2 时公式结果是 0，不会多算',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '同类题：LeetCode 446 等差数列划分 II（子序列）'],
    ),
)
