# appi
Another Portage Python Interface

## Why not `portage`?

The reason why I decided to create this alternative to the standard python `portage` module, is that I spent a few time trying to read and learn this API in order to be able to write portage utilities. However, I found it especially unreadable, having a complex inconsistent structure, and most of all, lacks of documentation. This made me flee each time I tried to put my nose into this module.

Note: I mean no offense to `portage` python module developers and former developers. I give them all due respect for maintaining such project.

So, after some back-and-forth, I said to myself: "Hey, it's Linux after all, if I don't like the way something is done, let's do it *my* way!".

So was born `appi`. It is still at an early stage, but I hope someday it will have enough features to enable portage-based distributions newcomers, having hard time with the `portage` api, to use it and improve it.

## Examples

### Atom

```python
>>> from appi.atom import Atom
>>> a = Atom('portage')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/tony/Workspace/Funtoo/appi/appi/atom.py", line 76, in __init__
    atom_string, code='missing_category')
appi.atom.AtomError: portage may be ambiguous, please specify the category.
>>> a = Atom('portage', strict=False)
>>> a.list_matching_ebuilds()
{<Ebuild: 'sys-apps/portage-2.4.1-r1::gentoo'>, <Ebuild: 'sys-apps/portage-2.4.3-r1::gentoo'>}
>>> a
<Atom: 'portage'>
>>> b = Atom('>=sys-apps/portage-2.4.2')
>>> b
<Atom: '>=sys-apps/portage-2.4.2'>
>>> b.list_matching_ebuilds()
{<Ebuild: 'sys-apps/portage-2.4.3-r1::gentoo'>}
```


## Contributing

If you would like to contribute, I'd be glad to merge your pull requests.

You should however stick to the [PEP8 Style Guide][1]. A text width of 79 characters
is recommended. However, you are allowed to go up to 99 characters per line *if* you
need some extra space for readability concerns.

[1]: https://www.python.org/dev/peps/pep-0008/
