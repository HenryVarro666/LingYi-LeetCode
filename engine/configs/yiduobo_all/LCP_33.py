CONFIG = dict(
    num='LCP 33', title='蓄水', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举蓄水轮数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def storeWater(self, bucket, vat):

        if sum(vat) == 0:
            return 0
        
        res = None
        for t in range(1, max(vat) + 1):
            now = 0
            for index, v in enumerate(vat):                
                min_buck = (v - 1) // t + 1
                if min_buck > bucket[index]:
                    now += min_buck - bucket[index]
            if res is None or res > t + now:
                res = t + now
        
        return res
''',
    call='Solution().storeWater([1, 2], [4, 5])',
    expect=4,
    views=[
        dict(type='array', var='vat', label='vat（每口水缸要装满的水量）', h=170),
        dict(type='array', var='bucket', label='bucket（水桶当前容量）', h=170),
        dict(type='text', h=130, fn=lambda S: (
            f"蓄水 `t={S['t']}` 轮：升级共 `{S['now']}` 次 + 蓄水 `{S['t']}` 次 = ==`{S['t'] + S['now']}`==" if 't' in S and 'now' in S else '')),
    ],
    watch=['t', 'now', 'min_buck', ('res', 'res', 'green')],
    skip=['now = 0'],
    captions={
        'if sum(vat) == 0': '所有水缸要求都是 0 → 什么都不用做，直接 `0`',
        'res = None': '`res` 记录最少操作数，先置空',
        'for t in range': '假设恰好蓄水 `t = {t}` 轮（`t` 最多枚举到最大要求 `{max(vat)}`，再多不会更优）',
        'for index, v': '看第 `{index}` 口缸：要装 `v = {v}`，水桶现容量 `{bucket[index]}`',
        'min_buck =': '只蓄 `{t}` 轮，每轮倒满一桶 → 桶至少要 `ceil({v}/{t})` = =={min_buck}==',
        'if min_buck > bucket': lambda S, B, r: (f'需要 `{S.min_buck}` > 现有 `{S.bucket[S.index]}` → 要升级' if S.min_buck > S.bucket[S.index]
                                                 else f'需要 `{S.min_buck}` ≤ 现有 `{S.bucket[S.index]}`，不用升级'),
        'now += min_buck': '升级 `{min_buck} − {bucket[index]}` 次，累计升级 `now` = =={now}==',
        'if res is None or': '这一轮总操作 `t + now = {t + now}`，与当前最少 `{B.res}` 比较',
        'res = t + now': '更优 → `res = {res}`',
        'return res': '最少操作次数 ==`{res}`==',
    },
    cards=dict(
        one_liner='枚举蓄水轮数 t，每口缸算出需要的桶容量，缺的就升级',
        complexity='时间 `O(n · max(vat))`，空间 `O(1)`',
        problem=['每次操作可以：给某个水桶容量 +1，或把所有水桶同时倒满对应的水缸（蓄水）',
                 '`bucket[i]` 是桶初始容量，`vat[i]` 是缸要装的水量，求让所有缸装满的最少操作数',
                 '示例：`bucket = [1,3], vat = [6,8]` → `4`',
                 '本视频：`bucket = [1,2], vat = [4,5]` → `4`'],
        quote='若当前的蓄水轮次为t，那么就可以枚举所有的水桶，通过对应的蓄水要求和t计算出当前水桶的最小容积，然后根据这个最小容积计算当前水桶需要扩容的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定蓄水 `t` 轮：缸 `v` 需要桶容量 `ceil(v / t)`',
              '容量不够的桶要升级，次数 = 缺的容量',
              '总操作 = `t` + 所有升级次数，枚举 `t` 取最小'],
        summary=['时间 `O(n · max(vat))`，空间 `O(1)`',
                 '全 0 要特判；`t` 从 1 开始，否则除零',
                 '原文为 Python 2 写法，`(v - 1) / t` 已改为 `//`',
                 '上取整写成 `(v-1)//t + 1`'],
    ),
)
