CONFIG = dict(
    num=905, title='按奇偶排序数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 先跳过再交换',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def sortArrayByParity(self, A):

        l = 0
        r = len(A) - 1
        while l < r:
            while l < r and A[l] % 2 == 0:
                l += 1
            while r > l and A[r] % 2 == 1:
                r -= 1
            if l < r:
                A[l], A[r] = A[r], A[l]
                l += 1
                r -= 1
        
        return A
''',
    call='Solution().sortArrayByParity([3,1,2,4,5,6,7])',
    expect=[6, 4, 2, 1, 5, 3, 7],
    views=[
        dict(type='array', var='A', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), h=300,
             color=lambda S, idx, v: ('green' if v % 2 == 0 else 'orange') if ('l' in S and (idx < S['l'] or idx > S['r'])) else None),
        dict(type='text', fn=lambda S: '绿 = 偶数已就位，橙 = 奇数已就位，框内是还没处理的部分'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'l = 0': '`l` 从最左开始',
        'r = len': '`r` 从最右开始：`r = {r}`',
        'while l < r:': '`l = {l}`，`r = {r}`：{"两指针没相遇 → 继续" if l < r else "相遇或交叉 → 结束"}',
        'while l < r and A[l]': '{"`A[" + str(l) + "] = " + str(A[l]) + "` 是偶数，已在前面 → `l` 右移" if (l < r and A[l] % 2 == 0) else "`l` 停在 " + str(l) + "：这里是奇数（或已碰到 r）"}',
        'while r > l and A[r]': '{"`A[" + str(r) + "] = " + str(A[r]) + "` 是奇数，已在后面 → `r` 左移" if (r > l and A[r] % 2 == 1) else "`r` 停在 " + str(r) + "：这里是偶数（或已碰到 l）"}',
        'if l < r': '{"`l = " + str(l) + " < r = " + str(r) + "`：A[l] 是奇数、A[r] 是偶数 → 交换" if l < r else "`l` 没有小于 `r` → 不用交换"}',
        'A[l], A[r] =': '交换后 `A = {A}`',
        'l += 1': '`l` → {l}',
        'r -= 1': '`r` → {r}',
        'return A': '返回 `{A}`',
    },
    cards=dict(
        one_liner='l 向右跳过偶数，r 向左跳过奇数，卡住就交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组里所有偶数排在所有奇数前面',
                 '返回任一满足条件的数组',
                 '示例：`[3,1,2,4]` → `[2,4,3,1]`，本视频用 `[3,1,2,4,5,6,7]`'],
        quote='可以使用两个指针l和r分别从左右两侧开始向另一侧扫描。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l` 一直向右，直到遇到奇数；`r` 一直向左，直到遇到偶数',
              '此时若 `l < r`，`A[l]` 是奇数、`A[r]` 是偶数，交换',
              '交换后各走一步，重复到 `l >= r`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '内层 while 都要带 `l < r`（或 `r > l`），否则会越界',
                 '交换前再判断一次 `l < r`，因为内层循环可能已使其相遇',
                 '原文本身已兼容 Python 3，无需修改',
                 '对比灵神：灵神用一层 while + if/elif/else 每轮只做一件事，yiduobo 用内层 while 一次跳完'],
    ),
)
