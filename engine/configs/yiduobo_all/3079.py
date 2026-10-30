CONFIG = dict(
    num=3079, title='求出加密整数的和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 分离数位',
    tags=[],
    code='''
class Solution(object):
    def sumOfEncryptedInt(self, nums):

        res = 0
        for v in nums:
            mul = 1
            ma = 0
            while True:
                ma = max(ma, v % 10)
                v //= 10
                if v == 0:
                    break
                mul = mul * 10 + 1
            
            res += mul * ma
        
        return res
''',
    call='Solution().sumOfEncryptedInt([10, 21, 999])',
    expect=11 + 22 + 999,
    views=[
        dict(type='array', var='nums', h=200),
        dict(type='text', h=120, size=40, fn=lambda S: (f"剩余 `v = {S['v']}`，当前最大数位 `ma = {S['ma']}`，基数 `mul = {S['mul']}`" if 'ma' in S and 'mul' in S else '')),
        dict(type='text', h=120, size=40, fn=lambda S: (f"加密值 = `mul × ma` = `{S['mul']} × {S['ma']}` = =={S['mul']*S['ma']}==" if 'ma' in S and 'mul' in S and S['_line'] == 15 else '')),
    ],
    watch=['v', ('ma', 'ma', 'pink'), ('mul', 'mul', 'blue'), ('res', 'res', 'green')],
    captions={
        'mul = 1': '新的数字：基数 `mul` 先是 1（至少有一位），最大值 `ma` 从 0 开始',
        'ma = max': '看最低位 `v % 10`，更新最大数位：`ma = {ma}`',
        'v //= 10': '去掉最低位：`v` → =={v}=={v == 0 and "，没有数位了" or ""}',
        'if v == 0': '`v == 0` 吗？{"==是==，数位分离完毕，退出循环" if v == 0 else "否，还有更高位"}',
        'mul = mul': '还有高位，基数多一位：`mul` → =={mul}==',
        'res += ': '`mul × ma` = `{mul} × {ma}` = =={mul*ma}==，累加：`res = {res}`',
    },
    cards=dict(
        one_liner='分离数位的同时，更新基数 111…111',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['加密：每一位都换成这个数里最大的数位，如 `523 → 555`',
                 '返回所有元素加密后的和',
                 '示例：`[10,21,31]` → `66`'],
        quote='分离完毕后，使用这个基数乘以分离出来的最大值就得到了加密后的整数，将其累加到答案中即可。',
        quote_src='—— yiduobo 题解',
        idea=['`while True` 先处理一位再判断：保证个位数也算一位',
              '基数的位数取决于分离数字的轮次',
              '分离完用 `mul * ma` 得到加密整数'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `v /= 10` 已改为 `v //= 10`',
                 '==基数初值是 1==，退出循环前才补位，所以位数刚好',
                 '这里用 `while True + break`，先取数位再判断是否结束']),
)
