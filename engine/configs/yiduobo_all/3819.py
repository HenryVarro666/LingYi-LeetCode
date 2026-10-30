CONFIG = dict(
    num=3819, title='非负元素轮替', difficulty='Medium', category='模拟',
    author='yiduobo', technique='提取非负数 + 切片轮替 + 重建答案', tags=[],
    code='''
class Solution(object):
    def rotateElements(self, nums, k):
        
        pos = []
        for v in nums:
            if v >= 0:
                pos.append(v)
        
        if not pos:
            return nums

        k %= len(pos)
        pos = pos[k:] + pos[:k]
        res = []
        p = 0
        for v in nums:
            if v < 0:
                res.append(v)
            else:
                res.append(pos[p])
                p += 1
        
        return res
''',
    call='Solution().rotateElements([5,4,-9,6,2], 2)',
    expect=[6, 2, -9, 5, 4],
    views=[
        dict(type='array', var='nums', label='nums', h=200, color=lambda S, k, v: 'red' if v < 0 else None),
        dict(type='array', var='pos', pointers={'p': 'pink'}, label='pos（非负数）', h=200),
        dict(type='array', var='res', label='res（答案）', h=200),
    ],
    watch=['k', 'p', 'v'],
    captions={
        'pos = []': '`pos` 用来存所有非负元素',
        'if v >= 0': lambda S, B, r: (f'`{S.v} >= 0` → 非负，放进 `pos`' if S.v >= 0 else f'`{S.v}` 是负数 → 不参与轮替'),
        'pos.append': '`pos` = {pos}',
        'if not pos': lambda S, B, r: ('`pos` 为空 → 没有元素需要轮替，直接返回 `nums`' if not S.pos else f'`pos` = {S.pos}，不为空，继续'),
        'k %= len(pos)': '轮替 `len(pos)` 次等于没动，所以 `k` 先取模：`k` → {k}',
        'pos = pos[k:]': '向左轮替 `k` 位：`pos[k:] + pos[:k]` = =={pos}==',
        'res = []': '`res` 存答案',
        'p = 0': '`p` 指向下一个要用的轮替后非负数，从 `pos[0]` 开始',
        'if v < 0': lambda S, B, r: (f'`{S.v} < 0` → 负数保持原位，直接放入 `res`' if S.v < 0 else f'`{S.v}` 非负 → 用 `pos[{S.p}]` 顶替'),
        'res.append(v)': '负数原样放入：`res` = {res}',
        'res.append(pos[p])': '取 `pos[{p}] = {pos[p]}` 放入：`res` = {res}',
        'p += 1': '`p` → {p}',
        'return res': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='先把非负数抽出来转一转，再按位置重新铺回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['非负元素向左循环轮替 `k` 位，负数保持不动', '轮替后的非负数按顺序填回原来非负的位置', '本视频：`[5,4,-9,6,2], k=2` → `[6,2,-9,5,4]`'],
        quote='将最后的pos[n - 1]移动到pos[n - k - 1]之后，就需要从头开始……换言之，在这里就是将pos迭代为pos[k:] + pos[:k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历提取非负元素得到 `pos`；为空就直接返回', '`k` 对 `len(pos)` 取模，再 `pos[k:] + pos[:k]` 完成向左轮替', '再遍历 `nums` 造答案：负数原样放，非负数取 `pos[p]` 并 `p + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`', '易错点：没有非负数时必须提前返回，否则 `k %= 0` 报错', '`k` 要先对 `len(pos)` 取模', '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神直接把读指针从 `k` 开始，省去切片轮替'],
    ),
)
