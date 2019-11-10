import re


class JNINativeMethodSignature:
    __tokens = [
        ('ARGS_START', r'\('),
        ('STRING', r'Ljava.lang.String;'),
        ('CLASS', r'Ljava.lang.Class;'),
        ('THROWABLE', r'Ljava.lang.Throwable;'),
        ('OBJECT', r'L([^;]+);'),
        ('OBJECT_ARRAY', r'\[L([^;]+);'),
        ('VOID', r'V'),
        ('BOOLEAN', r'Z'),
        ('BYTE', r'B'),
        ('CHAR', r'C'),
        ('SHORT', r'S'),
        ('INTEGER', r'I'),
        ('LONG', r'J'),
        ('FLOAT', r'F'),
        ('DOUBLE', r'D'),
        ('BOOLEAN_ARRAY', r'\[Z'),
        ('BYTE_ARRAY', r'\[B'),
        ('CHAR_ARRAY', r'\[C'),
        ('SHORT_ARRAY', r'\[S'),
        ('INTEGER_ARRAY', r'\[I'),
        ('LONG_ARRAY', r'\[J'),
        ('FLOAT_ARRAY', r'\[F'),
        ('DOUBLE_ARRAY', r'\[D'),
        ('ARGS_END', r'\)'),
        ('MISMATCH', r'.'),
    ]

    __regex = '|'.join('(?P<%s>%s)' % pair for pair in __tokens)

    __mapping = {
        'OBJECT': 'jobject',
        'CLASS': 'jclass',
        'STRING': 'jstring',
        'THROWABLE': 'jthrowable',
        'VOID': 'void',
        'BOOLEAN': 'jboolean',
        'BYTE': 'jbyte',
        'CHAR': 'jchar',
        'SHORT': 'jshort',
        'INTEGER': 'jint',
        'LONG': 'jlong',
        'FLOAT': 'jfloat',
        'DOUBLE': 'jdouble',
        'OBJECT_ARRAY': 'jobjectArray',
        'BOOLEAN_ARRAY': 'jbooleanArray',
        'BYTE_ARRAY': 'jbyteArray',
        'CHAR_ARRAY': 'jcharArray',
        'SHORT_ARRAY': 'jshortArray',
        'INTEGER_ARRAY': 'jintArray',
        'LONG_ARRAY': 'jlongArray',
        'FLOAT_ARRAY': 'jfloatArray',
        'DOUBLE_ARRAY': 'jdoubleArray',
    }

    def __init__(self, name, signature):
        self.name = name
        self.signature = signature
        self.c = self.__parse()
        pass

    def __parse(self):
        args = ["JNIEnv* env", "jobject thiz"]
        ret = 'VOID'
        args_end = False
        index = 0
        for matches in re.finditer(self.__regex, self.signature):
            kind = matches.lastgroup
            if args_end:
                ret = self.__mapping[kind]
                continue
            if kind == 'ARGS_START':
                continue
            if kind == 'ARGS_END':
                args_end = True
                continue
            if kind == 'MISMATCH':
                raise JNINativeMethodError()
            args.append(self.__mapping[kind] + (' a%i' % index))
            index += 1
        return "%s %s(%s);" % (ret, self.name, ', '.join(args))


class JNINativeMethodError(Exception):
    pass
