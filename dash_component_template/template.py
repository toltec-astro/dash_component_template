#!/usr/bin/env python


import numpy as np
import inspect
import functools
from collections.abc import Iterable
from abc import abstractmethod
from dash.development.base_component import Component as DashComponentBase
from dash.development.base_component import ComponentMeta as DashComponentMeta
import dash_bootstrap_components as dbc
from dataclasses import dataclass
from .idtree import IdTree


__all__ = [
    'Template', 'NullComponent', 'WrappedComponent', 'ComponentTemplate',
    'DashComponentInfo'
    ]


class Template(IdTree):
    """An abstract base class that encapsulate layout and callbacks into a
    reusable structure.

    The core of this class is the :meth:`child` method which creates and
    maintains a tree of instances whose nodes have unique ids assigned.

    Actual Dash components are typically not instantiated when template
    instances are created. Instead, the template instances hold the factories
    and the arguments, and they only get called when :attr:`layout` property is
    queried. This call will be propagated down to all the children of the
    calling instance, result in a tree of Dash component objects readily be
    consumed by the Dash ``app`` instance.

    Complex layout can be built in a declarative fashion with
    repeated call to the :meth:`child` factory function from any node in the
    tree. All the node have their unique id (the Dash component id) managed
    automatically and they can be accessed with the :attr:`id` property, which
    can then be consumed in callback definitions.

    Subclass of this base class shall implement method :meth:`setup_layout`,
    within which one can declare a layout using :meth:`child`, and define any
    callbacks for them components.

    Subclasses defined this way will act as re-usable templates that can be
    plugged anywhere in other trees of templates. Through this mechanism, very
    complex layout can be built in a fully modularized fashion.
    """

    @property
    def id(self):
        return getattr(self, '_static_id', IdTree.id.fget(self))

    # The id setter allows overwriting id manually for an object.
    @id.setter
    def id(self, value):
        self._static_id = value

    @property
    @abstractmethod
    def layout(self):
        """Implement this to return a valid Dash layout object."""
        return NotImplemented

    def before_setup_layout(self, app):
        """Hook that run before the `setup_layout` function call."""
        pass

    def after_setup_layout(self, app):
        """Hook that run after the `setup_layout` function call."""
        pass

    @abstractmethod
    def setup_layout(self, app):
        """Implement this to declare layout components and their callbacks.

        This base implementation has to be called in the subclass
        implementation to ensure any child templates also get properly setup.
        This is particularly important for templates that contain templates in
        their descendants.

        The convention is to structure the implementation in the following
        way::

            def setup_layout(self, app):
                child0 = self.child(some_dash_type, ...)
                child1 = child0.child(some_template_cls, ...)
                # This will trigger `setup_layout` call to all the children,
                # which may make available some attributes
                super().setup_layout(app)

                @app.callback(...)
                def some_callback(...):
                    return
        """
        self.before_setup_layout(app)
        for child in self.children:
            child.setup_layout(app)
        self.after_setup_layout(app)

    def child(self, factory, *args, **kwargs):
        """Return a child template instance.

        The actual type of child template is delegated to the appropriate
        subclass based on the type of `factory`:

        1. `factory` is a `Template` instance. The instance is
        added as-is as the child of this object. `ValueError` is raised if
        `args` or `kwargs` are passed.

        2. `factory` is a Dash component class, (e.g.,
        `~dash_html_components.Div`). A `ComponentTemplate` object is created
        and returned. `args` and `kwargs` are passed to the constructor of
        the ComponentTemplate, which is passed down to the Dash component class
        when actual Dash component is created.

        3. `factory` is a Dash component instance. The instance is wrapped in a
        `WrappedComponent` object and returned. `ValueError` is raised if
        `args` or `kwargs` are passed.

        `ValueError` is raised if `factory` does not conform to the cases
        listed above.

        """
        def ensure_no_extra_args():
            if args or kwargs:
                raise ValueError(
                    f"child call arguments and keyword arguments shall not"
                    f" be specified for factory {factory}")

        if isinstance(factory, Template):
            ensure_no_extra_args()
            factory.parent = self
            return factory

        if isinstance(factory, DashComponentMeta):
            # dash component class
            child_cls = _make_component_template_cls(factory)

        elif isinstance(factory, DashComponentBase):
            # dash component instance
            ensure_no_extra_args()
            args = (factory, )
            child_cls = WrappedComponent
        else:
            raise ValueError(
                    f"unable to create child template"
                    f" from type {type(factory)}")
        return child_cls(*args, **kwargs, parent=self)

    def grid(self, nrows, ncols, squeeze=True):
        """Return a dash bootstrap component grid.

        Parameters
        ----------
        nrows : int
            The number of rows.
        ncols : int
            The number of cols per row.
        squeeze : bool, optional
            If True, insignificant dimensions are removed from the returned
            array.
        """
        # note we need to check the current type and see if it is container
        # if not, a container object needs to be created to make
        # the grid functional correctly, per the documentation of dbc.
        result = np.full((nrows, ncols), None, dtype=object)
        if hasattr(self, 'dash_component_info') and (
                self.dash_component_info.type is dbc.Container):
            container = self
        else:
            container = self.child(dbc.Container, fluid=True)
        current_row = None
        for i in range(nrows):
            for j in range(ncols):
                if j == 0:
                    current_row = container.child(dbc.Row)
                result[i, j] = current_row.child(dbc.Col)
        if squeeze:
            result = np.squeeze(result)
        return result


