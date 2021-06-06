# -*- coding: utf-8 -*-
#    Copyright (C) 2021  The Project TONA Authors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import base64

class HTTPException(BaseException):

    def __init__(self, code, message, *args: object) -> None:
        self.code = code
        self.message = message
        super().__init__(*args)


class HTTPResponse:
    ok = False
    message = None
    payload = {}
    erros = []
    code = 500

    def to_dict(self):
        data = {
            "ok": self.ok,
            "code": self.code
        }
        if self.message:
            data.update(dict(message=self.message))
        if self.payload:
            data.update(dict(payload=self.payload))
        if len(self.erros):
            data.update(dict(erros=self.erros))
        return data

def api_response(ok=False, message=None, payload=None):
    return {
        "ok": ok,
        "message": message,
        "payload": payload
    }

def str2int(val: str):
    try:
        val = int("".join([n for n in val if n.isdigit()]))
        return val
    except Exception as e:
        pass
    return 0

def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def location_attachment(storage, attachment) -> tuple:
    res_model = str(attachment.res_model).replace('_', '/')
    fname = f"{attachment.id}-{attachment.name}"
    fpath = os.path.join(storage, res_model, str(attachment.res_id))
    return fpath, fname

def save_attachment(storage, attachment, content) -> bool:
    fpath, fname = location_attachment(storage, attachment)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    decoded = base64.b64decode(content)
    output_file = open(os.path.join(fpath, fname), 'w', encoding="utf-8")
    output_file.write(decoded.decode('utf-8'))
    output_file.close()
    return True

def remove_attachment(storage, attachment) -> bool:
    fpath, fname = location_attachment(storage, attachment)
    ffile = os.path.join(fpath, fname)
    if os.path.exists(ffile):
        os.remove(ffile)
    return True