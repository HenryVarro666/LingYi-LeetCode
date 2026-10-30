def _cmp(S):
    if 'm' not in S or 'l' not in S:
        return f"先排序，再取中位数"
    a, m = S['sorted_arr'], S['m']
    l, r = S['l'], S['r']
    if l > r:
        return f"中位数 `m = {m}`"
    return f"中位数 `m = {m}`：左端 `|{a[l]} − {m}| = {abs(a[l]-m)}`　右端 `|{a[r]} − {m}| = {abs(a[r]-m)}`"


CONFIG = dict(
    num=1471, title='数组中的 k 个最强值', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 相向双指针',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def getStrongest(self, arr, k):

        sorted_arr = sorted(arr)
        l = 0
        r = len(sorted_arr) - 1
        m = sorted_arr[r // 2]
        res = []
        while l <= r:
            if abs(sorted_arr[l] - m) > abs(sorted_arr[r] - m):
                res.append(sorted_arr[l])
                l += 1
            else:
                res.append(sorted_arr[r])
                r -= 1
        
            if len(res) == k:
                break

        return res
''',
    call='Solution().getStrongest([6,7,11,7,6,8], 5)',
    expect=[11,8,6,6,7],
    views=[
        dict(type='text', fn=_cmp, h=60),
        dict(type='array', var='sorted_arr', pointers={'l': 'blue', 'r': 'pink'}, h=250, label='sorted_arr（排序后）',
             color=lambda S, i, v: 'yellow' if 'm' in S and 'sorted_arr' in S and i == (len(S['sorted_arr']) - 1) // 2 else None),
        dict(type='array', var='res', h=200, label='res（按强弱依次选出）', color=lambda S, i, v: 'green'),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'm', ('len(res)', 'len(res)', 'green'), 'k'],
    captions={
        'sorted_arr = sorted': '先排序：`sorted_arr = {sorted_arr}`，最强值只会出现在两头',
        'm = sorted_arr': '中位数 `m = sorted_arr[{r} // 2]` = =={m}==（下标 `(n-1)//2`）',
        'while l <= r': lambda S, B, ret: ('`l <= r`：还有数没选' if S.l <= S.r else '`l > r`：数都选完了'),
        'if abs(': lambda S, B, ret: (
            f'左 `|{S.sorted_arr[S.l]} − {S.m}| = {abs(S.sorted_arr[S.l]-S.m)}`，右 `|{S.sorted_arr[S.r]} − {S.m}| = {abs(S.sorted_arr[S.r]-S.m)}`：'
            + ('==左端更强==' if abs(S.sorted_arr[S.l]-S.m) > abs(S.sorted_arr[S.r]-S.m)
               else ('==距离相等，值大的更强 → 右端==' if abs(S.sorted_arr[S.l]-S.m) == abs(S.sorted_arr[S.r]-S.m) else '==右端更强=='))),
        'res.append(sorted_arr[l])': '选左端 `{sorted_arr[l]}` 进答案：`res = {res}`',
        'res.append(sorted_arr[r])': '选右端 `{sorted_arr[r]}` 进答案：`res = {res}`',
        'l += 1': '左端被选走，`l` → {l}',
        'r -= 1': '右端被选走，`r` → {r}',
        'if len(res) == k': '`len(res) = {len(res)}`，`k = {k}`：=={"已经选够，break" if len(res) == k else "还不够，继续"}==',
        'return res': '返回 `res = {res}`',
    },
    cards=dict(
        one_liner='排序后最强值一定在两头，每轮选较强的一端',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`|a − m|` 越大越强，`m` 是排序后的中位数；距离相等时值更大的更强',
                 '返回最强的 `k` 个值，顺序任意',
                 '示例：`[6,7,11,7,6,8], k=5` 的中位数是 `7`'],
        quote='最强值必然就出现在数组的头部或者尾部。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，离中位数 `m` 最远的数只可能是最小或最大',
              '选走一个后，剩下的数里最强的仍在新的两头',
              '所以 `l`、`r` 从两端向中间，每轮比较绝对差，选强的那端'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '中位数下标是 `(n-1)//2`，不是 `n//2`',
                 '距离相等时要选值更大的一端：代码里 `else` 取右端',
                 '原文为 Python 2 写法，整数除法 `r / 2` 已改为 `r // 2`'],
    ),
)
