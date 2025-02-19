"""
Tensornetwork Simplification
"""
# part of the implementations and ideas are inspired from
# https://github.com/jcmgray/quimb/blob/a2968050eba5a8a04ced4bdaa5e43c4fb89edc33/quimb/tensor/tensor_core.py#L7309-L8293
# (Apache 2.0)
# We here more focus on tensornetwork derived from circuit simulation
# and consider less on general tensornetwork topology.
# Note we have no direct hyperedge support in tensornetwork package

from typing import Any, List, Optional, Tuple

import numpy as np
import tensornetwork as tn

from .cons import _multi_remove, backend


def infer_new_size(a: tn.Node, b: tn.Node, include_old: bool = True) -> Any:
    shared_edges = tn.get_shared_edges(a, b)
    a_dim = np.prod([e.dimension for e in a])
    b_dim = np.prod([e.dimension for e in b])
    new_dim = np.prod([e.dimension for e in a if e not in shared_edges]) * np.prod(
        [e.dimension for e in b if e not in shared_edges]
    )
    if include_old is True:
        return new_dim, a_dim, b_dim
    return new_dim


def infer_new_shape(a: tn.Node, b: tn.Node, include_old: bool = True) -> Any:
    """
    Get the new shape of two nodes, also supporting to return original shapes of two nodes.

    :Example:

    >>> a = tn.Node(np.ones([2, 3, 5]))
    >>> b = tn.Node(np.ones([3, 5, 7]))
    >>> a[1] ^ b[0]
    >>> a[2] ^ b[1]
    >>> tc.simplify.infer_new_shape(a, b)
    >>> ((2, 7), (2, 3, 5), (3, 5, 7))
    >>> # (shape of a, shape of b, new shape)

    :param a: node one
    :type a: tn.Node
    :param b: node two
    :type b: tn.Node
    :param include_old: Whether to include original shape of two nodes, default is True.
    :type include_old: bool
    :return: The new shape of the two nodes.
    :rtype: Union[Tuple[int, ...], Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]]
    """
    shared_edges = tn.get_shared_edges(a, b)
    a_shape = tuple([e.dimension for e in a])
    b_shape = tuple([e.dimension for e in b])
    new_shape = tuple(
        ([e.dimension for e in a if e not in shared_edges])
        + ([e.dimension for e in b if e not in shared_edges])
    )
    if include_old is True:
        return new_shape, a_shape, b_shape
    return new_shape


def pseudo_contract_between(a: tn.Node, b: tn.Node, **kws: Any) -> tn.Node:
    """
    Contract between Node ``a`` and ``b``, with correct shape only and no calculation

    :param a: [description]
    :type a: tn.Node
    :param b: [description]
    :type b: tn.Node
    :return: [description]
    :rtype: tn.Node
    """
    shared_edges = tn.get_shared_edges(a, b)
    new_shape = tuple(
        ([e.dimension for e in a if e not in shared_edges])
        + ([e.dimension for e in b if e not in shared_edges])
    )
    new_node = tn.Node(backend.zeros(new_shape))
    tn.network_components._remove_edges(shared_edges, a, b, new_node)
    return new_node


def _split_two_qubit_gate(
    a: tn.Node,
    max_singular_values: Optional[int] = None,
    max_truncation_err: Optional[float] = None,
    fixed_choice: Optional[int] = None,
) -> Any:
    if (max_singular_values is not None) and (fixed_choice is None):
        fixed_choice = 1
    ndict, _ = tn.copy([a])
    n = ndict[a]
    n1, n2, _ = tn.split_node(
        n,
        left_edges=[n[0], n[2]],
        right_edges=[n[1], n[3]],
        max_singular_values=max_singular_values,
        max_truncation_err=max_truncation_err,
    )
    if fixed_choice == 1:
        # still considering better API type for fixed_choice
        return n1, n2, False
    s1 = n1.tensor.shape[-1]  # bond dimension
    n3, n4, _ = tn.split_node(
        n,
        left_edges=[n[0], n[3]],
        right_edges=[n[1], n[2]],
        max_singular_values=max_singular_values,
        max_truncation_err=max_truncation_err,
    )
    if fixed_choice == 2:  # swap one
        return n3, n4, True  # swap
    s2 = n3.tensor.shape[-1]
    if (s1 >= 4) and (s2 >= 4):
        # jax jit unspport split_node with trun_err anyway
        # tf function doesn't work either, though I believe it may work on tf side
        # CANNOT DONE(@refraction-ray): tf.function version with trun_err set
        return None
    if s1 <= s2:  # equal is necessary for max values to pick on unswap one
        return n1, n2, False  # no swap
    return n3, n4, True  # swap


def _rank_simplify(nodes: List[Any]) -> Tuple[List[Any], bool]:
    # if total_size is None:
    # total_size = sum([_sizen(t) for t in nodes])
    is_changed = False
    l = len(nodes)
    for i in range(l):
        if i < len(nodes):
            n = nodes[i]
            for e in n:
                if not e.is_dangling():
                    nd, ad, bd = infer_new_shape(e.node1, e.node2)
                    if nd <= ad or nd <= bd:
                        njs = [
                            i
                            for i, n in enumerate(nodes)
                            if id(n) in [id(e.node1), id(e.node2)]
                        ]
                        new_node = tn.contract_between(e.node1, e.node2)
                        # contract(e) is not enough for multi edges between two tensors
                        nodes[njs[0]] = new_node
                        nodes = _multi_remove(nodes, [njs[1]])
                        is_changed = True
                        break  # switch to the next node
        else:
            break
    return nodes, is_changed


def _full_rank_simplify(nodes: List[Any]) -> List[Any]:
    """
    Simplify the list of tc.Nodes without increasing the rank of any tensors.

    :Example:

    .. code-block:: python

        a = tn.Node(np.ones([2, 2]), name="a")
        b = tn.Node(np.ones([2, 2]), name="b")
        c = tn.Node(np.ones([2, 2, 2, 2]), name="c")
        d = tn.Node(np.ones([2, 2, 2, 2, 2, 2]), name="d")
        e = tn.Node(np.ones([2, 2]), name="e")
        a[1] ^ c[0]
        b[1] ^ c[1]
        c[2] ^ d[0]
        c[3] ^ d[1]
        d[4] ^ e[0]

        f = tn.Node(np.ones([2, 2]), name="f")
        g = tn.Node(np.ones([2, 2, 2, 2]), name="g")
        h = tn.Node(np.ones([2, 2, 2, 2]), name="h")
        f[1] ^ g[0]
        g[2] ^ h[1]

    >>> nodes = simplify._full_rank_simplify([a, b, c, d, e])
    >>> nodes[0].shape
    [2, 2, 2, 2, 2, 2]
    >>> len(nodes)
    1
    >>> len(simplify._full_rank_simplify([f, g, h]))
    2

    :param nodes: List of Nodes
    :type nodes: List[Any]
    :return: List of Nodes
    :rtype: List[Any]
    """
    nodes, is_changed = _rank_simplify(nodes)
    while is_changed:
        nodes, is_changed = _rank_simplify(nodes)
    return nodes


# TODO(@refraction-ray): utilize more simplification method in contractor preprocessing
