NUMS = [4, 14, 2]


def _bits(S):
    if 'num' not in S:
        return '汉明距离按位算：每一位上，`0` 和 `1` 配对才产生距离'
    if S.get('_line', 0) >= 14:
        return '各数二进制：' + '，'.join(f'`{v:b}`' for v in S['nums']) + '；逐位累加 `0 与 1 的配对数`'
    if S.get('tmp') is None:
        return f'当前数 `num = {S["num"]}`，二进制 `{S["num"]:b}`'
    return f'`num = {S["num"]}`（二进制 `{S["num"]:b}`），剩余 `tmp = {S["tmp"]:b}`，正在看第 `pos = {S.get("pos", 0)}` 位'


def _res_txt(S):
    if 'cnt' not in S or S.get('_line') not in (16,):
        return ''
    n = len(S['nums'])
    return f'该位：`{S["cnt"]}` 个 1、`{n - S["cnt"]}` 个 0 → 配对数 `{S["cnt"]} × {n - S["cnt"]}` = =={S["cnt"] * (n - S["cnt"])}=='


CONFIG = dict(
    num=477, title='汉明距离总和', difficulty='Medium', category='位运算',
    author='yiduobo', technique='按位统计 · 1 的个数 × 0 的个数',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def totalHammingDistance(self, nums):

        one_cnt = {}
        for num in nums:
            tmp = num
            pos = 0
            while tmp:
                if tmp & 1:
                    one_cnt[pos] = one_cnt.get(pos, 0) + 1
                tmp >>= 1
                pos += 1

        res = 0
        for cnt in one_cnt.values():
            res += (len(nums) - cnt) * cnt

        return res
''',
    call=f'Solution().totalHammingDistance({NUMS})',
    expect=6,
    views=[
        dict(type='text', h=90, size=28, fn=_bits),
        dict(type='array', var='nums', label='nums', h=170, cell=96,
             color=lambda S, i, v: 'blue' if S.get('num') == v and S.get('_line', 0) <= 12 and 'num' in S else None),
        dict(type='map', var='one_cnt', label='one_cnt（第 pos 位上 1 的个数）', fmt=lambda k, v: f'第 {k} 位: {v} 个', h=200, font=30),
        dict(type='text', h=90, size=28, fn=_res_txt),
    ],
    watch=['num', 'tmp', 'pos', ('res', 'res', 'green')],
    captions={
        'one_cnt = {}': '不枚举数对：先==按位==统计，每一位上有几个 1',
        'tmp = num': '取出 `num = {num}`，拷贝到 `tmp`，准备逐位右移',
        'while tmp': '`tmp = {tmp}` {"还有位没处理 → 继续" if tmp else "已经移空 → 这个数处理完"}',
        'if tmp & 1': '`tmp & 1 = {tmp & 1}`：{"最低位是 1 → 第 pos 位上的 1 计数 +1" if tmp & 1 else "最低位是 0 → 不计数"}',
        'one_cnt[pos]': '第 `{pos}` 位的 1 增加到 =={one_cnt[pos]}== 个',
        'tmp >>= 1': '右移一位，下一位变成最低位：`tmp = {tmp}`',
        'pos += 1': '位号加一：`pos = {pos}`',
        'res = 0': '开始逐位累加：这一位上 0 和 1 配对的次数',
        'for cnt': '这一位有 `cnt = {cnt}` 个 1',
        'res += (': '该位 0 有 `{len(nums)} - {cnt} = {len(nums) - cnt}` 个，只有 0 和 1 配对才产生距离：`{len(nums) - cnt} × {cnt}` = {(len(nums) - cnt) * cnt}，`res` → =={res}==',
    },
    cards=dict(
        one_liner='每一位独立：1 的个数 × 0 的个数',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['求数组里所有数两两之间汉明距离（二进制不同位的个数）的总和。',
                 '示例：`[4,14,2]` → 6。'],
        quote='汉明距离是按位计算的，不同位之间互不干扰，那么可以想办法按位计算出所有数在某一位上的汉明距离之和。',
        quote_src='—— yiduobo 题解',
        idea=['两两枚举是 `O(n²)`，太慢。改成每一位单独算。',
              '设这一位有 `cnt` 个 1，则有 `n - cnt` 个 0。',
              '只有 0 和 1 配对才贡献 1 点距离：共 `cnt × (n - cnt)` 对，各位加起来就是答案。'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`。',
                 '只统计出现过 1 的位，没出现 1 的位贡献为 0，字典里没有也没关系。',
                 '易错：0 和 0、1 和 1 配对都不产生距离，别把 `cnt` 当成配对数。',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行。'],
    ),
)
