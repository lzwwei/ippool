class IpPoolError(Exception):
    def __str__(self):
        return repr('Cookie Pool Error!!!')

class PoolEmptyError(IpPoolError):
    def __str__(self):
        return repr('Ip Pool is Empty!!!')