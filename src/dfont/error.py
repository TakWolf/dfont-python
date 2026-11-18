
class DFontError(Exception):
    pass


class DFontParseError(DFontError):
    pass


class DFontDumpError(DFontError):
    pass


class DFontValidationError(DFontError):
    pass
