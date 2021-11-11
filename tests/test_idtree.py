#!/usr/bin/env python

from dash_component_template.idtree import IdTree


class TestIdTree(object):

    class ClassWithIdTree(IdTree):
        pass

    def setup_class(self):
        self.objs = [self.ClassWithIdTree() for _ in range(2)]

    def test_idt_class_label(self):
        assert self.ClassWithIdTree._idt_class_label == \
                "classwithidtree"

    def test_idt_instance_label(self):
        for i, obj in enumerate(self.objs):
            assert obj._idt_instance_label == i

    def test_idt_instances(self):
        for obj in self.objs:
            assert obj in self.ClassWithIdTree._idt_instances

    def test_idbase(self):
        assert self.objs[0].idbase == 'classwithidtree0'
        assert self.objs[1].idbase == 'classwithidtree1'

    def test_id(self):
        for i in range(2):
            self.objs[i].parent = None
            assert self.objs[i].id == self.objs[i].idbase == \
                f'classwithidtree{i}'
        self.objs[1].parent = self.objs[0]
        assert self.objs[1].id == 'classwithidtree0-classwithidtree1'
