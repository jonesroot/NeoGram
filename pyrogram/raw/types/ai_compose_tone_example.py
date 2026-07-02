#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class AiComposeToneExample(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AiComposeToneExample`.

    Details:
        - Layer: ``227``
        - ID: ``F1D628EC``

    Parameters:
        from (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

        to (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            aicompose.GetToneExample
    """

    __slots__: List[str] = ["from", "to"]

    ID = 0xf1d628ec
    QUALNAME = "types.AiComposeToneExample"

    def __init__(self, *, from: "raw.base.TextWithEntities", to: "raw.base.TextWithEntities") -> None:
        self.from = from  # TextWithEntities
        self.to = to  # TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AiComposeToneExample":
        # No flags
        
        from = TLObject.read(b)
        
        to = TLObject.read(b)
        
        return AiComposeToneExample(from=from, to=to)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.from.write())
        
        b.write(self.to.write())
        
        return b.getvalue()
