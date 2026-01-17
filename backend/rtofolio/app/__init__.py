"""Backend application package.

This file makes `app/` a regular Python package (not a namespace package),
which avoids import ambiguity (e.g. accidentally importing a different installed
package named `app`).
"""

