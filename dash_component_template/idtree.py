#! /usr/bin/env python

from anytree import NodeMixin
from abc import ABCMeta
import weakref
import functools


__all__ = ['IdTreeMeta', 'IdTree']


class IdTreeMeta(type):
    """A meta class that manages `IdTree` instances.

    This meta class assign a unique label to each instance created.
    """

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._idt_instances = weakref.WeakSet()
        cls._idt_instances_label_iter = cls._get_instance_label_iter()

    def __call__(cls, *args, **kwargs):
        inst = super().__call__(*args, **kwargs)
        cls._idt_instances.add(inst)
        inst._idt_instance_label = next(cls._idt_instances_label_iter)
        return inst

    @property
    def _idt_class_label(cls):
        # TODO Revisit this. Maybe we need longer name or a hash
        return cls.__name__.lower()

    @staticmethod
    def _get_instance_label_iter():
        h = 0
        while True:
            yield h
            h += 1


class IdTreeABCMeta(IdTreeMeta, ABCMeta):
    """An adaptor meta class for abstract class `IdTree`."""
    pass


class IdTree(NodeMixin, metaclass=IdTreeABCMeta):
    """A class for managing a tree of instances with unique ids.

    A hierarchy of ids are managed in a tree-like data structure,
    enabled by the underlying `~anytree.node.nodemixin.NodeMixin` class.
    The id of each tree node is a compositions of the parent's id and
    the label of this node.

    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    @property
    def idbase(self):
        """The base name to use for generated unique id."""
        return (
            f"{self.__class__._idt_class_label}"
            f"{self._idt_instance_label}"
            )

    @functools.cached_property
    def _id_cached(self):
        """The unique id, cached to avoid repeated computation."""
        if self.parent is None or self.parent.id is None:
            return self.idbase
        return f"{self.parent.id}-{self.idbase}"

    # these hooks are used to trigger invalidating of the cached id.
    def _pre_detach(self, parent):
        self.__dict__.pop('_id_cached', None)

    def _post_detach(self, parent):
        self.__dict__.pop('_id_cached', None)

    def _pre_attach(self, parent):
        self.__dict__.pop('_id_cached', None)

    def _post_attach(self, parent):
        self.__dict__.pop('_id_cached', None)

    @property
    def id(self):
        """The unique id."""
        return self._id_cached
