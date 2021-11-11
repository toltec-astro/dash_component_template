#!/usr/bin/env python

from dash_component_template.template import (
    NullComponent, WrappedComponent,
    _make_component_template_cls, _get_component_info)
import dash_bootstrap_components as dbc


def test_null_component():

    a = NullComponent(id=1)

    b = a.child(NullComponent(id=2))

    assert b.parent is a

    assert b.id == 2
    assert a.id == 1
    a.id = 'abc'
    assert a.id == 'abc'
    assert a.layout == [[]]


def test_wrapped_component():

    a = WrappedComponent(dbc.Button(color='primary'))

    b = a.child(dbc.Container(fluid=True))

    assert a.children == (b, )


def test_component_template():
    a = NullComponent(id='root')
    b = a.child(dbc.Button, color='primary')
    c1 = b.child(dbc.Button, color='secondary')
    c2 = b.child(dbc.Button, color='secondary')
    assert a.children == (b, )
    assert b.children == (c1, c2)
    assert b.color == 'primary'
    assert a.layout[0].color == 'primary'
    assert a.layout[0].id == b.id
    # assert a.layout

    # check cached
    template_cls = _make_component_template_cls(dbc.Container)
    assert template_cls._idt_class_label == 'container'

    template_cls2 = _make_component_template_cls(dbc.Container)

    assert template_cls is template_cls2

    assert _make_component_template_cls.cache_info().currsize > 0
    assert _get_component_info.cache_info().currsize > 0
