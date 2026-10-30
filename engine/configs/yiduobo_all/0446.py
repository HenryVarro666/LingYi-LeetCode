def _txt(S):
    if 'diff' not in S or 'cnt' not in S:
        return '`f[i][diff]` = 以第 i 个数结尾、公差为 diff 的（长度 >= 2）数列个数'
    return (f"`A[j] − A[i]` = `{S['A'][S['j']]} − {S['A'][S['i']]}` = diff `{S['diff']}`；"
            f"`f[j][diff]` = ==`{S['cnt']}`== 个数列可以延长")


CONFIG = dict(
    num=446, title='等差数列划分 II - 子序列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i][diff] 字典 DP',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numberOfArithmeticSlices(self, A):

        f = []
        ans = 0
        for i in range(len(A)):
            f.append({})
            for j in range(i):
                diff = A[j] - A[i]
                cnt = f[j].get(diff, 0)
                f[i][diff] = f[i].get(diff, 0) + cnt + 1
                ans += cnt
        return ans
''',
    call='Solution().numberOfArithmeticSlices([2,4,6,8])',
    expect=3,
    views=[
        dict(type='array', var='A', label='A', pointers={'j': 'blue', 'i': 'pink'}, h=170, cell=100),
        dict(type='map', var='f[j]', label='f[j]（以 j 结尾：公差 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var='f[i]', label='f[i]（以 i 结尾：公差 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    skip=['for j in range(i)', 'ans = 0'],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), 'diff', 'cnt', ('ans', 'ans', 'green')],
    captions={
        'f = []': '`f[i]` 是一个 dict：公差可能很大，不能开数组',
        'f.append({})': '新增第 `{i}` 个数（`{A[i]}`）的字典 `f[{i}]`，先是空的',
        'diff = A[j] - A[i]': '`j = {j}`：公差记为 `A[j] − A[i]` = `{A[j]} − {A[i]}` = =={diff}==（符号只是约定，两边一致即可）',
        'cnt = f[j]': '`f[{j}][{diff}]` = =={cnt}==：以 `A[{j}]` 结尾、公差 `{diff}` 的数列有 {cnt} 个，后面接上 `A[{i}]` 就都变成 ==>= 3 项==',
        'f[i][diff] =': '`f[{i}][{diff}]` = 原有 + 继承 {cnt} 个 + 仅 `{A[j]}, {A[i]}` 这一个 = =={f[i][diff]}==',
        'ans += cnt': '继承来的 {cnt} 个数列至少 3 项，是合法答案：`ans` = =={ans}==',
        'return ans': '所有合法的等差子序列共 `{ans}` 个',
    },
    cards=dict(
        one_liner='f[i][diff]：以 i 结尾、公差 diff 的数列个数，字典存',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['数组 `A`，数出所有 ==长度 >= 3== 的等差子序列个数（子序列，可不连续）',
                 '示例：`[2,4,6,8,10]` → `7`',
                 '本视频：`[2,4,6,8]` → `3`',
                 '和 413 题不同：这里是子序列，不是子串'],
        quote='设f[i][diff]表示以第i个数结尾，公差为diff的数列个数。由于这里的diff跨度很大，因此这里的f[i]需要以dict的形式储存。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个 `j < i`，`A[i]` 可接在 `f[j][diff]` 的每个数列后面',
              '仅 `A[j], A[i]` 两项的数列也要计入 `f[i][diff]`，所以多 `+1`',
              '只有被继承的数列才 >= 3 项，所以只把 `f[j][diff]` 加入答案，那个 `+1` 不加'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '易错：`+1` 代表两项数列，只进 `f` 不进 `ans`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；`xrange` 已写作 `range`'],
    ),
)
