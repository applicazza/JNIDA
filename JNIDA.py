import idaapi
import JNIDA.jni_native_method_handler as jni_native_method_handler


class JNIDA(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = "JNI IDA helpers"

    help = "JNI IDA helpers"
    wanted_name = "JNI IDA helpers"
    wanted_hotkey = ""

    @staticmethod
    def init():
        jni_native_method_handler.init()
        return idaapi.PLUGIN_KEEP

    @staticmethod
    def run():
        pass

    @staticmethod
    def term():
        jni_native_method_handler.fini()


def PLUGIN_ENTRY():
    return JNIDA()
