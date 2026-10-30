def _cap_for(S, B, ret):
    if 'num' in B and B.num == S.num:
        return f'扫描结束，`res = {S.res}`'
    if S.num > S.res[-1]:
        return f'`num = {S.num}` > `res[-1] = {S.res[-1]}` → 能接在最长的那条后面，==变得更长=='
    return f'`num = {S.num}`，不比 `res[-1] = {S.res[-1]}` 大 → 接不上最长的那条'


def _cap_if(S, B, ret):
    if S.num > S.res[-1]:
        return f'`{S.num} > res[-1] = {S.res[-1]}` → 能接在最长的那条后面，==变得更长=='
    return f'`{S.num}` 不比 `res[-1] = {S.res[-1]}` 大 → 接不上最长的那条'


def _cap_elif(S, B, ret):
    if S.num < S.res[-1]:
        return f'`{S.num} < res[-1]`：res 里有比它大的数 → ==二分==找第一个 ≥ `{S.num}` 的位置'
    return f'`{S.num} == res[-1]`：无事发生'


def _cap_cmp(S, B, ret):
    if S.num <= S.res[S.mid]:
        return f'`{S.num} ≤ res[{S.mid}] = {S.res[S.mid]}` → `mid` 可能就是答案，记下 `pos = {S.mid}`'
    return f'`{S.num} > res[{S.mid}] = {S.res[S.mid]}` → 答案在右半边'


def _text(S):
    res = S.get('res')
    if not res:
        return '`res[index]` = 长度为 `index + 1` 的上升子序列的==末尾最小值=='
    return '`res`：' + '，'.join(f'长 {k + 1} → =={v}==' for k, v in enumerate(res))


_L, _M, _R = 'l if l <= r else None', 'mid if l <= r else None', 'r if l <= r else None'

CONFIG = dict(
    num=300, title='最长递增子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心 + 二分（维护最小末尾）',
    code='''
class Solution(object):
    def lengthOfLIS(self, nums):
        if not nums:
            return 0

        res = [nums[0]]
        for num in nums[1:]:
            if num > res[-1]:
                res.append(num)
            elif num < res[-1]:
                l = 0
                r = len(res) - 1
                while l <= r:
                    mid = (l + r) // 2
                    if num <= res[mid]:
                        pos = mid
                        r = mid - 1
                    else:
                        l = mid + 1

                res[pos] = num

        return len(res)
''',
    call='Solution().lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18])',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（黄 = 当前 num，暗 = 已处理）', cell=96,
             color=lambda S, k, v: 'yellow' if 'num' in S and v == S['num'] else None,
             dim=lambda S, k, v: 'num' in S and k < S['nums'].index(S['num'])),
        dict(type='array', var='res', label='res', cell=96, min_slots=8, h=240,
             window=(_L, _R), pointers={_L: 'blue', _M: 'purple', _R: 'pink'},
             pointer_labels={_L: 'l', _M: 'mid', _R: 'r'},
             color=lambda S, k, v: 'purple' if 'mid' in S and S['l'] <= S['r'] and k == S['mid'] else None),
    ],
    watch=[('num', 'num', 'yellow'), ('l', 'l', 'blue'), ('mid', 'mid', 'purple'), ('r', 'r', 'pink'),
           ('pos', 'pos', 'green'), ('len(res)', 'len(res)', 'green')],
    skip=['l = 0', 'r = len(res) - 1', 'while l <= r', 'if num > res[-1]', 'pos = mid'],
    captions={
        'if not nums': '空数组直接返回 0（本例非空）',
        'res = [nums[0]]': '初始 `res = [{nums[0]}]`：长度为 1 的上升子序列，末尾最小是 `{nums[0]}`',
        'for num in': _cap_for,
        'res.append': '`res` 末尾加入 `{num}` → 上升子序列最长长度变成 =={len(res)}==',
        'elif num < res[-1]': _cap_elif,
        'mid = (l + r)': '二分区间 `[{l}, {r}]`，`mid = {mid}`，`res[{mid}] = {res[mid]}`',
        'if num <= res[mid]': _cap_cmp,
        'r = mid - 1': '再往左半边找更靠左的：`r = {r}`',
        'l = mid + 1': '往右半边找：`l = {l}`',
        'res[pos] = num': '二分结束：`res[{pos}]` 从 `{B.res[pos]}` 换成 =={num}==，长度 {pos + 1} 的末尾==变小了，以后更好接==',
        'return len(res)': '`res` 的长度就是答案 → =={ret}==（`res` 本身不一定是真实的子序列）',
    },
    cards=dict(
        one_liner='想要更长的上升子序列，末尾的数越小越好',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，求==最长严格递增子序列==的长度',
                 '子序列：删掉若干元素，不改变剩余元素的顺序',
                 '示例：`[10,9,2,5,3,7,101,18]` → `4`（`2,3,7,101`）'],
        before=[dict(heading='先写 O(n²) 的 DP', lines=[
            '`f[i]`：以第 i 个数结尾的最长上升子序列的长度',
            '`f[i] = max(f[j]) + 1`，其中 `j < i` 且 `nums[j] < nums[i]`，两重循环',
        ])],
        quote='要想得到更长的上升子序列，我们总是希望子序列中的数越小越好，于是可以维护一个数组res，其中==res[index]表示长度为index + 1的上升子序列中末尾最小的数==。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 3 的有 `2,3,7`、`2,3,101`、`5,7,18`…，最理想的是 `2,3,7` → `res[2] = 7`',
              '`num > res[-1]` → append；相等 → 无事发生',
              '`num < res[-1]` → ==二分==找第一个 ≥ `num` 的 `res[p+1]`，换成 `num` 一定更优'],
        after=[dict(heading='为什么 res 一定单调递增？', lines=[
            '反证：若存在 `p > q` 且 `res[p] < res[q]`',
            '以 `res[p]` 结尾的子序列 `x0, …, xq, …, res[p]` 中，`xq < res[p] < res[q]`',
            '而 `x0…xq` 也是长为 `q+1` 的上升子序列 → `xq` 比 `res[q]` ==更符合定义==，矛盾',
        ])],
        summary=['一趟扫描，每次最多一次二分 → `O(n log n)`',
                 '`res` 只有==长度==有意义，内容不一定是真实的 LIS',
                 '原文为 Python 2 写法：`(l + r) / 2` 已改为 `//`，并删掉 docstring；手写二分 = `bisect_left`'],
    ),
)
