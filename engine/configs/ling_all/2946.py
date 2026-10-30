MAT = [[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]]


CONFIG = dict(
    num=2946, title='循环移位后的矩阵相似检查', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='每行只需右移 k 次比较',
    tags=['灵神题单', '难度分 1406'],
    code='''
class Solution:
    def areSimilar(self, mat: List[List[int]], k: int) -> bool:
        k %= len(mat[0])  # 右移 n 次等价于右移 0 次，右移 n+1 次等价于右移 1 次，依此类推，先模个 n
        return k == 0 or all(row == row[k:] + row[:k] for row in mat)
''',
    call=f'Solution().areSimilar({MAT}, 2)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"右移 `k = {S['k']}` 后每一行：" if 'k' in S else '')),
        dict(type='grid', var='mat', h=300),
        dict(type='custom', h=200, draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T)),
    ],
    watch=['k', ('n', 'len(mat[0])', 'cyan')],
    captions={
        'k %= len': '`k %= {len(mat[0])}` → `k = {k}`：移动 n 次回到原样，先取模',
        'return k == 0': lambda S, B, ret: (
            f'`k = {S.k}`，对每行判断 `row == row[k:] + row[:k]`（右移 k 次）：'
            f'{"每一行都与移位后相同" if ret else "有一行移位后变了"} → ==返回 {ret}=='),
    },
    cards=dict(
        after=[dict(heading='为什么左右移等价', lines=[
            '两个不同数组 `a`、`b`：`a` 左移 k 次和右移 k 次结果不同',
            '但这里两个数组==都是 a 自己==',
            '`a` 左移 k 次后等于 `b` ⇔ `b` 右移 k 次后等于 `a`',
            'b 就是 a，所以只看 `a` 右移 k 次是否等于 `a`',
            '写法二：逐个比较 `row[j]` 与 `row[(j+k)%n]`，同一道理'])],
        one_liner='只需把每行右移 k 次，不用管奇偶、不用管左移',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['偶数行循环左移、奇数行循环右移，共 `k` 次',
                 '最终矩阵和原矩阵相同吗？',
                 '示例：`[[1,2,1,2],[5,5,5,5],[6,3,6,3]]`，`k = 2` → `true`'],
        quote='实际上，只需把每行右移 k 次。无需判断奇偶，无需考虑左移。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左移 k 次等于自己 ⇔ 它的逆过程（右移 k 次）也等于自己',
              '所以每一行只要比较 `row` 与 `row[k:] + row[:k]`',
              '先 `k %= n`；`k == 0` 时直接为真'],
        summary=['时间 `O(mn)`，空间 `O(1)`（切片比较的临时数组忽略）',
                 '关键：比较的是==自己和自己==，左移右移等价',
                 '易错：别忘了 `k %= n`，否则 k 超过列数会白白多转',
                 '写法二是双重循环比较 `row[j] != row[(j+k)%n]`，思路相同'],
    ),
)


def _draw(cv, S, B, box, T):
    if 'mat' not in S or 'k' not in S:
        return
    x0, y0, x1, y1 = box
    k = S['k']
    cv.text((x0 + 18, y0 + 4), f'每行右移 {k} 次的结果（和原行比较）', 24, T['muted'], bold=True)
    y = y0 + 44
    for i, r in enumerate(S['mat']):
        sh = r[k:] + r[:k]
        ok = sh == r
        cv.text((x0 + 18, y), f'行 {i}：{r} → {sh}  ' + ('相等' if ok else '不等'), 26,
                T['green'] if ok else T['red'], bold=True)
        y += 44
