import logging


class OneLineFormatter(logging.Formatter):
    def format(self, record) -> str:
        result = super(OneLineFormatter, self).format(record)
        result = result.replace('\n', '|')
        return result
