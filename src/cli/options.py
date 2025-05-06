from typing import Annotated

import typer

NameSpaceOption = Annotated[str, typer.Option("-n", "--namespace")]