class NullComponent(Template):
    """A component template that does not represent an actual component.

    This is useful to serve as a root to build standalone layout that does not
    attached immediately to the main Dash app layout tree.
    """

    def __init__(self, id, parent=None):
        self._node_id = id
        super().__init__(parent=parent)

    @property
    def idbase(self):
        self._node_id

    @property
    def id(self):
        return self._node_id

    @id.setter
    def id(self, id):
        self._node_id = id

    def setup_layout(self, app):
        super().setup_layout(app)

    @property
    def layout(self):
        return [c.layout for c in self.children]


@dataclass
class DashComponentInfo(object):
    """A class to hold Dash component class related info."""

    type: type
    """The Dash component class."""

    prop_names: list
    """The property names of the Dash component class."""

    @staticmethod
    def _get_component_prop_names(component_cls):
        return inspect.getfullargspec(component_cls.__init__).args[1:]

    @classmethod
    def from_component_cls(cls, component_cls):
        """Return the Dash component info from `component_cls`."""
        prop_names = cls._get_component_prop_names(component_cls)
        return cls(type=component_cls, prop_names=prop_names)


@functools.lru_cache(maxsize=None)
def _get_component_info(component_cls):
    return DashComponentInfo.from_component_cls(component_cls)


_missing_defualt = object()
"""A value used to indicate a missing default value."""


def _get_class_meta_attr(cls, attr, default=_missing_defualt):
    """A helper function to get class Meta attribute.

    This is a convention we use for defining attributes that are consumed
    during class construction::

        class A:
            class Meta:
                some_option = 1

    This example defines a meta attribute ``some_option`` for class ``A``.
    """
    Meta = getattr(cls, 'Meta', None)
    if Meta is None:
        if default is _missing_defualt:
            raise AttributeError(f"meta attribute {attr} not found.")
        return default
    if default is _missing_defualt:
        return getattr(Meta, attr)
    return getattr(Meta, attr, default)


class ComponentFactoryMixin(object):
    """A mixin class that holds and processes info about Dash components class.

    The methods of this mixin class depends on the presence of attribute
    ``dash_component_info`` on the implementing class or its instance.

    This attribute can be automatically created if the subclass provides
    ``Meta`` class member that provides a `component_cls` attribute.

    """
    def __init_subclass__(cls):
        component_cls = _get_class_meta_attr(cls, 'component_cls', None)
        if component_cls is not None:
            if not issubclass(component_cls, DashComponentBase):
                raise TypeError(
                    f"invalid Meta attribute component_cls {component_cls}")
            component_info = _get_component_info(component_cls)
        else:
            component_info = None
        cls.dash_component_info = component_info


class WrappedComponent(Template, ComponentFactoryMixin):
    """A thin wrapper round a Dash component instance.

    The id is the id of the wrapped Dash component.

    Instance of this class is typically created by the :meth:`Template.child`
    factory method with the first argument being a Dash component instance.
    """

    def __init__(self, component, parent=None):
        # Because dash component is set at instance level, we update
        # the dash_component info here at the instance level as well.
        super().__init__(parent=parent)
        self._component = component
        self.dash_component_info = _get_component_info(
            self._component.__class__)

    @property
    def idbase(self):
        self.id

    @property
    def id(self):
        return self._component.id

    @id.setter
    def id(self, id):
        self._component.id = id

    def setup_layout(self, app):
        super().setup_layout(app)

    @property
    def layout(self):
        return self._component


