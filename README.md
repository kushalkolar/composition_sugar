# Composition Sugar
Syntactic sugar for function composition in Python

See usage examples on binder\
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kushalkolar/composition_sugar/master)

Create readable pipelines for processing data.

```python
data >> FuncA(*args, **kwargs) >> FuncB(*args, **kwargs) >> FuncC(*args, **kwargs) >> ...
```

This is equivalent to:

```python
FuncC(FuncB(FuncA(data, *args, **kwargs), *args, **kwargs), *args, **kwargs)
```

### Data Container

Define a data container

Example with pandas DataFrame:

```python
from core import Container

class DataFrameContainer(Container):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    @classmethod
    def from_hdf5(cls, path: str, key: str):
        df = pd.read_hdf(path, key=key, mode='r')
        return cls(df)
````

### Processing Node

Simply use the `@node` decorator on a function to use it with a data container

Example that splices arrays in a specific DataFrame column:

```python
from core import node

@node
def splice(container, data_column, start, stop):
    container.df['spliced'] = container.df[data_column].apply(lambda a: a[start:stop])
    return container
```
        
Basic format:

```python
@node
def func(container, *args, **kwargs):
    # do stuff to container
    return container
```

**The first argument _must_ always be the data container**

You can also create more complex processing nodes by inheriting from Node:

```python
from core import Node

class Complex(Node):        
def process(self, container, *args, **kwargs):
    # do more complex stuff
    something_complex = self.some_other_func()

    # do other stuff
    final_result = do_more_stuff(something_complex)

    # the container which went through complex processing
    return final_result

def some_other_func(self, ...):
    # does some stuff

def do_more_stuff(self, ...):
    # more stuff
```

See full examples on binder\
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kushalkolar/composition_sugar/master)
