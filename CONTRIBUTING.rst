============
Contributing
============

If you would like to contribute, I'd be glad to merge your pull requests.

You should however stick to the `PEP8 Style Guide`_. A text width of 79 characters
is recommended. However, you are allowed to go up to 99 characters per line *if* you
need some extra space for readability concerns.

Implementing a new feature that has a GitLab issue
--------------------------------------------------

If you wish to implement a new feature (or even only start working on it) that already has a
GitLab issue, please pay attention to its milestone. The milestone indicates in which version
this feature is planned, and thus, to which branch you should send your pull request.

If the issue has no milestone, please indicate in a comment that you are interested in working
on this feature and would like to know in which version it is planned. It is likely that in such
case, the feature was not scheduled because of a very low priority and nobody available to do it.
So we will be happy to merge your work into the next minor version.

If the issue is already assigned to someone, you should tell him in the comments that you are
willing to help on this feature.

Implementing a new feature that does not have a GitLab issue
------------------------------------------------------------

If you wish to implement a new feature that has no GitLab issue yet, please create a GitLab issue
so that:

- we know someone is working on this feature
- we can discuss about it before you send a pull request
- we can decide on which version it should be implemented

Note: any improvement that changes the code logic and is not a bug fix is considered a new feature.
So even if you only add an attribute an object, please create a new issue.

Fixing a bug, a typo or generally improving the code readability
----------------------------------------------------------------

Improving the documentation
---------------------------

Improving test cases
--------------------

.. _`PEP8 Style Guide`: https://www.python.org/dev/peps/pep-0008/