class ComponentTemplate(Template, ComponentFactoryMixin):
    """A component class for Dash component type.

    Instances of this class is typically created from calling the
    :meth:`Template.child` method, which allows declaring a tree
    of components with automatic unique ids.

    Subclasses of this class that wraps a single Dash component class
    is typically created automatically when used by the :meth:`child` call.
    Instances of these classes serves as a lazy evaluation proxy around the
    native Dash component class. Dash component properties on the template
    instance are passed to the Dash component class constructor when the
    :attr:`layout` property is queried.

    User code can define subclass of this class that implement the
    :meth:`setup_layout` method, in which a set of interrelated Dash components
    and their related callbacks can be defined. Such class acts as a "template"
    and one can use of multiple instances of it in a single page application,
    without the need to worrying about possible confliction in the ids.
    """

    # these are the props managed by this class to provide recursive
    # layout generation and automatic id
    _managed_prop_names = ['id', 'children']

    # we need keep a list of methods and properties for the class itself
    # any dash compoennt property that conflict with this list
    # will get shadowed.
    _reserved_prop_names = [
        k for k in dir(Template) if not (
            k.startswith('_')
            or k in ('children', 'id'))
        ]

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.dash_component_info is None:
            return
        # here we generate the properties and setters for all the template
        # prop names
        # in particular, prop names in the reserved prop names list will
        # have a '_' appended to it.

        def _make_property(var_name):

            def getter(self):
                return getattr(self, var_name)

            def setter(self, value):
                return setattr(self, var_name, value)
            return property(fget=getter, fset=setter)

        prop_names = cls.dash_component_info.prop_names
        for prop_name in prop_names:
            if prop_name in cls._managed_prop_names:
                # for managed prop names, we do not generate the property
                # otherwise the defined id and children hooks will be
                # shadowed
                continue
            var_name = f'_dcp_{prop_name}'
            setattr(
                cls, cls._encode_dash_prop_name(prop_name),
                _make_property(var_name))

    @classmethod
    def _encode_dash_prop_name(cls, prop_name):
        # this checks the reserved names and append a '_' when conflict.
        if prop_name in cls._reserved_prop_names:
            return f'{prop_name}_'
        return prop_name

    @classmethod
    def _decode_dash_prop_name(cls, prop_name):
        if prop_name.endswith('_'):
            return prop_name[:-1]
        return prop_name

    def _set_dash_props(self, kwargs):
        for prop_name, prop_value in kwargs.items():
            setattr(self, self._encode_dash_prop_name(prop_name), prop_value)

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent=parent)

        # put args in to kwargs by inspect the prop list.
        # this allows the syntax of creating template similar to
        # creating the underlying Dash components.
        prop_names = self.dash_component_info.prop_names
        for i, arg in enumerate(args):
            prop_name = prop_names[i]
            if prop_name in kwargs:
                raise ValueError(
                    f"duplicated argument {prop_name} in args and kwargs.")
            kwargs[prop_name] = arg
        self._set_dash_props(kwargs)
        # this dict is to hold any wildcard props for Dash compoennt
        # these properties cannot be set directly as attributes. Instead,
        # use set_wildcard_prop to set them.
        self._wildcard_props = dict()

    def set_wildcard_prop(self, name, value):
        """Set the wildcard props of the component.

        This is necessary because we do not have mechanism to handle those.
        """
        self._wildcard_props[name] = value

    @classmethod
    def _ensure_template_instance(cls, value):
        """Wrap `value` as a `Template` instance if it is not already one."""
        if value is None:
            return None
        if isinstance(value, Template):
            return value
        return WrappedComponent(value)

    @IdTree.parent.setter
    def parent(self, value):
        # we make sure the value set here is wrapped as a template
        IdTree.parent.fset(self, self._ensure_template_instance(value))

    @IdTree.children.setter
    def children(self, children):
        """Setter to ensure the children is also a `Template` instance."""
        # we make sure the value set here is wrapped as a template
        if not isinstance(children, Iterable) or isinstance(
                children, (str, DashComponentBase)):
            children = [children]
        children = list(map(self._ensure_template_instance, children))
        IdTree.children.fset(self, children)

    def setup_layout(self, app):
        super().setup_layout(app)

    @property
    def layout(self):
        """The layout generated from traversing the component tree.

        The traversing is depth first.

        .. note::
            Properties with callable values are evaluated the time the property
            is queried.
        """
        if self.dash_component_info is None:
            raise ValueError("No dash component info found.")
        component_kwargs = dict()
        for prop_name in self.dash_component_info.prop_names:
            attr_name = self._encode_dash_prop_name(prop_name)
            if not hasattr(self, attr_name):
                continue
            prop_value = getattr(self, attr_name)
            # get children layout
            if prop_name == 'children':
                prop_value = tuple(c.layout for c in prop_value)
                if len(prop_value) == 1:
                    # let dash handle the re-wrapping
                    prop_value = prop_value[0]
            if callable(prop_value):
                prop_value = prop_value()
            component_kwargs[prop_name] = prop_value
        return self.dash_component_info.type(
            **component_kwargs, **self._wildcard_props)


@functools.lru_cache(maxsize=None)
def _make_component_template_cls(component_cls):
    """Return `ComponentTemplate` for dash component class `component_cls`."""
    # create if not exists
    return ComponentTemplate.__class__(
            f"{component_cls.__name__}",
            (ComponentTemplate, ), dict(
                Meta=type(
                    'Meta', (object, ), dict(component_cls=component_cls)),
                )
            )
