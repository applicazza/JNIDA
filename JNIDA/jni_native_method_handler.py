from jni_native_method import JNINativeMethodSignature, JNINativeMethodError
import ida_bytes
import idaapi
import ida_kernwin
import ida_name
import ida_typeinf


class JNINativeMethodHandler(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        selection = idaapi.read_selection()
        if not selection[0]:
            return 0

        start = selection[1] - 1
        stop = selection[2] + 1

        print('Parsing selection between %X -> %X' % (start, stop))

        prefix = ida_kernwin.ask_str('', 0, 'Prefix')

        if prefix is not None:
            prefix = prefix.replace('/', '::')

        while True:
            name_address = ida_bytes.next_head(start, stop)

            if name_address == idaapi.BADADDR:
                break

            name_offset = ida_bytes.get_dword(name_address)

            name = ida_bytes.get_strlit_contents(name_offset, -1, 0)

            if prefix is not None:
                name = prefix + '::' + name

            signature_address = ida_bytes.next_head(name_address, stop)

            if signature_address == idaapi.BADADDR:
                break

            signature_offset = ida_bytes.get_dword(signature_address)

            signature = ida_bytes.get_strlit_contents(signature_offset, -1, 0)

            function_address = ida_bytes.next_head(signature_address, stop)

            if function_address == idaapi.BADADDR:
                break

            function_offset = ida_bytes.get_dword(function_address)

            if function_offset % 2 != 0:
                function_offset -= 1

            try:
                c_signature = JNINativeMethodSignature(name, signature).c
            except JNINativeMethodError:
                break

            start = function_address

            parsed_decl = ida_typeinf.idc_parse_decl(None, c_signature, ida_typeinf.PT_SIL)

            if parsed_decl is None:
                return 0

            ida_typeinf.apply_type(None, parsed_decl[1], parsed_decl[2], function_offset, 1)

            ida_name.set_name(function_offset, name, ida_name.SN_FORCE)

        return 1

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS


def init():
    action_desc = idaapi.action_desc_t(
        'jni_native_method:rename',
        'Rename JNI native methods',
        JNINativeMethodHandler(),
        'Ctrl+/',
        'Rename JNI native methods',
        199
    )

    idaapi.register_action(action_desc)

    idaapi.attach_action_to_menu(
        'Edit/Other/Manual instruction...',
        'jni_native_method:rename',
        idaapi.SETMENU_APP
    )


def fini():
    idaapi.detach_action_from_menu(
        'Edit/Other/Manual instruction...',
        'jni_native_method:rename'
    )

    idaapi.unregister_action('jni_native_method:rename')
