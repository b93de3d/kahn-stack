from types import NoneType
from typing import List, Dict

import core.models as core_models


class Field:
    def __init__(self, name, value):
        self.name = name
        self.possible_types = []
        self.possible_values = []
        self.spec = None

        self.add_value(value)

    def add_value(self, value):
        if type(value) == dict:
            if self.spec is None:
                self.spec = Spec()
            self.spec.add_example(value)
            return

        if type(value) == list:
            if self.spec is None:
                self.spec = Spec()
            for v in value:
                if type(v) == dict:
                    self.spec.add_example(v)
                else:
                    self.spec.add_field("list[]", v)
            return

        if value not in self.possible_values:
            self.possible_values.append(value)
        if type(value) not in self.possible_types:
            self.possible_types.append(type(value))

    def summarise_type(self):
        summary = []
        for t in self.possible_types:
            if t in (int, float):
                min_value = min(
                    v for v in self.possible_values if type(v) in (int, float)
                )
                max_value = max(
                    list(v for v in self.possible_values if type(v) in (int, float))
                )
                summary.append(
                    f"{'Int' if t == int else 'Float'}[{min_value} to {max_value}]"
                )
            elif t == str:
                example_values = list(
                    f"`{v}`" for v in self.possible_values if type(v) == str
                )
                summary.append(f"String[{', '.join(example_values[:5])}]")
            elif t == NoneType:
                summary.append("None")
            elif t == bool:
                summary.append(f"Boolean[{self.possible_values}]")
            else:
                assert False, f"Unhandled type: {t}"

        return f"[{'| '.join(summary)}]"


class Spec:

    def __init__(self):
        self.fields: dict[str, Field] = {}

    def add_field(self, name, value):
        if name in self.fields:
            self.fields[name].add_value(value)
        else:
            self.fields[name] = Field(name, value)

    def add_example(self, obj):
        for name, value in obj.items():
            self.add_field(name, value)

    def get_summary(self, summary_lines=None, indent=0):
        if summary_lines is None:
            summary_lines = []
        for field in self.fields.values():
            padding = " " * indent * 2
            if field.spec is None:
                summary_lines.append(f"{padding}{field.name}: {field.summarise_type()}")
            else:
                summary_lines.append(f"{padding}{field.name}:")
                summary_lines = field.spec.get_summary(summary_lines, indent=indent + 1)

        return summary_lines

    def print_summary(self):
        summary_lines = self.get_summary()
        for line in summary_lines:
            print(line)


def object_explorer(examples: List[Dict]):
    s = Spec()
    for e in examples:
        s.add_example(e)
    s.print_summary()


if __name__ == "__main__":
    eg_data = [
        {"amount": 4, "type": "D", "user": "Matthew"},
        {
            "amount": 5,
            "type": "D",
            "user": "Mark",
            "friends": ["John", "Matthew", "Luke"],
        },
        {"amount": 2, "type": "W", "user": "Luke", "friends": ["John", "Matthew"]},
        {"amount": 1, "type": "W", "user": "John", "stats": {"height": 5, "weight": 7}},
        {
            "amount": 1,
            "type": "W",
            "user": "John",
            "friends_with_stats": [  # TODO: This kind of thing isn't a handled properly
                {"Mark": {"height": 5, "weight": 7}},
                {"Luke": {"height": 5, "weight": 7}},
                {"Luke": {"height": 5, "weight": 8}},
            ],
        },
    ]
    # TODO: Show when a field is optional
    object_explorer(eg_data)
    # object_explorer([t.detail for t in core_models.Transaction.objects.all()])
