Release Process and Rules
=========================

Major Releases
--------------

A major release will include breaking changes. When it is versioned, it will
be versioned as ``vX.0.0``. For example, if the previous release was
``v1.2.10`` the next version will be ``v2.0.0``.

Breaking changes are changes that break backwards compatibility with prior
versions.

Major releases may also include miscellaneous bug fixes. The core developers of
conveyance are committed to providing a good user experience. This means we're
also committed to preserving backwards compatibility as much as possible. Major
releases will be infrequent and will need strong justifications before they are
considered.

Minor Releases
--------------

A minor release will not include breaking changes but may include miscellaneous
bug fixes. If the previous version of conveyance released was ``v1.2.10`` a minor
release would be versioned as ``v1.3.0``.

Minor releases will be backwards compatible with releases that have the same
major version number. In other words, all versions that would start with
``v1.`` should be compatible with each other.

Hotfix Releases
---------------

A hotfix release will only include bug fixes that were missed when the project
released the previous version. If the previous version of Requests released
``v1.2.10`` the hotfix release would be versioned as ``v1.2.11``.
