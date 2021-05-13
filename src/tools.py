from typing import List, Any, TypeVar, Callable, Optional

T = TypeVar('T')
OperationFunc = Callable[[T], T]


def rotate(lis: List[Any], n: int) -> List[Any]:
    n = n % len(lis)
    return lis[n:] + lis[:n]


def list_reverse(lis: List[Any]) -> List[Any]:
    ret = lis.copy()
    ret.reverse()
    return ret


def multi_operation(lis: List[T], operation: OperationFunc):
    return [operation(i) for i in lis]


def pull_octaves(n: int):
    def operation(x: int): return x + n * 12

    return operation


def flatten(lis: List[Optional[List[T]]]) -> List[T]:
    ret: List[T] = []
    for sublist in lis:
        if sublist is not None:
            for item in sublist:
                ret.append(item)
    return ret
