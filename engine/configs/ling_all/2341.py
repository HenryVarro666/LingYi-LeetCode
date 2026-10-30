def _cnt_txt(S):
    from collections import Counter as C
    nums = S['nums']
    c = C(nums)
    parts = '，'.join(f'{k}×{v}' for k, v in sorted(c.items()))
    if 'pairs' not in S:
        return f'`Counter(nums)`：{parts}'
    return f'每种数 `c // 2` 对：' + ' + '.join(f'{v}//2' for k, v in sorted(c.items())) + f' = =={S["pairs"]}== 对'


def _res_txt(S):
    if 'pairs' not in S:
        return '先统计每个数的出现次数，两两配对'
    return f'剩余 = `len(nums) − 2×pairs` = `{len(S["nums"])} − 2×{S["pairs"]}` = =={len(S["nums"]) - 2 * S["pairs"]}=='


CONFIG = dict(
    num=2341, title='数组能形成多少数对', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 每种数 c//2 对',
    code='''
class Solution:
    def numberOfPairs(self, nums: List[int]) -> List[int]:
        pairs = sum(c // 2 for c in Counter(nums).values())
        return [pairs, len(nums) - pairs * 2]
''',
    call='Solution().numberOfPairs([1,3,2,1,3,2,2])',
    expect=[3, 1],
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             color=lambda S, i, v: 'green' if v in (1, 3) else ('yellow' if v == 2 else None)),
        dict(type='text', fn=_cnt_txt, size=32, h=120),
        dict(type='text', fn=_res_txt, size=32, h=120),
    ],
    watch=[('pairs', 'pairs', 'green')],
    captions={
        'pairs = sum': '统计每个数的出现次数 `c`，每种数能配 `c // 2` 对，全部加起来：`pairs` = =={pairs}==',
        'return [pairs': '剩下的数 = 总数 − 配走的 `2 × pairs` = `{len(nums)} − {pairs} × 2` = =={len(nums) - pairs * 2}==，返回 `{ret}`',
    },
    cards=dict(
        before=[dict(heading='先看示例怎么配对', lines=['`[1,3,2,1,3,2,2]` 里：`1` 出现 2 次，`3` 出现 2 次，`2` 出现 3 次', '`2//2 + 2//2 + 3//2 = 1 + 1 + 1 = 3` 对', '用掉 6 个数，原来 7 个，==剩 1 个==（落单的那个 `2`）', '所以和配对顺序无关，只看每种数的个数'])],
        one_liner='先数每个数出现几次，两两一对，剩下的就是落单的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次从 `nums` 里选两个==相等==的数，一起删掉，形成一个数对',
                 '尽量多地操作，返回 `[数对数, 剩余数字个数]`',
                 '示例：`[1,3,2,1,3,2,2]` → `[3,1]`'],
        quote='统计每个元素的出现次数，两两一对，得到对数。用 nums 长度减去对数的两倍就得到剩余数字的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['出现 `c` 次的数，最多配成 `c // 2` 对，与顺序无关',
              '用 `Counter` 数一遍，对所有计数求和得 `pairs`',
              '每对用掉 2 个数，所以剩余 = `len(nums) − 2×pairs`'],
        summary=['时间 `O(n)`，空间 `O(n)`（`Counter`）',
                 '剩余个数不需要再统计：总数减去 `2 × pairs` 即可',
                 '题目值域只有 0~100，用长为 101 的数组计数也行',
                 '题解还给了一次遍历的写法（出现偶数次就加一对），这里演示最简的计数写法'],
    ),
)
