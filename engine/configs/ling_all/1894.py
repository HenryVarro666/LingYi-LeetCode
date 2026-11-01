CONFIG = dict(
    num=1894, title='找到需要补充粉笔的学生编号', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='取模消掉整轮 + 一次遍历（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def chalkReplacer(self, a: List[int], k: int) -> int:
        s = 0
        for v in a:
            s += v
        k %= s
        for i, v in enumerate(a):
            if k < v:
                return i
            k -= v
        raise Exception(-1)  # panic(-1)
''',
    call='Solution().chalkReplacer([3,4,1,2], 25)',
    expect=1,
    views=[
        dict(type='text', size=34, h=90, fn=lambda S: (
            f"粉笔盒还剩 `k = {S['k']}`" + (f"；一整轮共耗 `s = {S['s']}`" if 's' in S else ''))),
        dict(type='array', var='a', pointers={'i': 'blue'}, h=260, label='a（每个学生每次要用的粉笔）',
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
    ],
    watch=['s', 'k', ('i', 'i', 'blue'), ('v', 'v', 'cyan')],
    captions={
        's = 0': '先算一整轮所有学生共用多少粉笔，累加器 `s = 0`',
        's += v': '加上学生需要的 `{v}`，`s` → =={s}==',
        'k %= s': '每整轮正好用掉 `{s}` 支，整轮的部分不影响答案 → `k %= s`：=={B.k} → {k}== 支',
        'for i, v in enumerate': '从学生 0 开始，依次看谁的粉笔不够',
        'if k < v': lambda S, B, r: (f'剩 `k = {S.k}` < 需要 `{S.v}` → ==学生 {S.i} 粉笔不够，就是他=='
                                     if S.k < S.v else f'剩 `k = {S.k}` ≥ 需要 `{S.v}` → 学生 {S.i} 够用，继续'),
        'k -= v': '学生 {i} 用掉 `{v}` 支，剩下 `k` = =={k}==',
        'return i': '学生 `{i}` 需要补充粉笔，返回 =={i}==',
        'raise': '取模后 `k < s`，一定会在某个学生处返回，到不了这里',
    },
    cards=dict(
        one_liner='先对一整轮的总和取模，再扫一遍找第一个不够的人',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 个学生轮流答题，学生 `i` 每次用 `chalk[i]` 支粉笔',
                 '粉笔盒里一开始有 `k` 支，剩余粉笔严格小于所需时就要补充',
                 '示例：`chalk=[3,4,1,2], k=25` → 学生 `1`'],
        quote='k %= s',
        quote_src='—— 灵茶山艾府题解代码（原文为 Go）',
        idea=['每一整轮要用 `s` 支，`k` 里能凑出的整轮可以直接丢掉，只留 `k % s`',
              '余下的 `k < s`，从头扫：`k < a[i]` 的第一个 `i` 就是答案；否则 `k -= a[i]`',
              '一遍求和 + 一遍扫描，不需要前缀和数组'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`panic(-1)` 对应 `raise Exception(-1)`',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：必须先 `k %= s`，`k` 最大 `10^9`，不取模会白白转很多圈',
                 '判断是严格小于：`k < v` 不够；`k == v` 刚好用完，下一个才不够'],
    ),
)
