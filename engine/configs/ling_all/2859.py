def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, k = S.get('nums'), S.get('k')
    if nums is None:
        return
    n = len(nums)
    cv.text((x0 + 18, y0 + 4), f'逐个下标看二进制里 1 的个数（绿 = 恰好 {k} 个，要加进答案）', 22, T['muted'], bold=True)
    cols = [('下标 i', 130), ('二进制', 170), ('1 的个数', 170), ('nums[i]', 150), ('是否选中', 170)]
    row_h = min(64, (y1 - y0 - 120) / (n + 1))
    X0 = x0 + 30
    ty = y0 + 56
    X = X0
    for name, w in cols:
        cv.text((X + w / 2, ty), name, 24, T['muted'], anchor='mm', bold=True)
        X += w
    total = 0
    for i, v in enumerate(nums):
        c = i.bit_count()
        ok = c == k
        y = ty + row_h * (i + 1)
        if ok:
            total += v
            cv.rect((X0 - 8, y - row_h / 2 + 3, X0 + sum(w for _, w in cols), y + row_h / 2 - 3), fill=T['green'], alpha=45, r=8)
        vals = [str(i), bin(i)[2:], str(c), str(v), '选中' if ok else '—']
        X = X0
        for (name, w), t in zip(cols, vals):
            cv.text((X + w / 2, y), t, 30, T['green'] if ok else T['text'], anchor='mm', bold=ok, mono=True)
            X += w
    cv.text((X0, y1 - 40), f'选中元素之和 = {total}', 30, T['green'], bold=True)


CONFIG = dict(
    num=2859, title='计算 K 置位下标对应元素的和', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='bit_count 一行求和',
    code='''
class Solution:
    def sumIndicesWithKSetBits(self, nums: List[int], k: int) -> int:
        return sum(x for i, x in enumerate(nums) if i.bit_count() == k)
''',
    call='[Solution().sumIndicesWithKSetBits([5,10,1,5,2], 1), Solution().sumIndicesWithKSetBits([4,3,2,1], 2)]',
    expect=[13, 1],
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['k'],
    captions={
        'return sum': lambda S, B, ret: (
            f'一行搞定：遍历所有下标，`i.bit_count() == {S.k}` 的 `nums[i]` 累加 → 返回 =={ret}=='
            if ret is not None else f'把下标二进制里 1 的个数恰为 `k = {S.k}` 的 `nums[i]` 全部加起来'),
    },
    cards=dict(
        one_liner='下标的二进制里 1 的个数等于 k，就把它加进答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给 `nums` 和 `k`，求下标二进制里恰有 `k` 个 1 的元素之和',
                 '例如下标 `1, 2, 4` 的二进制都只有一个 1',
                 '示例：`[5,10,1,5,2], k=1` → `13`；`[4,3,2,1], k=2` → `1`',
                 '本视频连着演示这两个示例'],
        quote='把所有满足下标的二进制中的 1 的个数等于 k 的 nums[i] 加起来，就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接按题意遍历，不需要任何技巧',
              '`i.bit_count()` 一步得到下标二进制中 1 的个数',
              '生成器表达式边筛边求和，空间 `O(1)`'],
        after=[dict(heading='bit_count 在做什么', lines=['`i.bit_count()` 返回 `i` 二进制里 1 的个数，如 `7 → 3`', '等价于不断 `i &= i - 1` 去掉最低位的 1，数几次', '`i = 0` 时一个 1 也没有，只有 `k = 0` 才选下标 0'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`int.bit_count()` 是 Python 3.10 新增的方法',
                 '易错点：数的是「下标」的二进制，不是 `nums[i]` 的',
                 '更多位运算技巧见灵神的位运算题单'],
    ),
)
