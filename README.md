# appi
Another Portage Python Interface


## Why not `portage`?

The reason why I decided to create this alternative to the standard python `portage` module,
is that I spent a few time trying to read and learn this API in order to be able to write
portage utilities. However, I found it especially unreadable, having a complex inconsistent
structure, and most of all, lacks of documentation. This made me flee each time I tried to
put my nose into this module.

Note: I mean no offense to `portage` python module developers and former developers.
I give them all due respect for maintaining such project.

So, after some back-and-forth, I said to myself: "Hey, it's Linux after all, if I don't like
the way something is done, let's do it *my* way!".

So was born `appi`. It is still at an early stage, but I hope someday it will have enough features
to enable portage-based distributions newcomers, having hard time with the `portage` api,
to use it and improve it.  


## Examples

### Atom

```python
>>> from appi import Atom
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
>>> # Considering a second repository named "sapher" containing qtile ebuilds
...
>>> Atom('=x11-wm/qtile-9999').list_matching_ebuilds()
{<Ebuild: 'x11-wm/qtile-9999::gentoo'>, <Ebuild: 'x11-wm/qtile-9999::sapher'>}
```


## Versioning Policy

We use the following version format: `M.m.p`

- `M` is the major version
- `m` is the minor version
- `p` is the patch version

We may also package pre-releases (postfixed with `_preN`, where `N` is the pre-release version)
and release candidates (postfixed with `_rcN`, where N is the release candidate version).

**Starting from version `1.0.0`,** a major version bump means:

- Global refactoring of the code base
- Removal of features deprecated in the previous releases

A minor version bump means:

- New features
- Existing features improvement
- Features deprecation (raising warnings) which will be removed in the next major version

A patch version bump means:

- Bug fixes
- Security fixes

Thus, backward compatibility is maintained across minor versions, but broken at each
major version bump. However:

- Major version bumps should be very rare
- If you pay attention to the few deprecation warnings that may appear across minor version bumps,
  and fix them along the way, upgrading to a new major version will require no work at all.
- Support and patches **will** still be provided for the last two minor versions before
  the curent version.

**Before version `1.0.0`,** any minor version bump may break backward compatibility.


## Contributing

If you would like to contribute, I'd be glad to merge your pull requests.

You should however stick to the [PEP8 Style Guide][1]. A text width of 79 characters
is recommended. However, you are allowed to go up to 99 characters per line *if* you
need some extra space for readability concerns.

### Implementing a new feature that has a GitHub issue

If you wish to implement a new feature (or even only start working on it) that already has a
GitHub issue, please pay attention to its milestone. The milestone indicates in which version
this feature is planned, and thus, to which branch you should send your pull request.

If the issue has no milestone, please indicate in a comment that you are interested in working
on this feature and would like to know in which version it is planned. It is likely that in such
case, the feature was not scheduled because of a very low priority and nobody available to do it.
So we will be happy to merge your work into the next minor version.

If the issue is already assigned to someone, you should tell him in the comments that you are
willing to help on this feature.

### Implementing a new feature that does not have a GitHub issue

If you wish to implement a new feature that has no GitHub issue yet, please create a GitHub issue
so that:

- we know someone is working on this feature
- we can discuss about it before you send a pull request
- we can decide on which version it should be implemented

Note: any improvement that changes the code logic and is not a bug fix is considered a new feature.
So even if you only add an attribute an object, please create a new issue.

### Fixing a bug, a typo or generally improving the code readability

### Improving the documentation

### Improving test cases


[1]: https://www.python.org/dev/peps/pep-0008/
